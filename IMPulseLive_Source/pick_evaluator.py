import os
import sys
import json
import math
import time
import requests
from typing import Dict, List, Tuple, Any

STRATZ_TOKEN = ""

class Evaluator:
    def __init__(self, data_dir=None):
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), 'data')
        self.meta_path = os.path.join(self.data_dir, 'meta_history.json')
        self.daily_meta_path = os.path.join(self.data_dir, 'daily_meta.json')
        self.patches_path = os.path.join(self.data_dir, 'patches.json')
        self.constants_json_path = os.path.join(self.data_dir, 'constants.json')
        self.constants_path = os.path.join(self.data_dir, 'constants.js')
        self.stratz_token = STRATZ_TOKEN
        self.id_to_name: Dict[int, str] = {}
        self.cdn_to_id: Dict[str, int] = {}
        self.id_to_cdn: Dict[int, str] = {}
        self.meta_history = {}
        self.daily_meta = {}
        self.meta: Dict[int, Dict[str, Any]] = {}
        self.matchups: Dict[int, Dict[str, Dict[int, Dict[str, Any]]]] = {}
        self.patches: List[Dict[str, Any]] = []
        self.current_mode = '1m'
        self.total_matches_12w = 1
        self.total_matches_1w = 1
        self.player_stats = {}
        self.current_rank = 'all'
        self.load_data()

    def set_rank(self, rank):
        self.current_rank = rank or 'all'
        filename = 'meta_history.json' if self.current_rank == 'all' else f'meta_history_{self.current_rank}.json'
        self.meta_path = os.path.join(self.data_dir, filename)
        daily_filename = 'daily_meta.json' if self.current_rank == 'all' else f'daily_meta_{self.current_rank}.json'
        self.daily_meta_path = os.path.join(self.data_dir, daily_filename)
        self.load_data()

    def load_data(self):
        # 1. Load constants.json
        if os.path.exists(self.constants_json_path):
            try:
                with open(self.constants_json_path, 'r', encoding='utf-8') as f:
                    c_data = json.load(f)
                    for hid_str, hinfo in c_data.items():
                        if hid_str.isdigit() and isinstance(hinfo, dict):
                            hid = int(hid_str)
                            disp_name = hinfo.get('name', '')
                            cdn_name = hinfo.get('cdnName', '').lower()
                            self.id_to_name[hid] = disp_name
                            self.cdn_to_id[cdn_name] = hid
                            self.id_to_cdn[hid] = cdn_name
            except Exception as e:
                print(f'[Evaluator] Failed to load constants.json: {e}')

        # 2. Load patches.json
        if os.path.exists(self.patches_path):
            try:
                with open(self.patches_path, 'r', encoding='utf-8') as f:
                    self.patches = json.load(f)
            except Exception:
                self.patches = []

        # 3. Load daily_meta.json
        if os.path.exists(self.daily_meta_path):
            try:
                with open(self.daily_meta_path, 'r', encoding='utf-8') as f:
                    self.daily_meta = json.load(f)
            except Exception:
                self.daily_meta = {}

        # 4. Load meta_history.json
        if os.path.exists(self.meta_path):
            try:
                with open(self.meta_path, 'r', encoding='utf-8') as f:
                    self.meta_history = json.load(f)
            except Exception:
                self.meta_history = {}

        self.aggregate_meta(self.current_mode)

    def fetch_patches(self):
        return self.patches

    def get_recent_patches(self):
        return self.patches[-5:] if self.patches else []

    def aggregate_meta(self, mode='1m'):
        self.current_mode = mode
        self.meta.clear()
        self.matchups.clear()

        weeks_dict = self.meta_history.get('weeks', {})
        if not weeks_dict:
            return

        sorted_week_keys = sorted(weeks_dict.keys(), reverse=True)
        # 1m is last 4 weeks, 3m is up to 12 weeks
        n_weeks = 4 if mode == '1m' else min(12, len(sorted_week_keys))
        target_keys = sorted_week_keys[:n_weeks]

        for wk in target_keys:
            wk_data = weeks_dict[wk]
            base_wr = wk_data.get('baseWinrates', {})
            for hid_str, h_stats in base_wr.items():
                hid = int(hid_str)
                if hid not in self.meta:
                    self.meta[hid] = {
                        'winCount': 0,
                        'matchCount': 0,
                        'winrate': 0.5,
                        'raw_winrate': 0.5,
                        'positions': {str(p): {'winCount': 0, 'matchCount': 0, 'winrate': 0.5, 'raw_winrate': 0.5} for p in range(1, 6)}
                    }

                entry = self.meta[hid]
                entry['winCount'] += h_stats.get('winCount', 0)
                entry['matchCount'] += h_stats.get('matchCount', 0)

                pos_data = h_stats.get('positions', {})
                for p_idx_str, p_stat in pos_data.items():
                    if p_idx_str in entry['positions']:
                        p_entry = entry['positions'][p_idx_str]
                        p_entry['winCount'] += p_stat.get('winCount', 0)
                        p_entry['matchCount'] += p_stat.get('matchCount', 0)

            # Matchups aggregation
            matchups_data = wk_data.get('matchups', {})
            for hid_str, m_info in matchups_data.items():
                hid = int(hid_str)
                if hid not in self.matchups:
                    self.matchups[hid] = {'vs': {}, 'with': {}}

                for item in m_info.get('vs', []):
                    h2 = item.get('heroId2')
                    if h2:
                        vs_map = self.matchups[hid]['vs']
                        if h2 not in vs_map:
                            vs_map[h2] = {'winCount': 0, 'matchCount': 0}
                        vs_map[h2]['winCount'] += item.get('winCount', 0)
                        vs_map[h2]['matchCount'] += item.get('matchCount', 0)

                for item in m_info.get('with', []):
                    h2 = item.get('heroId2')
                    if h2:
                        with_map = self.matchups[hid]['with']
                        if h2 not in with_map:
                            with_map[h2] = {'winCount': 0, 'matchCount': 0}
                        with_map[h2]['winCount'] += item.get('winCount', 0)
                        with_map[h2]['matchCount'] += item.get('matchCount', 0)

        # Recalculate winrates
        for hid, entry in self.meta.items():
            if entry['matchCount'] > 0:
                wr = entry['winCount'] / entry['matchCount']
                entry['winrate'] = wr
                entry['raw_winrate'] = wr
            for p_idx_str, p_entry in entry['positions'].items():
                if p_entry['matchCount'] > 0:
                    p_wr = p_entry['winCount'] / p_entry['matchCount']
                    p_entry['winrate'] = p_wr
                    p_entry['raw_winrate'] = p_wr

    @staticmethod
    def normalize_meta(base_wr: float) -> float:
        return math.tanh((base_wr - 0.5) / 0.08)

    @staticmethod
    def normalize_synergy(synergy_delta: float) -> float:
        return math.tanh(synergy_delta / 4.0)

    @staticmethod
    def normalize_counter(counter_delta: float) -> float:
        return math.tanh(counter_delta / 5.0)

    @staticmethod
    def normalize_personal(p_winrate: float, p_matches: int, role_transfer: float = 1.0) -> float:
        eff_m = p_matches * role_transfer
        if eff_m <= 0:
            return 0.0
        return math.tanh((p_winrate - 0.5) / 0.10) * (eff_m / (eff_m + 10.0))

    def calculate_normalized_advantage(self, base_wr: float, synergy: float, counter: float, p_winrate: float, p_matches: int, role_transfer: float = 1.0) -> Tuple[float, float, float, float, float]:
        norm_m = self.normalize_meta(base_wr)
        norm_s = self.normalize_synergy(synergy)
        norm_c = self.normalize_counter(counter)
        norm_p = self.normalize_personal(p_winrate, p_matches, role_transfer)
        total_adv = 0.40 * norm_m + 0.25 * norm_s + 0.25 * norm_c + 0.10 * norm_p
        return (total_adv, norm_m, norm_s, norm_c, norm_p)

    def get_pair_matchup(self, h1_cdn: str, h2_cdn: str) -> Tuple[float, float, int]:
        h1 = self.cdn_to_id.get(h1_cdn)
        h2 = self.cdn_to_id.get(h2_cdn)
        if not h1 or not h2:
            return (0.0, 0.5, 0)

        vs_map = self.matchups.get(h1, {}).get('vs', {})
        matchup = vs_map.get(h2)
        if not matchup or matchup['matchCount'] == 0:
            return (0.0, 0.5, 0)

        wr = matchup['winCount'] / matchup['matchCount']
        cnt = matchup['matchCount']
        h2_base = self.meta.get(h2, {}).get('winrate', 0.5)
        adv = (wr - h2_base) * 100.0
        return (adv, wr, cnt)

    def get_pair_synergy(self, h1_cdn: str, h2_cdn: str) -> Tuple[float, float, int]:
        h1 = self.cdn_to_id.get(h1_cdn)
        h2 = self.cdn_to_id.get(h2_cdn)
        if not h1 or not h2:
            return (0.0, 0.5, 0)

        with_map = self.matchups.get(h1, {}).get('with', {})
        synergy = with_map.get(h2)
        if not synergy or synergy['matchCount'] == 0:
            return (0.0, 0.5, 0)

        wr = synergy['winCount'] / synergy['matchCount']
        cnt = synergy['matchCount']
        h1_base = self.meta.get(h1, {}).get('winrate', 0.5)
        h2_base = self.meta.get(h2, {}).get('winrate', 0.5)
        expected_wr = (h1_base + h2_base) / 2.0
        adv = (wr - expected_wr) * 100.0
        return (adv, wr, cnt)

    def calc_clash(self, rad_duo: Tuple[str, str], dire_duo: Tuple[str, str]) -> Tuple[float, str, float]:
        r1, r2 = rad_duo
        d1, d2 = dire_duo
        r_syn, _, _ = self.get_pair_synergy(r1, r2)
        d_syn, _, _ = self.get_pair_synergy(d1, d2)

        m11, _, _ = self.get_pair_matchup(r1, d1)
        m12, _, _ = self.get_pair_matchup(r1, d2)
        m21, _, _ = self.get_pair_matchup(r2, d1)
        m22, _, _ = self.get_pair_matchup(r2, d2)

        rad_score = r_syn + (m11 + m12 + m21 + m22) / 2.0 - d_syn
        diff = round(rad_score, 1)
        team = 'Radiant' if diff >= 0 else 'Dire'
        return (abs(diff), team, diff)

    def predict_roles(self, cdns: List[str]) -> Dict[str, int]:
        valid_cdns = [c for c in cdns if c and c in self.cdn_to_id]
        if not valid_cdns:
            return {}

        roles_assigned = {}
        avail_roles = {1, 2, 3, 4, 5}

        # Greedy best-role assignment
        scores = []
        for cdn in valid_cdns:
            hid = self.cdn_to_id[cdn]
            pos_dict = self.meta.get(hid, {}).get('positions', {})
            for role in range(1, 6):
                cnt = pos_dict.get(str(role), {}).get('matchCount', 0)
                scores.append((cnt, cdn, role))

        scores.sort(reverse=True, key=lambda x: x[0])
        for cnt, cdn, role in scores:
            if cdn not in roles_assigned and role in avail_roles:
                roles_assigned[cdn] = role
                avail_roles.remove(role)

        # Fallback for remaining
        for cdn in valid_cdns:
            if cdn not in roles_assigned:
                assigned = avail_roles.pop() if avail_roles else 1
                roles_assigned[cdn] = assigned

        return roles_assigned

    def get_meta_heroes(self, target_role='all', top_n=15, timeframe='1m', calc_mode='meta', strictness='normal', decay=False, role_transfer_enabled=False, popularity='meta', winrate_filter='all', eval_method='bayes') -> List[Dict[str, Any]]:
        results = []
        total_meta_matches = sum(e['matchCount'] for e in self.meta.values()) or 1

        for hid, h_stats in self.meta.items():
            cdn = self.id_to_cdn.get(hid)
            name = self.id_to_name.get(hid, cdn)
            if not cdn:
                continue

            matches = h_stats['matchCount']
            wr = h_stats['winrate']
            pick_rate = (matches / total_meta_matches) * 100.0 * 10.0

            if target_role != 'all':
                try:
                    r_str = str(target_role)
                    p_stat = h_stats['positions'].get(r_str, {})
                    if p_stat.get('matchCount', 0) > 0:
                        wr = p_stat['winrate']
                except:
                    pass

            norm_adv, m_norm, s_norm, c_norm, p_norm = self.calculate_normalized_advantage(wr, 0.0, 0.0, 0.0, 0, 1.0)
            adv = wr * 100.0

            results.append({
                'name': name,
                'cdnName': cdn,
                'pick_rate': pick_rate,
                'base_wr': wr * 100.0,
                'trend_delta': 0.5,
                'trend_confidence': 89,
                'adv': adv,
                'adv_norm': norm_adv,
                'meta_norm': m_norm,
                'synergy_norm': s_norm,
                'counter_norm': c_norm,
                'personal_norm': p_norm,
                'synergy': 0,
                'counter': 0,
                'p_matches': 0,
                'p_winrate': 0,
                'p_imp': '-'
            })

        results.sort(key=lambda x: x['adv_norm'], reverse=True)
        return results[:top_n]

    def get_recommendations(self, ally_cdns: List[str], enemy_cdns: List[str], target_role='all', top_n=5, timeframe='1m', calc_mode='delta', strictness='normal', decay=False, role_transfer_enabled=False, popularity='meta', winrate_filter='all', eval_method='bayes') -> List[Dict[str, Any]]:
        picked_set = set(c for c in ally_cdns + enemy_cdns if c)
        results = []
        total_meta_matches = sum(e['matchCount'] for e in self.meta.values()) or 1

        for hid, h_stats in self.meta.items():
            cdn = self.id_to_cdn.get(hid)
            name = self.id_to_name.get(hid, cdn)
            if not cdn or cdn in picked_set:
                continue

            matches = h_stats['matchCount']
            base_wr = h_stats['winrate']
            pick_rate = (matches / total_meta_matches) * 100.0 * 10.0

            # Synergy with allies
            syn_deltas = []
            for a_cdn in ally_cdns:
                if a_cdn:
                    delta, _, _ = self.get_pair_synergy(cdn, a_cdn)
                    syn_deltas.append(delta)
            avg_syn = sum(syn_deltas) / len(syn_deltas) if syn_deltas else 0.0

            # Counters against enemies
            cnt_deltas = []
            for e_cdn in enemy_cdns:
                if e_cdn:
                    delta, _, _ = self.get_pair_matchup(cdn, e_cdn)
                    cnt_deltas.append(delta)
            avg_cnt = sum(cnt_deltas) / len(cnt_deltas) if cnt_deltas else 0.0

            norm_adv, m_norm, s_norm, c_norm, p_norm = self.calculate_normalized_advantage(base_wr, avg_syn, avg_cnt, 0.0, 0, 1.0)
            total_adv = avg_syn + avg_cnt

            results.append({
                'name': name,
                'cdnName': cdn,
                'pick_rate': pick_rate,
                'base_wr': base_wr * 100.0,
                'trend_delta': 0.0,
                'trend_confidence': 70,
                'adv': total_adv,
                'adv_norm': norm_adv,
                'meta_norm': m_norm,
                'synergy_norm': s_norm,
                'counter_norm': c_norm,
                'personal_norm': p_norm,
                'synergy': avg_syn,
                'counter': avg_cnt,
                'p_matches': 0,
                'p_winrate': 0,
                'p_imp': '-'
            })

        results.sort(key=lambda x: x['adv_norm'], reverse=True)
        return results[:top_n]

    def evaluate_draft(self, rad_cdns: List[str], dire_cdns: List[str], calc_mode='hybrid', rad_roles=None, dire_roles=None) -> Dict[str, Any]:
        rad_scores = {}
        dire_scores = {}

        for r_cdn in rad_cdns:
            if r_cdn:
                total_m = sum(self.get_pair_matchup(r_cdn, d)[0] for d in dire_cdns if d)
                total_s = sum(self.get_pair_synergy(r_cdn, r2)[0] for r2 in rad_cdns if r2 and r2 != r_cdn)
                rad_scores[r_cdn] = round(total_m + total_s, 2)

        for d_cdn in dire_cdns:
            if d_cdn:
                total_m = sum(self.get_pair_matchup(d_cdn, r)[0] for r in rad_cdns if r)
                total_s = sum(self.get_pair_synergy(d_cdn, d2)[0] for d2 in dire_cdns if d2 and d2 != d_cdn)
                dire_scores[d_cdn] = round(total_m + total_s, 2)

        rad_val = sum(rad_scores.values())
        dire_val = sum(dire_scores.values())
        diff = round(rad_val - dire_val, 2)

        return {
            'team': 'Radiant' if diff >= 0 else 'Dire',
            'advantage': round(abs(diff), 1),
            'rad_val': round(rad_val, 2),
            'dire_val': round(dire_val, 2),
            'raw_rad_val': round(rad_val, 2),
            'raw_dire_val': round(dire_val, 2),
            'diff': diff,
            'side_bias': 0.0,
            'rad_heroes': rad_scores,
            'dire_heroes': dire_scores,
            'calc_mode': calc_mode
        }

    def get_post_draft_analysis(self, rad_cdns: List[str], dire_cdns: List[str], user_team='radiant', custom_roles=None) -> Dict[str, Any]:
        rad_roles = self.predict_roles(rad_cdns)
        dire_roles = self.predict_roles(dire_cdns)

        if custom_roles:
            if 'radiant' in custom_roles:
                rad_roles.update(custom_roles['radiant'])
            if 'dire' in custom_roles:
                dire_roles.update(custom_roles['dire'])

        matrix = {}
        for r in rad_cdns:
            if r:
                matrix[r] = {}
                for d in dire_cdns:
                    if d:
                        matrix[r][d] = round(self.get_pair_matchup(r, d)[0], 1)

        return {
            'user_team': user_team,
            'summary': 'Draft analysis complete.',
            'rad_roles': rad_roles,
            'dire_roles': dire_roles,
            'matrix': matrix,
            'laning': {},
            'role_duels': {},
            'custom_roles': custom_roles or {},
            'highlights': []
        }

    def load_player_stats(self, account_ids_str: str, timeframe='all', force_fetch=False) -> bool:
        return True

    def get_hero_trend(self, hero_id: int, target_role='all') -> Dict[str, Any]:
        return {'trend': 0.5, 'confidence': 89}
