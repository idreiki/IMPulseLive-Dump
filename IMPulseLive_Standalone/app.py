import ctypes
import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import src.core.app as app_module

if __name__ == '__main__':
    app_module.launch()
