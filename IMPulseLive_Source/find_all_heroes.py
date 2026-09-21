import os
import sys
import re
import time
import glob
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor

BASE_RESOLUTION_WIDTH = 1920
BASE_RESOLUTION_HEIGHT = 1080
BASE_SCALE = 0.467
BASE_TEMPLATE_WIDTH = 256
BASE_TEMPLATE_HEIGHT = 144

DRAFT_RAD_OFFSETS = [(-751, -643), (-627, -519), (-503, -395), (-379, -271), (-255, -147)]
DRAFT_DIRE_OFFSETS = [(147, 255), (271, 379), (395, 503), (519, 627), (643, 751)]

INGAME_RAD_OFFSETS = [(-417, -356), (-354, -295), (-292, -233), (-230, -171), (-167, -108)]
INGAME_DIRE_OFFSETS = [(108, 167), (171, 230), (233, 292), (295, 354), (356, 417)]

SLOT_PLAYER_HUES = {
    ('rad', 0): (100, 122),
    ('rad', 1): (68, 90),
    ('rad', 2): (140, 160),
    ('rad', 3): (22, 38),
    ('rad', 4): (5, 20),
    ('dire', 0): (158, 175),
    ('dire', 1): (28, 44),
    ('dire', 2): (86, 106),
    ('dire', 3): (58, 77),
    ('dire', 4): (12, 26)
}

_cached_icons_dir = None
_cached_icon_files = []
_template_cache = {}
_prepared_templates_cache = {}
_color_profile_cache = {}

def cv2_imread_unicode(path, flags=1):
    try:
        with open(path, 'rb') as f:
            data = np.frombuffer(f.read(), dtype=np.uint8)
            return cv2.imdecode(data, flags)
    except Exception:
        return None

def cv2_imwrite_unicode(path, img, params=None):
    try:
        ext = os.path.splitext(path)[1]
        ret, buf = cv2.imencode(ext, img, params)
        if ret:
            with open(path, 'wb') as f:
                f.write(buf)
            return True
        return False
    except Exception:
        return False

def get_base_hero_name(icon_path):
    base = os.path.basename(icon_path)
    name = os.path.splitext(base)[0]
    name = re.sub(r'_(png|icon|horiz|vert|full)$', '', name, flags=re.I)
    name = re.sub(r'^npc_dota_hero_', '', name, flags=re.I)
    return name.lower()

def resolve_hero_icon_path(icons_dir, hero_name):
    if not icons_dir or not os.path.exists(icons_dir):
        return None
    cand = os.path.join(icons_dir, f"{hero_name}.png")
    if os.path.exists(cand):
        return cand
    cand2 = os.path.join(icons_dir, f"npc_dota_hero_{hero_name}.png")
    if os.path.exists(cand2):
        return cand2
    for ext in ['.png', '.jpg']:
        p = os.path.join(icons_dir, f"{hero_name}{ext}")
        if os.path.exists(p):
            return p
    return None

def get_prepared_templates(icons_dir, t_width, t_height, side=None):
    cache_key = (icons_dir, t_width, t_height)
    if cache_key in _prepared_templates_cache:
        return _prepared_templates_cache[cache_key]

    templates = []
    if not icons_dir or not os.path.exists(icons_dir):
        return templates

    files = glob.glob(os.path.join(icons_dir, '*.png'))
    for f in files:
        hero_name = get_base_hero_name(f)
        img = cv2_imread_unicode(f)
        if img is not None and img.size > 0:
            resized = cv2.resize(img, (int(t_width), int(t_height)), interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            templates.append((hero_name, resized, gray))

    _prepared_templates_cache[cache_key] = templates
    return templates

def is_valid_hero_slot(roi, allow_grayscale=False):
    if roi is None or roi.size == 0:
        return False
    std = float(np.std(roi))
    if std < 12.0:
        return False
    mean_val = float(np.mean(roi))
    if mean_val < 10.0 or mean_val > 245.0:
        return False
    return True

def snap_scale(scale):
    for ref in [0.75, 1.0, 1.25, 1.333, 1.5, 2.0]:
        if abs(scale - ref) < 0.04:
            return ref
    return scale

def compute_slot_anchors(w, h, offsets_1080, scale=None):
    if scale is None:
        scale = w / 1920.0
    center_x = w / 2.0
    slots = []
    for x1_off, x2_off in offsets_1080:
        x1 = int(center_x + x1_off * scale)
        x2 = int(center_x + x2_off * scale)
        sw = max(1, x2 - x1)
        slots.append((x1, x2, sw))
    return slots

def calibrate_hero_slots(img_scene, forced_resolution=None):
    h, w = img_scene.shape[:2]
    scale = snap_scale(w / 1920.0)

    rad_segs = compute_slot_anchors(w, h, DRAFT_RAD_OFFSETS, scale)
    dire_segs = compute_slot_anchors(w, h, DRAFT_DIRE_OFFSETS, scale)

    timer_gap = dire_segs[0][0] - rad_segs[-1][1] if (rad_segs and dire_segs) else 294

    return {
        'mode': 'draft',
        'source': 'fixed_base',
        'best_y': int(12 * scale),
        'center_x': w / 2.0,
        'scale': scale,
        'slot_w': float(rad_segs[0][2]) if rad_segs else 108.0,
        'rad_segs': rad_segs,
        'dire_segs': dire_segs,
        'timer_gap': timer_gap,
        'res_status': 'ok',
        'res_msg': f'Фиксированное: {w}x{h}',
        'resolution': f'{w}x{h}'
    }

def detect_heroes(img_scene, icons_dir=None, icons_path=None, forced_resolution=None):
    icons_dir = icons_dir or icons_path
    if img_scene is None or img_scene.size == 0:
        return {
            'radiant': ['', '', '', '', ''],
            'dire': ['', '', '', '', ''],
            'raw_results': [],
            'mode': 'draft',
            'calibration': {'res_status': 'error', 'res_msg': 'Empty image'}
        }

    h, w = img_scene.shape[:2]
    calib = calibrate_hero_slots(img_scene, forced_resolution)
    scale = calib['scale']

    # Draft slot dimensions
    slot_w = int(calib['slot_w'])
    slot_h = max(1, int(slot_w * (BASE_TEMPLATE_HEIGHT / BASE_TEMPLATE_WIDTH)))
    slot_y1 = int(14 * scale)
    slot_y2 = slot_y1 + slot_h

    templates = get_prepared_templates(icons_dir, slot_w, slot_h)

    radiant_res = [''] * 5
    dire_res = [''] * 5
    raw_results = []

    if templates:
        # Check Radiant slots
        for i, (x1, x2, sw) in enumerate(calib['rad_segs']):
            roi = img_scene[slot_y1:slot_y2, x1:x2]
            if is_valid_hero_slot(roi):
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                best_hero = None
                best_score = 0.62
                for h_name, t_bgr, t_gray in templates:
                    if gray_roi.shape == t_gray.shape:
                        score = float(cv2.matchTemplate(gray_roi, t_gray, cv2.TM_CCOEFF_NORMED)[0][0])
                        if score > best_score:
                            best_score = score
                            best_hero = h_name
                if best_hero:
                    radiant_res[i] = best_hero
                    raw_results.append((best_hero, 'rad', i, best_score, x1, slot_y1, False))

        # Check Dire slots
        for i, (x1, x2, sw) in enumerate(calib['dire_segs']):
            roi = img_scene[slot_y1:slot_y2, x1:x2]
            if is_valid_hero_slot(roi):
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                best_hero = None
                best_score = 0.62
                for h_name, t_bgr, t_gray in templates:
                    if gray_roi.shape == t_gray.shape:
                        score = float(cv2.matchTemplate(gray_roi, t_gray, cv2.TM_CCOEFF_NORMED)[0][0])
                        if score > best_score:
                            best_score = score
                            best_hero = h_name
                if best_hero:
                    dire_res[i] = best_hero
                    raw_results.append((best_hero, 'dire', i, best_score, x1, slot_y1, False))

    return {
        'radiant': radiant_res,
        'dire': dire_res,
        'raw_results': raw_results,
        'mode': 'draft',
        'calibration': calib
    }

def generate_debug_overlay(img_scene, output_path='assets/screenshots/debug_capture.png', icons_dir=None, forced_resolution=None):
    det = detect_heroes(img_scene, icons_dir=icons_dir, forced_resolution=forced_resolution)
    overlay = img_scene.copy()
    calib = det.get('calibration', {})
    scale = calib.get('scale', 1.0)
    slot_w = int(calib.get('slot_w', 108))
    slot_h = max(1, int(slot_w * (BASE_TEMPLATE_HEIGHT / BASE_TEMPLATE_WIDTH)))
    y1 = int(14 * scale)
    y2 = y1 + slot_h

    for i, (x1, x2, sw) in enumerate(calib.get('rad_segs', [])):
        h_name = det['radiant'][i]
        color = (0, 255, 0) if h_name else (255, 128, 0)
        cv2.rectangle(overlay, (x1, y1), (x2, y2), color, 2)
        if h_name:
            cv2.putText(overlay, h_name, (x1, y2 + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

    for i, (x1, x2, sw) in enumerate(calib.get('dire_segs', [])):
        h_name = det['dire'][i]
        color = (0, 128, 255) if h_name else (0, 0, 255)
        cv2.rectangle(overlay, (x1, y1), (x2, y2), color, 2)
        if h_name:
            cv2.putText(overlay, h_name, (x1, y2 + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    cv2_imwrite_unicode(output_path, overlay)
    return output_path
