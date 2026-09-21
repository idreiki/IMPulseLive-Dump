import os
import sys
import ctypes
from ctypes import wintypes
import time
import math
import threading
import queue

user32 = ctypes.WinDLL('user32')
gdi32 = ctypes.WinDLL('gdi32')
gdiplus = ctypes.WinDLL('gdiplus')
kernel32 = ctypes.WinDLL('kernel32')

kernel32.GetModuleHandleW.restype = wintypes.HMODULE
kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]

user32.CreateWindowExW.argtypes = [
    wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD,
    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    wintypes.HWND, wintypes.HMENU, wintypes.HINSTANCE, wintypes.LPVOID
]
user32.CreateWindowExW.restype = wintypes.HWND

user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.DefWindowProcW.restype = wintypes.LPARAM

user32.RegisterClassExW.argtypes = [ctypes.c_void_p]
user32.RegisterClassExW.restype = wintypes.ATOM

user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.UINT]
user32.SetWindowPos.restype = wintypes.BOOL

user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
user32.ShowWindow.restype = wintypes.BOOL

user32.DestroyWindow.argtypes = [wintypes.HWND]
user32.DestroyWindow.restype = wintypes.BOOL

user32.GetDC.argtypes = [wintypes.HWND]
user32.GetDC.restype = wintypes.HDC

user32.ReleaseDC.argtypes = [wintypes.HWND, wintypes.HDC]
user32.ReleaseDC.restype = ctypes.c_int

gdi32.CreateCompatibleDC.argtypes = [wintypes.HDC]
gdi32.CreateCompatibleDC.restype = wintypes.HDC

gdi32.DeleteDC.argtypes = [wintypes.HDC]
gdi32.DeleteDC.restype = wintypes.BOOL

gdi32.SelectObject.argtypes = [wintypes.HDC, wintypes.HGDIOBJ]
gdi32.SelectObject.restype = wintypes.HGDIOBJ

gdi32.DeleteObject.argtypes = [wintypes.HGDIOBJ]
gdi32.DeleteObject.restype = wintypes.BOOL

gdi32.CreateDIBSection.argtypes = [wintypes.HDC, ctypes.c_void_p, wintypes.UINT, ctypes.c_void_p, wintypes.HANDLE, wintypes.DWORD]
gdi32.CreateDIBSection.restype = wintypes.HBITMAP

user32.UpdateLayeredWindow.argtypes = [
    wintypes.HWND, wintypes.HDC, ctypes.c_void_p, ctypes.c_void_p,
    wintypes.HDC, ctypes.c_void_p, wintypes.COLORREF, ctypes.c_void_p, wintypes.DWORD
]
user32.UpdateLayeredWindow.restype = wintypes.BOOL

WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
WS_EX_TOPMOST = 0x00000008
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_NOACTIVATE = 0x08000000
WS_POPUP = 0x80000000

HWND_TOPMOST = -1
SWP_NOACTIVATE = 0x0010
SWP_SHOWWINDOW = 0x0040
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SW_HIDE = 0
SW_SHOWNOACTIVATE = 4
ULW_ALPHA = 2
AC_SRC_OVER = 0x00
AC_SRC_ALPHA = 0x01
WM_USER = 1024

HERO_GRID = {'strength': [['alchemist', 'Alchemist'], ['axe', 'Axe'], ['bristleback', 'Bristleback'], ['centaur', 'Centaur Warrunner'], ['chaos_knight', 'Chaos Knight'], ['rattletrap', 'Clockwerk'], ['dawnbreaker', 'Dawnbreaker'], ['doom_bringer', 'Doom'], ['dragon_knight', 'Dragon Knight'], ['earth_spirit', 'Earth Spirit'], ['earthshaker', 'Earthshaker'], ['elder_titan', 'Elder Titan'], ['huskar', 'Huskar'], ['kunkka', 'Kunkka'], ['largo', 'Largo'], ['legion_commander', 'Legion Commander'], ['life_stealer', 'Lifestealer'], ['lycan', 'Lycan'], ['mars', 'Mars'], ['night_stalker', 'Night Stalker'], ['ogre_magi', 'Ogre Magi'], ['omniknight', 'Omniknight'], ['phoenix', 'Phoenix'], ['primal_beast', 'Primal Beast'], ['pudge', 'Pudge'], ['slardar', 'Slardar'], ['spirit_breaker', 'Spirit Breaker'], ['sven', 'Sven'], ['tidehunter', 'Tidehunter'], ['shredder', 'Timbersaw'], ['tiny', 'Tiny'], ['treant', 'Treant Protector'], ['tusk', 'Tusk'], ['abyssal_underlord', 'Underlord'], ['undying', 'Undying'], ['skeleton_king', 'Wraith King']], 'agility': [['antimage', 'Anti-Mage'], ['bloodseeker', 'Bloodseeker'], ['bounty_hunter', 'Bounty Hunter'], ['broodmother', 'Broodmother'], ['clinkz', 'Clinkz'], ['drow_ranger', 'Drow Ranger'], ['ember_spirit', 'Ember Spirit'], ['faceless_void', 'Faceless Void'], ['gyrocopter', 'Gyrocopter'], ['hoodwink', 'Hoodwink'], ['juggernaut', 'Juggernaut'], ['kez', 'Kez'], ['lone_druid', 'Lone Druid'], ['luna', 'Luna'], ['medusa', 'Medusa'], ['meepo', 'Meepo'], ['mirana', 'Mirana'], ['monkey_king', 'Monkey King'], ['morphling', 'Morphling'], ['naga_siren', 'Naga Siren'], ['phantom_assassin', 'Phantom Assassin'], ['phantom_lancer', 'Phantom Lancer'], ['razor', 'Razor'], ['riki', 'Riki'], ['nevermore', 'Shadow Fiend'], ['slark', 'Slark'], ['sniper', 'Sniper'], ['spectre', 'Spectre'], ['templar_assassin', 'Templar Assassin'], ['terrorblade', 'Terrorblade'], ['troll_warlord', 'Troll Warlord'], ['ursa', 'Ursa'], ['vengefulspirit', 'Vengeful Spirit'], ['viper', 'Viper'], ['weaver', 'Weaver']], 'intelligence': [['ancient_apparition', 'Ancient Apparition'], ['chen', 'Chen'], ['crystal_maiden', 'Crystal Maiden'], ['dark_seer', 'Dark Seer'], ['dark_willow', 'Dark Willow'], ['disruptor', 'Disruptor'], ['enchantress', 'Enchantress'], ['grimstroke', 'Grimstroke'], ['invoker', 'Invoker'], ['jakiro', 'Jakiro'], ['keeper_of_the_light', 'Keeper of the Light'], ['leshrac', 'Leshrac'], ['lich', 'Lich'], ['lina', 'Lina'], ['lion', 'Lion'], ['muerta', 'Muerta'], ['necrolyte', 'Necrophos'], ['oracle', 'Oracle'], ['obsidian_destroyer', 'Outworld Destroyer'], ['puck', 'Puck'], ['pugna', 'Pugna'], ['queenofpain', 'Queen of Pain'], ['ringmaster', 'Ringmaster'], ['rubick', 'Rubick'], ['shadow_demon', 'Shadow Demon'], ['shadow_shaman', 'Shadow Shaman'], ['silencer', 'Silencer'], ['skywrath_mage', 'Skywrath Mage'], ['storm_spirit', 'Storm Spirit'], ['tinker', 'Tinker'], ['warlock', 'Warlock'], ['winter_wyvern', 'Winter Wyvern'], ['witch_doctor', 'Witch Doctor'], ['zuus', 'Zeus']], 'universal': [['abaddon', 'Abaddon'], ['arc_warden', 'Arc Warden'], ['bane', 'Bane'], ['batrider', 'Batrider'], ['beastmaster', 'Beastmaster'], ['brewmaster', 'Brewmaster'], ['dazzle', 'Dazzle'], ['death_prophet', 'Death Prophet'], ['enigma', 'Enigma'], ['wisp', 'Io'], ['magnataur', 'Magnus'], ['marci', 'Marci'], ['furion', "Nature's Prophet"], ['nyx_assassin', 'Nyx Assassin'], ['pangolier', 'Pangolier'], ['sand_king', 'Sand King'], ['snapfire', 'Snapfire'], ['techies', 'Techies'], ['venomancer', 'Venomancer'], ['visage', 'Visage'], ['void_spirit', 'Void Spirit'], ['windrunner', 'Windranger']]}

ATTR_INFO = {'strength': {'name_ru': 'Сила', 'name_en': 'Strength', 'short_ru': 'СИЛ', 'short_en': 'STR', 'start_x': 133, 'cols': 6, 'color': '#ef4444'}, 'agility': {'name_ru': 'Ловкость', 'name_en': 'Agility', 'short_ru': 'ЛОВ', 'short_en': 'AGI', 'start_x': 453, 'cols': 6, 'color': '#22c55e'}, 'intelligence': {'name_ru': 'Интеллект', 'name_en': 'Intelligence', 'short_ru': 'ИНТ', 'short_en': 'INT', 'start_x': 775, 'cols': 6, 'color': '#38bdf8'}, 'universal': {'name_ru': 'Универсальные', 'name_en': 'Universal', 'short_ru': 'УНИ', 'short_en': 'UNI', 'start_x': 1095, 'cols': 4, 'color': '#a855f7'}}

ALIASES = {'wraith_king': 'skeleton_king', 'windranger': 'windrunner', 'clockwerk': 'rattletrap', 'shadow_fiend': 'nevermore', 'outworld_destroyer': 'obsidian_destroyer', 'nature_prophet': 'furion', 'timbersaw': 'shredder', 'io': 'wisp', 'underlord': 'abyssal_underlord', 'zeus': 'zuus', 'treant_protector': 'treant', 'centaur_warrunner': 'centaur', 'doom': 'doom_bringer', 'necrophos': 'necrolyte', 'queen_of_pain': 'queenofpain', 'magnus': 'magnataur', 'lifestealer': 'life_stealer'}

BASE_Y0 = 209
BASE_CARD_W = 48
BASE_CARD_H = 79
BASE_STEP_X = 50.0
BASE_STEP_Y = 82.0

ATTR_BASE_X = {
    'strength': 133,
    'agility': 453,
    'intelligence': 775,
    'universal': 1095
}

HERO_INDEX_MAP = {}
for attr_k, h_list in HERO_GRID.items():
    cols_count = 4
    for idx_num, (cdn, disp) in enumerate(h_list):
        r = idx_num // cols_count
        c = idx_num % cols_count
        info_dict = {
            'attr': attr_k,
            'attr_ru': ATTR_INFO[attr_k]['name_ru'],
            'attr_en': ATTR_INFO[attr_k]['name_en'],
            'attr_short_ru': ATTR_INFO[attr_k]['short_ru'],
            'attr_short_en': ATTR_INFO[attr_k]['short_en'],
            'attr_color': ATTR_INFO[attr_k]['color'],
            'row': r,
            'col': c,
            'idx': idx_num,
            'cdn_name': cdn,
            'display_name': disp,
            'summary_ru': f"{ATTR_INFO[attr_k]['name_ru']} • {r + 1} ряд, {c + 1} кол.",
            'summary_en': f"{ATTR_INFO[attr_k]['name_en']} • Row {r + 1}, Col {c + 1}"
        }
        HERO_INDEX_MAP[cdn] = info_dict
        HERO_INDEX_MAP[disp.lower().replace(' ', '_').replace('-', '')] = info_dict

for k_alias, v_target in ALIASES.items():
    if v_target in HERO_INDEX_MAP:
        HERO_INDEX_MAP[k_alias] = HERO_INDEX_MAP[v_target]

class POINT(ctypes.Structure):
    _fields_ = [('x', wintypes.LONG), ('y', wintypes.LONG)]

class SIZE(ctypes.Structure):
    _fields_ = [('cx', wintypes.LONG), ('cy', wintypes.LONG)]

class BLENDFUNCTION(ctypes.Structure):
    _fields_ = [
        ('BlendOp', ctypes.c_byte),
        ('BlendFlags', ctypes.c_byte),
        ('SourceConstantAlpha', ctypes.c_byte),
        ('AlphaFormat', ctypes.c_byte)
    ]

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ('biSize', wintypes.DWORD),
        ('biWidth', wintypes.LONG),
        ('biHeight', wintypes.LONG),
        ('biPlanes', wintypes.WORD),
        ('biBitCount', wintypes.WORD),
        ('biCompression', wintypes.DWORD),
        ('biSizeImage', wintypes.DWORD),
        ('biXPelsPerMeter', wintypes.LONG),
        ('biYPelsPerMeter', wintypes.LONG),
        ('biClrUsed', wintypes.DWORD),
        ('biClrImportant', wintypes.DWORD)
    ]

class GdiplusStartupInput(ctypes.Structure):
    _fields_ = [
        ('GdiplusVersion', wintypes.DWORD),
        ('DebugEventCallback', ctypes.c_void_p),
        ('SuppressBackgroundThread', wintypes.BOOL),
        ('SuppressExternalCodecs', wintypes.BOOL)
    ]

class ClickThroughHighlightWindow:
    def __init__(self):
        self._hwnd = None
        self._is_visible = False
        self._gdi_token = ctypes.c_ulong()
        startup_in = GdiplusStartupInput(1, None, False, False)
        gdiplus.GdiplusStartup(ctypes.byref(self._gdi_token), ctypes.byref(startup_in), None)

        WNDPROC = ctypes.WINFUNCTYPE(wintypes.LPARAM, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
        def wnd_proc(hwnd, msg, wp, lp):
            return user32.DefWindowProcW(hwnd, msg, wp, lp)
        self._proc = WNDPROC(wnd_proc)

        class WNDCLASSEXW(ctypes.Structure):
            _fields_ = [
                ('cbSize', wintypes.UINT),
                ('style', wintypes.UINT),
                ('lpfnWndProc', WNDPROC),
                ('cbClsExtra', ctypes.c_int),
                ('cbExtra', ctypes.c_int),
                ('hInstance', wintypes.HINSTANCE),
                ('hIcon', wintypes.HICON),
                ('hCursor', wintypes.HICON),
                ('hbrBackground', wintypes.HBRUSH),
                ('lpszMenuName', wintypes.LPCWSTR),
                ('lpszClassName', wintypes.LPCWSTR),
                ('hIconSm', wintypes.HICON)
            ]

        w_class = WNDCLASSEXW()
        w_class.cbSize = ctypes.sizeof(WNDCLASSEXW)
        w_class.lpfnWndProc = self._proc
        w_class.hInstance = kernel32.GetModuleHandleW(None)
        w_class.lpszClassName = f'IMPulseHeroHighlight_{id(self)}'
        user32.RegisterClassExW(ctypes.byref(w_class))

        ex_style = WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE
        self._hwnd = user32.CreateWindowExW(
            ex_style,
            w_class.lpszClassName,
            'IMPulseHeroHighlight',
            WS_POPUP,
            0, 0, 10, 10,
            None, None, w_class.hInstance, None
        )

    @property
    def hwnd(self):
        return self._hwnd

    @property
    def is_visible(self):
        return self._is_visible

    def render_and_position(self, x, y, w, h, attr_color='#38bdf8'):
        if not self._hwnd:
            return
        pad = 6
        win_x = x - pad
        win_y = y - pad
        win_w = w + pad * 2
        win_h = h + pad * 2

        user32.SetWindowPos(
            self._hwnd, HWND_TOPMOST,
            win_x, win_y, win_w, win_h,
            SWP_NOACTIVATE | SWP_SHOWWINDOW
        )

        hdc_screen = user32.GetDC(None)
        hdc_mem = gdi32.CreateCompatibleDC(hdc_screen)

        bmi = BITMAPINFOHEADER()
        bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bmi.biWidth = win_w
        bmi.biHeight = -win_h
        bmi.biPlanes = 1
        bmi.biBitCount = 32
        bmi.biCompression = 0

        p_bits = ctypes.c_void_p()
        hbmp = gdi32.CreateDIBSection(hdc_mem, ctypes.byref(bmi), 0, ctypes.byref(p_bits), None, 0)
        gdi32.SelectObject(hdc_mem, hbmp)

        p_graphics = ctypes.c_void_p()
        gdiplus.GdipCreateFromHDC(hdc_mem, ctypes.byref(p_graphics))
        gdiplus.GdipSetSmoothingMode(p_graphics, 4)

        hex_c = attr_color.lstrip('#')
        if len(hex_c) == 6:
            r, g, b = int(hex_c[0:2], 16), int(hex_c[2:4], 16), int(hex_c[4:6], 16)
        else:
            r, g, b = 56, 189, 248

        bg_alpha = 45
        bg_argb = (bg_alpha << 24) | (r * bg_alpha // 255 << 16) | (g * bg_alpha // 255 << 8) | (b * bg_alpha // 255)
        p_brush = ctypes.c_void_p()
        gdiplus.GdipCreateSolidFill(bg_argb, ctypes.byref(p_brush))
        gdiplus.GdipFillRectangleI(p_graphics, p_brush, pad, pad, w, h)
        gdiplus.GdipDeleteBrush(p_brush)

        border_alpha = 230
        border_argb = (border_alpha << 24) | (r * border_alpha // 255 << 16) | (g * border_alpha // 255 << 8) | (b * border_alpha // 255)
        p_pen = ctypes.c_void_p()
        gdiplus.GdipCreatePen1(border_argb, ctypes.c_float(2.8), 0, ctypes.byref(p_pen))
        gdiplus.GdipDrawRectangleI(p_graphics, p_pen, pad, pad, w, h)
        gdiplus.GdipDeletePen(p_pen)

        blend = BLENDFUNCTION(AC_SRC_OVER, 0, 255, AC_SRC_ALPHA)
        pt_src = POINT(0, 0)
        pt_dst = POINT(win_x, win_y)
        sz_dst = SIZE(win_w, win_h)

        user32.UpdateLayeredWindow(
            self._hwnd, hdc_screen,
            ctypes.byref(pt_dst), ctypes.byref(sz_dst),
            hdc_mem, ctypes.byref(pt_src),
            0, ctypes.byref(blend), ULW_ALPHA
        )

        gdiplus.GdipDeleteGraphics(p_graphics)
        gdi32.DeleteDC(hdc_mem)
        gdi32.DeleteObject(hbmp)
        user32.ReleaseDC(None, hdc_screen)
        self._is_visible = True

    def hide(self):
        if self._hwnd and self._is_visible:
            user32.ShowWindow(self._hwnd, SW_HIDE)
            self._is_visible = False

    def cleanup(self):
        self.hide()
        if self._hwnd:
            user32.DestroyWindow(self._hwnd)
            self._hwnd = None
        if self._gdi_token:
            try:
                gdiplus.GdiplusShutdown(self._gdi_token)
            except:
                pass

class HeroGridLocator:
    def __init__(self):
        self._window = None
        self._lock = threading.Lock()

    def _ensure_window(self):
        if self._window is None:
            try:
                self._window = ClickThroughHighlightWindow()
            except Exception as e:
                print(f'[HeroGridLocator] Failed to init highlight window: {e}')
                self._window = None
        return self._window

    def get_hero_info(self, hero_key):
        if not hero_key:
            return None
        norm = str(hero_key).strip().lower().replace('npc_dota_hero_', '')
        if norm in HERO_INDEX_MAP:
            return HERO_INDEX_MAP[norm]
        clean = norm.replace('_', '').replace(' ', '').replace('-', '')
        for k, v in HERO_INDEX_MAP.items():
            if k.replace('_', '').replace(' ', '') == clean:
                return v
        return None

    def calculate_screen_rect(self, hero_info, monitor_info=None):
        if not hero_info:
            return None
        attr = hero_info['attr']
        row = hero_info['row']
        col = hero_info['col']

        base_x = ATTR_BASE_X.get(attr, 133) + col * BASE_STEP_X
        base_y = BASE_Y0 + row * BASE_STEP_Y

        if not monitor_info:
            sw = user32.GetSystemMetrics(0)
            sh = user32.GetSystemMetrics(1)
            left = 0
            top = 0
            mw = sw or 1920
            mh = sh or 1080
        else:
            left = monitor_info.get('left', 0)
            top = monitor_info.get('top', 0)
            mw = monitor_info.get('width', 1920)
            mh = monitor_info.get('height', 1080)

        scale_x = mw / 1920.0
        scale_y = mh / 1080.0

        return {
            'x': int(left + base_x * scale_x),
            'y': int(top + base_y * scale_y),
            'w': max(1, int(BASE_CARD_W * scale_x)),
            'h': max(1, int(BASE_CARD_H * scale_y))
        }

    def highlight_hero(self, hero_key, monitor_info=None):
        info = self.get_hero_info(hero_key)
        if not info:
            self.hide()
            return None
        rect = self.calculate_screen_rect(info, monitor_info)
        if not rect:
            self.hide()
            return None
        with self._lock:
            win = self._ensure_window()
            if win:
                win.render_and_position(rect['x'], rect['y'], rect['w'], rect['h'], info['attr_color'])
        return {'info': info, 'rect': rect}

    def hide(self):
        with self._lock:
            if self._window:
                self._window.hide()

    def cleanup(self):
        with self._lock:
            if self._window:
                self._window.cleanup()
                self._window = None
