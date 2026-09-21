let currentLang = 'en';
const translations = {
    en: {
        steam_id: 'Steam ID', api_key: 'Stratz API Key', range: 'Data Period', mode: 'Analysis',
        pick_rate: 'Pick Rate', patch_relevance: 'Patch Relevance', experience: 'Experience',
        hero_stats: 'Hero Stats', eval_method: 'Method', rank: 'Rank',
        radiant: 'Radiant', dire: 'Dire',
        meta: 'Meta', matchup: 'Matchup', hybrid: 'Hybrid', personal: 'Personal',
        any_pr: 'Any', average_pr: 'Average', high_pr: 'High',
        enabled: 'Enabled', disabled: 'Disabled',
        relaxed: 'All', familiar: 'Familiar', mains: 'Mains',
        overall: 'Overall', by_role: 'By Role',
        method_bayes: 'Balance', method_signature: 'Mastery', method_logit: 'Odds',
        hero: 'Hero', th_meta: 'Meta', th_syn: 'Syn', th_cnt: 'Cnt',
        th_matches: 'M', th_player: 'Player', th_adv: 'Adv',
        opt_1w: '1 Week', opt_2w: '2 Weeks', opt_1m: '1 Month', opt_trend: 'Patch Trends',
        no_data: 'No data available',
        rank_all: 'All', rank_herald: 'Herald-Guardian', rank_archon: 'Crusader-Archon', rank_ancient: 'Legend-Ancient', rank_divine: 'Divine-Immortal',
        live_draft: 'LIVE DRAFT', ready: 'READY', updating: 'UPDATING', error: 'ERROR',
        get_key: '(Get key)',
        range_title: 'Time period for meta statistics aggregation',
        rank_title: 'Filter meta stats by player rank bracket',
        mode_title: 'Scoring algorithm for hero recommendations',
        pick_rate_title: 'Filter heroes by popularity in current meta',
        patch_relevance_title: 'Hide heroes not played in the last 3 months',
        experience_title: 'Minimum games required to recommend a hero',
        hero_stats_title: 'Use overall or role-specific player statistics',
        eval_method_title: 'Calculation method: Balance (Bayesian), Mastery (Signatures), or Odds (Log-Odds probability)',
        method_bayes_title: 'Balance: optimal blend between draft strength and personal experience',
        method_signature_title: 'Mastery: prioritizes your proven signature heroes',
        method_logit_title: 'Odds: mathematically rigorous win probability model (Log-Odds)',
        hero_title: 'Hero name',
        th_meta_title: 'Meta Winrate',
        th_syn_title: 'Synergy with allies',
        th_cnt_title: 'Counter vs enemies',
        th_matches_title: 'Player matches',
        th_player_title: 'Player winrate',
        th_adv_title: 'Final advantage score',
        settings_title: 'Settings',
        lang_title: 'Language: English',
        sync_title: 'Sync with Stratz',
        tab_scoring: 'Scoring',
        tab_app: 'App',
        hotkey_label: 'Overlay Hotkey',
        hotkey_title: 'Global hotkey to show/hide the overlay in-game',
        tray_info_title: 'System Tray Active',
        tray_info_desc: 'IMPulse runs in the system tray near the Windows clock. Click the icon to minimize or restore.',
        open_browser: 'Open in Browser (Second Monitor)',
        opacity_label: 'Window Opacity',
        opacity_title: 'Overlay window opacity over Dota 2',
        perf_label: 'Performance',
        perf_title: 'Balance between detection speed and CPU usage',
        perf_eco: 'Eco (1.5s)',
        perf_balanced: 'Normal (0.3s)',
        perf_high: 'Max (Instant)',
        grid_highlight_label: 'Grid Highlight',
        res_label: 'Screen Resolution',
        res_title: 'Screen resolution calibration base',
        debug_capture_btn: 'Inspect Capture Area',
        tab_draft: 'Draft', tab_matrix: 'Summary', tab_laning: 'Laning & Map',
        matrix_title: '5v5 Matchups', matrix_subtitle: 'Head-to-head matchup advantage',
        btn_reset_roles: '↺ Reset roles',
        role_duels_title: 'Role vs Role Duels (1v1)', role_duels_subtitle: 'Mirror positions head-to-head advantage',
        hl_threats: 'Main Team Threats', hl_dominance: 'Team Counter-Picks', hl_combos: 'Team Combos',
        lane_top: 'Top Lane', lane_mid: 'Mid Lane', lane_bot: 'Bottom Lane',
        status_easy: 'Easy', status_fair: 'Fair', status_hard: 'Hard',
        in_game: 'IN MATCH',
        chip_meta: 'Meta',
        chip_matchups: 'Matchups',
        chip_map: 'Map',
        win_odds: 'PREDICTION',
        hint_click_hero: 'Select role or click hero in draft slots for personal analysis',
        reset_draft_btn: 'Reset Match',
        header_subtitle: 'AI DRAFT ANALYSIS',
        prediction_label: 'PREDICTION',
        btn_reset_roles_txt: 'Reset roles',
        analysis_title: 'Personal Analysis: YOU',
        callout_lead: 'Which one are you?',
        callout_desc: 'Click your hero in draft slots or select role position (1–5)!',
        col_strengths: 'Strengths',
        col_risks: 'Risks',
        col_timing: 'Key Moment',
        col_recommendation: 'Recommendation',
        col_my_strengths: 'You: Strengths',
        col_my_risks: 'You: Risks',
        col_team_strengths: 'Team: Strengths',
        col_team_risks: 'Team: Risks & Threats',
        laning_title: 'Laning Overview',
        laning_subtitle: 'Lane clash predictions & map control',
        laning_swap_hint: 'Swap lanes'
    },
    ru: {
        steam_id: 'Steam ID', api_key: 'Ключ Stratz API', range: 'Период', mode: 'Анализ',
        pick_rate: 'Пикрейт', patch_relevance: 'Актуальность', experience: 'Опыт',
        hero_stats: 'Статистика', eval_method: 'Метод', rank: 'Ранг',
        radiant: 'Свет', dire: 'Тьма',
        meta: 'Мета', matchup: 'Матчапы', hybrid: 'Гибрид', personal: 'Личный',
        any_pr: 'Все', average_pr: 'Средний', high_pr: 'Высокий',
        enabled: 'Вкл', disabled: 'Выкл',
        relaxed: 'Все', familiar: 'Знакомые', mains: 'Основные',
        overall: 'Общая', by_role: 'По роли',
        method_bayes: 'Баланс', method_signature: 'Сигнатурки', method_logit: 'Шансы',
        hero: 'Герой', th_meta: 'Мета', th_syn: 'Син', th_cnt: 'Кнтр',
        th_matches: 'М', th_player: 'Игрок', th_adv: 'Адв',
        opt_1w: '1 Неделя', opt_2w: '2 Недели', opt_1m: '1 Месяц', opt_trend: 'Тренды патча',
        no_data: 'Нет данных',
        rank_all: 'Все', rank_herald: 'Рекрут-Страж', rank_archon: 'Рыцарь-Герой', rank_ancient: 'Легенда-Властелин', rank_divine: 'Божество-Титан',
        live_draft: 'ДРАФТ', ready: 'ГОТОВ', updating: 'ОБНОВЛЕНИЕ', error: 'ОШИБКА',
        get_key: '(Получить)',
        range_title: 'Период сбора мета-статистики',
        rank_title: 'Фильтр мета-статистики по рангам игроков',
        mode_title: 'Алгоритм оценки рекомендаций героев',
        pick_rate_title: 'Фильтр героев по популярности в текущей мете',
        patch_relevance_title: 'Скрыть героев, на которых вы не играли последние 3 месяца',
        experience_title: 'Минимальное количество сыгранных матчей на герое',
        hero_stats_title: 'Использовать общую статистику или статистику по конкретной роли',
        eval_method_title: 'Метод расчета: Баланс (драфт+опыт), Сигнатурки (приоритет пула), Шансы (вероятностный Logit)',
        method_bayes_title: 'Баланс: компромисс между силой героя в драфте и вашим наигрышем',
        method_signature_title: 'Сигнатурки: приоритет вашего пула лучших героев, драфт лишь корректирует выбор',
        method_logit_title: 'Шансы: строгое вероятностное сложение шансов на победу (Log-Odds)',
        hero_title: 'Имя героя',
        th_meta_title: 'Винрейт героя в мете',
        th_syn_title: 'Синергия с союзниками',
        th_cnt_title: 'Контрпик против врагов',
        th_matches_title: 'Количество матчей игрока на герое',
        th_player_title: 'Винрейт игрока на герое',
        th_adv_title: 'Итоговый показатель преимущества',
        settings_title: 'Настройки',
        lang_title: 'Язык: Русский',
        sync_title: 'Синхронизировать со Stratz',
        tab_scoring: 'Выдача',
        tab_app: 'Приложение',
        hotkey_label: 'Горячая клавиша',
        hotkey_title: 'Глобальная клавиша для показа/скрытия оверлея в игре',
        tray_info_title: 'Работа в системном трее',
        tray_info_desc: 'IMPulse сворачивается в трей рядом с часами Windows. Кликните по иконке, чтобы скрыть или открыть окно.',
        open_browser: 'Открыть в браузере (Второй монитор)',
        opacity_label: 'Прозрачность',
        opacity_title: 'Прозрачность окна оверлея поверх Dota 2',
        perf_label: 'Производительность',
        perf_title: 'Баланс между скоростью детекта и нагрузкой на процессор',
        perf_eco: 'Эко (1.5с)',
        perf_balanced: 'Норма (0.3с)',
        perf_high: 'Макс (Без пауз)',
        grid_highlight_label: 'Подсветка в сетке',
        res_label: 'Разрешение экрана',
        res_title: 'Базовое разрешение экрана для калибровки',
        debug_capture_btn: 'Проверить область захвата',
        tab_draft: 'Драфт', tab_matrix: 'Сводка', tab_laning: 'Линии и Карта',
        matrix_title: 'Матчапы 5 на 5', matrix_subtitle: 'Оценки силы соперников против врагов',
        btn_reset_roles: '↺ Сброс ролей',
        role_duels_title: 'Очные дуэли по ролям (1v1)', role_duels_subtitle: 'Сравнение зеркальных позиций команд',
        hl_threats: 'Главные угрозы для команды', hl_dominance: 'Козыри команды (Контрпики)', hl_combos: 'Командные связки',
        lane_top: 'Верхняя линия', lane_mid: 'Центральная линия', lane_bot: 'Нижняя линия',
        status_easy: 'Легко', status_fair: 'Ровно', status_hard: 'Тяжело',
        in_game: 'В ИГРЕ',
        chip_meta: 'МЕТА',
        chip_matchups: 'МАТЧАПЫ',
        chip_map: 'КАРТА',
        win_odds: 'ПРОГНОЗ',
        hint_click_hero: 'Выберите роль или кликните героя в слотах драфта',
        reset_draft_btn: 'Сбросить матч',
        header_subtitle: 'AI АНАЛИЗ DOTA 2',
        prediction_label: 'ПРОГНОЗ',
        btn_reset_roles_txt: 'Сброс ролей',
        analysis_title: 'Персональный анализ: Вы',
        callout_lead: 'Кто из них вам?',
        callout_desc: 'Кликните по своему герою в слотах драфта или выберите позицию роли (1–5)!',
        col_strengths: 'Сильные стороны',
        col_risks: 'Риски',
        col_timing: 'Ключевой момент',
        col_recommendation: 'Рекомендация',
        col_my_strengths: 'Вы: Сильные стороны',
        col_my_risks: 'Вы: Риски',
        col_team_strengths: 'Команда: Сильные стороны',
        col_team_risks: 'Команда: Риски и угрозы',
        laning_title: 'Расстановка по линиям',
        laning_subtitle: 'Прогноз линий и контроль карты',
        laning_swap_hint: 'Смена линий'
    }
};
document.addEventListener('DOMContentLoaded', () => {
    let loaderAnimId = null;
    const loaderStartTime = Date.now();
    function init3DLoader() {
        const loader = document.getElementById('app-loader');
        const canvas = document.getElementById('loader-canvas');
        if (!canvas || !loader || loader.classList.contains('hidden')) return;
        const ctx = canvas.getContext('2d');
        let width = canvas.width = loader.offsetWidth || 464;
        let height = canvas.height = loader.offsetHeight || 650;
        const numPoints = 26;
        const radius = 130;
        const points = [];
        for (let i = 0; i < numPoints; i++) {
            const theta = Math.acos(2 * Math.random() - 1);
            const phi = 2 * Math.PI * Math.random();
            const r = radius * (0.65 + 0.35 * Math.random());
            points.push({
                x: r * Math.sin(theta) * Math.cos(phi),
                y: r * Math.sin(theta) * Math.sin(phi),
                z: r * Math.cos(theta),
                baseRadius: Math.random() * 1.6 + 1.4
            });
        }
        let angleX = 0;
        let angleY = 0;
        function render3D() {
            ctx.clearRect(0, 0, width, height);
            angleX += 0.007;
            angleY += 0.011;
            const cosX = Math.cos(angleX), sinX = Math.sin(angleX);
            const cosY = Math.cos(angleY), sinY = Math.sin(angleY);
            const cx = width / 2;
            const cy = height / 2;
            const fov = 350;
            const projected = [];
            for (let i = 0; i < points.length; i++) {
                const p = points[i];
                const x1 = p.x * cosY + p.z * sinY;
                const z1 = -p.x * sinY + p.z * cosY;
                const y2 = p.y * cosX - z1 * sinX;
                const z2 = p.y * sinX + z1 * cosX;
                const scale = fov / (fov + z2 + 200);
                const x2d = cx + x1 * scale;
                const y2d = cy + y2 * scale;
                projected.push({
                    x: x2d,
                    y: y2d,
                    z: z2,
                    scale: scale,
                    p: p
                });
            }
            for (let i = 0; i < projected.length; i++) {
                const p1 = projected[i];
                for (let j = i + 1; j < projected.length; j++) {
                    const p2 = projected[j];
                    const dx = p1.x - p2.x;
                    const dy = p1.y - p2.y;
                    const dist2d = Math.hypot(dx, dy);
                    if (dist2d < 88) {
                        const alpha = (1 - dist2d / 88) * 0.75 * Math.min(1.0, Math.min(p1.scale, p2.scale) * 1.3);
                        ctx.beginPath();
                        ctx.moveTo(p1.x, p1.y);
                        ctx.lineTo(p2.x, p2.y);
                        ctx.strokeStyle = `rgba(56, 189, 248, ${alpha})`;
                        ctx.lineWidth = 1.5;
                        ctx.stroke();
                    }
                }
            }
            for (let i = 0; i < projected.length; i++) {
                const pt = projected[i];
                const r = pt.p.baseRadius * pt.scale;
                const alpha = 0.55 + 0.45 * Math.max(0, (pt.z + radius) / (2 * radius));
                ctx.beginPath();
                ctx.arc(pt.x, pt.y, Math.max(1.2, r), 0, Math.PI * 2);
                ctx.fillStyle = `rgba(56, 189, 248, ${alpha})`;
                ctx.shadowColor = '#38bdf8';
                ctx.shadowBlur = 10;
                ctx.fill();
                ctx.shadowBlur = 0;
                ctx.beginPath();
                ctx.arc(pt.x, pt.y, Math.max(0.6, r * 0.45), 0, Math.PI * 2);
                ctx.fillStyle = `rgba(224, 242, 254, ${Math.min(1.0, alpha * 1.1)})`;
                ctx.fill();
            }
            loaderAnimId = requestAnimationFrame(render3D);
        }
        render3D();
    }
    init3DLoader();
    function hideLoader() {
        const loader = document.getElementById('app-loader');
        if (loader && !loader.classList.contains('hidden')) {
            const elapsed = Date.now() - loaderStartTime;
            const delay = Math.max(0, 900 - elapsed);
            setTimeout(() => {
                loader.classList.add('hidden');
                setTimeout(() => {
                    if (loaderAnimId) cancelAnimationFrame(loaderAnimId);
                }, 650);
            }, delay);
        }
    }
function updateLiveIndicator(data) {
    const liveIndicator = document.getElementById('live-indicator');
    if (!liveIndicator || !data || !data.state) return;
    const dsStatus = data.state.dataset_status || "";
    const t = translations[currentLang] || translations.en;
    if (dsStatus.startsWith("Error")) {
        liveIndicator.className = 'live-indicator error';
        liveIndicator.title = dsStatus.replace("Error: ", "");
        liveIndicator.innerHTML = `<span class="live-dot"></span><span>${t.error || 'ERROR'}</span>`;
    } else if (dsStatus && dsStatus !== "Idle" && dsStatus !== "Updated") {
        liveIndicator.className = 'live-indicator updating';
        liveIndicator.title = dsStatus;
        liveIndicator.innerHTML = `<span class="live-dot"></span><span>${t.updating || 'UPDATING'}</span>`;
    } else if (data.state.phase === 'ingame' || (data.state.num_picked === 10 && !data.state.draft_active)) {
        liveIndicator.className = 'live-indicator in-match';
        liveIndicator.title = '';
        liveIndicator.innerHTML = `<span class="live-dot"></span><span>${t.in_game || 'IN MATCH'}</span>`;
    } else if (data.state.draft_active) {
        liveIndicator.className = 'live-indicator draft-phase';
        liveIndicator.title = '';
        const pickCount = data.state.num_picked || 0;
        const draftLabel = (pickCount === 0)
            ? (currentLang === 'ru' ? 'ДРАФТ (1-Й ПИК)' : 'DRAFT (1ST PICK)')
            : (currentLang === 'ru' ? `ДРАФТ ${pickCount}/10` : `DRAFT ${pickCount}/10`);
        liveIndicator.innerHTML = `<span class="live-dot"></span><span>${draftLabel}</span>`;
    } else {
        liveIndicator.className = 'live-indicator ready';
        liveIndicator.title = '';
        liveIndicator.innerHTML = `<span class="live-dot"></span><span>${t.ready || 'READY'}</span>`;
    }
}
let isUpdatingUI = false;
function setLanguage(lang, refreshUI = true) {
    currentLang = lang;
    const t = translations[lang] || translations.en;
    const btnLang = document.getElementById('btn-lang');
    const langTxt = document.getElementById('lang-btn-text');
    if (langTxt) {
        langTxt.textContent = (lang === 'ru') ? 'RU' : 'EN';
    } else if (btnLang) {
        btnLang.textContent = (lang === 'ru') ? 'RU' : 'EN';
    }
    if (btnLang) {
        btnLang.title = t.lang_title || ((lang === 'ru') ? 'Язык: Русский' : 'Language: English');
    }
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t[key]) {
            if (el.tagName === 'OPTION') {
                el.textContent = t[key];
            } else {
                el.innerHTML = t[key];
            }
        }
    });
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        const key = el.getAttribute('data-i18n-title');
        if (t[key]) {
            el.title = t[key];
        }
    });
    lastPostAnalysisSignature = "";
    lastRecsSignature = "";
    if (refreshUI && currentState && !isUpdatingUI) {
        updateLiveIndicator(currentState);
        updateUI(currentState);
    }
}
    const btnLang = document.getElementById('btn-lang');
    if (btnLang) {
        btnLang.addEventListener('click', () => {
            const newLang = currentLang === 'en' ? 'ru' : 'en';
            setLanguage(newLang);
            fetch('/api/settings', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({lang: newLang})
            });
        });
    }
    const syncBtn = document.getElementById('btn-sync');
    const steamInput = document.getElementById('steam-id');
    const syncStatus = document.getElementById('sync-status');
    const tableBody = document.getElementById('recs-body');
    const radSlots = document.getElementById('radiant-slots').children;
    const direSlots = document.getElementById('dire-slots').children;
    let currentState = null;
    const btnToggleSettings = document.getElementById('btn-toggle-settings');
    const settingsPanel = document.getElementById('settings-panel');
    btnToggleSettings.addEventListener('click', () => {
        settingsPanel.classList.toggle('hidden');
    });
    const btnResetRoles = document.getElementById('btn-reset-roles');
    if (btnResetRoles) {
        btnResetRoles.addEventListener('click', () => {
            clearPendingSwap();
            lastPostAnalysisSignature = "";
            fetch('/api/reset_roles', { method: 'POST' })
                .then(r => r.json())
                .then(() => {
                    lastPostAnalysisSignature = "";
                    fetch('/api/state').then(r => r.json()).then(updateUI).catch(console.error);
                })
                .catch(console.error);
        });
    }
    const btnLockTelegram = document.getElementById('btn-lock-telegram');
    if (btnLockTelegram) {
        btnLockTelegram.addEventListener('click', () => {
            fetch('/api/open_telegram', { method: 'POST' })
                .then(r => r.json())
                .then(res => {
                    if (res && res.url) {
                        window.open(res.url, '_blank');
                    }
                })
                .catch(console.error);
        });
    }
    const btnLockRetry = document.getElementById('btn-lock-retry');
    if (btnLockRetry) {
        btnLockRetry.addEventListener('click', () => {
            btnLockRetry.disabled = true;
            btnLockRetry.style.opacity = '0.5';
            fetch('/api/check_license', { method: 'POST' })
                .then(r => r.json())
                .then(() => {
                    return fetch('/api/state').then(r => r.json()).then(updateUI);
                })
                .catch(console.error)
                .finally(() => {
                    setTimeout(() => {
                        btnLockRetry.disabled = false;
                        btnLockRetry.style.opacity = '1';
                    }, 1200);
                });
        });
    }
    let currentView = 'draft';
    let userManuallySelectedView = false;
    function switchView(viewName, isManual = true) {
        currentView = viewName;
        if (isManual) {
            userManuallySelectedView = true;
        }
        document.querySelectorAll('.view-tab-btn').forEach(btn => {
            if (btn.getAttribute('data-view') === viewName) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        const paneDraft = document.getElementById('view-pane-draft');
        const paneMatrix = document.getElementById('view-pane-matrix');
        const paneLaning = document.getElementById('view-pane-laning');
        if (paneDraft) paneDraft.classList.toggle('hidden', viewName !== 'draft');
        if (paneMatrix) paneMatrix.classList.toggle('hidden', viewName !== 'matrix');
        if (paneLaning) paneLaning.classList.toggle('hidden', viewName !== 'laning');
    }
    document.querySelectorAll('.view-tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const v = btn.getAttribute('data-view');
            switchView(v, true);
        });
    });
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('tab')) {
        switchView(urlParams.get('tab'), true);
    }
    if (urlParams.get('settings') === '1') {
        const sp = document.getElementById('settings-panel');
        if (sp) sp.classList.remove('hidden');
    }
    const btnResetMatchMatrix = document.getElementById('btn-reset-match-matrix');
    if (btnResetMatchMatrix) {
        btnResetMatchMatrix.addEventListener('click', () => {
            clearPendingSwap();
            fetch('/api/reset_draft', { method: 'POST' })
                .then(r => r.json())
                .then(() => {
                    userManuallySelectedView = false;
                    switchView('draft', false);
                    setMyHero(null, false);
                    lastPostAnalysisSignature = "";
                    fetch('/api/state').then(r => r.json()).then(updateUI).catch(console.error);
                }).catch(console.error);
        });
    }
    const matrixSideToggle = document.getElementById('matrix-side-toggle');
    if (matrixSideToggle) {
        matrixSideToggle.addEventListener('click', (e) => {
            const btn = e.target.closest('.matrix-side-btn');
            if (btn && btn.dataset.side) {
                setTeamExplicit(btn.dataset.side);
            }
        });
    }
    const radSlotsContainer = document.getElementById('radiant-slots');
    if (radSlotsContainer) {
        radSlotsContainer.addEventListener('click', (e) => {
            const slot = e.target.closest('.slot.filled');
            if (!slot) return;
            const h = slot.getAttribute('data-hero');
            if (h) setMyHero(h);
        });
    }
    const direSlotsContainer = document.getElementById('dire-slots');
    if (direSlotsContainer) {
        direSlotsContainer.addEventListener('click', (e) => {
            const slot = e.target.closest('.slot.filled');
            if (!slot) return;
            const h = slot.getAttribute('data-hero');
            if (h) setMyHero(h);
        });
    }
    document.querySelectorAll('.segmented-control').forEach(ctrl => {
        ctrl.addEventListener('click', (e) => {
            const btn = e.target.closest('button');
            if (btn && btn.dataset && btn.dataset.val !== undefined) {
                Array.from(ctrl.children).forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                if (ctrl.id === 'ctrl-team') {
                    const newTeam = btn.dataset.val;
                    if (selectedMyHero && currentState && currentState.state) {
                        const teamHeroes = (newTeam === 'dire') 
                            ? (currentState.state.dire || []) 
                            : (currentState.state.radiant || []);
                        if (!teamHeroes.includes(selectedMyHero)) {
                            selectedMyHero = null;
                            localStorage.removeItem('impulse_my_hero');
                        }
                    }
                    lastPostAnalysisSignature = "";
                }
                if (ctrl.id === 'ctrl-role') {
                    const roleVal = btn.dataset.val;
                    if (roleVal !== 'all') {
                        isManualMyHero = false;
                        if (currentState && currentState.state && currentState.state.post_analysis && currentState.state.post_analysis.matrix) {
                            const ally = (currentState.state.post_analysis.matrix.rows || []).find(r => r.role === parseInt(roleVal, 10));
                            if (ally) {
                                selectedMyHero = ally.cdn;
                            }
                        }
                    }
                    lastPostAnalysisSignature = "";
                }
                if (ctrl.id === 'ctrl-calc') {
                    const calcMode = btn.dataset.val;
                    document.querySelectorAll('.personal-only').forEach(el => {
                        el.style.display = (calcMode === 'smart') ? 'block' : 'none';
                    });
                }
                updateSettings();
            }
        });
    });
    function getSegmentedValue(id, defaultVal = null) {
        const el = document.querySelector(`#${id} .active`);
        if (el && el.dataset && el.dataset.val !== undefined) {
            return el.dataset.val;
        }
        const first = document.querySelector(`#${id} button`);
        if (first && first.dataset && first.dataset.val !== undefined) {
            first.classList.add('active');
            return first.dataset.val;
        }
        return defaultVal;
    }
    function setSegmentedValue(id, val) {
        const ctrl = document.getElementById(id);
        if (!ctrl) return;
        let matched = false;
        Array.from(ctrl.children).forEach(b => {
            if (b.dataset && b.dataset.val === String(val)) {
                b.classList.add('active');
                matched = true;
            } else {
                b.classList.remove('active');
            }
        });
        if (!matched && ctrl.children.length > 0) {
            ctrl.children[0].classList.add('active');
        }
    }
    syncBtn.addEventListener('click', () => {
        const steamId = steamInput.value.trim();
        if (!steamId) return;
        syncBtn.classList.add('spinning');
        const syncText = currentLang === 'ru' ? "Синхронизация..." : "Syncing...";
        syncStatus.textContent = syncText;
        syncStatus.title = syncText;
        syncStatus.className = "status-badge";
        syncStatus.style.display = "inline-flex";
        document.querySelector(".header").classList.add("sync-active");
        if (typeof lastSyncStatus !== 'undefined') lastSyncStatus = "Syncing...";
        const hideSync = () => {
            syncStatus.style.display = "none";
            if (document.getElementById("dataset-status").style.display === "none") document.querySelector(".header").classList.remove("sync-active");
        };
        fetch('/api/sync', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({steam_id: steamId, timeframe: 'all'})
        })
        .then(res => res.json())
        .then(data => {
            syncBtn.classList.remove('spinning');
            if (data.status === 'ok') {
                updateSettings();
                hideSync();
            } else {
                let msg = data.msg || (currentLang === 'ru' ? "Ошибка Stratz" : "Stratz Error");
                if (msg.startsWith("Wait")) {
                    const secs = msg.replace(/\D/g, '');
                    msg = currentLang === 'ru' ? `Подождите ${secs}с` : `Wait ${secs}s`;
                    syncStatus.className = "status-badge warning";
                } else {
                    syncStatus.className = "status-badge error";
                }
                syncStatus.textContent = msg;
                syncStatus.title = data.msg || msg;
                syncStatus.style.display = "inline-flex";
                document.querySelector(".header").classList.add("sync-active");
                clearTimeout(syncHideTimeout);
                syncHideTimeout = setTimeout(hideSync, 4000);
            }
        })
        .catch(err => {
            syncBtn.classList.remove('spinning');
            syncStatus.textContent = currentLang === 'ru' ? "Сетевая ошибка" : "Network Error";
            syncStatus.className = "status-badge error";
            syncStatus.style.display = "inline-flex";
                document.querySelector(".header").classList.add("sync-active");
            clearTimeout(syncHideTimeout);
            syncHideTimeout = setTimeout(hideSync, 4000);
        });
    });
    fetch('/api/patches')
        .then(r => r.json())
        .then(patches => {
            const select = document.getElementById('ctrl-mode-select');
            if(select && patches.length > 0) {
                patches.forEach(p => {
                    const opt = document.createElement('option');
                    opt.value = `Patch ${p.name}`;
                    opt.textContent = `Patch ${p.name}`;
                    select.appendChild(opt);
                });
            }
        }).catch(console.error);
    const modeSelect = document.getElementById('ctrl-mode-select');
    if (modeSelect) {
        modeSelect.addEventListener('change', () => {
            updateSettings();
        });
    }
    const rankSelect = document.getElementById('ctrl-rank-select');
    if (rankSelect) {
        rankSelect.addEventListener('change', () => {
            updateSettings();
        });
    }
    const hotkeySelect = document.getElementById('ctrl-hotkey');
    if (hotkeySelect) {
        hotkeySelect.addEventListener('change', () => {
            updateSettings();
        });
    }
    const resolutionSelect = document.getElementById('ctrl-resolution');
    if (resolutionSelect) {
        resolutionSelect.addEventListener('change', () => {
            updateSettings();
        });
    }
    const btnDebugCapture = document.getElementById('btn-debug-capture');
    if (btnDebugCapture) {
        btnDebugCapture.addEventListener('click', () => {
            btnDebugCapture.innerText = currentLang === 'ru' ? "⏳ Захват..." : "⏳ Capturing...";
            fetch('/api/debug_capture', { method: 'POST' })
                .then(r => r.json())
                .then(res => {
                    const label = currentLang === 'ru' ? "Проверить область захвата" : "Inspect Capture Area";
                    btnDebugCapture.innerHTML = `<span>📸</span> <span>${label}</span>`;
                })
                .catch(err => {
                    console.error(err);
                    const label = currentLang === 'ru' ? "Проверить область захвата" : "Inspect Capture Area";
                    btnDebugCapture.innerHTML = `<span>📸</span> <span>${label}</span>`;
                });
        });
    }
    document.querySelectorAll('.settings-tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            document.querySelectorAll('.settings-tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.querySelectorAll('.settings-tab-content').forEach(content => {
                if (content.id === targetTab) {
                    content.style.display = 'block';
                    content.classList.add('active');
                } else {
                    content.style.display = 'none';
                    content.classList.remove('active');
                }
            });
        });
    });
    if (urlParams.get('stab') === 'app') {
        const appTabBtn = document.querySelector('.settings-tab-btn[data-tab="tab-app"]');
        if (appTabBtn) appTabBtn.click();
    }
    function updateSettings() {
        const payload = {
            steam_id: steamInput.value.trim(),
            timeframe: 'all',
            team: getSegmentedValue('ctrl-team'),
            role: getSegmentedValue('ctrl-role'),
            rank: rankSelect ? rankSelect.value : "all",
            mode: modeSelect ? modeSelect.value : "1m",
            calc: getSegmentedValue('ctrl-calc'),
            strictness: getSegmentedValue('ctrl-strictness'),
            popularity: getSegmentedValue('ctrl-popularity'),
            decay: getSegmentedValue('ctrl-decay') === "true",
            role_transfer_enabled: getSegmentedValue('ctrl-role-transfer') === "true",
            eval_method: getSegmentedValue('ctrl-eval-method'),
            hotkey: hotkeySelect ? hotkeySelect.value : "INSERT",
            opacity: parseInt(getSegmentedValue('ctrl-opacity')) || 90,
            perf_mode: getSegmentedValue('ctrl-perf') || 'balanced',
            resolution: resolutionSelect ? resolutionSelect.value : "auto",
            grid_highlight: getSegmentedValue('ctrl-grid-highlight') === "true"
        };
        fetch('/api/settings', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        })
        .then(r => r.json())
        .then(data => {
            if (data && data.status === 'ok') {
                fetch('/api/state').then(r => r.json()).then(updateUI).catch(console.error);
            }
        }).catch(console.error);
    }
    function formatDelta(val) {
        if (val === undefined || val === null) return `<span class="val-neu">-</span>`;
        if (Math.abs(val) <= 1.0) return `<span class="val-neu">${val > 0 ? '+' : ''}${val.toFixed(1)}%</span>`;
        if (val > 1.0) return `<span class="val-pos">+${val.toFixed(1)}%</span>`;
        return `<span class="val-neg">${val.toFixed(1)}%</span>`;
    }
    function formatWinrate(val) {
        if (!val) return `<span class="val-neu">-</span>`;
        if (val > 51.0) return `<span class="val-pos">${val.toFixed(1)}%</span>`;
        if (val < 49.0) return `<span class="val-neg">${val.toFixed(1)}%</span>`;
        return `<span class="val-neu">${val.toFixed(1)}%</span>`;
    }
    let selectedMyHero = localStorage.getItem('impulse_my_hero') || null;
    let isManualMyHero = !!localStorage.getItem('impulse_my_hero');
    let pendingSwap = null;
    function applySwapHighlights() {
        document.querySelectorAll('.swap-pending').forEach(el => el.classList.remove('swap-pending'));
        if (!pendingSwap) return;
        const { cdn } = pendingSwap;
        document.querySelectorAll(`.matrix-hero-thumb[data-hero="${cdn}"], .map-hero-circle[data-hero="${cdn}"], .slot[data-hero="${cdn}"]`)
            .forEach(el => el.classList.add('swap-pending'));
    }
    function clearPendingSwap() {
        pendingSwap = null;
        applySwapHighlights();
    }
    function handleSwapSelection(team, cdn, role) {
        if (!team || !cdn) return;
        if (!pendingSwap) {
            pendingSwap = { team, cdn, role };
            applySwapHighlights();
            return;
        }
        if (pendingSwap.cdn === cdn) {
            clearPendingSwap();
            return;
        }
        if (pendingSwap.team === team) {
            const payload = {
                team: team,
                hero1: pendingSwap.cdn,
                role1: pendingSwap.role,
                hero2: cdn,
                role2: role
            };
            clearPendingSwap();
            lastPostAnalysisSignature = "";
            fetch('/api/swap_roles', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(r => r.json())
            .then(() => {
                lastPostAnalysisSignature = "";
                fetch('/api/state').then(r => r.json()).then(updateUI).catch(console.error);
            })
            .catch(console.error);
            return;
        }
        pendingSwap = { team, cdn, role };
        applySwapHighlights();
    }
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && pendingSwap) {
            clearPendingSwap();
        }
    });
    function setTeamExplicit(side) {
        if (!side || (side !== 'radiant' && side !== 'dire')) return;
        setSegmentedValue('ctrl-team', side);
        if (selectedMyHero && currentState && currentState.state) {
            const teamHeroes = (side === 'dire') 
                ? (currentState.state.dire || []) 
                : (currentState.state.radiant || []);
            if (!teamHeroes.includes(selectedMyHero)) {
                selectedMyHero = null;
                isManualMyHero = false;
                localStorage.removeItem('impulse_my_hero');
            }
        }
        lastPostAnalysisSignature = "";
        updateSettings();
    }
    function setMyHero(heroCdn, isManual = true) {
        lastPostAnalysisSignature = "";
        if (heroCdn === null || selectedMyHero === heroCdn) {
            selectedMyHero = null;
            isManualMyHero = false;
            localStorage.removeItem('impulse_my_hero');
        } else {
            selectedMyHero = heroCdn;
            isManualMyHero = isManual;
            if (isManual) {
                localStorage.setItem('impulse_my_hero', heroCdn);
            } else {
                localStorage.removeItem('impulse_my_hero');
            }
            if (currentState && currentState.state) {
                const inDire = (currentState.state.dire || []).includes(heroCdn);
                const inRad = (currentState.state.radiant || []).includes(heroCdn);
                const currentTeam = (currentState.settings && currentState.settings.team) || getSegmentedValue('ctrl-team') || 'radiant';
                if (inDire && currentTeam !== 'dire') {
                    setTeamExplicit('dire');
                    return;
                } else if (inRad && currentTeam !== 'radiant') {
                    setTeamExplicit('radiant');
                    return;
                }
            }
        }
        if (currentState) {
            updateUI(currentState);
        }
    }
    function renderSlots(slots, heroes, isUserTeam) {
        for (let i = 0; i < 5; i++) {
            const slot = slots[i];
            if (i < heroes.length && heroes[i]) {
                const hCdn = heroes[i];
                const bg = `url('/assets/panorama/images/heroes/icons/npc_dota_hero_${hCdn}_png.png')`;
                if (slot.getAttribute('data-hero') !== hCdn) {
                    slot.style.backgroundImage = bg;
                    slot.classList.remove('empty');
                    slot.classList.add('filled');
                    slot.setAttribute('data-hero', hCdn);
                }
                const isMy = (selectedMyHero === hCdn);
                const desiredTitle = isMy ? `${hCdn} (⭐ ВЫ - нажмите чтобы отменить)` : `${hCdn} (нажмите, чтобы выбрать своим героем)`;
                if (isMy && !slot.classList.contains('is-my-hero')) {
                    slot.classList.add('is-my-hero');
                } else if (!isMy && slot.classList.contains('is-my-hero')) {
                    slot.classList.remove('is-my-hero');
                }
                if (slot.title !== desiredTitle) {
                    slot.title = desiredTitle;
                }
            } else {
                if (slot.getAttribute('data-hero') || slot.classList.contains('filled') || slot.style.backgroundImage !== 'none') {
                    slot.style.backgroundImage = 'none';
                    slot.classList.add('empty');
                    slot.classList.remove('filled', 'is-my-hero', 'swap-pending');
                    slot.removeAttribute('data-hero');
                    slot.title = '';
                }
            }
        }
    }
    let lastSyncStatus = "";
    let syncHideTimeout = null;
    let lastRecsSignature = "";
    let lastPostAnalysisSignature = "";
    let highlightTimeout = null;
    let activeTargetHero = null;
    let lastSentHero = null;
    function requestHeroHighlight(heroKey) {
        if (!currentState || !currentState.state || !currentState.state.draft_active) {
            return;
        }
        if (currentState && currentState.settings && currentState.settings.grid_highlight === false) {
            return;
        }
        activeTargetHero = heroKey;
        if (highlightTimeout) {
            clearTimeout(highlightTimeout);
        }
        highlightTimeout = setTimeout(() => {
            const target = activeTargetHero;
            if (target === lastSentHero) return;
            lastSentHero = target;
            fetch('/api/highlight', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ hero: target })
            }).catch(() => {});
        }, 35);
    }
    function clearHeroHighlightImmediately() {
        activeTargetHero = null;
        if (highlightTimeout) {
            clearTimeout(highlightTimeout);
            highlightTimeout = null;
        }
        if (lastSentHero !== null) {
            lastSentHero = null;
            fetch('/api/highlight', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ hero: null })
            }).catch(() => {});
        }
    }
    const ROMAN_NUMERALS = ['', 'I', 'II', 'III', 'IV', 'V'];
    function renderDraftSummaryBanner(post) {
        const card = document.getElementById('match-summary-card');
        if (!card) return;
        if (!post || !post.summary) {
            card.style.display = 'none';
            return;
        }
        card.style.display = 'flex';
        const { summary, matrix } = post;
        const userTeam = post.user_team || (currentState && currentState.settings && currentState.settings.team) || 'radiant';
        const wrEl = document.getElementById('summary-team-wr');
        const winProb = (summary.team_win_prob !== undefined) ? summary.team_win_prob : 50.0;
        if (wrEl) {
            wrEl.textContent = `${winProb.toFixed(1)}%`;
            wrEl.className = 'summary-score-val';
            if (winProb >= 51.0) {
                wrEl.classList.add('val-win');
            } else if (winProb <= 49.0) {
                wrEl.classList.add('val-loss');
            } else {
                wrEl.classList.add('val-even');
            }
            wrEl.title = currentLang === 'ru' ? `Прогноз победы: ${winProb.toFixed(1)}%` : `Win prediction: ${winProb.toFixed(1)}%`;
        }
        const teamAdvEl = document.getElementById('summary-team-adv');
        if (teamAdvEl) {
            const teamName = (userTeam === 'dire') 
                ? (currentLang === 'ru' ? 'Тьма' : 'Dire') 
                : (currentLang === 'ru' ? 'Свет' : 'Radiant');
            const netAdv = (summary.team_net_adv !== undefined) ? summary.team_net_adv : (winProb - 50.0);
            const netSign = netAdv >= 0 ? '+' : '';
            teamAdvEl.textContent = `${teamName}  ${netSign}${netAdv.toFixed(1)}%`;
            teamAdvEl.style.color = (netAdv >= 0) ? '#00e5ff' : '#ff4747';
        }
        function formatEvalChip(valEl, evData, defaultDesc) {
            if (!valEl) return;
            if (!evData) {
                valEl.textContent = '--';
                return;
            }
            const userAdv = evData.user_delta || 0;
            const sign = userAdv > 0 ? '+' : '';
            valEl.textContent = `${sign}${userAdv.toFixed(1)}%`;
            if (userAdv >= 0.5) {
                valEl.style.color = '#00e5ff';
            } else if (userAdv <= -0.5) {
                valEl.style.color = '#ff4747';
            } else {
                valEl.style.color = 'var(--imp-text-primary, #ffffff)';
            }
            if (valEl.parentElement) {
                valEl.parentElement.title = defaultDesc;
            }
        }
        const metaEl = document.getElementById('summary-meta-val');
        const draftEl = document.getElementById('summary-draft-val');
        const sideEl = document.getElementById('summary-side-val');
        formatEvalChip(metaEl, summary.meta, currentLang === 'ru' ? 'Оценка чисто по мете патча' : 'Meta rating');
        formatEvalChip(draftEl, summary.matchup, currentLang === 'ru' ? 'Оценка чисто по матчапам драфта' : 'Matchup rating');
        if (sideEl) {
            const sBias = summary.side_bias !== undefined ? summary.side_bias : (userTeam === 'radiant' ? 1.2 : -1.2);
            const sideSign = sBias > 0 ? '+' : '';
            sideEl.textContent = `${sideSign}${sBias.toFixed(1)}%`;
            sideEl.style.color = sBias > 0 ? '#00e5ff' : '#ff4747';
            if (sideEl.parentElement) {
                sideEl.parentElement.title = currentLang === 'ru'
                    ? `Исторический баланс стороны карты: ${sideSign}${sBias.toFixed(1)}%`
                    : `Map side bias: ${sideSign}${sBias.toFixed(1)}%`;
            }
        }
        const personalBlock = document.getElementById('summary-personal-block');
        if (personalBlock) {
            const activeRoleSetting = (currentState && currentState.settings && currentState.settings.role) || getSegmentedValue('ctrl-role') || 'all';
            if (!isManualMyHero && activeRoleSetting !== 'all' && matrix && matrix.rows) {
                const roleNum = parseInt(activeRoleSetting, 10);
                if (!isNaN(roleNum)) {
                    const allyMatchingRole = matrix.rows.find(r => r.role === roleNum);
                    if (allyMatchingRole && selectedMyHero !== allyMatchingRole.cdn) {
                        selectedMyHero = allyMatchingRole.cdn;
                    }
                }
            }
            let myAlly = null;
            if (selectedMyHero && matrix && matrix.rows) {
                myAlly = matrix.rows.find(r => r.cdn === selectedMyHero);
            }
            if (myAlly) {
                personalBlock.classList.add('has-hero');
                const expWr = (myAlly.expected_wr !== undefined) ? myAlly.expected_wr : myAlly.avg_wr;
                const scoreClass = (expWr >= 51.0) ? 'val-win' : (expWr <= 49.0 ? 'val-loss' : 'val-even');
                const roleTxt = ROMAN_NUMERALS[myAlly.role] || myAlly.role;
                const rolePrefix = (currentLang === 'ru') ? 'Рол ' : 'Role ';
                const diffWithTeam = expWr - winProb;
                const vsTeamSign = diffWithTeam >= 0 ? '+' : '';
                const vsTeamLabel = currentLang === 'ru' ? 'к команде' : 'vs team';
                personalBlock.innerHTML = `
                    <div class="summary-my-hero-row">
                        <div class="my-hero-main-info">
                            <span class="my-hero-pos-badge" style="color: var(--imp-accent); font-size: 8.5px; text-transform: uppercase; font-weight: 700;">${currentLang === 'ru' ? 'ВАШ ГЕРОЙ:' : 'YOUR HERO:'}</span>
                            <img src="/assets/panorama/images/heroes/icons/npc_dota_hero_${myAlly.cdn}_png.png" class="my-hero-avatar-sm" onerror="this.src=''">
                            <span class="my-hero-name-txt" title="${myAlly.name}">${myAlly.name}</span>
                            <span class="my-hero-pos-badge">${rolePrefix}${roleTxt}</span>
                        </div>
                        <div class="my-hero-stats-info">
                            <span class="my-hero-pred-score ${scoreClass}">${expWr.toFixed(1)}%</span>
                            <span class="my-hero-vs-team">(${vsTeamSign}${diffWithTeam.toFixed(1)}% ${vsTeamLabel})</span>
                        </div>
                    </div>
                `;
            } else {
                personalBlock.classList.remove('has-hero');
                personalBlock.innerHTML = `
                    <div class="summary-personal-hint">
                        <span class="hint-icon">★</span>
                        <span class="hint-text">${currentLang === 'ru' ? 'Выберите роль или кликните героя в слотах драфта' : 'Select role or click hero in draft slots for personal analysis'}</span>
                    </div>
                `;
            }
        }
    }
    function renderMatchupMatrix(post) {
        renderDraftSummaryBanner(post);
        const matrixTable = document.getElementById('matrix-table');
        if (!matrixTable || !post || !post.matrix) return;
        const btnResetRoles = document.getElementById('btn-reset-roles');
        if (btnResetRoles) {
            btnResetRoles.classList.remove('hidden');
        }
        const { rows, enemies } = post.matrix;
        if (!rows || rows.length === 0 || !enemies || enemies.length === 0) {
            matrixTable.innerHTML = `<tr><td style="padding:20px; text-align:center; color:#94a3b8;">${currentLang === 'ru' ? 'Ожидание пиков обеих команд...' : 'Awaiting team picks...'}</td></tr>`;
            return;
        }
        const userTeam = post.user_team || (currentState && currentState.settings && currentState.settings.team) || 'radiant';
        const enemyTeam = (userTeam === 'dire') ? 'radiant' : 'dire';
        const allySideClass = (userTeam === 'dire') ? 'side-dire' : 'side-rad';
        const enemySideClass = (userTeam === 'dire') ? 'side-rad' : 'side-dire';
        const rolePrefix = (currentLang === 'ru') ? 'Рол ' : 'Role ';
        let html = '<thead><tr>';
        html += `
            <th class="matrix-corner">
                <div class="matrix-corner-clean">
                    <span class="corner-foe" title="${currentLang === 'ru' ? 'Вражеские герои по колонкам' : 'Enemy heroes across columns'}">${currentLang === 'ru' ? 'ВРАГИ ►' : 'ENEMIES ►'}</span>
                    <span class="corner-ally" title="${currentLang === 'ru' ? 'Ваша команда по строкам' : 'Your team down rows'}">${currentLang === 'ru' ? '▼ ВЫ' : '▼ YOU'}</span>
                </div>
            </th>
        `;
        enemies.forEach(e => {
            const isSwapPending = (pendingSwap && pendingSwap.cdn === e.cdn);
            html += `
                <th class="matrix-col-enemy" data-enemy="${e.cdn}" data-role="${e.role}" data-team="${enemyTeam}" title="${e.name} (Pos ${e.role}) - ${currentLang === 'ru' ? 'Кликните для обмена позициями' : 'Click to swap role'}">
                    <div class="matrix-enemy-header">
                        <div class="matrix-hero-thumb enemy ${isSwapPending ? 'swap-pending' : ''}" data-hero="${e.cdn}">
                            <img src="/assets/panorama/images/heroes/icons/npc_dota_hero_${e.cdn}_png.png" class="mini-avatar" onerror="this.src=''">
                            <span class="matrix-pos-tag">${e.role}</span>
                        </div>
                    </div>
                </th>
            `;
        });
        html += `<th class="matrix-status-col">${currentLang === 'ru' ? 'Итог' : 'Total'}</th>`;
        html += '</tr></thead><tbody>';
        rows.forEach(ally => {
            const isMyHero = (selectedMyHero === ally.cdn);
            const myClass = isMyHero ? 'is-my-hero' : '';
            const isSwapPending = (pendingSwap && pendingSwap.cdn === ally.cdn);
            const star = isMyHero ? ' ⭐ ВЫ' : '';
            html += `<tr>`;
            html += `
                <th class="matrix-ally-th" data-ally="${ally.cdn}" data-role="${ally.role}" data-team="${userTeam}" title="${ally.name} (Pos ${ally.role})${star} - ${currentLang === 'ru' ? 'Кликните для обмена (двойной клик — выбор героя)' : 'Click to swap (double click to select hero)'}">
                    <div class="matrix-ally-header">
                        <div class="matrix-hero-thumb ally ${myClass} ${isSwapPending ? 'swap-pending' : ''}" data-hero="${ally.cdn}">
                            <img src="/assets/panorama/images/heroes/icons/npc_dota_hero_${ally.cdn}_png.png" class="mini-avatar ${myClass}" onerror="this.src=''">
                            <span class="matrix-pos-tag">${ally.role}</span>
                        </div>
                    </div>
                </th>
            `;
            ally.cells.forEach(c => {
                const sign = c.delta > 0 ? '+' : '';
                const tip = currentLang === 'ru'
                    ? `${ally.name} против ${c.enemy_name}: ${sign}${c.delta.toFixed(1)}% к винрейту (${c.wr}% очный WR, ${c.matches} матчей)`
                    : `${ally.name} vs ${c.enemy_name}: ${sign}${c.delta.toFixed(1)}% winrate shift (${c.wr}% vs WR, ${c.matches} matches)`;
                let innerContent = '';
                if (c.delta <= -1.0) {
                    innerContent = `<strong class="matrix-val-box box-threat"><span class="val-neg">${sign}${c.delta.toFixed(1)}%</span></strong>`;
                } else if (c.delta >= 1.0) {
                    innerContent = `<strong class="matrix-val-box box-counter"><span class="val-pos">${sign}${c.delta.toFixed(1)}%</span></strong>`;
                } else {
                    innerContent = `<span class="val-neu">${sign}${c.delta.toFixed(1)}%</span>`;
                }
                html += `<td class="matrix-cell" title="${tip}">${innerContent}</td>`;
            });
            const expWr = (ally.expected_wr !== undefined) ? ally.expected_wr : ally.avg_wr;
            let totalContent = '';
            if (expWr >= 51.0) {
                totalContent = `<strong class="matrix-val-box box-counter"><span class="val-pos">${expWr.toFixed(1)}%</span></strong>`;
            } else if (expWr <= 49.0) {
                totalContent = `<strong class="matrix-val-box box-threat"><span class="val-neg">${expWr.toFixed(1)}%</span></strong>`;
            } else {
                totalContent = `<span class="val-neu">${expWr.toFixed(1)}%</span>`;
            }
            const tipFinal = `${ally.name}: ${currentLang === 'ru' ? 'Ожидаемый винрейт в матче' : 'Expected match winrate'}: ${expWr.toFixed(1)}%`;
            html += `
                <td class="matrix-status-col matrix-cell" title="${tipFinal}">
                    ${totalContent}
                </td>
            `;
            html += `</tr>`;
        });
        html += '</tbody>';
        matrixTable.innerHTML = html;
        if (!matrixTable.dataset.listener) {
            matrixTable.dataset.listener = 'true';
            matrixTable.addEventListener('click', (e) => {
                const thAlly = e.target.closest('.matrix-ally-th');
                if (thAlly) {
                    const cdn = thAlly.getAttribute('data-ally');
                    const role = parseInt(thAlly.getAttribute('data-role'), 10);
                    const team = thAlly.getAttribute('data-team') || userTeam;
                    if (cdn) handleSwapSelection(team, cdn, role);
                    return;
                }
                const thEnemy = e.target.closest('.matrix-col-enemy');
                if (thEnemy) {
                    const cdn = thEnemy.getAttribute('data-enemy');
                    const role = parseInt(thEnemy.getAttribute('data-role'), 10);
                    const team = thEnemy.getAttribute('data-team') || enemyTeam;
                    if (cdn) handleSwapSelection(team, cdn, role);
                    return;
                }
            });
            matrixTable.addEventListener('dblclick', (e) => {
                const thAlly = e.target.closest('.matrix-ally-th');
                if (thAlly) {
                    clearPendingSwap();
                    const cdn = thAlly.getAttribute('data-ally');
                    if (cdn) setMyHero(cdn, true);
                }
            });
        }
    }
    function renderHighlights(post) {
        if (!post || !post.highlights) return;
        const myStrEl = document.getElementById('insight-my-strengths');
        const myRskEl = document.getElementById('insight-my-risks');
        const teamStrEl = document.getElementById('insight-team-strengths');
        const teamRskEl = document.getElementById('insight-team-risks');
        const cardTitleEl = document.getElementById('analysis-card-title');
        const calloutLeadEl = document.getElementById('callout-lead');
        const calloutDescEl = document.getElementById('callout-desc');
        const rolePrefix = (currentLang === 'ru') ? 'Рол ' : 'Role ';
        const myHeroRow = (post.matrix && post.matrix.rows) ? post.matrix.rows.find(r => r.cdn === selectedMyHero) : null;
        const threats = post.highlights.threats || [];
        const combos = post.highlights.combos || [];
        const dominance = post.highlights.dominance || [];
        if (myHeroRow) {
            const roleTxt = ROMAN_NUMERALS[myHeroRow.role] || myHeroRow.role;
            const fullTitle = (currentLang === 'ru')
                ? `Персональный анализ: ${myHeroRow.name} (${rolePrefix}${roleTxt})`
                : `Personal Analysis: ${myHeroRow.name} (${rolePrefix}${roleTxt})`;
            if (cardTitleEl) {
                cardTitleEl.textContent = fullTitle;
                cardTitleEl.title = fullTitle;
            }
            if (calloutLeadEl) {
                calloutLeadEl.textContent = (currentLang === 'ru') ? 'Выбранный герой:' : 'Selected Hero:';
            }
            if (calloutDescEl) {
                const expWr = (myHeroRow.expected_wr !== undefined) ? myHeroRow.expected_wr : myHeroRow.avg_wr;
                calloutDescEl.textContent = (currentLang === 'ru')
                    ? `${myHeroRow.name} • Прогноз победы: ${expWr.toFixed(1)}%`
                    : `${myHeroRow.name} • Win prediction: ${expWr.toFixed(1)}%`;
            }
            const cells = [...(myHeroRow.cells || [])];
            const myCounters = cells.filter(c => c.delta >= 0.5).sort((a, b) => b.delta - a.delta);
            const myThreats = cells.filter(c => c.delta <= -0.5).sort((a, b) => a.delta - b.delta);
            const myCombos = combos.filter(c => c.hero1_cdn === selectedMyHero || c.hero2_cdn === selectedMyHero);
            const myStrItems = [];
            if (myCounters.length > 0) {
                const topCounter = myCounters[0];
                const sign = topCounter.delta > 0 ? '+' : '';
                myStrItems.push(`
                    <div class="insight-point">
                        <span class="insight-bullet bullet-pos">✔</span>
                        <span class="insight-text">${currentLang === 'ru' ? 'Контрпик:' : 'Counter:'} <strong>${topCounter.enemy_name}</strong> <span class="val-pos">${sign}${topCounter.delta.toFixed(1)}%</span></span>
                    </div>
                `);
            }
            if (myCombos.length > 0) {
                const bCombo = myCombos[0];
                const partner = (bCombo.hero1_cdn === selectedMyHero) ? bCombo.hero2_name : bCombo.hero1_name;
                myStrItems.push(`
                    <div class="insight-point">
                        <span class="insight-bullet bullet-pos">✔</span>
                        <span class="insight-text">${currentLang === 'ru' ? 'Связка:' : 'Combo:'} с <strong>${partner}</strong> <span class="val-pos">+${bCombo.synergy.toFixed(1)}%</span></span>
                    </div>
                `);
            } else if (myCounters.length > 1) {
                const sc = myCounters[1];
                const sSign = sc.delta > 0 ? '+' : '';
                myStrItems.push(`
                    <div class="insight-point">
                        <span class="insight-bullet bullet-pos">✔</span>
                        <span class="insight-text">${currentLang === 'ru' ? 'Плюс против:' : 'Good vs:'} <strong>${sc.enemy_name}</strong> <span class="val-pos">${sSign}${sc.delta.toFixed(1)}%</span></span>
                    </div>
                `);
            }
            if (myStrItems.length === 0) {
                myStrItems.push(`
                    <div class="insight-point">
                        <span class="insight-bullet bullet-neu">★</span>
                        <span class="insight-text">${currentLang === 'ru' ? 'Сбалансированный нейтральный пик' : 'Balanced neutral pick'}</span>
                    </div>
                `);
            }
            if (myStrEl) myStrEl.innerHTML = myStrItems.join('');
            const myRskItems = [];
            if (myThreats.length > 0) {
                const topThreat = myThreats[0];
                myRskItems.push(`
                    <div class="insight-point">
                        <span class="insight-bullet bullet-neg">⚠</span>
                        <span class="insight-text">${currentLang === 'ru' ? 'Вас контрит:' : 'Threat:'} <strong>${topThreat.enemy_name}</strong> <span class="val-neg">${topThreat.delta.toFixed(1)}%</span></span>
                    </div>
                `);
                if (myThreats.length > 1) {
                    const st = myThreats[1];
                    myRskItems.push(`
                        <div class="insight-point">
                            <span class="insight-bullet bullet-neg">⚠</span>
                            <span class="insight-text">${currentLang === 'ru' ? 'Опасен:' : 'Danger:'} <strong>${st.enemy_name}</strong> <span class="val-neg">${st.delta.toFixed(1)}%</span></span>
                        </div>
                    `);
                }
            } else {
                myRskItems.push(`
                    <div class="insight-point">
                        <span class="insight-bullet bullet-pos">✔</span>
                        <span class="insight-text">${currentLang === 'ru' ? 'Критических контрпиков нет' : 'No critical direct counters'}</span>
                    </div>
                `);
            }
            if (myRskEl) myRskEl.innerHTML = myRskItems.join('');
        } else {
            const fullTitle = (currentLang === 'ru') ? 'Общий анализ драфта: Выберите героя' : 'Draft Analysis: Select a hero';
            if (cardTitleEl) {
                cardTitleEl.textContent = fullTitle;
                cardTitleEl.title = fullTitle;
            }
            if (calloutLeadEl) {
                calloutLeadEl.textContent = (currentLang === 'ru') ? 'Личный герой:' : 'Personal Hero:';
            }
            if (calloutDescEl) {
                calloutDescEl.textContent = (currentLang === 'ru')
                    ? 'Кликните по своему герою в слотах драфта (или дабл-клик в сетке) для персональной сводки!'
                    : 'Click your hero in draft slots for personal summary!';
            }
            if (myStrEl) {
                myStrEl.innerHTML = `
                    <div class="insight-point">
                        <span class="insight-bullet bullet-neu">★</span>
                        <span class="insight-text">${currentLang === 'ru' ? 'Кликните своего героя в драфте' : 'Select your hero above'}</span>
                    </div>
                `;
            }
            if (myRskEl) {
                myRskEl.innerHTML = `
                    <div class="insight-point">
                        <span class="insight-bullet bullet-neu">★</span>
                        <span class="insight-text">${currentLang === 'ru' ? 'Определите личные угрозы' : 'Identify personal threats'}</span>
                    </div>
                `;
            }
        }
        const teamStrItems = [];
        if (combos.length > 0) {
            const cb = combos[0];
            teamStrItems.push(`
                <div class="insight-point">
                    <span class="insight-bullet bullet-pos">✔</span>
                    <span class="insight-text">${currentLang === 'ru' ? 'Связка:' : 'Combo:'} <strong>${cb.hero1_name}</strong> + <strong>${cb.hero2_name}</strong> <span class="val-pos">+${cb.synergy.toFixed(1)}%</span></span>
                </div>
            `);
        }
        if (dominance.length > 0) {
            const dom = dominance[0];
            teamStrItems.push(`
                <div class="insight-point">
                    <span class="insight-bullet bullet-pos">✔</span>
                    <span class="insight-text">${currentLang === 'ru' ? 'Перевес:' : 'Advantage:'} <strong>${dom.ally_name}</strong> закрывает <strong>${dom.enemy_name}</strong> <span class="val-pos">+${dom.delta.toFixed(1)}%</span></span>
                </div>
            `);
        }
        if (teamStrItems.length === 0) {
            teamStrItems.push(`
                <div class="insight-point">
                    <span class="insight-bullet bullet-neu">★</span>
                    <span class="insight-text">${currentLang === 'ru' ? 'Сбалансированный командный потенциал' : 'Balanced team potential'}</span>
                </div>
            `);
        }
        if (teamStrEl) teamStrEl.innerHTML = teamStrItems.join('');
        const teamRskItems = [];
        if (threats.length > 0) {
            threats.slice(0, 2).forEach(th => {
                const deltaVal = (th.delta !== undefined) ? th.delta : -th.severity;
                const sign = deltaVal > 0 ? '+' : '';
                const vsText = th.ally_name ? ` ${currentLang === 'ru' ? 'против' : 'vs'} ${th.ally_name}` : '';
                teamRskItems.push(`
                    <div class="insight-point">
                        <span class="insight-bullet bullet-neg">⚠</span>
                        <span class="insight-text">${currentLang === 'ru' ? 'Угроза:' : 'Threat:'} <strong>${th.enemy_name}</strong>${vsText} <span class="val-neg">(${sign}${deltaVal.toFixed(1)}%)</span></span>
                    </div>
                `);
            });
        }
        if (teamRskItems.length === 0) {
            teamRskItems.push(`
                <div class="insight-point">
                    <span class="insight-bullet bullet-pos">✔</span>
                    <span class="insight-text">${currentLang === 'ru' ? 'Критических угроз для команды не выявлено' : 'No critical team threats'}</span>
                </div>
            `);
        }
        if (teamRskEl) teamRskEl.innerHTML = teamRskItems.join('');
        const threatsEl = document.getElementById('hl-threats-list');
        if (threatsEl) {
            const threats = post.highlights.threats || [];
            if (threats.length === 0) {
                threatsEl.innerHTML = `<span class="hl-empty-text">${currentLang === 'ru' ? 'Критических угроз для команды не выявлено' : 'No critical team threats detected'}</span>`;
            } else {
                threatsEl.innerHTML = threats.map(t => `
                    <div class="hl-item">
                        <div class="hl-item-left">
                            <img src="/assets/panorama/images/heroes/icons/npc_dota_hero_${t.enemy_cdn}_png.png" class="hl-avatar" title="${t.enemy_name}" onerror="this.src=''">
                            <span class="hl-hero-name">${t.enemy_name}</span>
                            <span class="hl-action-label threat">vs</span>
                            <img src="/assets/panorama/images/heroes/icons/npc_dota_hero_${t.ally_cdn}_png.png" class="hl-avatar" title="${t.ally_name}" onerror="this.src=''">
                            <span class="hl-hero-name">${t.ally_name}</span>
                        </div>
                        <span class="hl-delta-badge threat">${t.delta.toFixed(1)}%</span>
                    </div>
                `).join('');
            }
        }
        const domEl = document.getElementById('hl-dominance-list');
        if (domEl) {
            const doms = post.highlights.dominance || [];
            if (doms.length === 0) {
                domEl.innerHTML = `<span class="hl-empty-text">${currentLang === 'ru' ? 'Явных контр-пиков пока нет' : 'No strong counter-picks yet'}</span>`;
            } else {
                domEl.innerHTML = doms.map(d => `
                    <div class="hl-item">
                        <div class="hl-item-left">
                            <img src="/assets/panorama/images/heroes/icons/npc_dota_hero_${d.ally_cdn}_png.png" class="hl-avatar" title="${d.ally_name}" onerror="this.src=''">
                            <span class="hl-hero-name">${d.ally_name}</span>
                            <span class="hl-action-label">${currentLang === 'ru' ? 'контрит' : 'counters'}</span>
                            <img src="/assets/panorama/images/heroes/icons/npc_dota_hero_${d.enemy_cdn}_png.png" class="hl-avatar" title="${d.enemy_name}" onerror="this.src=''">
                            <span class="hl-hero-name">${d.enemy_name}</span>
                        </div>
                        <span class="hl-delta-badge pos">+${d.delta.toFixed(1)}%</span>
                    </div>
                `).join('');
            }
        }
        const combosEl = document.getElementById('hl-combos-list');
        if (combosEl) {
            const combos = post.highlights.combos || [];
            if (combos.length === 0) {
                combosEl.innerHTML = `<span class="hl-empty-text">${currentLang === 'ru' ? 'Стандартные синергии' : 'Standard team synergies'}</span>`;
            } else {
                combosEl.innerHTML = combos.map(c => `
                    <div class="hl-item">
                        <div class="hl-item-left">
                            <img src="/assets/panorama/images/heroes/icons/npc_dota_hero_${c.hero1_cdn}_png.png" class="hl-avatar" title="${c.hero1_name}" onerror="this.src=''">
                            <span class="hl-hero-name">${c.hero1_name}</span>
                            <span class="hl-conn">+</span>
                            <img src="/assets/panorama/images/heroes/icons/npc_dota_hero_${c.hero2_cdn}_png.png" class="hl-avatar" title="${c.hero2_name}" onerror="this.src=''">
                            <span class="hl-hero-name">${c.hero2_name}</span>
                        </div>
                        <span class="hl-delta-badge combo">+${c.synergy.toFixed(1)}%</span>
                    </div>
                `).join('');
            }
        }
    }
    function renderLaning(post) {
        if (!post || !post.laning) return;
        const laning = post.laning;
        const userTeam = post.user_team || 'radiant';
        const radRoles = post.rad_roles || {};
        const direRoles = post.dire_roles || {};
        const heroNames = {};
        if (post.matrix) {
            (post.matrix.rows || []).forEach(r => { heroNames[r.cdn] = r.name; });
            (post.matrix.enemies || []).forEach(e => { heroNames[e.cdn] = e.name; });
        }
        ['top', 'mid', 'bot'].forEach(k => {
            const l = laning[k];
            if (!l) return;
            const radContainer = document.getElementById(`map-${k}-rad`);
            const direContainer = document.getElementById(`map-${k}-dire`);
            const badgeEl = document.getElementById(`map-${k}-badge`);
            if (radContainer) {
                radContainer.innerHTML = (l.rad_heroes || []).map(cdn => {
                    const role = radRoles[cdn] || '';
                    const isAlly = (userTeam === 'radiant');
                    const isMy = (selectedMyHero === cdn);
                    const isPending = (pendingSwap && pendingSwap.cdn === cdn);
                    const hName = heroNames[cdn] || cdn;
                    const star = isMy ? ' ⭐ ВЫ' : '';
                    return `
                        <div class="map-hero-circle ${isAlly ? 'ally' : 'enemy'} ${isMy ? 'is-my-hero' : ''} ${isPending ? 'swap-pending' : ''}" 
                             data-hero="${cdn}" data-role="${role}" data-team="radiant" 
                             title="${hName} (Pos ${role})${star} - ${currentLang === 'ru' ? 'Кликните для обмена' : 'Click to swap'}">
                            <img src="/assets/panorama/images/heroes/icons/npc_dota_hero_${cdn}_png.png" onerror="this.src=''">
                            ${role ? `<span class="map-pos-tag">${role}</span>` : ''}
                        </div>
                    `;
                }).join('');
            }
            if (direContainer) {
                direContainer.innerHTML = (l.dire_heroes || []).map(cdn => {
                    const role = direRoles[cdn] || '';
                    const isAlly = (userTeam === 'dire');
                    const isMy = (selectedMyHero === cdn);
                    const isPending = (pendingSwap && pendingSwap.cdn === cdn);
                    const hName = heroNames[cdn] || cdn;
                    const star = isMy ? ' ⭐ ВЫ' : '';
                    return `
                        <div class="map-hero-circle ${isAlly ? 'ally' : 'enemy'} ${isMy ? 'is-my-hero' : ''} ${isPending ? 'swap-pending' : ''}" 
                             data-hero="${cdn}" data-role="${role}" data-team="dire" 
                             title="${hName} (Pos ${role})${star} - ${currentLang === 'ru' ? 'Кликните для обмена' : 'Click to swap'}">
                            <img src="/assets/panorama/images/heroes/icons/npc_dota_hero_${cdn}_png.png" onerror="this.src=''">
                            ${role ? `<span class="map-pos-tag">${role}</span>` : ''}
                        </div>
                    `;
                }).join('');
            }
            if (badgeEl) {
                const laneNamesRu = { top: 'ТОП', mid: 'МИД', bot: 'БОТ' };
                const lTitle = currentLang === 'ru' ? laneNamesRu[k] : k.toUpperCase();
                if (l.winner === 'Radiant') {
                    badgeEl.className = 'map-clash-badge rad-win';
                    badgeEl.textContent = `${lTitle} RAD +${l.val.toFixed(1)}%`;
                } else if (l.winner === 'Dire') {
                    badgeEl.className = 'map-clash-badge dire-win';
                    badgeEl.textContent = `${lTitle} DIRE +${l.val.toFixed(1)}%`;
                } else {
                    badgeEl.className = 'map-clash-badge even-clash';
                    badgeEl.textContent = `${lTitle} 50/50`;
                }
            }
        });
        const mapFrame = document.getElementById('dota-minimap-frame');
        if (mapFrame && !mapFrame.dataset.listener) {
            mapFrame.dataset.listener = 'true';
            mapFrame.addEventListener('click', (e) => {
                const circle = e.target.closest('.map-hero-circle');
                if (circle) {
                    const h = circle.dataset.hero;
                    const role = parseInt(circle.dataset.role, 10);
                    const team = circle.dataset.team;
                    if (h) handleSwapSelection(team, h, role);
                }
            });
            mapFrame.addEventListener('dblclick', (e) => {
                const circle = e.target.closest('.map-hero-circle');
                if (circle && circle.dataset.team === userTeam) {
                    clearPendingSwap();
                    if (circle.dataset.hero) setMyHero(circle.dataset.hero, true);
                }
            });
        }
        const duelsContainer = document.getElementById('role-duels-list');
        const duelsCard = document.getElementById('role-duels-card');
        if (duelsContainer && duelsCard) {
            const duels = post.role_duels || [];
            if (duels.length === 0) {
                duelsCard.classList.add('hidden');
            } else {
                duelsCard.classList.remove('hidden');
                const allySideClass = (userTeam === 'dire') ? 'side-dire' : 'side-rad';
                const enemySideClass = (userTeam === 'dire') ? 'side-rad' : 'side-dire';
                duelsContainer.innerHTML = duels.map(d => {
                    const roleTitle = currentLang === 'ru' ? d.role_title_ru : d.role_title_en;
                    const sign = d.delta > 0 ? '+' : '';
                    let scoreClass = 'even-duel';
                    if (d.winner === 'ally') scoreClass = 'ally-win';
                    else if (d.winner === 'enemy') scoreClass = 'enemy-win';
                    const isMy = (selectedMyHero === d.ally_cdn);
                    const myBadge = isMy ? ` ★ ${currentLang === 'ru' ? 'ВЫ' : 'YOU'}` : '';
                    const tip = currentLang === 'ru'
                        ? `${d.ally_name} vs ${d.enemy_name}: ${sign}${d.delta.toFixed(1)}% (${d.ally_wr}% винрейт, ${d.matches} матчей)`
                        : `${d.ally_name} vs ${d.enemy_name}: ${sign}${d.delta.toFixed(1)}% (${d.ally_wr}% winrate, ${d.matches} matches)`;
                    return `
                        <div class="role-duel-card ${isMy ? 'my-role-duel' : ''}" title="${tip}">
                            <div class="role-duel-top">
                                <span class="role-duel-badge">${roleTitle}${myBadge}</span>
                            </div>
                            <div class="role-duel-matchup">
                                <div class="role-duel-hero ally">
                                    <img src="/assets/panorama/images/heroes/icons/npc_dota_hero_${d.ally_cdn}_png.png" class="role-duel-avatar ${allySideClass} ${isMy ? 'is-my-hero' : ''}" onerror="this.src=''">
                                    <span class="role-duel-name ${isMy ? 'is-my-hero' : ''}">${d.ally_name}</span>
                                </div>
                                <div class="role-duel-vs">
                                    <span class="role-duel-score ${scoreClass}">${sign}${d.delta.toFixed(1)}%</span>
                                </div>
                                <div class="role-duel-hero enemy">
                                    <span class="role-duel-name">${d.enemy_name}</span>
                                    <img src="/assets/panorama/images/heroes/icons/npc_dota_hero_${d.enemy_cdn}_png.png" class="role-duel-avatar ${enemySideClass}" onerror="this.src=''">
                                </div>
                            </div>
                        </div>
                    `;
                }).join('');
            }
        }
    }
    function updateUI(data) {
        if (!data || isUpdatingUI) return;
        isUpdatingUI = true;
        try {
            currentState = data;
            hideLoader();
            const isLocked = !!(data.locked || (data.state && data.state.locked));
            const lockOverlay = document.getElementById('app-lock-overlay');
            if (isLocked) {
                if (lockOverlay) {
                    lockOverlay.classList.remove('hidden');
                    const lockInfo = data.lock_info || (data.state && data.state.lock_info) || {};
                    if (lockInfo.title) {
                        const titleEl = document.getElementById('lock-title');
                        if (titleEl) titleEl.textContent = lockInfo.title;
                    }
                    if (lockInfo.message) {
                        const msgEl = document.getElementById('lock-message');
                        if (msgEl) msgEl.textContent = lockInfo.message;
                    }
                }
                const heroList = document.getElementById('hero-list');
                if (heroList) heroList.innerHTML = '';
                const matrixGrid = document.getElementById('matrix-grid');
                if (matrixGrid) matrixGrid.innerHTML = '';
                const insightTeamCombos = document.getElementById('insight-team-combos');
                if (insightTeamCombos) insightTeamCombos.innerHTML = '';
                const insightTeamRisks = document.getElementById('insight-team-risks');
                if (insightTeamRisks) insightTeamRisks.innerHTML = '';
                if (tableBody) tableBody.innerHTML = '';
                const slots = document.querySelectorAll('.slot');
                slots.forEach(s => {
                    s.innerHTML = '';
                    s.classList.remove('filled', 'active');
                });
                isUpdatingUI = false;
                return;
            } else {
                if (lockOverlay && !lockOverlay.classList.contains('hidden')) {
                    lockOverlay.classList.add('hidden');
                }
            }
            if (!window.langInitialized && data.settings && data.settings.lang) {
                window.langInitialized = true;
                setLanguage(data.settings.lang, false);
            }
        if (data.state.sync_status !== lastSyncStatus) {
            lastSyncStatus = data.state.sync_status;
            if (data.state.sync_status === "OK") {
                const count = data.state.player_count || 0;
                const txt = currentLang === 'ru' ? `Stratz: ${count} матчей` : `Stratz: ${count} matches`;
                syncStatus.textContent = txt;
                syncStatus.title = txt;
                syncStatus.className = "status-badge ok";
                syncStatus.style.display = "inline-flex";
                document.querySelector(".header").classList.add("sync-active");
                clearTimeout(syncHideTimeout);
                syncHideTimeout = setTimeout(() => {
                    syncStatus.style.display = "none";
                if (document.getElementById("dataset-status").style.display === "none") document.querySelector(".header").classList.remove("sync-active");
                }, 3500);
            } else if (data.state.sync_status === "Syncing...") {
                const txt = currentLang === 'ru' ? "Синхронизация..." : "Syncing...";
                syncStatus.textContent = txt;
                syncStatus.title = txt;
                syncStatus.className = "status-badge";
                syncStatus.style.display = "inline-flex";
                document.querySelector(".header").classList.add("sync-active");
                clearTimeout(syncHideTimeout);
            } else if (data.state.sync_status === "Error" || data.state.sync_status === "Server error") {
                const txt = currentLang === 'ru' ? "Ошибка Stratz" : "Stratz Error";
                syncStatus.textContent = txt;
                syncStatus.title = currentLang === 'ru' ? "Не удалось загрузить данные со Stratz API (проверьте ID или ключ)" : "Failed to load stats from Stratz API (check ID or API key)";
                syncStatus.className = "status-badge error";
                syncStatus.style.display = "inline-flex";
                document.querySelector(".header").classList.add("sync-active");
                clearTimeout(syncHideTimeout);
                syncHideTimeout = setTimeout(() => {
                    syncStatus.style.display = "none";
                if (document.getElementById("dataset-status").style.display === "none") document.querySelector(".header").classList.remove("sync-active");
                }, 4000);
            } else if (data.state.sync_status && data.state.sync_status.startsWith("Wait")) {
                const secs = data.state.sync_status.replace(/\D/g, '');
                const txt = currentLang === 'ru' ? `Подождите ${secs}с` : `Wait ${secs}s`;
                syncStatus.textContent = txt;
                syncStatus.title = currentLang === 'ru' ? `Подождите ${secs} сек перед повторной синхронизацией` : `Please wait ${secs}s before syncing again`;
                syncStatus.className = "status-badge warning";
                syncStatus.style.display = "inline-flex";
                document.querySelector(".header").classList.add("sync-active");
                clearTimeout(syncHideTimeout);
            } else {
                syncStatus.style.display = "none";
                if (document.getElementById("dataset-status").style.display === "none") document.querySelector(".header").classList.remove("sync-active");
                clearTimeout(syncHideTimeout);
            }
        }
        const datasetStatus = document.getElementById('dataset-status');
        if (data.state.dataset_status && data.state.dataset_status !== "Idle" && data.state.dataset_status !== "Updated") {
            datasetStatus.textContent = data.state.dataset_status;
            datasetStatus.style.display = "inline-flex";
                document.querySelector(".header").classList.add("sync-active");
        } else {
            datasetStatus.style.display = "none";
                if (document.getElementById("sync-status").style.display === "none") document.querySelector(".header").classList.remove("sync-active");
        }
        const evalBadge = document.getElementById('draft-evaluation');
        const evalPanel = document.getElementById('draft-eval-panel');
        const headerSubtitle = document.getElementById('header-subtitle');
        const radScoresContainer = document.getElementById('rad-hero-scores');
        const direScoresContainer = document.getElementById('dire-hero-scores');
        const hasAnyRad = data.state.radiant && data.state.radiant.some(h => !!h);
        const hasAnyDire = data.state.dire && data.state.dire.some(h => !!h);
        const hasAnyHero = hasAnyRad || hasAnyDire;
        if (hasAnyHero && data.state.draft_active && data.state.evaluation) {
            const ev = data.state.evaluation;
            if (ev.team === "Radiant") {
                headerSubtitle.textContent = `RADIANT +${ev.advantage.toFixed(1)}%`;
                headerSubtitle.className = 'header-subtitle eval-rad';
            } else if (ev.team === "Dire") {
                headerSubtitle.textContent = `DIRE +${ev.advantage.toFixed(1)}%`;
                headerSubtitle.className = 'header-subtitle eval-dire';
            } else {
                headerSubtitle.textContent = `EVEN ~${ev.advantage.toFixed(1)}%`;
                headerSubtitle.className = 'header-subtitle eval-even';
            }
            const radAvgTxt = ev.rad_val !== undefined ? `${ev.rad_val >= 0 ? '+' : ''}${ev.rad_val.toFixed(1)}%` : '';
            const direAvgTxt = ev.dire_val !== undefined ? `${ev.dire_val >= 0 ? '+' : ''}${ev.dire_val.toFixed(1)}%` : '';
            headerSubtitle.title = currentLang === 'ru'
                ? (ev.team !== 'Even' 
                    ? `Перевес ${ev.team === 'Radiant' ? 'Света' : 'Тьмы'}: +${ev.advantage.toFixed(1)}% (разница средних по командам: ${radAvgTxt} vs ${direAvgTxt})`
                    : 'Силы команд равны (разница менее 0.15%)')
                : (ev.team !== 'Even'
                    ? `${ev.team} advantage: +${ev.advantage.toFixed(1)}% (${radAvgTxt} vs ${direAvgTxt})`
                    : 'Even match');
            evalPanel.classList.remove('hidden');
            const currentCalc = getSegmentedValue('ctrl-calc') || (ev.calc_mode || 'delta');
            function getHeroScoreTooltip(s) {
                const sign = s > 0 ? '+' : '';
                const deltaTxt = `${sign}${s.toFixed(1)}%`;
                if (currentCalc === 'meta') {
                    const wr = 50.0 + s;
                    return currentLang === 'ru'
                        ? `Винрейт в мете: ${wr.toFixed(1)}% (${deltaTxt} от 50%)`
                        : `Meta winrate: ${wr.toFixed(1)}% (${deltaTxt} vs 50%)`;
                } else if (currentCalc === 'delta') {
                    return currentLang === 'ru'
                        ? `Матчап-бонус: ${deltaTxt} (против вражеской команды)`
                        : `Matchup bonus: ${deltaTxt} (vs enemy team)`;
                } else {
                    return currentLang === 'ru'
                        ? `Персональный рейтинг: ${deltaTxt} (Драфт + Опыт)`
                        : `Personal rating: ${deltaTxt} (Draft + Mastery)`;
                }
            }
            const radScoresHtml = [];
            for (let i = 0; i < 5; i++) {
                const hero = (data.state.radiant && data.state.radiant[i]) || null;
                const slotFilled = hero && radSlots[i] && radSlots[i].classList.contains('filled');
                if (slotFilled && ev.rad_heroes && ev.rad_heroes[hero] !== undefined) {
                    const s = ev.rad_heroes[hero];
                    const sign = s > 0 ? '+' : '';
                    const cls = `eval-hero-score ${s > 0.5 ? 'val-pos' : (s < -0.5 ? 'val-neg' : 'val-neu')}`;
                    const valTxt = `${sign}${s.toFixed(1)}%`;
                    radScoresHtml.push(`<div class="${cls}">${valTxt}</div>`);
                } else {
                    radScoresHtml.push(`<div class="eval-hero-score empty"></div>`);
                }
            }
            const newRadHtml = radScoresHtml.join('');
            if (radScoresContainer && radScoresContainer.innerHTML !== newRadHtml) {
                radScoresContainer.innerHTML = newRadHtml;
            }
            const direScoresHtml = [];
            for (let i = 0; i < 5; i++) {
                const hero = (data.state.dire && data.state.dire[i]) || null;
                const slotFilled = hero && direSlots[i] && direSlots[i].classList.contains('filled');
                if (slotFilled && ev.dire_heroes && ev.dire_heroes[hero] !== undefined) {
                    const s = ev.dire_heroes[hero];
                    const sign = s > 0 ? '+' : '';
                    const cls = `eval-hero-score ${s > 0.5 ? 'val-pos' : (s < -0.5 ? 'val-neg' : 'val-neu')}`;
                    const valTxt = `${sign}${s.toFixed(1)}%`;
                    direScoresHtml.push(`<div class="${cls}">${valTxt}</div>`);
                } else {
                    direScoresHtml.push(`<div class="eval-hero-score empty"></div>`);
                }
            }
            const newDireHtml = direScoresHtml.join('');
            if (direScoresContainer && direScoresContainer.innerHTML !== newDireHtml) {
                direScoresContainer.innerHTML = newDireHtml;
            }
        } else {
            if (evalBadge) evalBadge.classList.add('hidden');
            if (evalPanel) evalPanel.classList.add('hidden');
            if (radScoresContainer) radScoresContainer.innerHTML = '';
            if (direScoresContainer) direScoresContainer.innerHTML = '';
            if (headerSubtitle) {
                headerSubtitle.className = 'header-subtitle';
                headerSubtitle.textContent = currentLang === 'ru' ? 'AI АНАЛИЗ DOTA 2' : 'AI DRAFT ANALYSIS';
                headerSubtitle.removeAttribute('title');
            }
        }
        if (data.settings && data.settings.team) {
            const currentTeam = getSegmentedValue('ctrl-team');
            if (currentTeam !== data.settings.team) {
                setSegmentedValue('ctrl-team', data.settings.team);
            }
            document.querySelectorAll('.matrix-side-btn').forEach(b => {
                b.classList.toggle('active', b.dataset.side === data.settings.team);
            });
        }
        if (selectedMyHero && data.state) {
            const currentTeam = (data.settings && data.settings.team) || getSegmentedValue('ctrl-team') || 'radiant';
            const teamHeroes = (currentTeam === 'dire') 
                ? (data.state.dire || []) 
                : (data.state.radiant || []);
            if (teamHeroes.length > 0 && !teamHeroes.includes(selectedMyHero)) {
                selectedMyHero = null;
                localStorage.removeItem('impulse_my_hero');
                lastPostAnalysisSignature = "";
            }
        }
        if (!window.settingsLoaded && data.settings) {
            steamInput.value = data.settings.steam_id || "";
            setSegmentedValue('ctrl-team', data.settings.team || "radiant");
            setSegmentedValue('ctrl-role', data.settings.role || "all");
            if (modeSelect) {
                modeSelect.value = data.settings.mode || "1m";
            }
            if (rankSelect && data.settings.rank) {
                rankSelect.value = data.settings.rank;
            }
            if (hotkeySelect && data.settings.hotkey) {
                hotkeySelect.value = data.settings.hotkey;
            }
            if (data.settings.opacity) {
                setSegmentedValue('ctrl-opacity', String(data.settings.opacity));
            }
            if (data.settings.perf_mode) {
                setSegmentedValue('ctrl-perf', data.settings.perf_mode);
            }
            if (resolutionSelect && data.settings.resolution) {
                resolutionSelect.value = data.settings.resolution;
            }
            if (data.settings.grid_highlight !== undefined) {
                setSegmentedValue('ctrl-grid-highlight', data.settings.grid_highlight ? "true" : "false");
            }
            setSegmentedValue('ctrl-calc', data.settings.calc || "meta");
            if (data.settings.strictness) setSegmentedValue('ctrl-strictness', data.settings.strictness);
            if (data.settings.popularity) setSegmentedValue('ctrl-popularity', data.settings.popularity);
            if (data.settings.decay !== undefined) setSegmentedValue('ctrl-decay', data.settings.decay ? "true" : "false");
            if (data.settings.role_transfer_enabled !== undefined) setSegmentedValue('ctrl-role-transfer', data.settings.role_transfer_enabled ? "true" : "false");
            if (data.settings.eval_method) setSegmentedValue('ctrl-eval-method', data.settings.eval_method);
            const calcMode = data.settings.calc || "meta";
            document.querySelectorAll('.personal-only').forEach(el => {
                el.style.display = (calcMode === 'smart') ? 'block' : 'none';
            });
            window.settingsLoaded = true;
        }
        const smartBtn = document.querySelector('button[data-val="smart"]');
        if (!data.settings.steam_id || data.settings.steam_id.trim() === "") {
            smartBtn.disabled = true;
            smartBtn.style.opacity = '0.3';
            smartBtn.style.cursor = 'not-allowed';
            if (getSegmentedValue('ctrl-calc') === 'smart') {
                setSegmentedValue('ctrl-calc', 'delta');
                updateSettings(); // fallback trigger
            }
        } else {
            smartBtn.disabled = false;
            smartBtn.style.opacity = '1';
            smartBtn.style.cursor = 'pointer';
        }
        const currentSide = (data.settings && data.settings.team) || 'radiant';
        renderSlots(radSlots, data.state.radiant, currentSide === 'radiant');
        renderSlots(direSlots, data.state.dire, currentSide === 'dire');
        updateLiveIndicator(data);
        const calibDot = document.getElementById('calib-status-dot');
        const calibText = document.getElementById('calib-status-text');
        if (calibDot && calibText && data.state) {
            const status = data.state.calibration_status || "ok";
            const msg = data.state.calibration_message || (currentLang === 'ru' ? "Готов" : "Ready");
            calibText.textContent = (currentLang === 'ru' ? "Калибровка: " : "Calibration: ") + msg;
            if (status === 'warning') {
                calibDot.style.background = '#ff8c00';
            } else if (status === 'error') {
                calibDot.style.background = '#ff4747';
            } else {
                calibDot.style.background = '#00e5ff';
            }
        }
        if (data.state.num_picked === 10 && !userManuallySelectedView && currentView === 'draft') {
            switchView('matrix', false);
        } else if (data.state.num_picked === 0 && !userManuallySelectedView && currentView !== 'draft') {
            switchView('draft', false);
        }
        const calcMode = getSegmentedValue('ctrl-calc');
        const customRolesSig = JSON.stringify((data.state.post_analysis && data.state.post_analysis.custom_roles) || {});
        const pendingSwapSig = pendingSwap ? `${pendingSwap.team}:${pendingSwap.cdn}` : 'none';
        const postSig = `${(data.settings && data.settings.team) || 'radiant'}|${currentLang}|${selectedMyHero}|${(data.state.radiant || []).join(',')}|${(data.state.dire || []).join(',')}|${data.state.num_picked}|${calcMode}|${customRolesSig}|${pendingSwapSig}`;
        if (postSig !== lastPostAnalysisSignature) {
            lastPostAnalysisSignature = postSig;
            if (data.state.post_analysis) {
                renderMatchupMatrix(data.state.post_analysis);
                renderHighlights(data.state.post_analysis);
                renderLaning(data.state.post_analysis);
            } else {
                renderDraftSummaryBanner(null);
                const matrixTable = document.getElementById('matrix-table');
                if (matrixTable && (!data.state.num_picked || data.state.num_picked === 0)) {
                    matrixTable.innerHTML = `<tr><td style="padding:40px 20px; text-align:center; color:#6b8a8f; font-size:12px;">${currentLang === 'ru' ? 'Ожидание пиков обеих команд (начните драфт)...' : 'Awaiting team picks (start draft)...'}</td></tr>`;
                }
            }
        }
        const table = document.querySelector('.recs-table');
        if (calcMode === 'smart') {
            table.classList.add('mode-smart');
        } else {
            table.classList.remove('mode-smart');
        }
        const recs = data.state.recs || [];
        const currentPeriodMode = (modeSelect ? modeSelect.value : '') || (data.settings && data.settings.mode) || '1m';
        const dsStatus = (data.state && data.state.dataset_status) || '';
        const recsSignature = calcMode + '|' + currentPeriodMode + '|' + currentLang + '|' + dsStatus + '|' + recs.map(r => `${r.cdnName}:${r.adv}:${r.p_matches || 0}:${r.p_winrate || 0}`).join(',');
        if (recsSignature !== lastRecsSignature) {
            lastRecsSignature = recsSignature;
            tableBody.innerHTML = '';
            if (recs.length > 0) {
                recs.forEach(r => {
                    const tr = document.createElement('tr');
                    tr.style.userSelect = 'none';
                    const advHTML = calcMode === 'delta' ? formatDelta(r.adv) : formatWinrate(r.adv);
                    let matchCountCol = `<span style="color:#6b8a8f">-</span>`;
                    let playerWrCol = `<span style="color:#6b8a8f">-</span>`;
                    if (r.p_matches > 0) {
                        matchCountCol = `<span style="color:#6b8a8f; font-size:11px;">${r.p_matches}</span>`;
                        playerWrCol = formatWinrate(r.p_winrate);
                    }
                    tr.innerHTML = `
                        <td class="col-hero">
                            <div class="hero-cell">
                                <img src="/assets/panorama/images/heroes/icons/npc_dota_hero_${r.cdnName}_png.png" class="hero-icon" onerror="this.src=''">
                                <span>${r.name}</span>
                            </div>
                        </td>
                        <td class="col-meta">${formatWinrate(r.base_wr)}</td>
                        <td>${formatDelta(r.synergy)}</td>
                        <td>${formatDelta(r.counter)}</td>
                        <td class="smart-col">${matchCountCol}</td>
                        <td class="smart-col">${playerWrCol}</td>
                        <td><strong>${advHTML}</strong></td>
                    `;
                    tr.setAttribute('data-hero', r.cdnName);
                    tableBody.appendChild(tr);
                });
            } else {
                const colspan = calcMode === 'smart' ? 7 : 5;
                let noDataText = (translations[currentLang] && translations[currentLang].no_data) || 'No data available';
                let isSyncing = data.state && data.state.dataset_status && data.state.dataset_status !== "Idle" && data.state.dataset_status !== "Updated";
                if (isSyncing) {
                    noDataText = currentLang === 'ru' ? `Синхронизация базы данных с сервера (${data.state.dataset_status})...` : `Syncing meta dataset (${data.state.dataset_status})...`;
                    tableBody.innerHTML = `<tr><td colspan="${colspan}" style="padding: 35px 20px; text-align: center; color: #00e5ff; font-size: 11px;"><span style="display:inline-block; animation: pulse 1s infinite; margin-right:6px;">⚡</span>${noDataText}</td></tr>`;
                } else {
                    tableBody.innerHTML = `<tr><td colspan="${colspan}" style="padding: 35px 20px; text-align: center; color: #6b8a8f; font-size: 11px;">${noDataText}</td></tr>`;
                }
            }
        }
    } finally {
        applySwapHighlights();
        isUpdatingUI = false;
    }
}
    if (tableBody) {
        tableBody.addEventListener('mouseover', (e) => {
            const heroCell = e.target.closest('.col-hero');
            if (heroCell) {
                const tr = heroCell.closest('tr[data-hero]');
                if (tr) {
                    const hero = tr.getAttribute('data-hero');
                    if (hero) {
                        requestHeroHighlight(hero);
                        return;
                    }
                }
            }
            requestHeroHighlight(null);
        });
        tableBody.addEventListener('mouseleave', () => {
            requestHeroHighlight(null);
        });
    }
    document.addEventListener('mouseleave', () => {
        clearHeroHighlightImmediately();
    });
    function schedulePoll() {
        let delay = 600;
        if (currentState && currentState.settings) {
            const perf = currentState.settings.perf_mode;
            if (perf === 'eco') delay = 2000;
            else if (perf === 'high') delay = 100; // 10 updates per second for instant reaction!
        }
        setTimeout(() => {
            fetch('/api/state')
                .then(r => r.json())
                .then(data => {
                    updateUI(data);
                    schedulePoll();
                })
                .catch(err => {
                    console.error(err);
                    schedulePoll();
                });
        }, delay);
    }
    schedulePoll();
});