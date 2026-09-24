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
        return True

    def verify_live_status(self):
        """Always allowed in Standalone edition."""
        if not self._remote_token:
            self._fetch_remote_config()
        if not self._remote_token:
            self._remote_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiMDJhMjhkN2MtOTMxNi00YjVjLTgyNTctNzkxYzg1YTI5NzMxIiwiU3RlYW1JZCI6IjE3MTE5MjY0NjUiLCJBUElVc2VyIjoidHJ1ZSIsIm5iZiI6MTc3NDAxNDc5NCwiZXhwIjoxODA1NTUwNzk0LCJpYXQiOjE3NzQwMTQ3OTQsImlzcyI6Imh0dHBzOi8vYXBpLnN0cmF0ei5jb20ifQ.dsZTN-tyzZxC9Ece3l34adQze75nZbZmESllsLZq3yE'
        return True, "OK"

    def _fetch_remote_config(self):
        FALLBACK_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiMDJhMjhkN2MtOTMxNi00YjVjLTgyNTctNzkxYzg1YTI5NzMxIiwiU3RlYW1JZCI6IjE3MTE5MjY0NjUiLCJBUElVc2VyIjoidHJ1ZSIsIm5iZiI6MTc3NDAxNDc5NCwiZXhwIjoxODA1NTUwNzk0LCJpYXQiOjE3NzQwMTQ3OTQsImlzcyI6Imh0dHBzOi8vYXBpLnN0cmF0ei5jb20ifQ.dsZTN-tyzZxC9Ece3l34adQze75nZbZmESllsLZq3yE'
        try:
            resp = requests.get(GITHUB_CONFIG_URL, timeout=5)
            if resp.status_code == 200:
                config = resp.json()
                self._sync_enabled = True
                api_token = config.get('api_token')
                if api_token:
                    self._remote_token = decrypt_token(api_token) or FALLBACK_TOKEN
                else:
                    self._remote_token = FALLBACK_TOKEN
                self._meta_timestamps = config.get('meta_timestamps', {})
                self._daily_timestamps = config.get('daily_timestamps', {})
                self._last_check_time = time.time()
                return True
        except Exception as e:
            print(f'[DatasetUpdater] Offline mode active: {e}')
        self._sync_enabled = True
        self._remote_token = FALLBACK_TOKEN
        return True

    def start_update_thread(self, target_weeks=4, force_full=False, rank='all'):
        with self._lock:
            if self.is_updating:
                return
            self.is_updating = True
            self._requested_rank = rank
            self.status = 'Checking server...'
        t = threading.Thread(target=self._update_worker, args=(target_weeks, force_full), daemon=True)
        t.start()

    def _update_worker(self, target_weeks, force_full):
        try:
            self._fetch_remote_config()
            rank = self._requested_rank or 'all'
            self._sync_rank(rank, target_weeks, force_full)
            self._sync_daily_meta(rank)
            with self._lock:
                self.status = 'Idle'
                self.is_updating = False
        except Exception as e:
            print(f'[DatasetUpdater] Error: {e}')
            with self._lock:
                self.status = 'Error'
                self.is_updating = False

    def _sync_rank(self, rank, target_weeks, force_full):
        meta_filename = 'meta_history.json' if rank == 'all' else f'meta_history_{rank}.json'
        meta_file = os.path.join(self.data_dir, meta_filename)
        meta_url = f'https://raw.githubusercontent.com/twirlspro/IMPulse-Live/main/data/{meta_filename}'

        needs_download = False
        remote_ts = self._meta_timestamps.get(rank, 0)
        local_ts = 0

        if not os.path.exists(meta_file) or os.path.getsize(meta_file) == 0:
            needs_download = True
        elif force_full:
            needs_download = True
        elif remote_ts > 0:
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    local_ts = data.get('updatedAt', 0)
                if remote_ts > local_ts:
                    print(f'[DatasetUpdater] New meta detected on GitHub (remote={remote_ts} > local={local_ts})')
                    needs_download = True
            except Exception:
                needs_download = True

        if needs_download:
            self.status = 'Downloading meta...'
            tmp_file = meta_file + '.tmp'
            max_retries = 3
            success = False
            for attempt in range(max_retries):
                try:
                    resp = requests.get(meta_url, timeout=30, stream=True)
                    if resp.status_code == 200:
                        with open(tmp_file, 'wb') as f:
                            for chunk in resp.iter_content(chunk_size=65536):
                                if chunk:
                                    f.write(chunk)
                        if os.path.exists(meta_file):
                            os.remove(meta_file)
                        os.replace(tmp_file, meta_file)
                        success = True
                        print(f'[DatasetUpdater] Successfully updated {meta_filename}')
                        break
                except Exception as e:
                    print(f'[DatasetUpdater] Download error: {e}')
                    if os.path.exists(tmp_file):
                        try: os.remove(tmp_file)
                        except: pass
                    time.sleep(1)

            if success:
                self.status = 'Updated'
                if self.on_update:
                    try:
                        self.on_update(rank)
                    except Exception as e:
                        print(f'[DatasetUpdater] on_update error: {e}')

    def _sync_daily_meta(self, rank):
        """
        Optionally downloads fresh daily_meta.json from GitHub if remote timestamp is newer.
        Fails gracefully and non-destructively if file is not on GitHub.
        """
        daily_filename = 'daily_meta.json' if rank == 'all' else f'daily_meta_{rank}.json'
        daily_file = os.path.join(self.data_dir, daily_filename)
        daily_url = f'https://raw.githubusercontent.com/twirlspro/IMPulse-Live/main/data/{daily_filename}'
        remote_ts = self._daily_timestamps.get(rank, 0)
        local_ts = 0

        if os.path.exists(daily_file):
            try:
                with open(daily_file, 'r', encoding='utf-8') as f:
                    d_json = json.load(f)
                    local_ts = d_json.get('updatedAt', 0)
            except:
                pass

        if not os.path.exists(daily_file) or (remote_ts > 0 and remote_ts > local_ts):
            try:
                resp = requests.get(daily_url, timeout=15)
                if resp.status_code == 200:
                    d_json = resp.json()
                    tmp_d = daily_file + '.tmp'
                    with open(tmp_d, 'w', encoding='utf-8') as f:
                        json.dump(d_json, f, indent=2)
                    if os.path.exists(daily_file):
                        os.remove(daily_file)
                    os.replace(tmp_d, daily_file)
                    print(f'[DatasetUpdater] Updated {daily_filename}')
            except Exception as e:
                print(f'[DatasetUpdater] Daily meta sync note: {e}')

    def _ensure_essential_files(self):
        """Ensures constants.json and patches.json exist locally; downloads from GitHub if missing."""
        base_url = 'https://raw.githubusercontent.com/twirlspro/IMPulse-Live/main/data/'
        for filename in ['constants.json', 'patches.json']:
            path = os.path.join(self.data_dir, filename)
            if not os.path.exists(path) or os.path.getsize(path) == 0:
                try:
                    r = requests.get(base_url + filename, timeout=10)
                    if r.status_code == 200:
                        with open(path, 'wb') as f:
                            f.write(r.content)
                        print(f'[DatasetUpdater] Restored essential file {filename}')
                except Exception as e:
                    print(f'[DatasetUpdater] Error restoring {filename}: {e}')
        c_js = os.path.join(self.data_dir, 'constants.js')
        if not os.path.exists(c_js) and not os.path.exists(os.path.join(self.data_dir, 'constants.json')):
            try:
                r = requests.get(base_url + 'constants.js', timeout=10)
                if r.status_code == 200:
                    with open(c_js, 'wb') as f:
                        f.write(r.content)
                    print('[DatasetUpdater] Restored legacy constants.js from GitHub as fallback.')
            except Exception as e:
                print(f'[DatasetUpdater] Error restoring constants.js: {e}')
