"""
Avatar Control Hub - Centro de Control Interactivo y Profesional del Avatar
===========================================================================
Panel flotante glassmórfico de alta fidelidad para el control completo del Avatar:
- Sistema de pestañas organizadas (Modelo, Postura & Gestos, Props & Personalidad)
- Altura auto-adaptativa con QScrollArea para evitar desbordes en cualquier resolución
- Disparador visual de gestos de alta fidelidad sin textos truncados
- Mapeo universal de props y accesorios en tiempo real
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QMenu, QScrollArea, QFileDialog, QTabBar
)

from memory.config_manager import (
    get_live2d_skin, save_live2d_skin,
    get_edith_autonomy_enabled, save_edith_autonomy_enabled,
    get_edith_spontaneity_level, save_edith_spontaneity_level,
    get_auto_animations_enabled, save_auto_animations_enabled,
    get_hud_style, save_hud_style,
    get_vrm_model, save_vrm_model,
)
from core.live2d.skin_manager import discover_live2d_skins, open_skins_folder
from core.vrm.vrm_widget import discover_vrm_models

def open_vrm_folder():
    p = os.path.abspath(os.path.join(os.path.dirname(__file__), "vrm", "models"))
    os.makedirs(p, exist_ok=True)
    if os.name == 'nt':
        os.startfile(p)

if TYPE_CHECKING:
    from ui import MainWindow


def _rgba(hex_color: str, alpha: float) -> str:
    c = QColor(hex_color)
    return f"rgba({c.red()},{c.green()},{c.blue()},{alpha:.3f})"


class AvatarControlDrawer(QWidget):
    """Editorial Studio control hub for the Live2D / 2D / VRM 3D Avatar."""

    _WIDTH = 368

    def __init__(self, main_window: "MainWindow", parent: QWidget | None = None):
        super().__init__(parent or main_window.centralWidget())
        self.main_window = main_window
        self.setObjectName("AvatarControlDrawer")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedWidth(self._WIDTH)
        self.hide()

        # Active props memory
        self._prop_rings = False
        self._active_game_mode = "idle"

        self._build_ui()

    def _build_ui(self):
        from ui import C, UI_FONT
        self._C = C
        self._UI_FONT = UI_FONT

        self.setStyleSheet(f"""
            QWidget#AvatarControlDrawer {{
                background: {_rgba(C.PANEL, 0.97)};
                border: 1px solid {C.BORDER_B};
                border-radius: 14px;
            }}
            QScrollArea {{
                background: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                border: none;
                background: transparent;
                width: 4px;
                margin: 4px 0;
            }}
            QScrollBar::handle:vertical {{
                background: {_rgba(C.PRI, 0.40)};
                border-radius: 2px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        root_lay = QVBoxLayout(self)
        root_lay.setContentsMargins(12, 12, 12, 12)
        root_lay.setSpacing(8)

        # ── 1. HEADER MODERNO ──────────────────────────────────────────────
        hdr = QHBoxLayout()
        hdr.setSpacing(8)

        icon_lbl = QLabel("🎭")
        icon_lbl.setFont(QFont(self._UI_FONT, 15))
        icon_lbl.setStyleSheet("background: transparent;")
        hdr.addWidget(icon_lbl)

        title_box = QVBoxLayout()
        title_box.setSpacing(1)
        self._title_lbl = QLabel("Presencia y avatar")
        tf = QFont(self._UI_FONT, 10, QFont.Weight.Bold)
        self._title_lbl.setFont(tf)
        self._title_lbl.setStyleSheet(f"color: {C.WHITE}; background: transparent;")
        title_box.addWidget(self._title_lbl)

        self._sub_lbl = QLabel("Motor expresivo en tiempo real")
        sf = QFont(self._UI_FONT, 7, QFont.Weight.Medium)
        self._sub_lbl.setFont(sf)
        self._sub_lbl.setStyleSheet(f"color: {C.TEXT_MED}; background: transparent;")
        title_box.addWidget(self._sub_lbl)
        hdr.addLayout(title_box, stretch=1)

        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(24, 24)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setFont(QFont(self._UI_FONT, 9, QFont.Weight.Bold))
        close_btn.setStyleSheet(f"""
            QPushButton {{
                color: {C.TEXT_MED}; background: {_rgba(C.WHITE, 0.05)};
                border: 1px solid {C.BORDER}; border-radius: 12px;
            }}
            QPushButton:hover {{
                color: {C.WHITE}; background: {_rgba(C.RED, 0.40)};
                border-color: {C.RED};
            }}
        """)
        close_btn.clicked.connect(self.main_window._close_avatar)
        hdr.addWidget(close_btn)
        root_lay.addLayout(hdr)

        # ── 2. BARRA DE PESTAÑAS (TABS) ────────────────────────────────────
        self._tab_bar = QHBoxLayout()
        self._tab_bar.setSpacing(4)

        self._btn_tab_model = self._create_tab_btn("🎭 Modelo", 0)
        self._btn_tab_gestures = self._create_tab_btn("🎮 Gestos y Modos", 1)
        self._btn_tab_props = self._create_tab_btn("👗 Props y Voz", 2)

        self._tab_bar.addWidget(self._btn_tab_model)
        self._tab_bar.addWidget(self._btn_tab_gestures)
        self._tab_bar.addWidget(self._btn_tab_props)
        root_lay.addLayout(self._tab_bar)

        root_lay.addWidget(self._divider())

        # ── 3. CONTENEDOR CON SCROLL ───────────────────────────────────────
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll_widget = QWidget()
        self._scroll_widget.setStyleSheet("background: transparent;")
        self._scroll_layout = QVBoxLayout(self._scroll_widget)
        self._scroll_layout.setContentsMargins(2, 2, 6, 2)
        self._scroll_layout.setSpacing(10)

        # PÁGINA 0: MODELO Y ENTORNO
        self._page_model = QWidget()
        self._build_page_model(self._page_model)
        self._scroll_layout.addWidget(self._page_model)

        # PÁGINA 1: GESTOS Y POSTURA
        self._page_gestures = QWidget()
        self._build_page_gestures(self._page_gestures)
        self._scroll_layout.addWidget(self._page_gestures)

        # PÁGINA 2: PROPS Y PERSONALIDAD
        self._page_props = QWidget()
        self._build_page_props(self._page_props)
        self._scroll_layout.addWidget(self._page_props)

        self._scroll.setWidget(self._scroll_widget)
        root_lay.addWidget(self._scroll)

        # Activar pestaña inicial (Modelo)
        self._switch_tab(0)

    # ── CONSTRUCCIÓN DE PÁGINAS ────────────────────────────────────────────

    def _build_page_model(self, page: QWidget):
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)
        C = self._C

        # Motor de Renderizado (Live2D vs Holograma Core)
        lay.addWidget(self._section_tag("MOTOR DE RENDERIZADO"))
        engine_row = QHBoxLayout()
        engine_row.setSpacing(6)

        self._btn_engine_2d = QPushButton("🎨 Live2D (Cubism)")
        self._btn_engine_2d.setFixedHeight(30)
        self._btn_engine_2d.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_engine_2d.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Bold))
        self._btn_engine_2d.clicked.connect(lambda: self._set_avatar_engine("edith_live2d"))
        engine_row.addWidget(self._btn_engine_2d)

        self._btn_engine_core = QPushButton("🔮 Holograma Core")
        self._btn_engine_core.setFixedHeight(30)
        self._btn_engine_core.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_engine_core.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Bold))
        self._btn_engine_core.clicked.connect(lambda: self._set_avatar_engine("core"))
        engine_row.addWidget(self._btn_engine_core)

        lay.addLayout(engine_row)

        # ── TARJETA MODELO 2D LIVE2D ───────────────────────────────────────
        self._tag_skin = self._section_tag("PERSONAJE LIVE2D ACTIVO")
        lay.addWidget(self._tag_skin)
        self._skin_card = QFrame()
        self._skin_card.setStyleSheet(f"""
            QFrame {{
                background: {_rgba(C.WHITE, 0.03)};
                border: 1px solid {C.BORDER};
                border-radius: 10px;
                padding: 4px;
            }}
        """)
        sk_lay = QVBoxLayout(self._skin_card)
        sk_lay.setContentsMargins(8, 8, 8, 8)
        sk_lay.setSpacing(8)

        sk_row = QHBoxLayout()
        sk_row.setSpacing(6)
        self._skin_label = QLabel("🎭  huohuo")
        self._skin_label.setFont(QFont(self._UI_FONT, 9, QFont.Weight.Bold))
        self._skin_label.setStyleSheet(f"color: {C.WHITE}; background: transparent;")
        sk_row.addWidget(self._skin_label, stretch=1)

        self._change_skin_btn = QPushButton("Cambiar  ▾")
        self._change_skin_btn.setFixedHeight(26)
        self._change_skin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._change_skin_btn.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Bold))
        self._change_skin_btn.setStyleSheet(self._btn_style(accent=True))
        self._change_skin_btn.clicked.connect(self._show_skin_menu)
        sk_row.addWidget(self._change_skin_btn)
        sk_lay.addLayout(sk_row)

        tools_row = QHBoxLayout()
        tools_row.setSpacing(6)

        ai_rig_btn = QPushButton("✨ Autorigging IA")
        ai_rig_btn.setFixedHeight(26)
        ai_rig_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ai_rig_btn.setFont(QFont(self._UI_FONT, 7, QFont.Weight.Bold))
        ai_rig_btn.setStyleSheet(self._btn_style(accent=True))
        ai_rig_btn.clicked.connect(self._generate_avatar_from_image)
        tools_row.addWidget(ai_rig_btn)

        open_folder_btn = QPushButton("📂 Abrir Carpeta")
        open_folder_btn.setFixedHeight(26)
        open_folder_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        open_folder_btn.setFont(QFont(self._UI_FONT, 7, QFont.Weight.Medium))
        open_folder_btn.setStyleSheet(self._btn_style(dim=True))
        open_folder_btn.clicked.connect(open_skins_folder)
        tools_row.addWidget(open_folder_btn)

        sk_lay.addLayout(tools_row)
        lay.addWidget(self._skin_card)

        # Vista & Entorno
        lay.addWidget(self._section_tag("VISTA Y ENTORNO"))
        view_grid = QGridLayout()
        view_grid.setSpacing(6)

        self._zen_btn = QPushButton("🌸 Modo Zen (F10)")
        self._zen_btn.setFixedHeight(30)
        self._zen_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._zen_btn.setFont(QFont(self._UI_FONT, 8, QFont.Weight.DemiBold))
        self._zen_btn.setStyleSheet(self._btn_style(dim=True))
        self._zen_btn.clicked.connect(self._on_toggle_zen)
        view_grid.addWidget(self._zen_btn, 0, 0)

        self._bg_btn = QPushButton("🌅 Ciclar Fondo")
        self._bg_btn.setFixedHeight(30)
        self._bg_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._bg_btn.setFont(QFont(self._UI_FONT, 8, QFont.Weight.DemiBold))
        self._bg_btn.setStyleSheet(self._btn_style(dim=True))
        self._bg_btn.clicked.connect(self._on_cycle_bg)
        view_grid.addWidget(self._bg_btn, 0, 1)

        self._vision_btn = QPushButton("👁️ Visión: OFF")
        self._vision_btn.setFixedHeight(30)
        self._vision_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._vision_btn.setFont(QFont(self._UI_FONT, 8, QFont.Weight.DemiBold))
        self._vision_btn.setStyleSheet(self._btn_style(dim=True))
        self._vision_btn.clicked.connect(self._on_toggle_vision)
        view_grid.addWidget(self._vision_btn, 1, 0, 1, 2)

        lay.addLayout(view_grid)
        lay.addStretch()

    def _build_page_gestures(self, page: QWidget):
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        # Modos y Postura
        lay.addWidget(self._section_tag("MODOS Y POSTURA"))
        modes_grid = QGridLayout()
        modes_grid.setSpacing(6)

        self._btn_mode_idle = self._create_tile_btn("🎮", "Libre", "Postura relajada RPG", lambda: self._set_mode("idle"))
        self._btn_mode_combat = self._create_tile_btn("⚔️", "Combate", "Guardia de batalla", lambda: self._set_mode("combat"))
        self._btn_mode_study = self._create_tile_btn("🔍", "Análisis", "Enfoque y escaneo", lambda: self._set_mode("study"))
        self._btn_mode_victory = self._create_tile_btn("🏆", "Victoria", "Celebración y pose", lambda: self._set_mode("celebrate"))

        modes_grid.addWidget(self._btn_mode_idle, 0, 0)
        modes_grid.addWidget(self._btn_mode_combat, 0, 1)
        modes_grid.addWidget(self._btn_mode_study, 1, 0)
        modes_grid.addWidget(self._btn_mode_victory, 1, 1)
        lay.addLayout(modes_grid)

        # Probador de Gestos en Vivo (2 columnas anchas con texto completo)
        lay.addWidget(self._section_tag("PROBADOR DE GESTOS EN VIVO"))
        gestures_grid = QGridLayout()
        gestures_grid.setSpacing(6)

        g_list = [
            ("👋  Saludo Amable", "GREETING_WAVE", False),
            ("💖  Caricia en Cabeza", "headpat", True),
            ("😤  Puchero / Negar", "cheek_poke", True),
            ("🎉  Celebración", "doll_poke", True),
            ("⚡  Pánico / Tail", "shock", True),
            ("🙆‍♀️  Somnolienta / Relax", "stretch", True),
            ("🔍  Curiosidad / Buscar", "inspect", True),
            ("🚩  Guardia Taoísta", "combat", True),
            ("🏆  Pose de Victoria", "celebrate", True),
            ("🤔  Gesto de Duda", "scratch", True),
        ]
        for idx, (label, action_name, is_interact) in enumerate(g_list):
            r, c = divmod(idx, 2)
            btn = QPushButton(label)
            btn.setFixedHeight(30)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Medium))
            btn.setStyleSheet(self._btn_style(dim=True))
            def _make_trigger(act=action_name, direct=is_interact):
                return lambda: self._trigger_reaction(act, direct)
            btn.clicked.connect(_make_trigger())
            gestures_grid.addWidget(btn, r, c)

        lay.addLayout(gestures_grid)

        # Autonomía
        lay.addWidget(self._section_tag("NIVEL DE AUTONOMÍA"))
        auto_row = QHBoxLayout()
        auto_row.setSpacing(4)

        self._auto_off_btn = self._create_segment_btn("OFF", lambda: self._set_autonomy(False, 0.0))
        self._auto_low_btn = self._create_segment_btn("Tranquila", lambda: self._set_autonomy(True, 0.5))
        self._auto_med_btn = self._create_segment_btn("Natural", lambda: self._set_autonomy(True, 1.0))
        self._auto_high_btn = self._create_segment_btn("Expresiva", lambda: self._set_autonomy(True, 1.5))

        auto_row.addWidget(self._auto_off_btn)
        auto_row.addWidget(self._auto_low_btn)
        auto_row.addWidget(self._auto_med_btn)
        auto_row.addWidget(self._auto_high_btn)
        lay.addLayout(auto_row)

        self._anim_toggle_btn = QPushButton("✨  Animaciones Espontáneas: SÍ")
        self._anim_toggle_btn.setFixedHeight(28)
        self._anim_toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._anim_toggle_btn.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Medium))
        self._anim_toggle_btn.setStyleSheet(self._btn_style(dim=True))
        self._anim_toggle_btn.clicked.connect(self._toggle_auto_animations)
        lay.addWidget(self._anim_toggle_btn)
        lay.addStretch()

    def _build_page_props(self, page: QWidget):
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)
        C = self._C

        # Accesorios y Props
        lay.addWidget(self._section_tag("ACCESORIOS Y PROPS EN VIVO"))
        props_grid = QGridLayout()
        props_grid.setSpacing(6)

        self._prop_rings_btn = self._create_chip_btn("🌐  Anillos / Luces 3D", lambda: self._toggle_prop("hologram_rings"))
        props_grid.addWidget(self._prop_rings_btn, 0, 0, 1, 2)
        lay.addLayout(props_grid)

        # Personalidad, Nacionalidad y Forma de Hablar
        lay.addWidget(self._section_tag("PERSONALIDAD, NACIONALIDAD Y HABLA"))
        pers_card = QFrame()
        pers_card.setStyleSheet(f"""
            QFrame {{
                background: {_rgba(C.WHITE, 0.03)};
                border: 1px solid {C.BORDER};
                border-radius: 10px;
                padding: 4px;
            }}
        """)
        pers_lay = QVBoxLayout(pers_card)
        pers_lay.setContentsMargins(10, 10, 10, 10)
        pers_lay.setSpacing(8)

        pers_row = QHBoxLayout()
        pers_row.setSpacing(6)
        from core.personality_manager import get_personality_manager, DIALECT_SPECS
        _p_active = get_personality_manager().get_active_profile()
        _d_info = DIALECT_SPECS.get(_p_active.dialect_id, {})
        _nat_txt = (getattr(_p_active, "nationality", "") or "").strip() or _d_info.get("region", "")

        pers_info_col = QVBoxLayout()
        pers_info_col.setSpacing(2)
        self._pers_label = QLabel(f"🎭  {_p_active.name}")
        self._pers_label.setFont(QFont(self._UI_FONT, 9, QFont.Weight.Bold))
        self._pers_label.setStyleSheet(f"color: {C.WHITE}; background: transparent;")
        pers_info_col.addWidget(self._pers_label)

        self._pers_sub_label = QLabel(f"🌎  {_nat_txt} · {_d_info.get('name', _p_active.dialect_id)}")
        self._pers_sub_label.setFont(QFont(self._UI_FONT, 7, QFont.Weight.Medium))
        self._pers_sub_label.setStyleSheet(f"color: {C.TEXT_MED}; background: transparent;")
        pers_info_col.addWidget(self._pers_sub_label)
        pers_row.addLayout(pers_info_col, stretch=1)

        self._pers_config_btn = QPushButton("Personalizar  ▾")
        self._pers_config_btn.setFixedHeight(28)
        self._pers_config_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._pers_config_btn.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Bold))
        self._pers_config_btn.setStyleSheet(self._btn_style(accent=True))
        self._pers_config_btn.clicked.connect(self._open_personality_dialog)
        pers_row.addWidget(self._pers_config_btn)
        pers_lay.addLayout(pers_row)

        chips_grid = QGridLayout()
        chips_grid.setSpacing(5)
        self._pers_chips: dict[str, QPushButton] = {}
        quick_presets = [
            ("🇨🇷 Tica", "edith_tica_sarcastica"),
            ("🇨🇴 Paisa", "edith_paisa_bromista"),
            ("🇲🇽 Mexicana", "edith_mexicana_alegre"),
            ("🇦🇷 Porteña", "edith_rioplatense_astuta"),
            ("🌸 Kawaii", "edith_kawaii_tierna"),
            ("💼 Ejecutiva", "edith_profesional_ejecutiva"),
        ]
        for idx, (chip_lbl, chip_pid) in enumerate(quick_presets):
            r, c = divmod(idx, 3)
            c_btn = self._create_segment_btn(chip_lbl, lambda p=chip_pid: self._quick_set_personality(p))
            self._pers_chips[chip_pid] = c_btn
            chips_grid.addWidget(c_btn, r, c)
        pers_lay.addLayout(chips_grid)
        lay.addWidget(pers_card)
        lay.addStretch()

    # ── GESTIÓN DE PESTAÑAS ────────────────────────────────────────────────

    def _create_tab_btn(self, text: str, tab_idx: int) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedHeight(28)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Bold))
        btn.clicked.connect(lambda: self._switch_tab(tab_idx))
        return btn

    def _switch_tab(self, idx: int):
        self._current_tab = idx
        self._page_model.setVisible(idx == 0)
        self._page_gestures.setVisible(idx == 1)
        self._page_props.setVisible(idx == 2)

        C = self._C
        for i, b in enumerate([self._btn_tab_model, self._btn_tab_gestures, self._btn_tab_props]):
            active = (i == idx)
            b.setStyleSheet(f"""
                QPushButton {{
                    background: {_rgba(C.PRI, 0.22) if active else _rgba(C.WHITE, 0.04)};
                    color: {C.WHITE if active else C.TEXT_MED};
                    border: 1px solid {_rgba(C.PRI, 0.55) if active else C.BORDER};
                    border-radius: 6px;
                    font-weight: {'bold' if active else '600'};
                }}
                QPushButton:hover {{
                    background: {_rgba(C.PRI, 0.32)};
                    color: {C.WHITE};
                }}
            """)

    # ── HELPERS DE UI Y ESTILOS ────────────────────────────────────────────

    def _section_tag(self, text: str) -> QLabel:
        clean = text.capitalize() if text.isupper() else text
        lbl = QLabel(clean)
        f = QFont(self._UI_FONT, 8, QFont.Weight.DemiBold)
        lbl.setFont(f)
        lbl.setStyleSheet(f"color: {self._C.TEXT_MED}; background: transparent; padding-top: 2px;")
        return lbl

    def _divider(self) -> QFrame:
        ln = QFrame()
        ln.setFixedHeight(1)
        ln.setStyleSheet(f"background: {self._C.BORDER_A}; border: none;")
        return ln

    def _btn_style(self, on=False, accent=False, dim=False) -> str:
        C = self._C
        if on:
            fg, bg, bd = C.GREEN, _rgba(C.GREEN, 0.18), _rgba(C.GREEN, 0.50)
            hv = _rgba(C.GREEN, 0.28)
        elif accent:
            fg, bg, bd = C.PRI, _rgba(C.PRI, 0.16), _rgba(C.PRI, 0.45)
            hv = _rgba(C.PRI, 0.26)
        elif dim:
            fg, bg, bd = C.TEXT_MED, _rgba(C.WHITE, 0.04), C.BORDER
            hv = _rgba(C.WHITE, 0.10)
        else:
            fg, bg, bd = C.WHITE, _rgba(C.WHITE, 0.06), C.BORDER_B
            hv = _rgba(C.WHITE, 0.14)

        return f"""
            QPushButton {{
                background: {bg}; color: {fg};
                border: 1px solid {bd}; border-radius: 8px;
                padding: 0 8px; font-weight: 600;
            }}
            QPushButton:hover {{
                background: {hv}; color: {C.WHITE};
                border-color: {C.PRI};
            }}
            QPushButton:pressed {{
                background: {_rgba(C.PRI, 0.35)};
            }}
        """

    def _create_tile_btn(self, icon: str, title: str, tip: str, slot) -> QPushButton:
        btn = QPushButton(f"{icon}  {title}")
        btn.setFixedHeight(34)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFont(QFont(self._UI_FONT, 8, QFont.Weight.DemiBold))
        btn.setToolTip(tip)
        btn.setStyleSheet(self._btn_style(dim=True))
        btn.clicked.connect(slot)
        return btn

    def _create_chip_btn(self, text: str, slot) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedHeight(32)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFont(QFont(self._UI_FONT, 8, QFont.Weight.DemiBold))
        btn.setStyleSheet(self._btn_style(dim=True))
        btn.clicked.connect(slot)
        return btn

    def _create_segment_btn(self, text: str, slot) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedHeight(26)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFont(QFont(self._UI_FONT, 7, QFont.Weight.Bold))
        btn.setStyleSheet(self._btn_style(dim=True))
        btn.clicked.connect(slot)
        return btn

    # ── MÉTODOS DE CONTROL Y CONEXIÓN CON LIVE2D ───────────────────────────

    def refresh_state(self):
        """Sincroniza la interfaz con la configuración activa."""
        skin = get_live2d_skin()
        self._skin_label.setText(f"🎭  {skin}")

        # Motor de Renderizado (solo Live2D o Holograma Core)
        active_style = get_hud_style()
        if active_style not in ("edith_live2d", "core"):
            active_style = "edith_live2d"
            save_hud_style(active_style)
        if hasattr(self, "_btn_engine_2d"):
            self._btn_engine_2d.setStyleSheet(self._btn_style(accent=(active_style == "edith_live2d"), dim=(active_style != "edith_live2d")))
            self._btn_engine_core.setStyleSheet(self._btn_style(accent=(active_style == "core"), dim=(active_style != "core")))

        is_live2d = (active_style == "edith_live2d")
        if hasattr(self, "_tag_skin"):
            self._tag_skin.setVisible(is_live2d)
            self._skin_card.setVisible(is_live2d)

        # Autonomía
        auto_enabled = get_edith_autonomy_enabled()
        level = get_edith_spontaneity_level()

        self._auto_off_btn.setStyleSheet(self._btn_style(on=not auto_enabled))
        self._auto_low_btn.setStyleSheet(self._btn_style(on=(auto_enabled and level <= 0.6)))
        self._auto_med_btn.setStyleSheet(self._btn_style(on=(auto_enabled and 0.6 < level <= 1.1)))
        self._auto_high_btn.setStyleSheet(self._btn_style(on=(auto_enabled and level > 1.1)))

        # Animaciones
        anim_on = get_auto_animations_enabled()
        self._anim_toggle_btn.setText(f"✨  Animaciones Espontáneas: {'SÍ' if anim_on else 'NO'}")
        self._anim_toggle_btn.setStyleSheet(self._btn_style(on=anim_on, dim=not anim_on))

        # Modos
        self._update_mode_buttons()

        # Props
        self._update_prop_buttons()

        # Visión Continua
        try:
            from core.realtime_vision import get_vision_coordinator
            v_on = get_vision_coordinator().is_active()
            self._vision_btn.setText(f"👁️ Visión: {'ON' if v_on else 'OFF'}")
            self._vision_btn.setStyleSheet(self._btn_style(on=v_on, dim=not v_on))
        except Exception:
            pass

        # Personalidad, Nacionalidad y Dialectos
        try:
            from core.personality_manager import get_personality_manager, DIALECT_SPECS
            prof = get_personality_manager().get_active_profile()
            d_info = DIALECT_SPECS.get(prof.dialect_id, {})
            nat_txt = (getattr(prof, "nationality", "") or "").strip() or d_info.get("region", "")
            if hasattr(self, "_pers_label"):
                self._pers_label.setText(f"🎭  {prof.name}")
            if hasattr(self, "_pers_sub_label"):
                self._pers_sub_label.setText(f"🌎  {nat_txt} · {d_info.get('name', prof.dialect_id)}")
            if hasattr(self, "_pers_chips"):
                for chip_pid, chip_btn in self._pers_chips.items():
                    is_active = (chip_pid == prof.id)
                    chip_btn.setStyleSheet(self._btn_style(accent=is_active, dim=not is_active))
        except Exception:
            pass

    def _show_skin_menu(self):
        try:
            skins = discover_live2d_skins()
            current_skin = get_live2d_skin()

            menu = QMenu(self)
            C = self._C
            menu.setStyleSheet(f"""
                QMenu {{
                    background-color: {C.PANEL};
                    color: {C.TEXT};
                    border: 1px solid {C.BORDER_A};
                    border-radius: 8px;
                    padding: 6px;
                    font-family: {self._UI_FONT};
                    font-size: 11px;
                }}
                QMenu::item {{
                    padding: 6px 20px 6px 16px;
                    border-radius: 4px;
                }}
                QMenu::item:selected {{
                    background-color: {C.PANEL2};
                    color: {C.PRI};
                }}
            """)

            hdr = menu.addAction("🎭 PERSONAJES DISPONIBLES")
            hdr.setEnabled(False)
            menu.addSeparator()

            for s_name, s_data in skins.items():
                is_active = (s_name.lower() == current_skin.lower())
                label = f"✓  {s_name}" if is_active else f"    {s_name}"
                act = menu.addAction(label)
                def _make_handler(name=s_name, url=s_data["model_url"]):
                    return lambda: self._apply_skin(name, url)
                act.triggered.connect(_make_handler())

            menu.addSeparator()
            gen_act = menu.addAction("✨  Generar Avatar 2D desde Imagen (IA)...")
            gen_act.triggered.connect(self._generate_avatar_from_image)
            open_act = menu.addAction("📂  Abrir carpeta de modelos...")
            open_act.triggered.connect(open_skins_folder)

            pos = self._change_skin_btn.mapToGlobal(QPoint(0, self._change_skin_btn.height() + 2))
            menu.exec(pos)
        except Exception as e:
            print(f"[AvatarControlDrawer] Error al desplegar menú de skins: {e}")

    def _show_vrm_menu(self):
        try:
            from core.vrm.vrm_widget import discover_vrm_models
            vrm_files = discover_vrm_models()
            current_vrm = get_vrm_model()
            C = self._C

            menu = QMenu(self)
            menu.setStyleSheet(f"""
                QMenu {{
                    background-color: {C.PANEL};
                    color: {C.TEXT};
                    border: 1px solid {C.BORDER_A};
                    border-radius: 8px;
                    padding: 6px;
                    font-family: {self._UI_FONT};
                    font-size: 11px;
                }}
                QMenu::item {{
                    padding: 6px 20px 6px 16px;
                    border-radius: 4px;
                }}
                QMenu::item:selected {{
                    background-color: {C.PANEL2};
                    color: {C.PRI};
                }}
            """)

            hdr = menu.addAction("✨ MODELOS 3D VRM DISPONIBLES")
            hdr.setEnabled(False)
            menu.addSeparator()

            for vf in vrm_files:
                is_active = (vf.lower() == current_vrm.lower())
                label = f"✓  {vf}" if is_active else f"    {vf}"
                act = menu.addAction(label)
                def _make_vrm_handler(m_name=vf):
                    return lambda: self._apply_vrm_model(m_name)
                act.triggered.connect(_make_vrm_handler())

            menu.addSeparator()
            imp_act = menu.addAction("➕  Importar archivo .VRM...")
            imp_act.triggered.connect(self._import_vrm_file)
            open_act = menu.addAction("📂  Abrir carpeta de modelos 3D...")
            open_act.triggered.connect(open_vrm_folder)

            pos = self._vrm_change_btn.mapToGlobal(QPoint(0, self._vrm_change_btn.height() + 2))
            menu.exec(pos)
        except Exception as e:
            print(f"[AvatarControlDrawer] Error al desplegar menú de VRM: {e}")

    def _import_vrm_file(self):
        try:
            import shutil
            from pathlib import Path
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Seleccionar Modelo Humanoide VRM (*.vrm)",
                "",
                "Modelos 3D VRM (*.vrm)"
            )
            if not file_path:
                return

            src = Path(file_path)
            dest_dir = Path(__file__).resolve().parent / "vrm" / "models"
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / src.name
            if src.resolve() != dest.resolve():
                shutil.copy2(src, dest)

            self._apply_vrm_model(src.name)
        except Exception as e:
            print(f"[AvatarControlDrawer] Error importando VRM: {e}")

    def _apply_vrm_model(self, model_name: str):
        save_vrm_model(model_name)
        hud = getattr(self.main_window, "hud", None)
        if hud and hasattr(hud, "_vrm_widget") and hud._vrm_widget is not None:
            hud._vrm_widget.load_model(model_name)
        self.refresh_state()
        if hasattr(self.main_window, "_log"):
            self.main_window._log.append_log(f"SYS: Modelo 3D cambiado a '{model_name}'.")

    def _generate_avatar_from_image(self):
        """Dispara el pipeline de autorigging por IA para convertir una imagen en un avatar animable."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Ilustración del Personaje para Autorigging",
            "",
            "Imágenes (*.png *.jpg *.jpeg)"
        )
        if not file_path:
            return

        img_p = Path(file_path)
        char_name = img_p.stem.replace("_", " ").title()

        if hasattr(self.main_window, "_log") and self.main_window._log:
            self.main_window._log.append_log(f"SYS: Iniciando Autorigging 2D por IA para '{char_name}'...")

        try:
            from core.avatar_engine.autorigger import AutoRigger
            from core.live2d.skin_manager import MODELS_DIR

            target_dir = MODELS_DIR / char_name.replace(" ", "_")
            rig = AutoRigger.generate_rig_from_image(
                image_path=img_p,
                output_dir=target_dir,
                avatar_name=char_name.replace(" ", "_")
            )

            rel_url = f"../../live2d_models/{char_name.replace(' ', '_')}/{char_name.replace(' ', '_')}.edith2d.json"
            self._apply_skin(char_name, rel_url)

            try:
                from core.notifications import notify, LEVEL_SUCCESS
                notify(
                    title="✨ Avatar 2D Generado con Éxito",
                    message=f"El personaje '{char_name}' ha sido descompuesto en capas, rigeado con mallas CDT y activado.",
                    level=LEVEL_SUCCESS,
                    category="AVATAR_ENGINE"
                )
            except Exception:
                pass
        except Exception as e:
            if hasattr(self.main_window, "_log") and self.main_window._log:
                self.main_window._log.append_log(f"ERR: Falló el autorigging de avatar: {e}")

    def _apply_skin(self, name: str, url: str):
        save_live2d_skin(name)
        if hasattr(self.main_window, "hud") and hasattr(self.main_window.hud, "_live2d_widget"):
            w = self.main_window.hud._live2d_widget
            if w is not None:
                w.load_model(url)
        self.refresh_state()
        if hasattr(self.main_window, "_refresh_skin_btn"):
            self.main_window._refresh_skin_btn()
        if hasattr(self.main_window, "_log"):
            self.main_window._log.append_log(f"SYS: Avatar Live2D cambiado a '{name}'.")

    def _set_mode(self, mode: str):
        self._active_game_mode = mode
        hud = getattr(self.main_window, "hud", None)
        if hud:
            if getattr(hud, "hud_style", "") == "vrm_3d" and hasattr(hud, "_vrm_widget") and hud._vrm_widget:
                if mode == "combat":
                    hud._vrm_widget.set_float_mode(True)
                elif mode == "celebrate":
                    hud._vrm_widget.trigger_gesture("CELEBRATE", 3.5)
                elif mode == "study":
                    hud._vrm_widget.trigger_gesture("THINKING", 3.5)
                else:
                    hud._vrm_widget.set_float_mode(False)
            elif hasattr(hud, "_live2d_widget") and hud._live2d_widget:
                hud._live2d_widget.set_game_mode(mode)
        self._update_mode_buttons()

        if mode == "combat":
            self._prop_rings = True
        elif mode == "study":
            self._prop_rings = True
        elif mode == "celebrate":
            self._prop_rings = True
        self._update_prop_buttons()

    def _update_mode_buttons(self):
        m = self._active_game_mode
        self._btn_mode_idle.setStyleSheet(self._btn_style(accent=(m == "idle"), dim=(m != "idle")))
        self._btn_mode_combat.setStyleSheet(self._btn_style(accent=(m == "combat"), dim=(m != "combat")))
        self._btn_mode_study.setStyleSheet(self._btn_style(accent=(m == "study"), dim=(m != "study")))
        self._btn_mode_victory.setStyleSheet(self._btn_style(accent=(m == "celebrate"), dim=(m != "celebrate")))

    def _toggle_prop(self, prop_name: str):
        if prop_name == "hologram_rings":
            self._prop_rings = not self._prop_rings
            val = self._prop_rings
        else:
            return

        if hasattr(self.main_window, "hud"):
            hud = self.main_window.hud
            w = getattr(hud, "_live2d_widget", None)
            if w is not None:
                w.set_prop_state(prop_name, val, duration=999999.0 if val else 0.0)
            vrm = getattr(hud, "_vrm_widget", None)
            if vrm is not None and getattr(hud, "_hud_style", None) == "vrm_3d":
                vrm.set_float_mode(val)

        self._update_prop_buttons()

    def _update_prop_buttons(self):
        if hasattr(self, "_prop_rings_btn"):
            self._prop_rings_btn.setStyleSheet(self._btn_style(on=self._prop_rings, dim=not self._prop_rings))

    def _set_autonomy(self, enabled: bool, level: float):
        save_edith_autonomy_enabled(enabled)
        save_edith_spontaneity_level(level)

        if hasattr(self.main_window, "hud"):
            hud = self.main_window.hud
            w = getattr(hud, "_live2d_widget", None)
            if w is not None:
                w.set_autonomy_enabled(enabled)
                w.set_spontaneity_level(level)
            vrm = getattr(hud, "_vrm_widget", None)
            if vrm is not None:
                vrm.set_autonomy_enabled(enabled)
                vrm.set_spontaneity_level(level)

        if hasattr(self.main_window, "_refresh_edith_btn"):
            self.main_window._refresh_edith_btn()

        self.refresh_state()

    def _toggle_auto_animations(self):
        if hasattr(self.main_window, "_toggle_auto_animations"):
            self.main_window._toggle_auto_animations()
        self.refresh_state()

    def _set_avatar_engine(self, style: str):
        if style not in ("edith_live2d", "core"):
            style = "edith_live2d"
        save_hud_style(style)
        if hasattr(self.main_window, "hud"):
            self.main_window.hud.set_hud_style(style)
        self.refresh_state()
        if hasattr(self.main_window, "_log"):
            names = {
                "edith_live2d": "Edith Live2D (Cubism)",
                "core": "Holograma Core Orbital",
            }
            self.main_window._log.append_log(f"SYS: Motor visual cambiado a '{names.get(style, style)}'.")

    def _set_camera_preset(self, preset: str):
        if hasattr(self.main_window, "hud") and hasattr(self.main_window.hud, "_vrm_widget"):
            w = self.main_window.hud._vrm_widget
            if w is not None:
                w.set_camera_preset(preset)

    def _trigger_reaction(self, action: str, is_interact: bool):
        hud = getattr(self.main_window, "hud", None)
        if not hud:
            return

        if getattr(hud, "hud_style", "") == "vrm_3d":
            # Direct VRM 3D gesture & emotion mapping
            vrm_gestures = {
                "GREETING": "WAVE_HELLO",
                "GREETING_WAVE": "WAVE_HELLO",
                "headpat": "NOD_AGREE",
                "cheek_poke": "SHY",
                "shock": "HEAD_SHAKE",
                "stretch": "RELAXED",
                "inspect": "THINKING",
                "scratch": "CONFUSED",
                "doll_poke": "EXPLAIN",
                "combat": "CELEBRATE",
                "celebrate": "CELEBRATE",
            }
            vrm_emos = {
                "GREETING": "happy",
                "GREETING_WAVE": "happy",
                "headpat": "happy",
                "cheek_poke": "shy",
                "shock": "surprised",
                "stretch": "relaxed",
                "inspect": "thinking",
                "scratch": "confused",
                "doll_poke": "happy",
                "combat": "enthusiastic",
                "celebrate": "proud",
            }
            g_name = vrm_gestures.get(action, "WAVE_HELLO")
            e_name = vrm_emos.get(action, "happy")
            hud.set_emotion(e_name, 0.85, 3.2)
            hud.trigger_gesture(g_name, duration=3.5)
        elif hasattr(hud, "_live2d_widget") and hud._live2d_widget is not None:
            if is_interact:
                hud._live2d_widget.interact(action)
            else:
                hud._live2d_widget.trigger_gesture(action, duration=3.2)

    def _on_toggle_zen(self):
        if hasattr(self.main_window, "_toggle_avatar_only"):
            self.main_window._toggle_avatar_only()
            self.main_window._close_avatar()

    def _on_cycle_bg(self):
        if hasattr(self.main_window, "_cycle_background_mode"):
            self.main_window._cycle_background_mode()

    def _on_toggle_vision(self):
        if hasattr(self.main_window, "_toggle_realtime_vision"):
            self.main_window._toggle_realtime_vision()
        self.refresh_state()

    def _open_personality_dialog(self):
        try:
            from core.personality_dialog import PersonalitySettingsDialog
            dlg = PersonalitySettingsDialog(self.main_window)
            dlg.exec()
            self.refresh_state()
        except Exception as e:
            print(f"[AvatarControlDrawer] Error abriendo diálogo de personalidad: {e}")

    def _quick_set_personality(self, pid: str):
        try:
            from core.personality_manager import get_personality_manager
            mgr = get_personality_manager()
            mgr.set_active_profile(pid, persist=True)
            self.refresh_state()
            if hasattr(self.main_window, "_log"):
                prof = mgr.get_active_profile()
                self.main_window._log.append_log(f"SYS: Personalidad cambiada a '{prof.name}'.")
        except Exception as e:
            print(f"[AvatarControlDrawer] Error configurando personalidad rápida: {e}")

