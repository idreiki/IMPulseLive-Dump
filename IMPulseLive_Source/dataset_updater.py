import os
import sys
import json
import time
import requests
import threading
import base64

GITHUB_CONFIG_URL = 'https://raw.githubusercontent.com/twirlspro/IMPulse-Live/main/data/app_config.json'
GITHUB_META_URL = 'https://raw.githubusercontent.com/twirlspro/IMPulse-Live/main/data/meta_history.json'
SECRET_KEY_V1 = b'IMPulseLiveSecretKey2026_DotaVision'

def _derive_k():
    raw = [468, 393, 47, 106, 433, 126, 51, 456, 93, 402, 27, 506, 71, 108, 387, 485]
    return bytes([(x ^ 0x5A) & 0xFF for x in raw])

def decrypt_token(enc_str):
    """Decrypts token strictly using non-linear multi-stage ciphertext (V2)."""
    if not enc_str:
        return None
    try:
        enc = base64.b64decode(enc_str)
        try:
            k = _derive_k()
            out = bytearray()
            for i, b in enumerate(enc):
                xored = (b - (43 + (i * 11) % 251)) % 256
                rot = xored ^ k[i % len(k)]
                orig = ((rot >> 3) | (rot << 5)) & 0xFF
                out.append(orig)
            plain = out.decode('utf-8', errors='ignore')
            if plain.startswith('eyJ'):
                return plain
        except Exception:
            pass

        try:
            dec = bytes([((b - (7 + (i % 13))) % 256) ^ SECRET_KEY_V1[i % len(SECRET_KEY_V1)] for i, b in enumerate(enc)])
            plain = dec.decode('utf-8', errors='ignore')
            if plain.startswith('eyJ'):
                return plain
            dec_legacy = bytes([b ^ SECRET_KEY_V1[i % len(SECRET_KEY_V1)] for i, b in enumerate(enc)])
            plain_legacy = dec_legacy.decode('utf-8', errors='ignore')
            if plain_legacy.startswith('eyJ'):
                return plain_legacy
        except Exception:
            pass

        return None
    except Exception as e:
        print(f'[DatasetUpdater] Failed decrypting token: {e}')
        return None

class DatasetUpdater:
    def __init__(self, data_dir, on_update=None):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.meta_file = os.path.join(self.data_dir, 'meta_history.json')
        self.is_updating = False
        self.status = 'Idle'
        self.on_update = on_update
        self._lock = threading.Lock()
        self._requested_rank = None
        self._remote_token = None
        self._sync_enabled = False
        self._meta_timestamps = {}
        self._daily_timestamps = {}
        self._last_check_time = 0
        self._ensure_essential_files()

    def get_active_token(self):
        """Get the in-memory decrypted Stratz API token."""
        return self._remote_token

    def is_sync_enabled(self):
        """Check if player sync is currently permitted."""
        return self._sync_enabled

    def verify_live_status(self):
        """
        Enforces a mandatory LIVE check against GitHub before performing any Stratz API operations.
        Ensures kill-switch cannot be bypassed offline or via firewall blocking.
        Returns: (allowed: bool, message: str)
        """
        now = time.time()
        if now - self._last_check_time > 300 or not self._remote_token:
            success = self._fetch_remote_config()
            if not success:
                return False, "Could not verify service status with GitHub. Please check your internet connection."
        if not self._sync_enabled:
            return False, "Player sync is temporarily paused by the developer."
        if not self._remote_token:
            return False, "No valid API key received from server."
        return True, "OK"

    def _fetch_remote_config(self):
        """
        Fetch remote config from GitHub:
        1. Verifies kill-switch (sync_enabled)
        2. Decrypts API token in-memory (XOR + Base64)
        3. Updates rank meta timestamps for update detection
        """
        try:
            resp = requests.get(GITHUB_CONFIG_URL, timeout=5)
            if resp.status_code == 200:
                config = resp.json()
                self._sync_enabled = config.get('sync_enabled', False)
                api_token = config.get('api_token')
                if api_token:
                    self._remote_token = decrypt_token(api_token)
                self._meta_timestamps = config.get('meta_timestamps', {})
                self._daily_timestamps = config.get('daily_timestamps', {})
                self._last_check_time = time.time()
                return True
            else:
                print(f'[DatasetUpdater] GitHub config returned HTTP {resp.status_code}')
                return False
        except Exception as e:
            print(f'[DatasetUpdater] Live config verification failed: {e}')
            return False

    def start_update_thread(self, target_weeks=4, force_full=False, rank='all'):
        with self._lock:
            if self.is_updating:
                return False
            self.is_updating = True
            self.status = 'Starting...'
            self._requested_rank = rank
            t = threading.Thread(
                target=self._run_sync,
                args=(target_weeks, force_full, rank),
                daemon=True
            )
            t.start()
            return True

    def _run_sync(self, target_weeks, force_full, rank):
        try:
            if not self.verify_live_status()[0]:
                self.status = 'Error: Sync not allowed'
                return

            self.status = 'Checking updates...'
            if not self._remote_token:
                self.status = 'Error: No Token'
                return

            self._download_remote_metadata(rank)
            self.status = 'Idle'
            if self.on_update:
                self.on_update()
        except Exception as e:
            print(f'[DatasetUpdater] Sync error: {e}')
            self.status = 'Error'
        finally:
            with self._lock:
                self.is_updating = False

    def _download_remote_metadata(self, rank='all'):
        try:
            resp = requests.get(GITHUB_META_URL, timeout=10)
            if resp.status_code == 200:
                with open(self.meta_file, 'wb') as f:
                    f.write(resp.content)
        except Exception as e:
            print(f'[DatasetUpdater] Metadata download error: {e}')

    def _ensure_essential_files(self):
        default_files = ['constants.json', 'patches.json']
        for fname in default_files:
            fpath = os.path.join(self.data_dir, fname)
            if not os.path.exists(fpath):
                try:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        json.dump({}, f)
                except Exception:
                    pass
