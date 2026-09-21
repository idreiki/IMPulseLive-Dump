import os
import sys
import time

APP_VERSION = '2.0.0'
BUILD_TIMESTAMP = 1789622600.0

def check_debugger_present() -> bool:
    return False

def parse_semver(v_str):
    return (999, 999, 999)

class SecurityGuard:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.last_check_time = time.time()
        self.last_online_success = time.time()
        self._is_locked = False
        self._lock_reason = ''
        self._lock_title = ''
        self._lock_message = ''
        self._telegram_url = 'https://t.me/impulse_dota'

    def is_locked(self):
        return False

    def get_lock_payload(self):
        return {
            'locked': False,
            'reason': '',
            'title': '',
            'message': '',
            'telegram_url': self._telegram_url,
            'app_version': APP_VERSION,
            'last_check': time.time()
        }

    def check_security(self, force=False, mock_config=None) -> bool:
        return True

    def start_heartbeat_poller(self, interval=7200):
        pass

    def stop_heartbeat(self):
        pass
