"""
Vision & Local AI Settings Dialog - Panel de Control de Visión Continua e IA Local
==================================================================================
Interfaz gráfica moderna para configurar:
- Estado de Visión Continua / Habitación (ON/OFF)
- Selector de Cámara de hardware (Índice 0, 1, 2...)
- Modo de previsualización (PiP Flotante vs Panel Central HUD)
- Sensibilidad del Centinela de Habitación y Reacciones de Edith
- Selector de Motor de Visión (IA Local vs Nube Gemini)
- Opciones de Privacidad y Parada de Emergencia
"""

from __future__ import annotations

import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QCheckBox, QSlider, QFrame,
    QScrollArea, QMessageBox
)

from core.realtime_vision import get_vision_coordinator
from core.local_ai_service import get_local_ai_service


def _rgba(hex_color: str, alpha: float) -> str:
    c = QColor(hex_color)
    return f"rgba({c.red()},{c.green()},{c.blue()},{alpha:.3f})"


class VisionSettingsDialog(QDialog):
    """Modern dark cybernetic dialog for Realtime Vision and Local AI configuration."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Configuración de Visión en Vivo e IA Local")
        self.setFixedSize(560, 680)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        from ui import C, UI_FONT
        self._C = C
        self._UI_FONT = UI_FONT

        self.coordinator = get_vision_coordinator()
        self.local_ai = get_local_ai_service()

        self._build_ui()
        self._load_values()

        # Update status timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh_live_status)
        self._timer.start(1500)

    def _build_ui(self):
        C = self._C
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {C.PANEL};
                color: {C.WHITE};
                font-family: {self._UI_FONT};
            }}
            QLabel {{
                color: {C.TEXT};
                background: transparent;
            }}
            QFrame#Card {{
                background-color: {_rgba(C.PANEL2, 0.95)};
                border: 1px solid {C.BORDER};
                border-radius: 12px;
            }}
            QComboBox {{
                background-color: {_rgba(C.WHITE, 0.06)};
                color: {C.WHITE};
                border: 1px solid {C.BORDER_A};
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 11px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {C.PANEL2};
                color: {C.WHITE};
                selection-background-color: {C.PRI};
                selection-color: {C.WHITE};
                border: 1px solid {C.BORDER_B};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)

        # ── Header ──────────────────────────────────────────────────────────
        hdr = QHBoxLayout()
        icon = QLabel("👁️")
        icon.setFont(QFont(self._UI_FONT, 18))
        hdr.addWidget(icon)

        t_box = QVBoxLayout()
        t_box.setSpacing(1)
        title = QLabel("Visión en vivo e IA local")
        title.setFont(QFont(self._UI_FONT, 12, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {C.WHITE};")
        t_box.addWidget(title)

        sub = QLabel("Observación continua del entorno y análisis visual multimodal")
        sub.setFont(QFont(self._UI_FONT, 8))
        sub.setStyleSheet(f"color: {C.TEXT_MED};")
        t_box.addWidget(sub)
        hdr.addLayout(t_box, stretch=1)
        layout.addLayout(hdr)

        # ── Card 1: Estado en Vivo y Control de Cámara ──────────────────────
        c1 = QFrame(); c1.setObjectName("Card")
        l1 = QVBoxLayout(c1); l1.setContentsMargins(14, 12, 14, 12); l1.setSpacing(10)
        l1.addWidget(self._section_lbl("CÁMARA Y PERCEPCIÓN EN TIEMPO REAL"))

        # Status badge row
        stat_row = QHBoxLayout()
        self._cam_status_lbl = QLabel("● CÁMARA DESCONECTADA")
        self._cam_status_lbl.setFont(QFont(self._UI_FONT, 9, QFont.Weight.DemiBold))
        stat_row.addWidget(self._cam_status_lbl, stretch=1)

        self._toggle_cam_btn = QPushButton("Iniciar Visión en Vivo")
        self._toggle_cam_btn.setFixedHeight(30)
        self._toggle_cam_btn.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Bold))
        self._toggle_cam_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._toggle_cam_btn.clicked.connect(self._on_toggle_vision)
        stat_row.addWidget(self._toggle_cam_btn)
        l1.addLayout(stat_row)

        # Device selector
        dev_row = QHBoxLayout()
        dev_lbl = QLabel("Dispositivo de Cámara:")
        dev_lbl.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Medium))
        dev_row.addWidget(dev_lbl)
        self._cam_combo = QComboBox()
        self._cam_combo.addItem("Cámara Principal (Índice 0)", 0)
        self._cam_combo.addItem("Cámara Secundaria (Índice 1)", 1)
        self._cam_combo.addItem("Cámara Externa (Índice 2)", 2)
        dev_row.addWidget(self._cam_combo, stretch=1)
        l1.addLayout(dev_row)

        # Preview mode
        prev_row = QHBoxLayout()
        prev_lbl = QLabel("Modo de Previsualización:")
        prev_lbl.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Medium))
        prev_row.addWidget(prev_lbl)
        self._prev_combo = QComboBox()
        self._prev_combo.addItem("Miniatura Flotante PiP (Edith permanece visible)", "pip")
        self._prev_combo.addItem("Panel Completo en Pantalla (HUD)", "hud")
        prev_row.addWidget(self._prev_combo, stretch=1)
        l1.addLayout(prev_row)

        layout.addWidget(c1)

        # ── Card 2: Centinela de Habitación y Reacciones de Edith ───────────
        c2 = QFrame(); c2.setObjectName("Card")
        l2 = QVBoxLayout(c2); l2.setContentsMargins(14, 12, 14, 12); l2.setSpacing(10)
        l2.addWidget(self._section_lbl("CENTINELA DE HABITACIÓN & REACCIONES"))

        self._reactions_chk = QCheckBox("Permitir que Edith reaccione a movimientos o cambios en la habitación")
        self._reactions_chk.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Medium))
        self._reactions_chk.setStyleSheet(f"color: {C.WHITE};")
        l2.addWidget(self._reactions_chk)

        sens_row = QHBoxLayout()
        sens_lbl = QLabel("Sensibilidad de Detección:")
        sens_lbl.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Medium))
        sens_row.addWidget(sens_lbl)
        self._sens_combo = QComboBox()
        self._sens_combo.addItem("Baja (Solo movimientos grandes o personas)", "baja")
        self._sens_combo.addItem("Media (Equilibrada)", "media")
        self._sens_combo.addItem("Alta (Detecta pequeños cambios en el escritorio)", "alta")
        sens_row.addWidget(self._sens_combo, stretch=1)
        l2.addLayout(sens_row)

        # Analysis Interval
        int_row = QHBoxLayout()
        int_lbl = QLabel("Intervalo de Actualización de Escena:")
        int_lbl.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Medium))
        int_row.addWidget(int_lbl)
        self._interval_combo = QComboBox()
        self._interval_combo.addItem("Rápido (Cada 5 segundos)", 5.0)
        self._interval_combo.addItem("Equilibrado (Cada 15 segundos)", 15.0)
        self._interval_combo.addItem("Económico (Cada 30 segundos)", 30.0)
        self._interval_combo.addItem("Solo bajo demanda (Al preguntar)", 99999.0)
        int_row.addWidget(self._interval_combo, stretch=1)
        l2.addLayout(int_row)

        layout.addWidget(c2)

        # ── Card 3: Motor de Inteligencia Artificial (Local vs Nube) ─────────
        c3 = QFrame(); c3.setObjectName("Card")
        l3 = QVBoxLayout(c3); l3.setContentsMargins(14, 12, 14, 12); l3.setSpacing(10)
        l3.addWidget(self._section_lbl("MOTOR DE INTELIGENCIA ARTIFICIAL"))

        self._local_vision_chk = QCheckBox("Priorizar IA Local (Ollama) para preguntas de visión")
        self._local_vision_chk.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Medium))
        self._local_vision_chk.setStyleSheet(f"color: {C.WHITE};")
        l3.addWidget(self._local_vision_chk)

        ai_status_row = QHBoxLayout()
        self._ai_status_lbl = QLabel("Estado Ollama: Verificando...")
        self._ai_status_lbl.setFont(QFont(self._UI_FONT, 8))
        self._ai_status_lbl.setStyleSheet(f"color: {C.TEXT_MED};")
        ai_status_row.addWidget(self._ai_status_lbl, stretch=1)

        self._check_ai_btn = QPushButton("Comprobar Ollama")
        self._check_ai_btn.setFixedHeight(26)
        self._check_ai_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._check_ai_btn.setFont(QFont(self._UI_FONT, 8, QFont.Weight.DemiBold))
        self._check_ai_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {_rgba(C.WHITE, 0.06)};
                color: {C.TEXT};
                border: 1px solid {C.BORDER};
                border-radius: 6px;
                padding: 0 12px;
            }}
            QPushButton:hover {{
                background-color: {_rgba(C.PRI, 0.18)};
                border-color: {C.PRI};
                color: {C.WHITE};
            }}
        """)
        self._check_ai_btn.clicked.connect(self._refresh_local_ai)
        ai_status_row.addWidget(self._check_ai_btn)
        l3.addLayout(ai_status_row)

        # Vision Model Selector
        vm_row = QHBoxLayout()
        vm_lbl = QLabel("Modelo de Visión Local:")
        vm_lbl.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Medium))
        vm_row.addWidget(vm_lbl)
        self._vision_model_combo = QComboBox()
        vm_row.addWidget(self._vision_model_combo, stretch=1)
        l3.addLayout(vm_row)

        layout.addWidget(c3)

        # ── Footer / Privacy Notice ─────────────────────────────────────────
        foot_box = QVBoxLayout()
        foot_box.setSpacing(4)
        priv_lbl = QLabel("🔒 PRIVACIDAD GARANTIZADA: Todas las imágenes se procesan exclusivamente en memoria RAM volátil. No se almacena ninguna grabación ni fotografía permanente en disco.")
        priv_lbl.setFont(QFont(self._UI_FONT, 7))
        priv_lbl.setWordWrap(True)
        priv_lbl.setStyleSheet(f"color: {C.TEXT_MED};")
        foot_box.addWidget(priv_lbl)

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        save_btn = QPushButton("Guardar cambios")
        save_btn.setFixedHeight(34)
        save_btn.setFont(QFont(self._UI_FONT, 9, QFont.Weight.DemiBold))
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {C.PRI}; color: {C.WHITE};
                border: none; border-radius: 8px; padding: 0 20px;
            }}
            QPushButton:hover {{
                background-color: {C.PRI_DIM};
            }}
        """)
        save_btn.clicked.connect(self._save_and_close)
        btn_row.addWidget(save_btn)

        close_btn = QPushButton("Cerrar")
        close_btn.setFixedHeight(34)
        close_btn.setFont(QFont(self._UI_FONT, 9))
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {_rgba(C.WHITE, 0.06)}; color: {C.WHITE};
                border: 1px solid {C.BORDER}; border-radius: 8px; padding: 0 16px;
            }}
            QPushButton:hover {{
                background-color: {_rgba(C.WHITE, 0.12)};
            }}
        """)
        close_btn.clicked.connect(self.close)
        btn_row.addWidget(close_btn)

        foot_box.addLayout(btn_row)
        layout.addLayout(foot_box)

    def _section_lbl(self, text: str) -> QLabel:
        clean = text.capitalize() if text.isupper() else text
        lbl = QLabel(clean)
        f = QFont(self._UI_FONT, 8, QFont.Weight.DemiBold)
        lbl.setFont(f)
        lbl.setStyleSheet(f"color: {self._C.TEXT_MED}; background: transparent;")
        return lbl

    def _load_values(self):
        cfg = self.coordinator.get_config()

        # Camera Index
        idx = cfg.get("camera_index", 0)
        found = False
        for i in range(self._cam_combo.count()):
            if self._cam_combo.itemData(i) == idx:
                self._cam_combo.setCurrentIndex(i)
                found = True
                break
        if not found:
            self._cam_combo.addItem(f"Cámara (Índice {idx})", idx)
            self._cam_combo.setCurrentIndex(self._cam_combo.count() - 1)

        # Preview Mode
        p_mode = cfg.get("preview_mode", "pip")
        for i in range(self._prev_combo.count()):
            if self._prev_combo.itemData(i) == p_mode:
                self._prev_combo.setCurrentIndex(i)
                break

        # Reactions
        self._reactions_chk.setChecked(cfg.get("enable_reactions", True))

        # Sensitivity
        sens = cfg.get("reaction_sensitivity", "media")
        for i in range(self._sens_combo.count()):
            if self._sens_combo.itemData(i) == sens:
                self._sens_combo.setCurrentIndex(i)
                break

        # Interval
        interv = cfg.get("analysis_interval_s", 15.0)
        for i in range(self._interval_combo.count()):
            if abs(self._interval_combo.itemData(i) - interv) < 1.0:
                self._interval_combo.setCurrentIndex(i)
                break

        # Local Vision
        self._local_vision_chk.setChecked(cfg.get("prefer_local_vision", False))

        self._refresh_local_ai()
        self._refresh_live_status()

    def _refresh_local_ai(self):
        st = self.local_ai.get_status_info()
        self._vision_model_combo.clear()

        if st["is_available"]:
            v_models = st.get("vision_models", [])
            if v_models:
                self._ai_status_lbl.setText(f"Ollama ACTIVO: {len(v_models)} modelo(s) de visión detectado(s)")
                self._ai_status_lbl.setStyleSheet(f"color: {self._C.GREEN};")
                for vm in v_models:
                    self._vision_model_combo.addItem(f"👁️ {vm}", vm)
            else:
                self._ai_status_lbl.setText("Ollama ACTIVO (Sin modelo de visión. Recomendado: ollama pull llama3.2-vision)")
                self._ai_status_lbl.setStyleSheet(f"color: {self._C.ACC};")
                self._vision_model_combo.addItem("Ningún modelo de visión descargado", "")
        else:
            self._ai_status_lbl.setText("Ollama NO DETECTADO en localhost:11434")
            self._ai_status_lbl.setStyleSheet(f"color: {self._C.RED};")
            self._vision_model_combo.addItem("Servidor local no disponible", "")

    def _refresh_live_status(self):
        is_active = self.coordinator.is_active()
        if is_active:
            self._cam_status_lbl.setText("● CÁMARA ACTIVA — OBSERVACIÓN CONTINUA")
            self._cam_status_lbl.setStyleSheet(f"color: {self._C.GREEN};")
            self._toggle_cam_btn.setText("Detener Cámara")
            self._toggle_cam_btn.setStyleSheet(f"background-color: {_rgba(self._C.RED, 0.25)}; color: {self._C.RED}; border: 1px solid {self._C.RED}; border-radius: 6px;")
        else:
            self._cam_status_lbl.setText("○ CÁMARA EN REPOSO (Desconectada)")
            self._cam_status_lbl.setStyleSheet(f"color: {self._C.TEXT_MED};")
            self._toggle_cam_btn.setText("Iniciar Visión en Vivo")
            self._toggle_cam_btn.setStyleSheet(f"background-color: {_rgba(self._C.PRI, 0.20)}; color: {self._C.PRI}; border: 1px solid {self._C.PRI}; border-radius: 6px;")

    def _on_toggle_vision(self):
        if self.coordinator.is_active():
            self.coordinator.stop_continuous_vision()
            parent = self.parent()
            if hasattr(parent, "stop_camera_stream"):
                parent.stop_camera_stream()
        else:
            # Guardar índice actual antes de iniciar
            idx = self._cam_combo.currentData()
            self.coordinator.save_config({"camera_index": idx})
            self.coordinator.start_continuous_vision()
            parent = self.parent()
            if hasattr(parent, "start_camera_stream"):
                parent.start_camera_stream()

        self._refresh_live_status()

    def _save_and_close(self):
        updates = {
            "camera_index": self._cam_combo.currentData(),
            "vision_preview_mode": self._prev_combo.currentData(),
            "vision_enable_reactions": self._reactions_chk.isChecked(),
            "vision_sensitivity": self._sens_combo.currentData(),
            "vision_analysis_interval_s": self._interval_combo.currentData(),
            "prefer_local_vision": self._local_vision_chk.isChecked(),
        }
        vm = self._vision_model_combo.currentData()
        if vm:
            updates["vision_model"] = vm

        self.coordinator.save_config(updates)
        self.accept()
