from __future__ import annotations

import math
from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QLinearGradient,
    QPainter,
    QPen,
    QRadialGradient,
)


def _qcol(hex_str: str, alpha: int = 255) -> QColor:
    c = QColor(hex_str)
    c.setAlpha(max(0, min(255, int(alpha))))
    return c


def paint_procedural_backdrop(
    p: QPainter,
    rect: QRectF,
    mode: str,
    bg_hex: str,
    panel_hex: str,
    pri_hex: str,
    acc_hex: str,
    tick: float,
    amp: float,
    speaking: bool,
    glow_strength: float = 0.65,
) -> None:
    """Render high-precision architectural & atmospheric procedural backdrops."""
    w = rect.width()
    h = rect.height()
    if w <= 4 or h <= 4:
        return

    cx = w * 0.5
    cy = h * 0.5
    glow_k = max(0.0, min(1.0, float(glow_strength)))
    voice_boost = 1.0 + min(0.85, amp * 1.4)

    # Base deep gradient using active theme surface tokens
    base = QLinearGradient(0, 0, 0, h)
    base.setColorAt(0.0, _qcol(panel_hex))
    base.setColorAt(0.55, _qcol(bg_hex))
    base.setColorAt(1.0, QColor("#050609"))
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QBrush(base))
    p.drawRect(rect)

    primary = acc_hex if speaking else pri_hex
    secondary = pri_hex if speaking else acc_hex

    if mode == "aurora_atmos":
        # Soft dual-lobe atmospheric aurora waves
        for idx, (col_hex, speed, x_off, y_off, rad_k) in enumerate(
            (
                (primary, 0.018, 0.34, 0.32, 0.65),
                (secondary, 0.013, 0.68, 0.56, 0.58),
                (primary, 0.022, 0.50, 0.85, 0.48),
            )
        ):
            ox = cx * (x_off + 0.14 * math.sin(tick * speed + idx * 1.7)) * 2.0
            oy = h * (y_off + 0.07 * math.cos(tick * speed * 1.3 + idx))
            r = max(w, h) * rad_k
            alpha = int((42 if idx == 0 else 28) * glow_k * voice_boost)
            grad = QRadialGradient(ox, oy, r)
            grad.setColorAt(0.0, _qcol(col_hex, min(115, alpha)))
            grad.setColorAt(0.55, _qcol(col_hex, min(40, int(alpha * 0.32))))
            grad.setColorAt(1.0, QColor(0, 0, 0, 0))
            p.setBrush(QBrush(grad))
            p.drawRect(rect)

    elif mode == "orbital_horizon":
        # Planetary horizon arc & subtle starfield
        horizon_y = h * 1.38
        horizon_r = max(w, h) * 1.08
        halo = QRadialGradient(cx, horizon_y, horizon_r)
        halo_alpha = int(85 * glow_k * voice_boost)
        halo.setColorAt(0.76, QColor(0, 0, 0, 0))
        halo.setColorAt(0.84, _qcol(primary, min(140, halo_alpha)))
        halo.setColorAt(0.90, _qcol(secondary, min(70, int(halo_alpha * 0.5))))
        halo.setColorAt(1.0, QColor(0, 0, 0, 0))
        p.setBrush(QBrush(halo))
        p.drawRect(rect)

        # Crisp orbital rim arc
        p.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(_qcol(primary, int(110 * glow_k)), 1.4)
        p.setPen(pen)
        arc_r = horizon_r * 0.84
        p.drawEllipse(QPointF(cx, horizon_y), arc_r, arc_r)

        # Deterministic minimal starfield
        p.setPen(Qt.PenStyle.NoPen)
        for i in range(36):
            sx = ((i * 197 + 43) % 997) / 997.0 * w
            sy = ((i * 313 + 71) % 613) / 613.0 * (h * 0.68)
            twinkle = 0.45 + 0.55 * math.sin(tick * 0.04 + i * 1.3)
            p.setBrush(QColor(235, 244, 255, int(90 * twinkle * max(0.35, glow_k))))
            sz = 1.6 if i % 5 == 0 else 1.0
            p.drawEllipse(QPointF(sx, sy), sz, sz)

    elif mode == "neural_mesh":
        # Geometric tactical constellation mesh
        cols = 7
        rows = 5
        pts: list[QPointF] = []
        for r_idx in range(rows):
            for c_idx in range(cols):
                bx = (c_idx + 0.5) / cols * w
                by = (r_idx + 0.5) / rows * h
                dx = math.sin(tick * 0.025 + r_idx * 1.1 + c_idx * 0.7) * 14.0
                dy = math.cos(tick * 0.02 + c_idx * 1.3 + r_idx * 0.5) * 10.0
                pts.append(QPointF(bx + dx, by + dy))

        line_alpha = int(34 * glow_k * voice_boost)
        p.setPen(QPen(_qcol(primary, min(85, line_alpha)), 1.0))
        for r_idx in range(rows):
            for c_idx in range(cols):
                idx = r_idx * cols + c_idx
                if c_idx + 1 < cols:
                    p.drawLine(pts[idx], pts[idx + 1])
                if r_idx + 1 < rows:
                    p.drawLine(pts[idx], pts[idx + cols])

        p.setPen(Qt.PenStyle.NoPen)
        dot_alpha = int(95 * glow_k * voice_boost)
        p.setBrush(_qcol(secondary, min(170, dot_alpha)))
        for pt in pts:
            p.drawEllipse(pt, 2.0, 2.0)

    # Editorial vignette for high contrast behind HUD/Avatar
    vig = QRadialGradient(cx, cy * 0.9, max(w, h) * 0.75)
    vig.setColorAt(0.0, QColor(0, 0, 0, 0))
    vig.setColorAt(0.7, QColor(5, 7, 11, 55))
    vig.setColorAt(1.0, QColor(3, 4, 7, 165))
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QBrush(vig))
    p.drawRect(rect)
