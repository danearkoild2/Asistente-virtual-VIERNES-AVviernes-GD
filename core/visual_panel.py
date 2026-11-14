"""
Viernes — Edith Contextual Visual Intelligence Panel
====================================================
Dynamic, elegant, glassmorphic visual card positioned to the right of Edith.
Displays high-resolution imagery, title, category, concise summary, highlighted
interesting fact ("Dato Clave"), interactive thumbnail switcher, and source links.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from PyQt6.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QRect,
    QSize,
    Qt,
    QTimer,
    QUrl,
    pyqtProperty,
    pyqtSignal,
)
from PyQt6.QtGui import (
    QColor,
    QCursor,
    QDesktopServices,
    QFont,
    QIcon,
    QImage,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from core.visual_engine import VisualCardData

logger = logging.getLogger("Viernes.VisualPanel")


class ClickableImageLabel(QLabel):
    """Clickable thumbnail image with hover glow and selection border."""

    clicked = pyqtSignal(int)

    def __init__(self, index: int, parent=None):
        super().__init__(parent)
        self.index = index
        self.is_selected = False
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedSize(94, 60)
        self.setScaledContents(False)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._pixmap_orig: Optional[QPixmap] = None
        self._update_style()

    def set_thumbnail(self, pixmap: QPixmap, selected: bool = False):
        self._pixmap_orig = pixmap
        self.is_selected = selected
        self._render_rounded()
        self._update_style()

    def set_selected(self, selected: bool):
        self.is_selected = selected
        self._render_rounded()
        self._update_style()

    def _render_rounded(self):
        if not self._pixmap_orig or self._pixmap_orig.isNull():
            return
        w, h = self.width(), self.height()
        scaled = self._pixmap_orig.scaled(
            w, h,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        # Center-crop to fill w x h
        crop_x = max(0, (scaled.width() - w) // 2)
        crop_y = max(0, (scaled.height() - h) // 2)
        cropped = scaled.copy(crop_x, crop_y, w, h)

        # Rounded mask
        rounded = QPixmap(w, h)
        rounded.fill(Qt.GlobalColor.transparent)
        p = QPainter(rounded)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        path = QPainterPath()
        path.addRoundedRect(0, 0, w, h, 6, 6)
        p.setClipPath(path)
        p.drawPixmap(0, 0, cropped)
        p.end()

        self.setPixmap(rounded)

    def _update_style(self):
        border_col = "#6E6AF6" if self.is_selected else "#272730"
        bg_col = "#1E1D36" if self.is_selected else "#111114"
        self.setStyleSheet(f"""
            ClickableImageLabel {{
                border: 2px solid {border_col};
                border-radius: 6px;
                background: {bg_col};
            }}
            ClickableImageLabel:hover {{
                border: 2px solid #6E6AF6;
                background: #1F1F26;
            }}
        """)

    def mousePressEvent(self, ev):
        if ev.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.index)
        super().mousePressEvent(ev)


class EdithVisualPanel(QWidget):
    """
    Contextual Visual Panel positioned to the right of Edith.
    Features glassmorphism, responsive thumbnails, high-res presentation,
    summary, highlighted trivia pill, and smooth entrance/exit animations.
    """

    panel_closed = pyqtSignal()
    image_swapped = pyqtSignal(int)

    # Panel geometry bounds
    DEFAULT_W = 390
    MIN_W = 320
    MAX_W = 440

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("EdithVisualPanel")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.hide()

        self._card_data: Optional[VisualCardData] = None
        self._current_img_idx: int = 0
        self._thumb_widgets: List[ClickableImageLabel] = []
        self._pinned: bool = False  # By default unpinned, counts down after speech
        self._drag_pos: Optional[QPoint] = None

        # 5-second countdown timer after speech finishes
        self._countdown_timer = QTimer(self)
        self._countdown_timer.setInterval(1000)
        self._countdown_timer.timeout.connect(self._on_countdown_tick)
        self._countdown_remaining: int = 5
        self._waiting_for_speech: bool = False
        self._countdown_paused: bool = False

        self._auto_close_timer = QTimer(self)
        self._auto_close_timer.setSingleShot(True)
        self._auto_close_timer.setInterval(60000)
        self._auto_close_timer.timeout.connect(self.animate_hide)

        # Opacity effect for animations
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self._opacity_effect)

        # Entrance/exit property animations
        self._fade_anim = QPropertyAnimation(self._opacity_effect, b"opacity")
        self._fade_anim.setDuration(280)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._pos_anim = QPropertyAnimation(self, b"pos")
        self._pos_anim.setDuration(300)
        self._pos_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._setup_ui()

    def _setup_ui(self):
        # Clean editorial card with subtle warm carbon border
        self.setStyleSheet("""
            QWidget#EdithVisualPanel {
                background: rgba(23, 23, 28, 0.96);
                border: 1px solid #272730;
                border-radius: 14px;
            }
            QLabel {
                color: #EEEEF0;
                background: transparent;
            }
        """)

        main_lay = QVBoxLayout(self)
        main_lay.setContentsMargins(14, 12, 14, 12)
        main_lay.setSpacing(9)

        # ── 1. HEADER (Category + Title + Action buttons) ────────────────────
        hdr_top = QHBoxLayout()
        hdr_top.setContentsMargins(0, 0, 0, 0)
        hdr_top.setSpacing(6)

        # Category pill
        self._cat_lbl = QLabel("Exploración visual")
        self._cat_lbl.setFont(QFont("Segoe UI", 8, QFont.Weight.DemiBold))
        self._cat_lbl.setStyleSheet("""
            color: #6E6AF6;
            background: #1E1D36;
            border: 1px solid #6E6AF6;
            border-radius: 6px;
            padding: 2px 8px;
        """)
        hdr_top.addWidget(self._cat_lbl)
        hdr_top.addStretch(1)

        # Pin / Unpin button (Keep open permanently)
        self._btn_pin = QPushButton("📌")
        self._btn_pin.setFixedSize(24, 24)
        self._btn_pin.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._btn_pin.clicked.connect(self._toggle_pin)
        self._update_pin_style()
        hdr_top.addWidget(self._btn_pin)

        # Open in browser button
        self._btn_link = QPushButton("↗")
        self._btn_link.setToolTip("Abrir imagen en navegador")
        self._btn_link.setFixedSize(24, 24)
        self._btn_link.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._btn_link.setStyleSheet("""
            QPushButton {
                background: #1F1F26;
                border: 1px solid #272730;
                border-radius: 6px;
                color: #A0A0AB;
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #1E1D36;
                border-color: #6E6AF6;
                color: #FAF9F6;
            }
        """)
        self._btn_link.clicked.connect(self._open_in_browser)
        hdr_top.addWidget(self._btn_link)

        # Close button
        self._btn_close = QPushButton("✕")
        self._btn_close.setToolTip("Cerrar tarjeta")
        self._btn_close.setFixedSize(24, 24)
        self._btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._btn_close.setStyleSheet("""
            QPushButton {
                background: #1F1F26;
                border: 1px solid #272730;
                border-radius: 6px;
                color: #A0A0AB;
                font-family: 'Segoe UI', sans-serif;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #3A1F24;
                border-color: #F87171;
                color: #F87171;
            }
        """)
        self._btn_close.clicked.connect(self.animate_hide)
        hdr_top.addWidget(self._btn_close)

        main_lay.addLayout(hdr_top)

        # Title Label
        self._title_lbl = QLabel("Machu Picchu")
        self._title_lbl.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self._title_lbl.setStyleSheet("color: #FAF9F6; padding-left: 2px;")
        self._title_lbl.setWordWrap(True)
        main_lay.addWidget(self._title_lbl)

        # ── 2. MAIN IMAGE DISPLAY ────────────────────────────────────────────
        self._main_img_container = QFrame(self)
        self._main_img_container.setMinimumHeight(190)
        self._main_img_container.setMaximumHeight(230)
        self._main_img_container.setStyleSheet("""
            QFrame {
                background: #0C0C0E;
                border: 1px solid #272730;
                border-radius: 10px;
            }
        """)
        img_lay = QVBoxLayout(self._main_img_container)
        img_lay.setContentsMargins(3, 3, 3, 3)

        self._main_img_lbl = QLabel(self._main_img_container)
        self._main_img_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._main_img_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._main_img_lbl.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._main_img_lbl.mousePressEvent = lambda ev: self._on_next_image()
        self._main_img_lbl.setToolTip("Haz clic para ver la siguiente imagen")
        img_lay.addWidget(self._main_img_lbl)

        main_lay.addWidget(self._main_img_container)

        # ── 3. THUMBNAIL GALLERY & NAVIGATION ROW ────────────────────────────
        self._thumbs_row = QHBoxLayout()
        self._thumbs_row.setContentsMargins(0, 0, 0, 0)
        self._thumbs_row.setSpacing(6)

        # Prev button
        self._btn_prev_img = QPushButton("◀")
        self._btn_prev_img.setFixedSize(22, 54)
        self._btn_prev_img.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._btn_prev_img.setToolTip("Imagen anterior")
        self._btn_prev_img.setStyleSheet("""
            QPushButton {
                background: rgba(0, 212, 255, 0.10);
                border: 1px solid rgba(0, 212, 255, 0.25);
                border-radius: 4px;
                color: #00d4ff;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(0, 212, 255, 0.30);
                border-color: #00e5ff;
                color: #ffffff;
            }
        """)
        self._btn_prev_img.clicked.connect(self._on_prev_image)
        self._thumbs_row.addWidget(self._btn_prev_img)

        for i in range(4):
            thumb_btn = ClickableImageLabel(i, self)
            thumb_btn.clicked.connect(self._on_thumbnail_clicked)
            self._thumb_widgets.append(thumb_btn)
            self._thumbs_row.addWidget(thumb_btn)

        # Next button
        self._btn_next_img = QPushButton("▶")
        self._btn_next_img.setFixedSize(22, 54)
        self._btn_next_img.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._btn_next_img.setToolTip("Siguiente imagen")
        self._btn_next_img.setStyleSheet("""
            QPushButton {
                background: rgba(0, 212, 255, 0.10);
                border: 1px solid rgba(0, 212, 255, 0.25);
                border-radius: 4px;
                color: #00d4ff;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(0, 212, 255, 0.30);
                border-color: #00e5ff;
                color: #ffffff;
            }
        """)
        self._btn_next_img.clicked.connect(self._on_next_image)
        self._thumbs_row.addWidget(self._btn_next_img)

        self._thumbs_row.addStretch(1)

        # Counter label
        self._counter_lbl = QLabel("1 / 1")
        self._counter_lbl.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        self._counter_lbl.setStyleSheet("""
            color: #38bdf8;
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 4px;
            padding: 3px 7px;
        """)
        self._thumbs_row.addWidget(self._counter_lbl)

        main_lay.addLayout(self._thumbs_row)

        # ── 4. SUMMARY TEXT ──────────────────────────────────────────────────
        self._summary_lbl = QLabel("")
        self._summary_lbl.setFont(QFont("Segoe UI", 9))
        self._summary_lbl.setStyleSheet("""
            color: #c8e2f8;
            line-height: 1.4;
            padding: 3px 2px;
        """)
        self._summary_lbl.setWordWrap(True)
        main_lay.addWidget(self._summary_lbl)

        # ── 5. HIGHLIGHTED FACT BOX ("💡 DATO CLAVE") ────────────────────────
        self._fact_box = QFrame(self)
        self._fact_box.setStyleSheet("""
            QFrame {
                background: rgba(0, 229, 255, 0.08);
                border-left: 3px solid #00e5ff;
                border-radius: 4px;
                padding: 6px 10px;
            }
        """)
        fact_lay = QVBoxLayout(self._fact_box)
        fact_lay.setContentsMargins(8, 6, 8, 6)
        fact_lay.setSpacing(3)

        fact_tag = QLabel("💡  DATO CLAVE")
        fact_tag.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        fact_tag.setStyleSheet("color: #00e5ff; letter-spacing: 0.5px;")
        fact_lay.addWidget(fact_tag)

        self._fact_lbl = QLabel("")
        self._fact_lbl.setFont(QFont("Segoe UI", 9))
        self._fact_lbl.setStyleSheet("color: #e6f5ff; line-height: 1.35;")
        self._fact_lbl.setWordWrap(True)
        fact_lay.addWidget(self._fact_lbl)

        main_lay.addWidget(self._fact_box)

        # ── 5.5 COUNTDOWN BAR (Auto-close after speech unless cancelled/pinned) ────
        self._countdown_bar = QFrame(self)
        self._countdown_bar.setFixedHeight(32)
        self._countdown_bar.setStyleSheet("""
            QFrame {
                background: rgba(8, 20, 32, 0.90);
                border: 1px solid rgba(0, 229, 255, 0.40);
                border-radius: 6px;
            }
        """)
        c_lay = QHBoxLayout(self._countdown_bar)
        c_lay.setContentsMargins(10, 2, 10, 2)
        c_lay.setSpacing(8)

        self._countdown_lbl = QLabel("⏱  Cerrando en 5 s...")
        self._countdown_lbl.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self._countdown_lbl.setStyleSheet("color: #38bdf8; background: transparent;")
        c_lay.addWidget(self._countdown_lbl)

        c_lay.addStretch(1)

        self._btn_cancel_countdown = QPushButton("Mantener abierta")
        self._btn_cancel_countdown.setFixedHeight(22)
        self._btn_cancel_countdown.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        self._btn_cancel_countdown.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._btn_cancel_countdown.setToolTip("Cancelar autocierre y mantener la tarjeta fijada")
        self._btn_cancel_countdown.setStyleSheet("""
            QPushButton {
                background: rgba(0, 229, 255, 0.16);
                border: 1px solid #00e5ff;
                border-radius: 4px;
                color: #00ffff;
                padding: 0 10px;
            }
            QPushButton:hover {
                background: rgba(0, 229, 255, 0.38);
                color: #ffffff;
                border-color: #ffffff;
            }
        """)
        self._btn_cancel_countdown.clicked.connect(self._cancel_close_countdown)
        c_lay.addWidget(self._btn_cancel_countdown)

        main_lay.addWidget(self._countdown_bar)
        self._countdown_bar.hide()

        # ── 6. FOOTER (Source & Timestamp) ───────────────────────────────────
        ftr_lay = QHBoxLayout()
        ftr_lay.setContentsMargins(2, 0, 2, 0)

        self._source_lbl = QLabel("SerpAPI • Google Images")
        self._source_lbl.setFont(QFont("Segoe UI", 8))
        self._source_lbl.setStyleSheet("color: rgba(140, 180, 210, 0.65);")
        ftr_lay.addWidget(self._source_lbl)

        ftr_lay.addStretch(1)

        hint_lbl = QLabel("Click en miniaturas para cambiar")
        hint_lbl.setFont(QFont("Segoe UI", 8))
        hint_lbl.setStyleSheet("color: rgba(0, 212, 255, 0.55);")
        ftr_lay.addWidget(hint_lbl)

        main_lay.addLayout(ftr_lay)

    def display_card(self, card: VisualCardData, target_x: int, target_y: int, speech_active: bool = False):
        """Populates and smoothly displays the visual panel."""
        self._card_data = card
        self._current_img_idx = 0

        # Fresh card starts unpinned so it auto-closes after speech unless kept open
        self._pinned = False
        self._update_pin_style()
        self._countdown_timer.stop()
        self._countdown_bar.hide()
        self._countdown_paused = False

        # Dynamic theme color based on category and source platform
        cat_upper = card.category.upper()
        if "SPOTIFY" in cat_upper:
            c_accent = "#1ed760"
            c_bg = "rgba(30, 215, 96, 0.18)"
            c_border = "rgba(30, 215, 96, 0.60)"
            border_glow = "rgba(30, 215, 96, 0.40)"
        elif "YOUTUBE" in cat_upper:
            c_accent = "#ff3344"
            c_bg = "rgba(255, 0, 51, 0.20)"
            c_border = "rgba(255, 0, 51, 0.65)"
            border_glow = "rgba(255, 0, 51, 0.45)"
        elif "BRAVE" in cat_upper:
            c_accent = "#ff5500"
            c_bg = "rgba(255, 85, 0, 0.20)"
            c_border = "rgba(255, 85, 0, 0.60)"
            border_glow = "rgba(255, 85, 0, 0.40)"
        elif "VLC" in cat_upper:
            c_accent = "#ff9900"
            c_bg = "rgba(255, 153, 0, 0.20)"
            c_border = "rgba(255, 153, 0, 0.60)"
            border_glow = "rgba(255, 153, 0, 0.40)"
        elif "WINDOWS MEDIA" in cat_upper:
            c_accent = "#00bcf2"
            c_bg = "rgba(0, 188, 242, 0.18)"
            c_border = "rgba(0, 188, 242, 0.55)"
            border_glow = "rgba(0, 188, 242, 0.40)"
        else:
            c_accent = "#00e5ff"
            c_bg = "rgba(0, 229, 255, 0.12)"
            c_border = "rgba(0, 229, 255, 0.35)"
            border_glow = "rgba(0, 212, 255, 0.45)"

        self.setStyleSheet(f"""
            QWidget#EdithVisualPanel {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(4, 16, 26, 0.94),
                    stop: 0.5 rgba(3, 12, 20, 0.95),
                    stop: 1 rgba(1, 8, 14, 0.96)
                );
                border: 1px solid {border_glow};
                border-radius: 12px;
            }}
            QLabel {{
                color: #e0f2fe;
                background: transparent;
            }}
        """)

        self._cat_lbl.setStyleSheet(f"""
            color: {c_accent};
            background: {c_bg};
            border: 1px solid {c_border};
            border-radius: 4px;
            padding: 2px 8px;
            letter-spacing: 0.5px;
            font-weight: bold;
        """)

        # Update texts
        self._cat_lbl.setText(card.category.upper())
        self._title_lbl.setText(card.topic)
        self._summary_lbl.setText(card.summary)
        self._fact_lbl.setText(card.interesting_fact)
        self._source_lbl.setText(f"Fuente: {card.source}")

        # Populate thumbnails
        images = card.images or []
        for i, thumb_widget in enumerate(self._thumb_widgets):
            if i < len(images):
                img_data = images[i]
                path = img_data.get("local_thumb") or img_data.get("local_path")
                if path and Path(path).exists():
                    pm = QPixmap(str(path))
                    thumb_widget.set_thumbnail(pm, selected=(i == 0))
                    thumb_widget.show()
                else:
                    thumb_widget.hide()
            else:
                thumb_widget.hide()

        # Load main image
        self._load_main_image(0)

        # Animate entrance
        self._animate_show(target_x, target_y)

        # Speech-aware countdown:
        # If assistant is currently speaking, wait for speech completion before counting down 5s.
        if speech_active:
            self._waiting_for_speech = True
        else:
            self._waiting_for_speech = False
            self._start_close_countdown(5)

    def notify_speech_finished(self):
        """Called when VIERNES finishes speaking. Starts the 5-second countdown to auto-close."""
        if not self.isVisible() or self._pinned:
            return
        self._start_close_countdown(5)

    def _start_close_countdown(self, seconds: int = 5):
        """Initiates the 5-second auto-close countdown with an interactive cancel button."""
        if self._pinned:
            return
        self._waiting_for_speech = False
        self._countdown_remaining = seconds
        self._countdown_lbl.setText(f"⏱  Cerrando en {self._countdown_remaining} s...")
        self._countdown_bar.show()
        self._countdown_timer.stop()
        self._countdown_timer.start(1000)

    def _on_countdown_tick(self):
        """Countdown tick handler."""
        if self._pinned or not self.isVisible():
            self._countdown_timer.stop()
            self._countdown_bar.hide()
            return
        self._countdown_remaining -= 1
        if self._countdown_remaining > 0:
            self._countdown_lbl.setText(f"⏱  Cerrando en {self._countdown_remaining} s...")
        else:
            self._countdown_timer.stop()
            self._countdown_bar.hide()
            self.animate_hide()

    def _cancel_close_countdown(self):
        """Cancels countdown and keeps card pinned open indefinitely."""
        self._countdown_timer.stop()
        self._countdown_bar.hide()
        self._pinned = True
        self._update_pin_style()

    def _toggle_pin(self):
        """Toggle pin state. When pinned, the card stays open indefinitely."""
        self._pinned = not self._pinned
        self._update_pin_style()
        if self._pinned:
            self._countdown_timer.stop()
            self._countdown_bar.hide()
            self._auto_close_timer.stop()
        else:
            self._start_close_countdown(5)

    def _update_pin_style(self):
        """Update visual styling and tooltip for the pin toggle button."""
        if self._pinned:
            self._btn_pin.setStyleSheet("""
                QPushButton {
                    background: rgba(0, 229, 255, 0.25);
                    border: 1px solid #00e5ff;
                    border-radius: 12px;
                    color: #00ffff;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background: rgba(0, 229, 255, 0.45);
                    border-color: #ffffff;
                }
            """)
            self._btn_pin.setToolTip("Fijado permanente (No se cerrará solo). Haz clic para desfijar")
        else:
            self._btn_pin.setStyleSheet("""
                QPushButton {
                    background: rgba(148, 163, 184, 0.12);
                    border: 1px solid rgba(148, 163, 184, 0.3);
                    border-radius: 12px;
                    color: #94a3b8;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background: rgba(0, 229, 255, 0.20);
                    border-color: #00e5ff;
                    color: #00e5ff;
                }
            """)
            self._btn_pin.setToolTip("Desfijado (Se cerrará tras inactividad). Haz clic para fijar")

    def _on_prev_image(self):
        """Cycle to the previous image in the gallery."""
        if not self._card_data or not self._card_data.images:
            return
        total = len(self._card_data.images)
        if total <= 1:
            return
        new_idx = (self._current_img_idx - 1) % total
        self._load_main_image(new_idx)
        # Interacting with gallery keeps card open
        self._cancel_close_countdown()

    def _on_next_image(self):
        """Cycle to the next image in the gallery."""
        if not self._card_data or not self._card_data.images:
            return
        total = len(self._card_data.images)
        if total <= 1:
            return
        new_idx = (self._current_img_idx + 1) % total
        self._load_main_image(new_idx)
        # Interacting with gallery keeps card open
        self._cancel_close_countdown()

    def _load_main_image(self, index: int):
        if not self._card_data or not self._card_data.images:
            return
        if index < 0 or index >= len(self._card_data.images):
            return

        self._current_img_idx = index
        total_images = len(self._card_data.images)
        self._counter_lbl.setText(f"{index + 1} / {total_images}")

        img_data = self._card_data.images[index]
        path = img_data.get("local_path") or img_data.get("local_thumb")

        # Highlight thumbnail
        for i, thumb_w in enumerate(self._thumb_widgets):
            thumb_w.set_selected(i == index)

        if path and Path(path).exists():
            pm = QPixmap(str(path))
            if not pm.isNull():
                target_w = max(340, self.width() - 36)
                target_h = 205

                scaled = pm.scaled(
                    target_w, target_h,
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )
                crop_x = max(0, (scaled.width() - target_w) // 2)
                crop_y = max(0, (scaled.height() - target_h) // 2)
                cropped = scaled.copy(crop_x, crop_y, target_w, target_h)

                rounded = QPixmap(target_w, target_h)
                rounded.fill(Qt.GlobalColor.transparent)
                p = QPainter(rounded)
                p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
                p_path = QPainterPath()
                p_path.addRoundedRect(0, 0, target_w, target_h, 8, 8)
                p.setClipPath(p_path)
                p.drawPixmap(0, 0, cropped)
                p.end()

                self._main_img_lbl.setPixmap(rounded)
                self.image_swapped.emit(index)
                return

        # Fallback placeholder
        self._main_img_lbl.setText("Cargando imagen...")

    def _on_thumbnail_clicked(self, index: int):
        self._load_main_image(index)
        # Interacting with gallery cancels auto-close countdown and keeps card pinned
        self._cancel_close_countdown()

    def _open_in_browser(self):
        if not self._card_data or not self._card_data.images:
            return
        img = self._card_data.images[self._current_img_idx]
        url = img.get("url") or img.get("thumb")
        if url:
            QDesktopServices.openUrl(QUrl(url))

    def _animate_show(self, target_x: int, target_y: int):
        """Smoothly slides in from right + fades in."""
        try:
            self._fade_anim.finished.disconnect()
        except Exception:
            pass

        self.show()
        self.raise_()

        # Start slightly to the right
        start_x = target_x + 40
        self.move(start_x, target_y)

        # Position slide animation
        self._pos_anim.stop()
        self._pos_anim.setStartValue(QPoint(start_x, target_y))
        self._pos_anim.setEndValue(QPoint(target_x, target_y))
        self._pos_anim.start()

        # Fade in animation
        self._fade_anim.stop()
        self._fade_anim.setStartValue(0.0)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.start()

    def animate_hide(self):
        """Smoothly fades out and slides right."""
        if not self.isVisible():
            return
        self._countdown_timer.stop()
        self._countdown_bar.hide()
        self._auto_close_timer.stop()

        cur_pos = self.pos()
        end_pos = QPoint(cur_pos.x() + 45, cur_pos.y())

        self._pos_anim.stop()
        self._pos_anim.setStartValue(cur_pos)
        self._pos_anim.setEndValue(end_pos)
        self._pos_anim.start()

        self._fade_anim.stop()
        self._fade_anim.setStartValue(1.0)
        self._fade_anim.setEndValue(0.0)

        def _on_fade_finished():
            self.hide()
            self.panel_closed.emit()

        try:
            self._fade_anim.finished.disconnect()
        except Exception:
            pass
        self._fade_anim.finished.connect(_on_fade_finished)
        self._fade_anim.start()

    def mousePressEvent(self, ev):
        """Allow dragging the card freely across the screen from the header."""
        if ev.button() == Qt.MouseButton.LeftButton:
            if ev.position().y() <= 70:
                self._drag_pos = ev.globalPosition().toPoint() - self.pos()
                ev.accept()
                return
        super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev):
        if self._drag_pos is not None and ev.buttons() == Qt.MouseButton.LeftButton:
            self.move(ev.globalPosition().toPoint() - self._drag_pos)
            ev.accept()
            return
        super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev):
        self._drag_pos = None
        super().mouseReleaseEvent(ev)

    def enterEvent(self, ev):
        # Pause countdown and auto-close while user is hovering/reading
        if self._countdown_timer.isActive():
            self._countdown_paused = True
            self._countdown_timer.stop()
            self._countdown_lbl.setText(f"⏱  Pausado ({self._countdown_remaining} s)")
        self._auto_close_timer.stop()
        super().enterEvent(ev)

    def leaveEvent(self, ev):
        # Resume countdown if it was paused and not pinned
        if getattr(self, "_countdown_paused", False) and not self._pinned and self._countdown_remaining > 0:
            self._countdown_paused = False
            self._countdown_lbl.setText(f"⏱  Cerrando en {self._countdown_remaining} s...")
            self._countdown_timer.start(1000)
        elif not self._pinned:
            self._auto_close_timer.start()
        super().leaveEvent(ev)
