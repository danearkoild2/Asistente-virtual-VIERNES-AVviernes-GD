from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QCheckBox,
    QColorDialog,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSlider,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from core.hud_theme import (
    DEFAULT_HUD_CONFIG,
    HUD_BACKGROUNDS,
    HUD_THEMES,
    LAYOUT_PRESETS,
    get_theme_palette,
)


class _ThemeCard(QFrame):
    """Visual theme selector card with live color swatches."""

    clicked = pyqtSignal(str)

    def __init__(self, theme_id: str, meta: dict[str, Any], active: bool, parent=None) -> None:
        super().__init__(parent)
        self.theme_id = theme_id
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(74)
        self._meta = meta
        self._active = active
        self._build()
        self.set_active(active)

    def _build(self) -> None:
        pal = self._meta["palette"]
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 8, 10, 8)
        lay.setSpacing(5)

        top = QHBoxLayout()
        top.setSpacing(6)
        title = QLabel(self._meta["name"])
        title.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {pal['TEXT']}; background: transparent; border: none;")
        top.addWidget(title)
        top.addStretch()

        for col_key in ("BG", "PANEL2", "PRI", "ACC"):
            dot = QLabel()
            dot.setFixedSize(11, 11)
            dot.setStyleSheet(
                f"background: {pal[col_key]}; border: 1px solid rgba(255,255,255,0.22); border-radius: 5px;"
            )
            top.addWidget(dot)
        lay.addLayout(top)

        sub = QLabel(self._meta["subtitle"])
        sub.setFont(QFont("Segoe UI", 8))
        sub.setStyleSheet(f"color: {pal['TEXT_MED']}; background: transparent; border: none;")
        lay.addWidget(sub)

    def set_active(self, active: bool) -> None:
        self._active = active
        pal = self._meta["palette"]
        border = pal["PRI"] if active else pal["BORDER"]
        bw = "2px" if active else "1px"
        self.setStyleSheet(
            f"_ThemeCard {{ background: {pal['PANEL']}; border: {bw} solid {border}; border-radius: 10px; }}"
        )

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.theme_id)
        super().mousePressEvent(event)


class HudStudioOverlay(QWidget):
    """Professional live-preview customization studio for Viernes's main HUD."""

    config_changed = pyqtSignal(dict, bool)  # (config, persist)
    closed = pyqtSignal()
    _OW, _OH = 640, 620

    def __init__(self, current_cfg: dict[str, Any], parent=None) -> None:
        super().__init__(parent)
        self._cfg = deepcopy(current_cfg)
        self._theme_cards: dict[str, _ThemeCard] = {}
        self._preset_btns: dict[str, QPushButton] = {}
        self._bg_btns: dict[str, QPushButton] = {}
        self._density_btns: dict[str, QPushButton] = {}
        self._radius_btns: dict[int, QPushButton] = {}
        self._widget_checks: dict[str, QCheckBox] = {}
        self._building = True

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._apply_chrome_style()
        self._build_ui()
        self._sync_controls_from_cfg()
        self._building = False

    def _pal(self) -> dict[str, str]:
        return get_theme_palette(
            self._cfg.get("theme_id", "obsidian_pro"),
            self._cfg.get("accent_override", ""),
        )

    def _apply_chrome_style(self) -> None:
        p = self._pal()
        self.setStyleSheet(
            f"HudStudioOverlay {{ background: {p['PANEL']}; border: 1px solid {p['BORDER_B']}; border-radius: 14px; }}"
        )

    def _build_ui(self) -> None:
        p = self._pal()
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(12)

        # Header
        hdr = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(1)
        t_lbl = QLabel("HUD Studio · Personalización Profesional")
        t_lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        t_lbl.setStyleSheet(f"color: {p['WHITE']}; background: transparent;")
        s_lbl = QLabel("Vista previa en tiempo real — ajusta tema, densidad, paneles y módulos.")
        s_lbl.setFont(QFont("Segoe UI", 8))
        s_lbl.setStyleSheet(f"color: {p['TEXT_MED']}; background: transparent;")
        title_box.addWidget(t_lbl)
        title_box.addWidget(s_lbl)
        hdr.addLayout(title_box)
        hdr.addStretch()

        close_x = QPushButton("✕")
        close_x.setFixedSize(28, 28)
        close_x.setCursor(Qt.CursorShape.PointingHandCursor)
        close_x.setStyleSheet(
            f"QPushButton {{ background: transparent; color: {p['TEXT_MED']}; border: 1px solid {p['BORDER']}; border-radius: 7px; }}"
            f"QPushButton:hover {{ color: {p['WHITE']}; border-color: {p['BORDER_B']}; }}"
        )
        close_x.clicked.connect(self.closed.emit)
        hdr.addWidget(close_x)
        root.addLayout(hdr)

        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet(
            f"QTabWidget::pane {{ border: 1px solid {p['BORDER']}; border-radius: 10px; background: {p['BG']}; padding: 8px; }}"
            f"QTabBar::tab {{ background: {p['PANEL2']}; color: {p['TEXT_MED']}; padding: 7px 16px; border-top-left-radius: 8px; border-top-right-radius: 8px; margin-right: 4px; font-weight: 600; }}"
            f"QTabBar::tab:selected {{ background: {p['PRI_GHO']}; color: {p['PRI']}; border-bottom: 2px solid {p['PRI']}; }}"
        )
        tabs.addTab(self._build_theme_tab(), "Estética & Tema")
        tabs.addTab(self._build_backdrop_tab(), "Fondos & Ambiente")
        tabs.addTab(self._build_layout_tab(), "Layout & Módulos")
        root.addWidget(tabs, stretch=1)

        # Footer
        foot = QHBoxLayout()
        reset_btn = QPushButton("Restablecer Pro")
        reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_btn.setFixedHeight(34)
        reset_btn.setStyleSheet(
            f"QPushButton {{ background: transparent; color: {p['TEXT_MED']}; border: 1px solid {p['BORDER']}; border-radius: 8px; padding: 0 14px; font-weight: 600; }}"
            f"QPushButton:hover {{ color: {p['WHITE']}; border-color: {p['BORDER_B']}; }}"
        )
        reset_btn.clicked.connect(self._reset_defaults)
        foot.addWidget(reset_btn)
        foot.addStretch()

        save_btn = QPushButton("Aplicar y Guardar")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setFixedHeight(34)
        save_btn.setStyleSheet(
            f"QPushButton {{ background: {p['PRI']}; color: {p['WHITE']}; border: none; border-radius: 8px; padding: 0 18px; font-weight: 700; }}"
            f"QPushButton:hover {{ background: {p['PRI_DIM']}; }}"
        )
        save_btn.clicked.connect(self._save_and_close)
        foot.addWidget(save_btn)
        root.addLayout(foot)

    def _build_theme_tab(self) -> QWidget:
        p = self._pal()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        box = QWidget()
        box.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(box)
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setSpacing(12)

        lbl1 = QLabel("PALETAS PROFESIONALES DE SUPERFICIE")
        lbl1.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        lbl1.setStyleSheet(f"color: {p['TEXT_DIM']}; background: transparent;")
        lay.addWidget(lbl1)

        grid = QGridLayout()
        grid.setSpacing(8)
        for idx, (tid, meta) in enumerate(HUD_THEMES.items()):
            card = _ThemeCard(tid, meta, tid == self._cfg.get("theme_id"), box)
            card.clicked.connect(self._on_theme_selected)
            self._theme_cards[tid] = card
            grid.addWidget(card, idx // 2, idx % 2)
        lay.addLayout(grid)

        # Custom accent row
        acc_row = QHBoxLayout()
        acc_lbl = QLabel("Color de acento personalizado:")
        acc_lbl.setStyleSheet(f"color: {p['TEXT']}; font-weight: 600; background: transparent;")
        acc_row.addWidget(acc_lbl)
        acc_row.addStretch()

        self._accent_pick_btn = QPushButton("Elegir color…")
        self._accent_pick_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._accent_pick_btn.setFixedHeight(28)
        self._accent_pick_btn.setStyleSheet(
            f"QPushButton {{ background: {p['PANEL2']}; color: {p['TEXT']}; border: 1px solid {p['BORDER']}; border-radius: 7px; padding: 0 12px; }}"
            f"QPushButton:hover {{ border-color: {p['PRI']}; }}"
        )
        self._accent_pick_btn.clicked.connect(self._pick_accent_color)
        acc_row.addWidget(self._accent_pick_btn)

        self._accent_clear_btn = QPushButton("Usar del tema")
        self._accent_clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._accent_clear_btn.setFixedHeight(28)
        self._accent_clear_btn.setStyleSheet(
            f"QPushButton {{ background: transparent; color: {p['TEXT_MED']}; border: 1px solid {p['BORDER']}; border-radius: 7px; padding: 0 10px; }}"
        )
        self._accent_clear_btn.clicked.connect(self._clear_accent_override)
        acc_row.addWidget(self._accent_clear_btn)
        lay.addLayout(acc_row)

        # Density & Radius
        style_row = QHBoxLayout()
        style_row.setSpacing(12)

        dens_col = QVBoxLayout()
        d_lbl = QLabel("DENSIDAD VISUAL")
        d_lbl.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        d_lbl.setStyleSheet(f"color: {p['TEXT_DIM']}; background: transparent;")
        dens_col.addWidget(d_lbl)
        d_btns = QHBoxLayout()
        for key, text in (("compact", "Compacta"), ("balanced", "Equilibrada"), ("spacious", "Amplia")):
            b = QPushButton(text)
            b.setCheckable(True)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setFixedHeight(28)
            b.clicked.connect(lambda _=False, k=key: self._on_density_selected(k))
            self._density_btns[key] = b
            d_btns.addWidget(b)
        dens_col.addLayout(d_btns)
        style_row.addLayout(dens_col)

        rad_col = QVBoxLayout()
        r_lbl = QLabel("ESTILO DE BORDES")
        r_lbl.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        r_lbl.setStyleSheet(f"color: {p['TEXT_DIM']}; background: transparent;")
        rad_col.addWidget(r_lbl)
        r_btns = QHBoxLayout()
        for rad, text in ((8, "Técnico 8px"), (12, "Pro 12px"), (16, "Suave 16px")):
            b = QPushButton(text)
            b.setCheckable(True)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setFixedHeight(28)
            b.clicked.connect(lambda _=False, rv=rad: self._on_radius_selected(rv))
            self._radius_btns[rad] = b
            r_btns.addWidget(b)
        rad_col.addLayout(r_btns)
        style_row.addLayout(rad_col)
        lay.addLayout(style_row)

        # Visual effects toggles
        eff_row = QHBoxLayout()
        self._chk_glow = QCheckBox("Iluminación y profundidad en marco central")
        self._chk_glow.setStyleSheet(f"color: {p['TEXT']}; background: transparent;")
        self._chk_glow.toggled.connect(lambda v: self._set_flag("glass_glow", v))
        eff_row.addWidget(self._chk_glow)

        self._chk_grid = QCheckBox("Retícula técnica de fondo en HUD")
        self._chk_grid.setStyleSheet(f"color: {p['TEXT']}; background: transparent;")
        self._chk_grid.toggled.connect(lambda v: self._set_flag("hud_grid", v))
        eff_row.addWidget(self._chk_grid)
        lay.addLayout(eff_row)

        lay.addStretch()
        scroll.setWidget(box)
        return scroll

    def _build_backdrop_tab(self) -> QWidget:
        p = self._pal()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        box = QWidget()
        box.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(box)
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setSpacing(12)

        lbl = QLabel("AMBIENTE Y ESCENARIO DEL HUD")
        lbl.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        lbl.setStyleSheet(f"color: {p['TEXT_DIM']}; background: transparent;")
        lay.addWidget(lbl)

        grid = QGridLayout()
        grid.setSpacing(8)
        for idx, (bid, bmeta) in enumerate(HUD_BACKGROUNDS.items()):
            b = QPushButton(f"{bmeta['name']}\n{bmeta['desc']}")
            b.setCheckable(True)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setFixedHeight(54)
            b.clicked.connect(lambda _=False, k=bid: self._on_bg_selected(k))
            self._bg_btns[bid] = b
            grid.addWidget(b, idx // 2, idx % 2)
        lay.addLayout(grid)

        custom_row = QHBoxLayout()
        self._custom_bg_lbl = QLabel("Imagen propia: ninguna seleccionada")
        self._custom_bg_lbl.setStyleSheet(f"color: {p['TEXT_MED']}; background: transparent;")
        custom_row.addWidget(self._custom_bg_lbl, stretch=1)

        pick_btn = QPushButton("Elegir imagen…")
        pick_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        pick_btn.setFixedHeight(28)
        pick_btn.setStyleSheet(
            f"QPushButton {{ background: {p['PANEL2']}; color: {p['TEXT']}; border: 1px solid {p['BORDER']}; border-radius: 7px; padding: 0 12px; }}"
            f"QPushButton:hover {{ border-color: {p['PRI']}; }}"
        )
        pick_btn.clicked.connect(self._pick_custom_bg)
        custom_row.addWidget(pick_btn)
        lay.addLayout(custom_row)

        self._dim_lbl = QLabel()
        self._dim_lbl.setStyleSheet(f"color: {p['TEXT_MED']}; background: transparent;")
        self._dim_slider = QSlider(Qt.Orientation.Horizontal)
        self._dim_slider.setRange(0, 85)
        self._dim_slider.valueChanged.connect(self._on_dim_changed)
        lay.addWidget(self._dim_lbl)
        lay.addWidget(self._dim_slider)

        self._glow_lbl = QLabel()
        self._glow_lbl.setStyleSheet(f"color: {p['TEXT_MED']}; background: transparent;")
        self._glow_slider = QSlider(Qt.Orientation.Horizontal)
        self._glow_slider.setRange(0, 100)
        self._glow_slider.valueChanged.connect(self._on_glow_changed)
        lay.addWidget(self._glow_lbl)
        lay.addWidget(self._glow_slider)

        lay.addStretch()
        scroll.setWidget(box)
        return scroll

    def _build_layout_tab(self) -> QWidget:
        p = self._pal()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        box = QWidget()
        box.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(box)
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setSpacing(12)

        lbl_p = QLabel("PRESETS DE ESPACIO DE TRABAJO")
        lbl_p.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        lbl_p.setStyleSheet(f"color: {p['TEXT_DIM']}; background: transparent;")
        lay.addWidget(lbl_p)

        p_grid = QGridLayout()
        p_grid.setSpacing(8)
        for idx, (pid, pmeta) in enumerate(LAYOUT_PRESETS.items()):
            b = QPushButton(f"{pmeta['label']}\n{pmeta['desc']}")
            b.setCheckable(True)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setFixedHeight(56)
            b.clicked.connect(lambda _=False, k=pid: self._apply_layout_preset(k))
            self._preset_btns[pid] = b
            p_grid.addWidget(b, idx // 2, idx % 2)
        lay.addLayout(p_grid)

        lbl_w = QLabel("VISIBILIDAD DE PANELES Y MÓDULOS")
        lbl_w.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        lbl_w.setStyleSheet(f"color: {p['TEXT_DIM']}; background: transparent;")
        lay.addWidget(lbl_w)

        w_grid = QGridLayout()
        w_grid.setSpacing(8)
        items = [
            ("__left_panel", "Mostrar barra lateral izquierda"),
            ("__right_panel", "Mostrar panel derecho (Chat)"),
            ("voice_monitor", "Módulo: Voz y Presencia"),
            ("weather", "Módulo: Clima Local"),
            ("system_metrics", "Módulo: Diagnóstico del Equipo"),
            ("news_panel", "Módulo: Noticias / Contenido Central"),
            ("attachments", "Módulo: Contexto Adjunto"),
        ]
        for idx, (key, text) in enumerate(items):
            chk = QCheckBox(text)
            chk.setStyleSheet(f"color: {p['TEXT']}; background: transparent;")
            chk.toggled.connect(lambda val, k=key: self._on_widget_toggled(k, val))
            self._widget_checks[key] = chk
            w_grid.addWidget(chk, idx // 2, idx % 2)
        lay.addLayout(w_grid)

        lbl_s = QLabel("ANCHO DE COLUMNAS LATERALES")
        lbl_s.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        lbl_s.setStyleSheet(f"color: {p['TEXT_DIM']}; background: transparent;")
        lay.addWidget(lbl_s)

        self._left_w_lbl = QLabel()
        self._left_w_lbl.setStyleSheet(f"color: {p['TEXT_MED']}; background: transparent;")
        self._left_slider = QSlider(Qt.Orientation.Horizontal)
        self._left_slider.setRange(220, 340)
        self._left_slider.valueChanged.connect(lambda v: self._on_width_changed("left_width", v))

        self._right_w_lbl = QLabel()
        self._right_w_lbl.setStyleSheet(f"color: {p['TEXT_MED']}; background: transparent;")
        self._right_slider = QSlider(Qt.Orientation.Horizontal)
        self._right_slider.setRange(290, 440)
        self._right_slider.valueChanged.connect(lambda v: self._on_width_changed("right_width", v))

        lay.addWidget(self._left_w_lbl)
        lay.addWidget(self._left_slider)
        lay.addWidget(self._right_w_lbl)
        lay.addWidget(self._right_slider)

        lay.addStretch()
        scroll.setWidget(box)
        return scroll

    def _style_toggle_btn(self, btn: QPushButton, active: bool) -> None:
        p = self._pal()
        if active:
            btn.setStyleSheet(
                f"QPushButton {{ background: {p['PRI_GHO']}; color: {p['PRI']}; border: 1px solid {p['PRI']}; border-radius: 8px; padding: 4px 10px; font-weight: 700; text-align: left; }}"
            )
        else:
            btn.setStyleSheet(
                f"QPushButton {{ background: {p['PANEL2']}; color: {p['TEXT_MED']}; border: 1px solid {p['BORDER']}; border-radius: 8px; padding: 4px 10px; text-align: left; }}"
                f"QPushButton:hover {{ color: {p['WHITE']}; border-color: {p['BORDER_B']}; }}"
            )

    def _sync_controls_from_cfg(self) -> None:
        self._building = True
        tid = self._cfg.get("theme_id", "obsidian_pro")
        for k, card in self._theme_cards.items():
            card.set_active(k == tid)

        for k, b in self._density_btns.items():
            act = k == self._cfg.get("density", "balanced")
            b.setChecked(act)
            self._style_toggle_btn(b, act)

        for rv, b in self._radius_btns.items():
            act = rv == int(self._cfg.get("card_radius", 12))
            b.setChecked(act)
            self._style_toggle_btn(b, act)

        for pid, b in self._preset_btns.items():
            act = pid == self._cfg.get("layout_preset", "studio")
            b.setChecked(act)
            self._style_toggle_btn(b, act)

        cur_bg = self._cfg.get("bg_mode", "aurora_atmos")
        for bid, b in self._bg_btns.items():
            act = bid == cur_bg
            b.setChecked(act)
            self._style_toggle_btn(b, act)

        cpath = str(self._cfg.get("bg_custom_path") or "").strip()
        if cpath:
            from pathlib import Path as _P
            self._custom_bg_lbl.setText(f"Imagen propia: {_P(cpath).name}")
        else:
            self._custom_bg_lbl.setText("Imagen propia: ninguna seleccionada")

        dim_pct = int(round(float(self._cfg.get("bg_dim", 0.42)) * 100))
        glow_pct = int(round(float(self._cfg.get("bg_glow", 0.65)) * 100))
        self._dim_slider.setValue(dim_pct)
        self._glow_slider.setValue(glow_pct)
        self._dim_lbl.setText(f"Oscurecimiento de fondo fotográfico: {dim_pct}%")
        self._glow_lbl.setText(f"Intensidad de luz ambiental / aurora: {glow_pct}%")

        self._chk_glow.setChecked(bool(self._cfg.get("glass_glow", True)))
        self._chk_grid.setChecked(bool(self._cfg.get("hud_grid", True)))

        widgets = self._cfg.get("widgets", {})
        self._widget_checks["__left_panel"].setChecked(bool(self._cfg.get("show_left_panel", True)))
        self._widget_checks["__right_panel"].setChecked(bool(self._cfg.get("show_right_panel", True)))
        for wk in ("voice_monitor", "weather", "system_metrics", "news_panel", "attachments"):
            self._widget_checks[wk].setChecked(bool(widgets.get(wk, True)))

        lw = int(self._cfg.get("left_width", 266))
        rw = int(self._cfg.get("right_width", 356))
        self._left_slider.setValue(lw)
        self._right_slider.setValue(rw)
        self._left_w_lbl.setText(f"Ancho panel izquierdo: {lw} px")
        self._right_w_lbl.setText(f"Ancho panel derecho (Chat): {rw} px")
        self._building = False

    def _emit_preview(self) -> None:
        if not self._building:
            self.config_changed.emit(deepcopy(self._cfg), False)

    def _on_theme_selected(self, theme_id: str) -> None:
        self._cfg["theme_id"] = theme_id
        self._cfg["accent_override"] = ""
        self._sync_controls_from_cfg()
        self._apply_chrome_style()
        self._emit_preview()

    def _on_bg_selected(self, bg_id: str) -> None:
        self._cfg["bg_mode"] = bg_id
        self._sync_controls_from_cfg()
        self._emit_preview()

    def _pick_custom_bg(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar fondo personalizado",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.webp *.bmp)",
        )
        if path:
            self._cfg["bg_custom_path"] = path
            self._cfg["bg_mode"] = "custom_image"
            self._sync_controls_from_cfg()
            self._emit_preview()

    def _on_dim_changed(self, val: int) -> None:
        self._cfg["bg_dim"] = round(val / 100.0, 2)
        self._dim_lbl.setText(f"Oscurecimiento de fondo fotográfico: {val}%")
        self._emit_preview()

    def _on_glow_changed(self, val: int) -> None:
        self._cfg["bg_glow"] = round(val / 100.0, 2)
        self._glow_lbl.setText(f"Intensidad de luz ambiental / aurora: {val}%")
        self._emit_preview()

    def _pick_accent_color(self) -> None:
        cur = self._pal()["PRI"]
        col = QColorDialog.getColor(QColor(cur), self, "Elegir color de acento")
        if col.isValid():
            self._cfg["accent_override"] = col.name().upper()
            self._sync_controls_from_cfg()
            self._emit_preview()

    def _clear_accent_override(self) -> None:
        self._cfg["accent_override"] = ""
        self._sync_controls_from_cfg()
        self._emit_preview()

    def _on_density_selected(self, density: str) -> None:
        self._cfg["density"] = density
        self._sync_controls_from_cfg()
        self._emit_preview()

    def _on_radius_selected(self, radius: int) -> None:
        self._cfg["card_radius"] = radius
        self._sync_controls_from_cfg()
        self._emit_preview()

    def _set_flag(self, key: str, value: bool) -> None:
        self._cfg[key] = bool(value)
        self._emit_preview()

    def _apply_layout_preset(self, preset_id: str) -> None:
        preset = LAYOUT_PRESETS.get(preset_id)
        if not preset:
            return
        self._cfg["layout_preset"] = preset_id
        self._cfg["show_left_panel"] = preset["show_left_panel"]
        self._cfg["show_right_panel"] = preset["show_right_panel"]
        self._cfg["left_width"] = preset["left_width"]
        self._cfg["right_width"] = preset["right_width"]
        self._cfg["widgets"] = dict(preset["widgets"])
        self._sync_controls_from_cfg()
        self._emit_preview()

    def _on_widget_toggled(self, key: str, val: bool) -> None:
        if self._building:
            return
        if key == "__left_panel":
            self._cfg["show_left_panel"] = bool(val)
        elif key == "__right_panel":
            self._cfg["show_right_panel"] = bool(val)
        else:
            self._cfg.setdefault("widgets", {})[key] = bool(val)
        self._cfg["layout_preset"] = "custom"
        self._sync_controls_from_cfg()
        self._emit_preview()

    def _on_width_changed(self, key: str, val: int) -> None:
        self._cfg[key] = int(val)
        if key == "left_width":
            self._left_w_lbl.setText(f"Ancho panel izquierdo: {val} px")
        else:
            self._right_w_lbl.setText(f"Ancho panel derecho (Chat): {val} px")
        self._emit_preview()

    def _reset_defaults(self) -> None:
        self._cfg = deepcopy(DEFAULT_HUD_CONFIG)
        self._sync_controls_from_cfg()
        self._apply_chrome_style()
        self.config_changed.emit(deepcopy(self._cfg), True)

    def _save_and_close(self) -> None:
        self.config_changed.emit(deepcopy(self._cfg), True)
        self.closed.emit()
