import os
import sys
import time
import json
import hashlib
import threading
import requests
import ctypes
import re

APP_VERSION = '2.0.0'
BUILD_TIMESTAMP = 1789622600.0
GITHUB_CONFIG_URL = 'https://raw.githubusercontent.com/twirlspro/IMPulse-Live/main/data/app_config.json'
HEARTBEAT_INTERVAL = 7200
MAX_BUILD_LIFETIME = 5184000
OFFLINE_GRACE_PERIOD = 172800

_K = b'\x9cO\xb2\x17'

def _dx(b: bytes, k: bytes = _K) -> str:
    return bytes([b[i] ^ k[i % len(k)] for i in range(len(b))]).decode('utf-8')

_CFG_ENC = bytes([ord(c) ^ _K[i % len(_K)] for i, c in enumerate(GITHUB_CONFIG_URL)])
_TG_ENC = bytes([ord(c) ^ _K[i % len(_K)] for i, c in enumerate('https://t.me/impulse_dota')])

def check_debugger_present() -> bool:
    try:
        return bool(ctypes.windll.kernel32.IsDebuggerPresent())
    except Exception:
        return False

def parse_semver(v_str):
    """Parses semantic version string into a tuple of ints for accurate comparison."""
    if not v_str:
        return (0, 0, 0)
    nums = [int(x) for x in re.findall(r'\d+', str(v_str))]
    while len(nums) < 3:
        nums.append(0)
    return tuple(nums[:3])

class SecurityGuard:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.config_url = _dx(_CFG_ENC)
        self.cache_file = os.path.join(self.data_dir, '.license_cache')
        self.lock = threading.Lock()
        self._is_locked = False
        self._lock_reason = ''
        self._lock_title = ''
        self._lock_message = ''
        self._telegram_url = _dx(_TG_ENC)
        self.last_check_time = 0
        self.last_online_success = 0.0
        self._heartbeat_thread = None
        self._running = False

    def _read_cached_timestamp(self):
        """Reads cryptographically authenticated and encrypted timestamp."""
        if not os.path.exists(self.cache_file):
            return None
        try:
            with open(self.cache_file, 'rb') as f:
                raw = f.read()
            dec = bytes([b ^ 0x5A for b in raw]).decode('utf-8', errors='ignore')
            if '|' not in dec:
                return None
            ts_str, sig = dec.split('|', 1)
            expected_sig = hashlib.sha256(f"{ts_str}|IMPULSE_SEC_2026".encode('utf-8')).hexdigest()[:16]
            if sig != expected_sig:
                print('[SecurityGuard] Cache integrity check failed (signature mismatch).')
                return None
            return float(ts_str)
        except Exception as e:
            print(f'[SecurityGuard] Cache read error: {e}')
            return None

    def _write_cached_timestamp(self, ts):
        """Writes obfuscated timestamp with HMAC signature to cache file."""
        try:
            sig = hashlib.sha256(f"{ts}|IMPULSE_SEC_2026".encode('utf-8')).hexdigest()[:16]
            raw = f"{ts}|{sig}".encode('utf-8')
            enc = bytes([b ^ 0x5A for b in raw])
            with open(self.cache_file, 'wb') as f:
                f.write(enc)
        except Exception as e:
            print(f'[SecurityGuard] Cache write warning: {e}')

    def is_locked(self):
        with self.lock:
            return self._is_locked

    def get_lock_payload(self):
        with self.lock:
            return {
                'locked': self._is_locked,
                'reason': self._lock_reason,
                'title': self._lock_title,
                'message': self._lock_message,
                'telegram_url': self._telegram_url,
                'app_version': APP_VERSION,
                'last_check': self.last_check_time
            }

    def _set_locked(self, reason, title, message, telegram_url=None):
        with self.lock:
            self._is_locked = True
            self._lock_reason = reason
            self._lock_title = title
            self._lock_message = message
            if telegram_url:
                self._telegram_url = telegram_url
            print(f'[SecurityGuard] LOCK ENGAGED: {reason} - {title}')

    def _set_unlocked(self):
        with self.lock:
            if self._is_locked:
                print('[SecurityGuard] LOCK DISENGAGED: App successfully verified and unlocked.')
            self._is_locked = False
            self._lock_reason = ''
            self._lock_title = ''
            self._lock_message = ''

    def check_security(self, force=False, mock_config=None) -> bool:
        """
        1. Clock rollback & integrity checks
        2. Evaluates version gate ('min_version' vs APP_VERSION)
        3. Evaluates offline grace period (48 hours)
        """
        now = time.time()
        if not force and self.last_check_time > 0 and (now - self.last_check_time < 300):
            return not self._is_locked

        if check_debugger_present():
            self._set_locked(
                'debugger_detected',
                'Система безопасности',
                'Обнаружен отладчик. Запуск заблокирован.'
            )
            return False

        if now < (BUILD_TIMESTAMP - 86400):
            self._set_locked(
                'clock_tampered',
                'Системное время',
                'Системные часы сбиты назад относительно даты сборки приложения. Пожалуйста, синхронизируйте системное время Windows.'
            )
            return False

        config = mock_config
        network_ok = False

        if config is None:
            try:
                resp = requests.get(self.config_url, timeout=5)
                if resp.status_code == 200:
                    config = resp.json()
                    network_ok = True
                    self.last_online_success = now
                    self._write_cached_timestamp(now)
            except Exception as e:
                print(f'[SecurityGuard] Network check failed: {e}')
                config = None
        else:
            network_ok = True

        if network_ok and config:
            tg = config.get('telegram_url')
            if tg:
                self._telegram_url = tg

            if not config.get('sync_enabled', True):
                msg = config.get('status_message', 'Приложение временно приостановлено разработчиком.')
                self._set_locked(
                    'kill_switch',
                    'Технические работы',
                    msg
                )
                return False

            min_ver = config.get('min_version', '1.0.0')
            if parse_semver(APP_VERSION) < parse_semver(min_ver):
                self._set_locked(
                    'version_outdated',
                    'Требуется обновление',
                    f'Ваша версия приложения ({APP_VERSION}) устарела. Минимальная поддерживаемая версия: {min_ver}. Пожалуйста, скачайте обновление в Telegram.',
                    telegram_url=self._telegram_url
                )
                return False

            self.last_check_time = now
            self._set_unlocked()
            return True

        # Offline path
        cached_ts = self._read_cached_timestamp()
        ref_ts = cached_ts or self.last_online_success or BUILD_TIMESTAMP

        if now < ref_ts - 3600:
            self._set_locked(
                'clock_tampered',
                'Системное время',
                'Обнаружена манипуляция с системным временем Windows. Синхронизируйте время через интернет.'
            )
            return False

        time_offline = now - ref_ts
        if time_offline > OFFLINE_GRACE_PERIOD:
            hours_offline = int(time_offline // 3600)
            self._set_locked(
                'offline_expired',
                'Нет подключения к сети',
                f'Приложение находится оффлайн слишком долго ({hours_offline} ч.). Для подтверждения лицензии необходимо подключение к интернету.'
            )
            return False

        build_age = now - BUILD_TIMESTAMP
        if build_age > MAX_BUILD_LIFETIME:
            self._set_locked(
                'build_expired',
                'Срок сборки истек',
                'Срок действия данной тестовой сборки истек. Пожалуйста, получите актуальную версию в Telegram-канале.',
                telegram_url=self._telegram_url
            )
            return False

        self.last_check_time = now
        self._set_unlocked()
        return True

    def start_heartbeat_poller(self, interval=HEARTBEAT_INTERVAL):
        if self._running:
            return
        self._running = True

        def _poller_task():
            print(f'[SecurityGuard] Background heartbeat poller started (interval={interval}s)')
            while self._running:
                time.sleep(interval)
                if not self._running:
                    break
                try:
                    self.check_security(force=True)
                except Exception as e:
                    print(f'[SecurityGuard] Heartbeat error: {e}')

        self._heartbeat_thread = threading.Thread(target=_poller_task, daemon=True)
        self._heartbeat_thread.start()

    def stop_heartbeat(self):
        self._running = False
