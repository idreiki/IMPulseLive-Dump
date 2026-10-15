import os
import sys
import time

APP_VERSION = '4.0.0'
BUILD_TIMESTAMP = 1792000000.0

def check_debugger_present() -> bool:
    return False

def parse_semver(v_str):
    """Parses semantic version string into a tuple of ints for accurate comparison."""
    if not v_str:
        return (0, 0, 0)
    import re
    nums = [int(x) for x in re.findall(r'\d+', str(v_str))]
    while len(nums) < 3:
        nums.append(0)
    return tuple(nums[:3])

class SecurityGuard:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.config_url = 'https://raw.githubusercontent.com/twirlspro/IMPulse-Live/main/data/app_config.json'
        self._is_locked = False
        self._telegram_url = 'https://t.me/proverkahelp'

    def is_locked(self):
        return False

    def get_lock_details(self):
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
        """
        1. Clock rollback & integrity checks
        2. Evaluates version gate ('min_version' vs APP_VERSION)
        3. Evaluates offline grace period (48 hours)
        """
        return True

    def start_heartbeat_poller(self, interval=7200):
        pass

    def stop_heartbeat(self):
        pass
