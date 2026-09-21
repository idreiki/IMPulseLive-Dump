import os
import sys
import subprocess
import threading
import time
import json
import math
import random
import ctypes
from ctypes import wintypes

MUTEX_NAME = 'Global\\IMPulseLive_SingleInstance_Mutex'

def ensure_single_instance():
    try:
        kernel32 = ctypes.windll.kernel32
        mutex = kernel32.CreateMutexW(None, False, MUTEX_NAME)
        last_error = kernel32.GetLastError()
        ERROR_ALREADY_EXISTS = 183
        if last_error == ERROR_ALREADY_EXISTS:
            hwnd = ctypes.windll.user32.FindWindowW(None, 'IMPulse')
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 9)
                ctypes.windll.user32.SetForegroundWindow(hwnd)
            os._exit(0)
        return mutex
    except Exception as e:
        print('Single instance mutex error:', e)
        return None

user32 = ctypes.WinDLL('user32')
gdi32 = ctypes.WinDLL('gdi32')
gdiplus = ctypes.windll.gdiplus
kernel32 = ctypes.WinDLL('kernel32')

try:
    ctypes.windll.user32.SetWindowPos.argtypes = None
except Exception:
    pass

user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.DefWindowProcW.restype = wintypes.LPARAM
user32.CreateWindowExW.restype = wintypes.HWND
user32.CreateWindowExW.argtypes = [
    wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD,
    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    wintypes.HWND, wintypes.HMENU, wintypes.HINSTANCE, wintypes.LPVOID
]
user32.GetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int]
user32.GetWindowLongPtrW.restype = ctypes.c_ssize_t
user32.SetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_ssize_t]
user32.SetWindowLongPtrW.restype = ctypes.c_ssize_t
user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.UINT]
user32.SetWindowPos.restype = wintypes.BOOL
user32.SetLayeredWindowAttributes.argtypes = [wintypes.HWND, wintypes.COLORREF, ctypes.c_byte, wintypes.DWORD]
user32.SetLayeredWindowAttributes.restype = wintypes.BOOL
user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
user32.ShowWindow.restype = wintypes.BOOL
user32.SetForegroundWindow.argtypes = [wintypes.HWND]
user32.SetForegroundWindow.restype = wintypes.BOOL
user32.BringWindowToTop.argtypes = [wintypes.HWND]
user32.BringWindowToTop.restype = wintypes.BOOL
user32.FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
user32.FindWindowW.restype = wintypes.HWND

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

class POINT(ctypes.Structure):
    _fields_ = [('x', wintypes.LONG), ('y', wintypes.LONG)]

class SIZE(ctypes.Structure):
    _fields_ = [('cx', wintypes.LONG), ('cy', wintypes.LONG)]

user32.UpdateLayeredWindow.argtypes = [
    wintypes.HWND, wintypes.HDC, ctypes.POINTER(POINT), ctypes.POINTER(SIZE),
    wintypes.HDC, ctypes.POINTER(POINT), wintypes.COLORREF,
    ctypes.POINTER(BLENDFUNCTION), wintypes.DWORD
]

class GdiplusStartupInput(ctypes.Structure):
    _fields_ = [
        ('GdiplusVersion', wintypes.DWORD),
        ('DebugEventCallback', ctypes.c_void_p),
        ('SuppressBackgroundThread', wintypes.BOOL),
        ('SuppressExternalCodecs', wintypes.BOOL)
    ]

class GdiplusSplash:
    def __init__(self, min_duration=2.0):
        self.min_duration = min_duration
        self.start_time = time.time()
        self.running = True
        self.backend_ready = False
        self.gdi_token = ctypes.c_ulong()
        startup_in = GdiplusStartupInput(1, None, False, False)
        gdiplus.GdiplusStartup(ctypes.byref(self.gdi_token), ctypes.byref(startup_in), None)

        self.width = 440
        self.height = 440
        sw = user32.GetSystemMetrics(0)
        sh = user32.GetSystemMetrics(1)
        self.x = (sw - self.width) // 2
        self.y = (sh - self.height) // 2

        WNDPROC = ctypes.WINFUNCTYPE(wintypes.LPARAM, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
        def wnd_proc(hwnd, msg, wp, lp):
            return user32.DefWindowProcW(hwnd, msg, wp, lp)
        self.proc = WNDPROC(wnd_proc)

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

        wnd_class = WNDCLASSEXW()
        wnd_class.cbSize = ctypes.sizeof(WNDCLASSEXW)
        wnd_class.lpfnWndProc = self.proc
        wnd_class.hInstance = kernel32.GetModuleHandleW(None)
        wnd_class.lpszClassName = f'IMPulseGdiSplash_{id(self)}'
        user32.RegisterClassExW(ctypes.byref(wnd_class))

        WS_EX_LAYERED = 524288
        WS_EX_TOPMOST = 8
        WS_EX_TOOLWINDOW = 128
        WS_POPUP = 2147483648

        self.hwnd = user32.CreateWindowExW(
            WS_EX_LAYERED | WS_EX_TOPMOST | WS_EX_TOOLWINDOW,
            wnd_class.lpszClassName, 'IMPulseSplash', WS_POPUP,
            self.x, self.y, self.width, self.height,
            None, None, wnd_class.hInstance, None
        )

        self.hdc_screen = user32.GetDC(None)
        self.hdc_mem = gdi32.CreateCompatibleDC(self.hdc_screen)

        bmi = BITMAPINFOHEADER()
        bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bmi.biWidth = self.width
        bmi.biHeight = -self.height
        bmi.biPlanes = 1
        bmi.biBitCount = 32
        bmi.biCompression = 0

        self.p_bits = ctypes.c_void_p()
        self.hbmp = gdi32.CreateDIBSection(self.hdc_mem, ctypes.byref(bmi), 0, ctypes.byref(self.p_bits), None, 0)
        gdi32.SelectObject(self.hdc_mem, self.hbmp)

        self.p_graphics = ctypes.c_void_p()
        gdiplus.GdipCreateFromHDC(self.hdc_mem, ctypes.byref(self.p_graphics))
        gdiplus.GdipSetSmoothingMode(self.p_graphics, 4)

        random.seed(1337)
        self.radius = 140.0
        self.points = []
        for _ in range(26):
            theta = math.acos(2 * random.random() - 1)
            phi = 2 * math.pi * random.random()
            r = self.radius * (0.65 + 0.35 * random.random())
            self.points.append({
                'x': r * math.sin(theta) * math.cos(phi),
                'y': r * math.sin(theta) * math.sin(phi),
                'z': r * math.cos(theta),
                'base_r': random.uniform(3.0, 4.4)
            })

        self.blend = BLENDFUNCTION(0, 0, 255, 1)
        self.pt_src = POINT(0, 0)
        self.pt_dst = POINT(self.x, self.y)
        self.sz_dst = SIZE(self.width, self.height)
        user32.ShowWindow(self.hwnd, 5)

    def mark_ready(self):
        self.backend_ready = True

    def run_loop(self):
        try:
            angle_x = 0.0
            angle_y = 0.0
            fov = 360.0
            cx, cy = (self.width / 2, self.height / 2)
            ULW_ALPHA = 2
            while self.running:
                elapsed = time.time() - self.start_time
                if self.backend_ready and elapsed >= self.min_duration:
                    break
                ctypes.memset(self.p_bits, 0, self.width * self.height * 4)
                angle_x += 0.008
                angle_y += 0.012
                cos_x, sin_x = (math.cos(angle_x), math.sin(angle_x))
                cos_y, sin_y = (math.cos(angle_y), math.sin(angle_y))
                projected = []
                for p in self.points:
                    x1 = p['x'] * cos_y + p['z'] * sin_y
                    z1 = -p['x'] * sin_y + p['z'] * cos_y
                    y2 = p['y'] * cos_x - z1 * sin_x
                    z2 = p['y'] * sin_x + z1 * cos_x
                    scale = fov / (fov + z2 + 240)
                    x2d = cx + x1 * scale
                    y2d = cy + y2 * scale
                    projected.append((x2d, y2d, z2, scale, p))

                for i in range(len(projected)):
                    p1 = projected[i]
                    for j in range(i + 1, len(projected)):
                        p2 = projected[j]
                        dx = p1[0] - p2[0]
                        dy = p1[1] - p2[1]
                        dist = math.hypot(dx, dy)
                        if dist < 88:
                            dist_factor = 1.0 - dist / 88.0
                            depth_factor = min(1.0, min(p1[3], p2[3]) * 1.35)
                            alpha = int(dist_factor * 215 * depth_factor)
                            alpha = max(25, min(230, alpha))
                            pr_r = 56 * alpha // 255
                            pr_g = 189 * alpha // 255
                            pr_b = 248 * alpha // 255
                            color_argb = alpha << 24 | pr_r << 16 | pr_g << 8 | pr_b
                            p_pen = ctypes.c_void_p()
                            gdiplus.GdipCreatePen1(color_argb, ctypes.c_float(1.6), 0, ctypes.byref(p_pen))
                            gdiplus.GdipDrawLine(self.p_graphics, p_pen, ctypes.c_float(p1[0]), ctypes.c_float(p1[1]), ctypes.c_float(p2[0]), ctypes.c_float(p2[1]))
                            gdiplus.GdipDeletePen(p_pen)

                for pt in projected:
                    x2d, y2d, z2, scale, p = pt
                    r = max(2.2, p['base_r'] * scale)
                    norm_z = max(0.0, min(1.0, (pt[2] + self.radius) / (2 * self.radius)))
                    alpha = int((0.6 + 0.4 * norm_z) * 255)
                    glow_r = r * 2.2
                    glow_alpha = int(alpha * 0.35)
                    g_r = 14 * glow_alpha // 255
                    g_g = 165 * glow_alpha // 255
                    g_b = 233 * glow_alpha // 255
                    glow_argb = glow_alpha << 24 | g_r << 16 | g_g << 8 | g_b
                    p_brush_glow = ctypes.c_void_p()
                    gdiplus.GdipCreateSolidFill(glow_argb, ctypes.byref(p_brush_glow))
                    gdiplus.GdipFillEllipse(self.p_graphics, p_brush_glow, ctypes.c_float(x2d - glow_r), ctypes.c_float(y2d - glow_r), ctypes.c_float(2 * glow_r), ctypes.c_float(2 * glow_r))
                    gdiplus.GdipDeleteBrush(p_brush_glow)

                    pr_r = 56 * alpha // 255
                    pr_g = 189 * alpha // 255
                    pr_b = 248 * alpha // 255
                    color_argb = alpha << 24 | pr_r << 16 | pr_g << 8 | pr_b
                    p_brush = ctypes.c_void_p()
                    gdiplus.GdipCreateSolidFill(color_argb, ctypes.byref(p_brush))
                    gdiplus.GdipFillEllipse(self.p_graphics, p_brush, ctypes.c_float(x2d - r), ctypes.c_float(y2d - r), ctypes.c_float(2 * r), ctypes.c_float(2 * r))
                    gdiplus.GdipDeleteBrush(p_brush)

                    inner_r = max(1.2, r * 0.5)
                    inner_alpha = min(255, int(alpha * 1.1))
                    in_r = 224 * inner_alpha // 255
                    in_g = 242 * inner_alpha // 255
                    in_b = 254 * inner_alpha // 255
                    inner_argb = inner_alpha << 24 | in_r << 16 | in_g << 8 | in_b
                    p_brush_in = ctypes.c_void_p()
                    gdiplus.GdipCreateSolidFill(inner_argb, ctypes.byref(p_brush_in))
                    gdiplus.GdipFillEllipse(self.p_graphics, p_brush_in, ctypes.c_float(x2d - inner_r), ctypes.c_float(y2d - inner_r), ctypes.c_float(2 * inner_r), ctypes.c_float(2 * inner_r))
                    gdiplus.GdipDeleteBrush(p_brush_in)

                user32.UpdateLayeredWindow(self.hwnd, self.hdc_screen, ctypes.byref(self.pt_dst), ctypes.byref(self.sz_dst), self.hdc_mem, ctypes.byref(self.pt_src), 0, ctypes.byref(self.blend), ULW_ALPHA)
                time.sleep(0.016)
        except Exception as e:
            print('Splash loop warning:', e)
        finally:
            self.cleanup()

    def cleanup(self):
        self.running = False
        try:
            gdiplus.GdipDeleteGraphics(self.p_graphics)
            user32.DestroyWindow(self.hwnd)
            user32.ReleaseDC(None, self.hdc_screen)
            gdi32.DeleteDC(self.hdc_mem)
            gdi32.DeleteObject(self.hbmp)
            gdiplus.GdiplusShutdown(self.gdi_token)
        except Exception:
            return None

from flask import Flask, render_template, request, jsonify, send_from_directory, Response

try:
    import ui_bundle
    HAS_UI_BUNDLE = True
except ImportError:
    HAS_UI_BUNDLE = False

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.abspath(os.path.dirname(__file__))

BASE_DIR = get_base_path()

def find_free_port(start_port=5000, max_tries=50):
    import socket
    for p in range(start_port, start_port + max_tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', p))
                return p
        except OSError:
            continue
    return start_port

SERVER_PORT = find_free_port(5000)
app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'static'), template_folder=os.path.join(BASE_DIR, 'templates'))
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

settings = {
    'steam_id': '', 'timeframe': 'all', 'team': 'radiant', 'role': 'all',
    'mode': '1m', 'calc': 'meta', 'strictness': 'normal', 'decay': False,
    'role_transfer_enabled': False, 'popularity': 'meta', 'winrate': 'all',
    'eval_method': 'bayes', 'rank': 'all', 'lang': 'ru', 'hotkey': 'INSERT',
    'opacity': 90, 'perf_mode': 'balanced', 'auto': {'resolution': 'auto', 'grid_highlight': True}
}

def get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.abspath(os.path.dirname(__file__))

APP_DIR = get_app_dir()
BASE_DIR = getattr(sys, '_MEIPASS', APP_DIR)
CONFIG_FILE = os.path.join(APP_DIR, 'config.json')

def ensure_overlay_window_styles(hwnd):
    """Enforces WS_EX_TOOLWINDOW (hidden from taskbar), WS_EX_TOPMOST (always on top of games/apps), and opacity."""
    try:
        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 524288
        WS_EX_TOOLWINDOW = 128
        WS_EX_APPWINDOW = 262144
        LWA_ALPHA = 2
        HWND_TOPMOST = -1
        SWP_NOMOVE = 2
        SWP_NOSIZE = 1
        SWP_SHOWWINDOW = 64

        alpha = int(255 * (float(settings.get('opacity', 90)) / 100.0))
        alpha = max(60, min(255, alpha))

        style = user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
        new_style = (style | WS_EX_LAYERED | WS_EX_TOOLWINDOW) & ~WS_EX_APPWINDOW
        user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, new_style)
        user32.SetLayeredWindowAttributes(hwnd, 0, alpha, LWA_ALPHA)
        user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
        user32.ShowWindow(hwnd, 5)
        user32.BringWindowToTop(hwnd)
        user32.SetForegroundWindow(hwnd)

        WM_SETICON = 128
        ICON_SMALL = 0
        ICON_BIG = 1
        IMAGE_ICON = 1
        LR_LOADFROMFILE = 16
        ico_path = os.path.join(APP_DIR, 'assets', 'icon.ico')
        if not os.path.exists(ico_path):
            ico_path = os.path.join(BASE_DIR, 'assets', 'icon.ico')
        if os.path.exists(ico_path):
            h_icon = user32.LoadImageW(None, ico_path, IMAGE_ICON, 0, 0, LR_LOADFROMFILE)
            if h_icon:
                user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, h_icon)
                user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, h_icon)
    except Exception as e:
        print('Overlay window style error:', e)

def set_window_opacity(val):
    try:
        if window:
            hwnd = user32.FindWindowW(None, 'IMPulse')
            if hwnd:
                alpha = int(255 * (float(val) / 100.0))
                user32.SetLayeredWindowAttributes(hwnd, 0, alpha, 2)
    except Exception as e:
        print('Set opacity error:', e)

def get_data_dir():
    """Resolves data directory strictly at APP_DIR/data or fallback."""
    for cand in [os.path.join(APP_DIR, 'data'), os.path.join(APP_DIR, '..', 'IMPulseLive', 'data')]:
        if os.path.exists(cand):
            return os.path.abspath(cand)
    data_dir = os.path.join(APP_DIR, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def get_icons_path():
    possible_paths = [
        os.path.join(BASE_DIR, 'assets', 'panorama', 'images', 'heroes'),
        os.path.join(APP_DIR, 'assets', 'panorama', 'images', 'heroes'),
        os.path.join(APP_DIR, '..', 'IMPulseLive', '_internal', 'assets', 'panorama', 'images', 'heroes')
    ]
    for p in possible_paths:
        if os.path.exists(p):
            return os.path.abspath(p)
    return None

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                settings.update(saved)
                if settings.get('calc') == 'player':
                    settings['calc'] = 'smart'
        except Exception as e:
            print(f'Failed to load config: {e}')

def save_config():
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print(f'Failed to save config: {e}')

evaluator = None
dataset_updater = None
security_guard = None
manual_team_lock = False
state_lock = threading.Lock()
cached_monitor = None
custom_roles = {'radiant': {}, 'dire': {}}

from hero_grid_locator import HeroGridLocator
hero_locator = HeroGridLocator()

state = {
    'radiant': [], 'dire': [], 'recs': [], 'draft_active': False,
    'is_draft_screen': False, 'detection_mode': 'draft', 'sync_status': 'Idle',
    'dataset_status': 'Idle', 'player_count': 0, 'calibration_status': 'ok',
    'calibration_message': 'Готов', 'screen_resolution': '', 'phase': 'menu',
    'num_picked': 0, 'post_analysis': None, 'locked': False, 'lock_info': None
}

def on_dataset_updated(rank=None):
    current_rank = rank or settings.get('rank', 'all')
    if evaluator:
        evaluator.set_rank(current_rank)
        evaluator.aggregate_meta(settings.get('mode', '1m'))
        recalculate_recs()
    with state_lock:
        if dataset_updater:
            state['dataset_status'] = dataset_updater.status

def recalculate_recs():
    if security_guard and security_guard.is_locked():
        with state_lock:
            state['locked'] = True
            state['lock_info'] = security_guard.get_lock_payload()
            state['recs'] = []
            state['evaluation'] = None
            state['post_analysis'] = None
            state['radiant'] = [''] * 5
            state['dire'] = [''] * 5
        return

    if not evaluator:
        return

    with state_lock:
        enemies = list(state['dire'] if settings['team'] == 'radiant' else state['radiant'])
        allies = list(state['radiant'] if settings['team'] == 'radiant' else state['dire'])
        rad_copy = list(state['radiant'])
        dire_copy = list(state['dire'])
        has_picks = any(h for h in allies if h) or any(h for h in enemies if h)
        is_draft_screen = state.get('is_draft_screen', False)
        detection_mode = state.get('detection_mode', 'draft')

    if has_picks:
        post_res = evaluator.get_post_draft_analysis(rad_copy, dire_copy, user_team=settings.get('team', 'radiant'), custom_roles=custom_roles)
        eval_res = evaluator.evaluate_draft(rad_copy, dire_copy, calc_mode=settings.get('calc', 'delta'), rad_roles=post_res.get('rad_roles') if post_res else None, dire_roles=post_res.get('dire_roles') if post_res else None)
        recs_res = evaluator.get_recommendations(
            allies, enemies, target_role=settings['role'], top_n=20,
            timeframe=settings['mode'], calc_mode=settings['calc'],
            strictness=settings.get('strictness', 'normal'), decay=settings.get('decay', False),
            role_transfer_enabled=settings.get('role_transfer_enabled', False),
            popularity=settings.get('popularity', 'meta'), winrate_filter=settings.get('winrate', 'all'),
            eval_method=settings.get('eval_method', 'bayes')
        )
        n_picked = sum(1 for h in rad_copy + dire_copy if h)
        is_ingame = detection_mode == 'ingame'
        current_phase = 'ingame' if is_ingame else ('post' if n_picked == 10 else 'draft')
        with state_lock:
            state['draft_active'] = not is_ingame
            state['evaluation'] = eval_res
            state['recs'] = recs_res
            state['post_analysis'] = post_res
            state['num_picked'] = n_picked
            state['phase'] = current_phase
    else:
        meta_res = evaluator.get_meta_heroes(
            target_role=settings['role'], top_n=15, timeframe=settings['mode'],
            calc_mode=settings['calc'], strictness=settings.get('strictness', 'normal'),
            decay=settings.get('decay', False), role_transfer_enabled=settings.get('role_transfer_enabled', False),
            popularity=settings.get('popularity', 'meta'), winrate_filter=settings.get('winrate', 'all'),
            eval_method=settings.get('eval_method', 'bayes')
        )
        with state_lock:
            in_draft = is_draft_screen and detection_mode == 'draft'
            state['draft_active'] = in_draft
            state['evaluation'] = None
            state['recs'] = meta_res
            state['post_analysis'] = None
            state['num_picked'] = 0
            state['phase'] = 'draft' if in_draft else 'menu'

    with state_lock:
        if state.get('recs'):
            for r in state['recs']:
                loc_info = hero_locator.get_hero_info(r.get('cdnName') or r.get('name'))
                if loc_info:
                    r['grid'] = {
                        'attr': loc_info['attr'], 'attr_ru': loc_info['attr_ru'],
                        'attr_en': loc_info['attr_en'],
                        'attr_short_ru': loc_info.get('attr_short_ru', loc_info['attr_ru'][:3].upper()),
                        'attr_short_en': loc_info.get('attr_short_en', loc_info['attr_en'][:3].upper()),
                        'attr_color': loc_info['attr_color'], 'row': loc_info['row'],
                        'col': loc_info['col'], 'summary_ru': loc_info['summary_ru'],
                        'summary_en': loc_info['summary_en']
                    }

def get_capture_monitor(sct):
    target_idx = settings.get('monitor_index', None)
    if target_idx is not None and 0 <= target_idx < len(sct.monitors):
        return sct.monitors[target_idx]
    for m in sct.monitors[1:]:
        if m.get('is_primary'):
            return m
    if len(sct.monitors) > 1:
        return sct.monitors[1]
    else:
        return sct.monitors[0]

def log_scan(msg):
    try:
        log_file = os.path.join(APP_DIR, 'scan_debug.log')
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    except Exception:
        pass

def detect_team_unified(img_bgr, ui_scale):
    import cv2
    import numpy as np
    h, w = img_bgr.shape[:2]
    y1, y2 = (int(75 * ui_scale), int(125 * ui_scale))
    rad_crop = img_bgr[y1:y2, int(w * 0.08):int(w * 0.44)]
    dire_crop = img_bgr[y1:y2, int(w * 0.56):int(w * 0.92)]
    if rad_crop.size > 0 and dire_crop.size > 0:
        rad_gray = cv2.cvtColor(rad_crop, cv2.COLOR_BGR2GRAY)
        dire_gray = cv2.cvtColor(dire_crop, cv2.COLOR_BGR2GRAY)
        r_bright = int(np.sum(rad_gray > 185))
        d_bright = int(np.sum(dire_gray > 185))
        if r_bright > 90 and r_bright > d_bright * 1.4:
            return 'radiant'
        elif d_bright > 90 and d_bright > r_bright * 1.4:
            return 'dire'
    return None

def scan_loop():
    global cached_monitor
    global manual_team_lock
    import mss
    import numpy as np
    import cv2
    from find_all_heroes import detect_heroes

    icons_path = get_icons_path()
    log_scan(f'Scan loop started. Resolved icons_path: {icons_path} (exists={icons_path is not None and os.path.exists(icons_path)})')
    last_team_check = 0
    consecutive_empty_scans = 0
    gray_buffer = {}

    with (getattr(mss, 'MSS', None) or mss.mss)() as sct:
        monitor = get_capture_monitor(sct)
        cached_monitor = monitor
        log_scan(f'MSS session opened. Target monitor: {monitor}')

        while True:
            try:
                if 'security_guard' in globals() and security_guard and security_guard.is_locked():
                    with state_lock:
                        state['radiant'] = [''] * 5
                        state['dire'] = [''] * 5
                        state['recs'] = []
                        state['evaluation'] = None
                    time.sleep(1.0)
                    continue

                if 'is_hidden' in globals() and is_hidden:
                    time.sleep(1.0)
                    continue

                img_bgra = np.array(sct.grab(monitor))
                img_bgr = cv2.cvtColor(img_bgra, cv2.COLOR_BGRA2BGR)
                h, w = img_bgr.shape[:2]
                ui_scale = min(w / 1920.0, h / 1080.0)

                t0 = time.time()
                detection_data = detect_heroes(img_bgr, icons_dir=icons_path, forced_resolution=settings.get('resolution', 'auto'))
                detect_elapsed = time.time() - t0

                calib_info = detection_data.get('calibration', {})
                with state_lock:
                    state['calibration_status'] = calib_info.get('res_status', 'ok')
                    state['calibration_message'] = calib_info.get('res_msg', 'Готов')
                    state['screen_resolution'] = calib_info.get('resolution', f'{w}x{h}')
                    curr_rad = list(state['radiant'])
                    curr_dire = list(state['dire'])

                raw_res = detection_data.get('raw_results', [])
                gray_heroes = set(item[0] for item in raw_res if len(item) >= 7 and item[6])
                detected_radiant = list(detection_data.get('radiant', [''] * 5))
                detected_dire = list(detection_data.get('dire', [''] * 5))

                for i in range(5):
                    h_name = detected_radiant[i]
                    if h_name and h_name in gray_heroes:
                        k = f'r_{i}_{h_name}'
                        gray_buffer[k] = gray_buffer.get(k, 0) + 1
                        if gray_buffer[k] < 2 and (i >= len(curr_rad) or curr_rad[i] != h_name):
                            detected_radiant[i] = ''
                    else:
                        if not h_name:
                            for k in list(gray_buffer.keys()):
                                if k.startswith(f'r_{i}_'):
                                    del gray_buffer[k]

                for i in range(5):
                    h_name = detected_dire[i]
                    if h_name and h_name in gray_heroes:
                        k = f'd_{i}_{h_name}'
                        gray_buffer[k] = gray_buffer.get(k, 0) + 1
                        if gray_buffer[k] < 2 and (i >= len(curr_dire) or curr_dire[i] != h_name):
                            detected_dire[i] = ''
                    else:
                        if not h_name:
                            for k in list(gray_buffer.keys()):
                                if k.startswith(f'd_{i}_'):
                                    del gray_buffer[k]

                num_detected = sum(1 for h in detected_radiant + detected_dire if h)
                detection_mode = detection_data.get('mode', 'draft')
                calib_source = calib_info.get('source', '')
                is_draft_screen = (detection_mode == 'draft' and calib_source == 'adaptive_draft')
                is_ingame_screen = (detection_mode == 'ingame')

                with state_lock:
                    state['detection_mode'] = detection_mode
                    state['is_draft_screen'] = is_draft_screen

                if is_ingame_screen:
                    was_draft = False
                    with state_lock:
                        if state.get('draft_active', False) or state.get('phase') != 'ingame':
                            state['draft_active'] = False
                            state['phase'] = 'ingame'
                            was_draft = True
                    if was_draft:
                        hero_locator.hide()
                        log_scan('In-game HUD detected - Draft finished. Transitioning to match phase.')
                else:
                    if is_draft_screen and num_detected == 0:
                        consecutive_empty_scans = 0
                        entered_draft = False
                        with state_lock:
                            if not state.get('draft_active', False) or state.get('phase') != 'draft':
                                state['draft_active'] = True
                                state['phase'] = 'draft'
                                entered_draft = True
                        if entered_draft:
                            log_scan('Draft screen detected - First Pick phase.')
                            recalculate_recs()

                if num_detected > 0:
                    consecutive_empty_scans = 0
                    cur_heroes = set(h for h in curr_rad + curr_dire if h)
                    det_heroes = set(h for h in detected_radiant + detected_dire if h)
                    overlap = cur_heroes.intersection(det_heroes)
                    is_new_match = False

                    if not cur_heroes:
                        is_new_match = True
                    elif len(cur_heroes) >= 6 and num_detected <= 4 and (len(overlap) <= 1):
                        is_new_match = True
                    elif len(overlap) == 0 and num_detected >= 2:
                        is_new_match = True
                    else:
                        for i in range(5):
                            if i < len(curr_rad) and curr_rad[i] and detected_radiant[i] and (curr_rad[i] != detected_radiant[i]):
                                is_new_match = True
                                break
                            if i < len(curr_dire) and curr_dire[i] and detected_dire[i] and (curr_dire[i] != detected_dire[i]):
                                is_new_match = True
                                break

                    if is_new_match:
                        manual_team_lock = False
                        new_r = list(detected_radiant)
                        new_d = list(detected_dire)
                    else:
                        new_r = list(detected_radiant)
                        new_d = list(detected_dire)
                        for i in range(5):
                            if not new_r[i] and i < len(curr_rad) and curr_rad[i]:
                                new_r[i] = curr_rad[i]
                            if not new_d[i] and i < len(curr_dire) and curr_dire[i]:
                                new_d[i] = curr_dire[i]

                    if new_r != curr_rad or new_d != curr_dire:
                        with state_lock:
                            state['radiant'] = new_r
                            state['dire'] = new_d
                        r_valid = [h for h in new_r if h]
                        d_valid = [h for h in new_d if h]
                        log_scan(f'Picks updated ({detect_elapsed:.3f}s) | Radiant: {r_valid} | Dire: {d_valid}')
                        recalculate_recs()
                else:
                    if num_detected == 0 and (not is_draft_screen):
                        consecutive_empty_scans += 1
                        cur_picked = sum(1 for h in curr_rad + curr_dire if h)
                        empty_threshold = 15 if cur_picked >= 8 else 2
                        if consecutive_empty_scans >= empty_threshold and (any(curr_rad) or any(curr_dire) or state.get('draft_active', False) or (state.get('phase') != 'menu')):
                            with state_lock:
                                state['radiant'] = [''] * 5
                                state['dire'] = [''] * 5
                                state['is_draft_screen'] = False
                                state['draft_active'] = False
                                state['phase'] = 'menu'
                                state['detection_mode'] = 'draft'
                            manual_team_lock = False
                            hero_locator.hide()
                            log_scan(f'Picks cleared after {consecutive_empty_scans} empty frames.')
                            recalculate_recs()

                with state_lock:
                    has_all_heroes = sum(1 for h in state['radiant'] + state['dire'] if h) == 10
                    if is_ingame_screen:
                        state['phase'] = 'ingame'
                        state['draft_active'] = False
                    elif has_all_heroes:
                        state['phase'] = 'post'

                perf = settings.get('perf_mode', 'balanced')
                num_picked = sum(1 for h in curr_rad + curr_dire if h)
                if not manual_team_lock and state.get('draft_active', False) and (detection_mode == 'draft') and (calib_source == 'adaptive_draft') and (0 <= num_picked <= 10) and (time.time() - last_team_check > 2.0):
                    last_team_check = time.time()
                    new_team = detect_team_unified(img_bgr, ui_scale)
                    if new_team and new_team != settings['team']:
                        settings['team'] = new_team
                        save_config()
                        log_scan(f'Team automatically identified: {new_team.upper()}')
                        recalculate_recs()

                if (detection_mode == 'ingame' or has_all_heroes) and num_detected >= 8:
                    time.sleep(3.5 if perf != 'high' else 2.0)
                elif perf == 'eco':
                    time.sleep(1.2)
                elif perf == 'high':
                    time.sleep(0.3)
                else:
                    time.sleep(0.6)

            except Exception as grab_err:
                log_scan(f'Screen capture error: {grab_err}')
                time.sleep(1.0)

@app.route('/assets/<path:path>')
def send_assets(path):
    assets_dir = os.path.join(BASE_DIR, 'assets')
    return send_from_directory(assets_dir, path)

@app.route('/')
def index():
    if HAS_UI_BUNDLE:
        try:
            return Response(ui_bundle.get_index_html(), mimetype='text/html')
        except Exception:
            pass
    return render_template('index.html')

@app.route('/tiktok')
def tiktok_deck():
    return render_template('tiktok_deck.html')

@app.route('/static/css/style.css')
def send_style_css():
    if HAS_UI_BUNDLE:
        try:
            return Response(ui_bundle.get_style_css(), mimetype='text/css')
        except Exception:
            pass
    return send_from_directory(os.path.join(BASE_DIR, 'static', 'css'), 'style.css')

@app.route('/static/js/main.js')
def send_main_js():
    if HAS_UI_BUNDLE:
        try:
            return Response(ui_bundle.get_main_js(), mimetype='application/javascript')
        except Exception:
            pass
    return send_from_directory(os.path.join(BASE_DIR, 'static', 'js'), 'main.js')

@app.route('/static/icon.png')
def send_icon_png():
    if HAS_UI_BUNDLE:
        try:
            return Response(ui_bundle.get_icon_png(), mimetype='image/png')
        except Exception:
            pass
    return send_from_directory(os.path.join(BASE_DIR, 'static'), 'icon.png')

@app.route('/static/favicon.ico')
def send_favicon_ico():
    if HAS_UI_BUNDLE:
        try:
            return Response(ui_bundle.get_favicon(), mimetype='image/x-icon')
        except Exception:
            pass
    return send_from_directory(os.path.join(BASE_DIR, 'static'), 'favicon.ico')

@app.route('/api/state')
def get_state():
    is_locked = False
    lock_info = None
    if 'security_guard' in globals() and security_guard:
        is_locked = security_guard.is_locked()
        if is_locked:
            lock_info = security_guard.get_lock_payload()
    with state_lock:
        if is_locked:
            state['locked'] = True
            state['lock_info'] = lock_info
            state['recs'] = []
            state['evaluation'] = None
            state['radiant'] = [''] * 5
            state['dire'] = [''] * 5
        else:
            state['locked'] = False
            state['lock_info'] = None
            if dataset_updater:
                state['dataset_status'] = dataset_updater.status
                if dataset_updater.status == 'Updated' and evaluator:
                    evaluator.set_rank(settings.get('rank', 'all'))
                    evaluator.aggregate_meta(settings.get('mode', '1m'))
                    recalculate_recs()
                    dataset_updater.status = 'Idle'
        state_copy = {k: list(v) if isinstance(v, list) else v for k, v in state.items()}
        settings_copy = dict(settings)
    return jsonify({'state': state_copy, 'settings': settings_copy, 'locked': is_locked, 'lock_info': lock_info})

@app.route('/api/open_telegram', methods=['POST'])
def open_telegram():
    url = 'https://t.me/impulse_dota'
    if 'security_guard' in globals() and security_guard:
        payload = security_guard.get_lock_payload()
        url = payload.get('telegram_url') or url
    try:
        import webbrowser
        webbrowser.open(url)
        return jsonify({'status': 'ok', 'url': url})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/check_license', methods=['POST'])
def check_license():
    global dataset_updater
    global evaluator
    if 'security_guard' in globals() and security_guard:
        ok = security_guard.check_security(force=True)
        if ok:
            data_dir = get_data_dir()
            if not evaluator:
                from pick_evaluator import Evaluator
                evaluator = Evaluator(data_dir=data_dir)
            evaluator.set_rank(settings.get('rank', 'all'))
            evaluator.aggregate_meta(settings.get('mode', '1m'))
            if not dataset_updater:
                from dataset_updater import DatasetUpdater
                dataset_updater = DatasetUpdater(data_dir, on_update=on_dataset_updated)
                dataset_updater.start_update_thread(rank=settings.get('rank', 'all'))
            recalculate_recs()
        return jsonify(security_guard.get_lock_payload())
    else:
        return jsonify({'locked': False})

@app.route('/api/reset_draft', methods=['POST'])
def reset_draft():
    global custom_roles
    global manual_team_lock
    with state_lock:
        state['radiant'] = [''] * 5
        state['dire'] = [''] * 5
        state['draft_active'] = False
        state['is_draft_screen'] = False
        state['evaluation'] = None
        state['num_picked'] = 0
        state['phase'] = 'menu'
        state['detection_mode'] = 'draft'
    custom_roles = {'radiant': {}, 'dire': {}}
    manual_team_lock = False
    hero_locator.hide()
    recalculate_recs()
    return jsonify({'success': True})

@app.route('/api/swap_roles', methods=['POST'])
def swap_roles():
    data = request.json or {}
    team = data.get('team', 'radiant').lower()
    if team not in ['radiant', 'dire']:
        team = 'radiant'
    h1 = data.get('hero1')
    h2 = data.get('hero2')
    r1 = data.get('role1')
    r2 = data.get('role2')
    if h1 and h2:
        if r1 is None or r2 is None:
            with state_lock:
                pa = state.get('post_analysis')
                roles_map = {}
                if pa:
                    roles_map = pa.get(f'{team}_roles', {})
            if r1 is None:
                r1 = custom_roles[team].get(h1, roles_map.get(h1, 1))
            if r2 is None:
                r2 = custom_roles[team].get(h2, roles_map.get(h2, 2))
        custom_roles[team][h1] = int(r2)
        custom_roles[team][h2] = int(r1)
        recalculate_recs()
        return jsonify({'status': 'ok', 'custom_roles': custom_roles})
    else:
        return (jsonify({'status': 'error', 'message': 'Missing hero parameters'}), 400)

@app.route('/api/reset_roles', methods=['POST'])
def reset_roles():
    global custom_roles
    custom_roles = {'radiant': {}, 'dire': {}}
    recalculate_recs()
    return jsonify({'status': 'ok'})

@app.route('/api/debug_scan')
def get_debug_scan():
    log_content = ''
    try:
        log_file = os.path.join(APP_DIR, 'scan_debug.log')
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                log_content = ''.join(f.readlines()[-30:])
    except Exception:
        pass
    with state_lock:
        rad_copy = list(state['radiant'])
        dire_copy = list(state['dire'])
        draft_copy = state['draft_active']
    return jsonify({'radiant': rad_copy, 'dire': dire_copy, 'draft_active': draft_copy, 'log': log_content})

@app.route('/api/debug_capture', methods=['GET', 'POST'])
def debug_capture():
    from find_all_heroes import generate_debug_overlay
    import mss
    import numpy as np
    try:
        with (getattr(mss, 'MSS', None) or mss.mss)() as sct:
            monitor = get_capture_monitor(sct)
            sct_img = sct.grab(monitor)
            img_bgr = np.array(sct_img)[:, :, :3]
            out_file = os.path.join(APP_DIR, 'debug_capture.png')
            icons_path = get_icons_path()
            generate_debug_overlay(img_bgr, output_path=out_file, icons_dir=icons_path, forced_resolution=settings.get('resolution', 'auto'))
            if os.path.exists(out_file):
                try:
                    os.startfile(out_file)
                except Exception:
                    pass
            return jsonify({'status': 'ok', 'path': out_file})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/patches')
def get_patches():
    if not evaluator:
        return jsonify([])
    else:
        return jsonify(evaluator.get_recent_patches())

@app.route('/api/highlight', methods=['POST'])
def api_highlight():
    global cached_monitor
    try:
        with state_lock:
            if not state.get('draft_active', False) and (not state.get('is_draft_screen', False)):
                hero_locator.hide()
                return jsonify({'status': 'ignored', 'reason': 'draft not active'})

        if not settings.get('grid_highlight', True):
            hero_locator.hide()
            return jsonify({'status': 'ok', 'highlight': None, 'disabled': True})

        data = request.json or {}
        hero_key = data.get('hero')
        if hero_key:
            monitor = cached_monitor
            if not monitor:
                import mss
                with (getattr(mss, 'MSS', None) or mss.mss)() as sct:
                    monitor = get_capture_monitor(sct)
                    cached_monitor = monitor
            res = hero_locator.highlight_hero(hero_key, monitor)
            return jsonify({'status': 'ok', 'highlight': res})
        else:
            hero_locator.hide()
            return jsonify({'status': 'ok', 'highlight': None})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/settings', methods=['POST'])
def update_settings():
    global manual_team_lock
    data = request.json or {}
    changed = False
    old_rank = settings.get('rank')
    old_mode = settings.get('mode')

    for k, v in data.items():
        if k in settings and settings[k] != v:
            settings[k] = v
            changed = True

    new_rank = settings.get('rank')
    new_mode = settings.get('mode', '1m')
    rank_changed = old_rank != new_rank
    mode_changed = old_mode != new_mode

    if 'team' in data and data['team'] in ['radiant', 'dire']:
        manual_team_lock = True
        log_scan(f"Team manually set by user: {data['team'].upper()} (auto-detection locked)")

    if changed:
        save_config()
        if 'grid_highlight' in data and (not settings.get('grid_highlight', True)):
            hero_locator.hide()
        if evaluator:
            if rank_changed:
                evaluator.set_rank(new_rank)
                evaluator.aggregate_meta(new_mode)
                if dataset_updater:
                    with state_lock:
                        state['dataset_status'] = 'Checking updates...'
                    dataset_updater.start_update_thread(rank=new_rank)
            elif mode_changed:
                evaluator.aggregate_meta(new_mode)
            if 'opacity' in data:
                set_window_opacity(settings.get('opacity', 90))

    if evaluator and (changed or 'team' in data):
        recalculate_recs()

    return jsonify({'status': 'ok'})

last_sync_time = 0
SYNC_COOLDOWN = 3.0

@app.route('/api/sync', methods=['POST'])
def sync_steam():
    global last_sync_time
    if not evaluator or not dataset_updater:
        return jsonify({'status': 'error', 'msg': 'Services initializing'})

    data = request.json or {}
    steam_id = data.get('steam_id', '').strip()
    timeframe = data.get('timeframe', 'all')

    if not steam_id:
        with state_lock:
            state['sync_status'] = 'No ID'
        return jsonify({'status': 'error', 'msg': 'No ID'})

    if not dataset_updater.is_sync_enabled():
        with state_lock:
            state['sync_status'] = 'Sync paused'
        return jsonify({'status': 'error', 'msg': 'Sync temporarily paused by developer'})

    now = time.time()
    if now - last_sync_time < SYNC_COOLDOWN:
        remaining = int(SYNC_COOLDOWN - (now - last_sync_time))
        with state_lock:
            state['sync_status'] = f'Wait {remaining}s'
        return jsonify({'status': 'error', 'msg': f'Wait {remaining}s'})

    allowed, msg = dataset_updater.verify_live_status()
    if not allowed:
        with state_lock:
            state['sync_status'] = 'Sync paused' if 'paused' in msg else 'Server error'
        return jsonify({'status': 'error', 'msg': msg})

    active_token = dataset_updater.get_active_token()
    with state_lock:
        state['sync_status'] = 'Syncing...'
    evaluator.stratz_token = active_token
    success = evaluator.load_player_stats(steam_id, timeframe, force_fetch=True)
    if success:
        last_sync_time = time.time()
        with state_lock:
            state['sync_status'] = 'OK'
            state['player_count'] = sum(s.get('matchCount', 0) for s in evaluator.player_stats.values())
        recalculate_recs()
        return jsonify({'status': 'ok'})
    else:
        with state_lock:
            state['sync_status'] = 'Error'
        return jsonify({'status': 'error', 'msg': 'Sync failed'})

def run_flask():
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='127.0.0.1', port=SERVER_PORT, debug=False, use_reloader=False)

def background_initial_sync():
    """Performs initial player stats check non-blocking in the background."""
    if not evaluator:
        return
    if settings.get('steam_id'):
        evaluator.load_player_stats(settings['steam_id'], settings.get('timeframe', 'all'))
        with state_lock:
            state['sync_status'] = 'OK' if evaluator.player_stats else 'Not Synced'
            state['player_count'] = sum(s.get('matchCount', 0) for s in evaluator.player_stats.values())
        recalculate_recs()
        active_token = dataset_updater.get_active_token()
        if active_token:
            evaluator.stratz_token = active_token
            evaluator.load_player_stats(settings['steam_id'], settings.get('timeframe', 'all'))
            with state_lock:
                state['sync_status'] = 'OK' if evaluator.player_stats else 'Not Synced'
                state['player_count'] = sum(s.get('matchCount', 0) for s in evaluator.player_stats.values())
            recalculate_recs()

window = None
is_hidden = False
tray_icon = None
HOTKEYS = {'INSERT': 45, 'F11': 122, 'F10': 121, 'F9': 120, 'HOME': 36, 'END': 35, 'DELETE': 46, 'TILDE': 192}

def toggle_ui():
    global is_hidden
    if window:
        try:
            if is_hidden:
                window.show()
                is_hidden = False
                hwnd = user32.FindWindowW(None, 'IMPulse')
                if hwnd:
                    user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 3)
            else:
                window.hide()
                is_hidden = True
        except Exception as e:
            print('Toggle UI error:', e)

def open_browser():
    try:
        import webbrowser
        webbrowser.open(f'http://127.0.0.1:{SERVER_PORT}')
    except Exception as e:
        print('Open browser error:', e)

def quit_app():
    try:
        if tray_icon:
            tray_icon.stop()
    except Exception:
        pass
    try:
        if window:
            window.destroy()
    except Exception:
        pass
    try:
        if 'hero_locator' in globals() and hero_locator:
            hero_locator.cleanup()
    except Exception:
        pass
    os._exit(0)

def bootstrap_services(splash=None):
    global dataset_updater
    global security_guard
    global evaluator

    try:
        from pick_evaluator import Evaluator
        from dataset_updater import DatasetUpdater
        from security_guard import SecurityGuard

        threading.Thread(target=run_flask, daemon=True).start()
        data_dir = get_data_dir()
        security_guard = SecurityGuard(data_dir=data_dir)
        security_guard.check_security(force=True)
        security_guard.start_heartbeat_poller(interval=7200)

        if security_guard.is_locked():
            with state_lock:
                state['locked'] = True
                state['lock_info'] = security_guard.get_lock_payload()
                state['recs'] = []
                state['evaluation'] = None
                state['radiant'] = [''] * 5
                state['dire'] = [''] * 5
            print('[Bootstrap] Security lock active on startup.')
        else:
            dataset_updater = DatasetUpdater(data_dir, on_update=on_dataset_updated)
            dataset_updater._fetch_remote_config()
            evaluator = Evaluator(data_dir=data_dir)
            active_token = dataset_updater.get_active_token()
            if active_token:
                evaluator.stratz_token = active_token
            evaluator.set_rank(settings.get('rank', 'all'))
            evaluator.aggregate_meta(settings.get('mode', '1m'))
            if settings.get('steam_id'):
                evaluator.load_player_stats(settings['steam_id'], settings.get('timeframe', 'all'))
                with state_lock:
                    state['sync_status'] = 'OK' if evaluator.player_stats else 'Not Synced'
                    state['player_count'] = sum(s.get('matchCount', 0) for s in evaluator.player_stats.values())
            recalculate_recs()
            dataset_updater.start_update_thread(rank=settings.get('rank', 'all'))

        threading.Thread(target=scan_loop, daemon=True).start()

        for _ in range(40):
            import urllib.request
            try:
                with urllib.request.urlopen(f'http://127.0.0.1:{SERVER_PORT}/api/state', timeout=0.2) as resp:
                    if resp.status == 200:
                        if splash:
                            splash.mark_ready()
                        break
            except Exception:
                time.sleep(0.05)
    except Exception as e:
        print('[CRITICAL] Bootstrap services failed:', e)
        try:
            ctypes.windll.user32.MessageBoxW(
                None, f'Критическая ошибка запуска: повреждены или отсутствуют системные компоненты приложения ({e}).',
                'IMPulse Security Error', 16
            )
        except Exception:
            pass

def apply_fast_initial_transparency():
    """Applies transparency, topmost, and toolwindow (hiding from taskbar) immediately upon window creation."""
    try:
        for _ in range(300):
            hwnd = user32.FindWindowW(None, 'IMPulse')
            if hwnd:
                ensure_overlay_window_styles(hwnd)
                return
            time.sleep(0.01)
    except Exception as e:
        print('Fast transparency error:', e)

def start_webview():
    global window
    global is_hidden
    global tray_icon

    internal_dir = os.path.join(APP_DIR, '_internal')
    clr_dir = os.path.join(internal_dir, 'clr_loader', 'ffi', 'dlls', 'amd64')
    pynet_dir = os.path.join(internal_dir, 'pythonnet', 'runtime')
    cfg_candidates = [
        os.path.join(APP_DIR, 'IMPulseLive.exe.config'),
        os.path.join(internal_dir, 'IMPulseLive.exe.config'),
        os.path.join(BASE_DIR, 'IMPulseLive.exe.config')
    ]
    for cfg in cfg_candidates:
        if os.path.exists(cfg):
            os.environ.setdefault('PYTHONNET_NETFX_CONFIG_FILE', cfg)
            break

    for p in [APP_DIR, internal_dir, clr_dir, pynet_dir]:
        if os.path.exists(p):
            if hasattr(os, 'add_dll_directory'):
                try:
                    os.add_dll_directory(p)
                except Exception:
                    pass
            if p not in os.environ.get('PATH', ''):
                os.environ['PATH'] = p + os.pathsep + os.environ.get('PATH', '')

    import webview
    threading.Thread(target=apply_fast_initial_transparency, daemon=True).start()
    window = webview.create_window('IMPulse', f'http://127.0.0.1:{SERVER_PORT}', width=464, height=680, background_color='#04070a', frameless=True, on_top=True)
    is_hidden = False

    try:
        def on_closing():
            toggle_ui()
            return False
        window.events.closing += on_closing
    except Exception as e:
        print('Window closing event setup:', e)

    try:
        import pystray
        from PIL import Image
        icon_candidates = [
            os.path.join(APP_DIR, 'assets', 'icon.ico'),
            os.path.join(BASE_DIR, 'assets', 'icon.ico'),
            os.path.join(APP_DIR, 'assets', 'icon.png'),
            os.path.join(BASE_DIR, 'assets', 'icon.png'),
            os.path.join(BASE_DIR, 'static', 'icon.png')
        ]
        tray_img = None
        for p in icon_candidates:
            if os.path.exists(p):
                try:
                    tray_img = Image.open(p)
                    break
                except Exception:
                    pass
        if tray_img:
            menu = pystray.Menu(
                pystray.MenuItem('Показать / Скрыть', lambda icon, item: toggle_ui(), default=True),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem('Выход', lambda icon, item: quit_app())
            )
            tray_icon = pystray.Icon('IMPulse', tray_img, 'IMPulse Live Draft', menu)
            tray_icon.run_detached()
    except Exception as e:
        print('Tray initialization warning:', e)

    try:
        def hotkey_poller():
            was_pressed = False
            while True:
                key_name = settings.get('hotkey', 'INSERT').upper()
                vk = HOTKEYS.get(key_name, 45)
                try:
                    is_pressed = user32.GetAsyncKeyState(vk) & 32768 != 0
                    if is_pressed and not was_pressed:
                        toggle_ui()
                    was_pressed = is_pressed
                except Exception:
                    pass
                time.sleep(0.05)
        threading.Thread(target=hotkey_poller, daemon=True).start()
    except Exception as e:
        print('Hotkey warning:', e)

    webview.start(debug=False)

if __name__ == '__main__':
    app_mutex = ensure_single_instance()
    load_config()
    splash = None
    try:
        splash = GdiplusSplash(min_duration=2.0)
    except Exception as e:
        print('Splash window skipped/fallback:', e)
        splash = None

    threading.Thread(target=bootstrap_services, args=(splash,), daemon=True).start()
    if splash:
        splash.run_loop()

    for _ in range(40):
        import urllib.request
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{SERVER_PORT}/api/state', timeout=0.2) as resp:
                if resp.status == 200:
                    start_webview()
                    break
        except Exception:
            time.sleep(0.05)
