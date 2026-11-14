from __future__ import annotations

import math
import random
from typing import Callable, Optional

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QLinearGradient, QPainter, QPen
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class _SpectrumCanvas(QWidget):
    """Animated multi-bar neon audio spectrum rendered at 30 FPS only while active."""

    def __init__(self, parent: Optional[QWidget] = None, bars: int = 36) -> None:
        super().__init__(parent)
        self._num_bars = bars
        self._levels = [0.08] * bars
        self._targets = [0.15] * bars
        self._phase = 0.0
        self._active = False
        self._muted = False

        self._timer = QTimer(self)
        self._timer.setInterval(33)  # ~30 FPS when active, 0% CPU when stopped
        self._timer.timeout.connect(self._tick)
        self.setMinimumHeight(140)

    def start(self) -> None:
        self._active = True
        if not self._timer.isActive():
            self._timer.start()
        self.update()

    def stop(self) -> None:
        self._active = False
        if self._timer.isActive():
            self._timer.stop()
        self._levels = [0.06] * self._num_bars
        self.update()

    def set_muted(self, muted: bool) -> None:
        self._muted = bool(muted)
        self.update()

    def _tick(self) -> None:
        if not self._active:
            return
        self._phase += 0.16
        center = (self._num_bars - 1) / 2.0
        for i in range(self._num_bars):
            dist = abs(i - center) / max(1.0, center)
            envelope = 1.0 - 0.55 * (dist ** 1.4)
            if self._muted:
                target = 0.06 + 0.03 * math.sin(self._phase + i * 0.4)
            else:
                wave = (
                    0.45
                    + 0.25 * math.sin(self._phase * 1.4 + i * 0.38)
                    + 0.18 * math.cos(self._phase * 0.9 - i * 0.61)
                    + random.uniform(-0.18, 0.24)
                )
                target = max(0.08, min(1.0, wave * envelope))
            self._targets[i] = target
            self._levels[i] += (self._targets[i] - self._levels[i]) * 0.34
        self.update()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        if w <= 10 or h <= 10:
            return

        # Subtle dark backdrop grid
        painter.fillRect(0, 0, w, h, QColor("#070b12"))
        grid_pen = QPen(QColor(0, 212, 255, 18), 1)
        painter.setPen(grid_pen)
        for y_step in range(24, h, 28):
            painter.drawLine(0, y_step, w, y_step)

        pad_x = 18
        pad_y = 14
        usable_w = max(1, w - 2 * pad_x)
        usable_h = max(1, h - 2 * pad_y)
        slot_w = usable_w / self._num_bars
        bar_w = max(3.0, slot_w * 0.62)

        for i, level in enumerate(self._levels):
            bar_h = max(6.0, level * usable_h)
            x = pad_x + i * slot_w + (slot_w - bar_w) / 2.0
            y = h - pad_y - bar_h

            grad = QLinearGradient(x, y, x, h - pad_y)
            if self._muted:
                grad.setColorAt(0.0, QColor("#64748b"))
                grad.setColorAt(1.0, QColor("#1e293b"))
            else:
                grad.setColorAt(0.0, QColor("#38bdf8"))
                grad.setColorAt(0.45, QColor("#06b6d4"))
                grad.setColorAt(1.0, QColor("#0f172a"))

            painter.setBrush(grad)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(int(x), int(y), int(bar_w), int(bar_h), 3, 3)

            # Peak cap glow
            cap_color = QColor("#94a3b8") if self._muted else QColor("#7dd3fc")
            painter.setBrush(cap_color)
            painter.drawRoundedRect(int(x), int(max(pad_y, y - 4)), int(bar_w), 3, 1, 1)


class RadioVisualizerWidget(QWidget):
    """HUD radio player panel with animated spectrum visualizer and quick controls."""

    randomRequested = pyqtSignal()
    stopRequested = pyqtSignal()

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        on_random: Optional[Callable[[], None]] = None,
        on_stop: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet("background: #070b12;")

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 16)
        root.setSpacing(10)

        header_row = QHBoxLayout()
        header_row.setSpacing(10)

        self._badge = QLabel("EN VIVO · RADIO")
        self._badge.setStyleSheet(
            "background: rgba(6, 182, 212, 0.16); color: #38bdf8;"
            "border: 1px solid rgba(56, 189, 248, 0.45); border-radius: 6px;"
            "padding: 3px 8px; font-size: 10px; font-weight: 700;"
        )
        header_row.addWidget(self._badge)
        header_row.addStretch(1)

        self._status_lbl = QLabel("AUDIO ACTIVO")
        self._status_lbl.setStyleSheet("color: #22c55e; font-size: 10px; font-weight: 700;")
        header_row.addWidget(self._status_lbl)
        root.addLayout(header_row)

        self._title_lbl = QLabel("Viernes Radio")
        self._title_lbl.setWordWrap(True)
        title_font = QFont()
        title_font.setPointSize(15)
        title_font.setBold(True)
        self._title_lbl.setFont(title_font)
        self._title_lbl.setStyleSheet("color: #f8fafc; background: transparent;")
        root.addWidget(self._title_lbl)

        self._subtitle_lbl = QLabel("Español · Streaming directo")
        self._subtitle_lbl.setWordWrap(True)
        self._subtitle_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; background: transparent;")
        root.addWidget(self._subtitle_lbl)

        self._canvas = _SpectrumCanvas(self)
        root.addWidget(self._canvas, stretch=1)

        footer = QHBoxLayout()
        footer.setSpacing(8)

        self._random_btn = QPushButton("Radio Random (ES)")
        self._random_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._random_btn.setStyleSheet(
            "QPushButton { background: rgba(14, 165, 233, 0.18); color: #38bdf8;"
            "border: 1px solid rgba(56, 189, 248, 0.45); border-radius: 6px;"
            "padding: 6px 12px; font-size: 11px; font-weight: 600; }"
            "QPushButton:hover { background: rgba(14, 165, 233, 0.30); }"
        )
        self._random_btn.clicked.connect(self.randomRequested.emit)
        if on_random is not None:
            self.randomRequested.connect(on_random)
        footer.addWidget(self._random_btn)

        footer.addStretch(1)

        self._stop_btn = QPushButton("Detener Radio")
        self._stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._stop_btn.setStyleSheet(
            "QPushButton { background: rgba(239, 68, 68, 0.18); color: #f87171;"
            "border: 1px solid rgba(248, 113, 113, 0.45); border-radius: 6px;"
            "padding: 6px 12px; font-size: 11px; font-weight: 600; }"
            "QPushButton:hover { background: rgba(239, 68, 68, 0.30); }"
        )
        self._stop_btn.clicked.connect(self.stopRequested.emit)
        if on_stop is not None:
            self.stopRequested.connect(on_stop)
        footer.addWidget(self._stop_btn)

        root.addLayout(footer)

    def set_station(self, title: str, subtitle: str = "", muted: bool = False) -> None:
        self._title_lbl.setText(title or "Viernes Radio")
        self._subtitle_lbl.setText(subtitle or "Español · Streaming directo")
        self.set_muted(muted)
        self._canvas.start()

    def set_muted(self, muted: bool) -> None:
        self._canvas.set_muted(muted)
        if muted:
            self._status_lbl.setText("SILENCIADO")
            self._status_lbl.setStyleSheet("color: #f59e0b; font-size: 10px; font-weight: 700;")
        else:
            self._status_lbl.setText("AUDIO ACTIVO")
            self._status_lbl.setStyleSheet("color: #22c55e; font-size: 10px; font-weight: 700;")

    def stop(self) -> None:
        self._canvas.stop()
