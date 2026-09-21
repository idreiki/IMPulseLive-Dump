import os
import sys

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_UI_DIR = os.path.join(_BASE_DIR, 'ui')

_INDEX_HTML_CACHE = None
_STYLE_CSS_CACHE = None
_MAIN_JS_CACHE = None
_ICON_PNG_CACHE = None
_FAVICON_CACHE = None

def is_bundle_active():
    return True

def get_index_html():
    global _INDEX_HTML_CACHE
    if _INDEX_HTML_CACHE is None:
        p = os.path.join(_UI_DIR, 'index.html')
        with open(p, 'r', encoding='utf-8') as f:
            _INDEX_HTML_CACHE = f.read()
    return _INDEX_HTML_CACHE

def get_style_css():
    global _STYLE_CSS_CACHE
    if _STYLE_CSS_CACHE is None:
        p = os.path.join(_UI_DIR, 'style.css')
        with open(p, 'r', encoding='utf-8') as f:
            _STYLE_CSS_CACHE = f.read()
    return _STYLE_CSS_CACHE

def get_main_js():
    global _MAIN_JS_CACHE
    if _MAIN_JS_CACHE is None:
        p = os.path.join(_UI_DIR, 'main.js')
        with open(p, 'r', encoding='utf-8') as f:
            _MAIN_JS_CACHE = f.read()
    return _MAIN_JS_CACHE

def get_icon_png():
    global _ICON_PNG_CACHE
    if _ICON_PNG_CACHE is None:
        p = os.path.join(_UI_DIR, 'icon.png')
        with open(p, 'rb') as f:
            _ICON_PNG_CACHE = f.read()
    return _ICON_PNG_CACHE

def get_favicon():
    global _FAVICON_CACHE
    if _FAVICON_CACHE is None:
        p = os.path.join(_UI_DIR, 'favicon.ico')
        with open(p, 'rb') as f:
            _FAVICON_CACHE = f.read()
    return _FAVICON_CACHE
