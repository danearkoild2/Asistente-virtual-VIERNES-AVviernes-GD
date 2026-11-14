"""
VIERNES — Centro de Gestión de Claves API & Credenciales
=========================================================
Panel profesional de configuración unificada para todas las llaves de acceso,
servicios de IA, conectores de domótica y mensajería.
Distingue claramente los Requisitos Obligatorios del Núcleo y las Mejoras Opcionales.
"""

from __future__ import annotations

import json
import os
import threading
import urllib.parse
import urllib.request
import webbrowser
from typing import Any, Callable, Dict, Optional, Tuple

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QCursor, QFont, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from memory.config_manager import (
    get_elevenlabs_config,
    get_gemini_key,
    get_serpapi_key,
    get_spotify_config,
    get_virustotal_key,
    get_weather_key,
    load_api_keys,
    save_all_api_keys,
)


# ── Color Palette & Styles ───────────────────────────────────────────────────
C_BG = "#111114"
C_PANEL = "#17171C"
C_PANEL_ALT = "#1F1F26"
C_BORDER = "#272730"
C_BORDER_ACTIVE = "#6E6AF6"
C_CYAN = "#6E6AF6"
C_GREEN = "#34D399"
C_AMBER = "#E07A5F"
C_RED = "#F87171"
C_TEXT = "#EEEEF0"
C_TEXT_MUTED = "#A0A0AB"
C_TEXT_DIM = "#6E6E7A"


def _create_badge(text: str, is_required: bool = False) -> QLabel:
    lbl = QLabel(text)
    lbl.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
    if is_required:
        lbl.setStyleSheet(f"""
            QLabel {{
                color: #ffffff;
                background: rgba(239, 68, 68, 0.25);
                border: 1px solid #ef4444;
                border-radius: 4px;
                padding: 3px 8px;
                letter-spacing: 0.5px;
            }}
        """)
    else:
        lbl.setStyleSheet(f"""
            QLabel {{
                color: #38bdf8;
                background: rgba(56, 189, 248, 0.14);
                border: 1px solid rgba(56, 189, 248, 0.35);
                border-radius: 4px;
                padding: 3px 8px;
                letter-spacing: 0.5px;
            }}
        """)
    return lbl


class ApiKeyEntryRow(QFrame):
    """Component for configuring a single API key with validation, toggle view, and direct links."""

    def __init__(
        self,
        service_name: str,
        env_var: str,
        description: str,
        current_val: str = "",
        is_required: bool = False,
        doc_url: str = "",
        validator_func: Optional[Callable[[str], Tuple[bool, str]]] = None,
        parent=None,
    ):
        super().__init__(parent)
        self.service_name = service_name
        self.env_var = env_var
        self.doc_url = doc_url
        self.is_required = is_required
        self.validator_func = validator_func

        self.setStyleSheet(f"""
            ApiKeyEntryRow {{
                background: {C_PANEL};
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
            }}
            ApiKeyEntryRow:hover {{
                border-color: {C_BORDER};
            }}
        """)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(8)

        # ── Header row: Title + Badge + Status ───────────────────────────────
        hdr = QHBoxLayout()
        hdr.setSpacing(10)

        title_lbl = QLabel(service_name)
        title_lbl.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        title_lbl.setStyleSheet(f"color: {C_TEXT}; background: transparent;")
        hdr.addWidget(title_lbl)

        badge_text = "🔴 REQUISITO OBLIGATORIO" if is_required else "🟢 OPCIONAL"
        hdr.addWidget(_create_badge(badge_text, is_required=is_required))

        hdr.addStretch(1)

        # Status indicator pill
        self.status_lbl = QLabel("○ No configurada" if not current_val else "● Guardada")
        self.status_lbl.setFont(QFont("Segoe UI", 8, QFont.Weight.DemiBold))
        self._update_status_style("saved" if current_val else "empty")
        hdr.addWidget(self.status_lbl)

        lay.addLayout(hdr)

        # ── Description ──────────────────────────────────────────────────────
        desc_lbl = QLabel(description)
        desc_lbl.setFont(QFont("Segoe UI", 8))
        desc_lbl.setStyleSheet(f"color: {C_TEXT_MUTED}; background: transparent;")
        desc_lbl.setWordWrap(True)
        lay.addWidget(desc_lbl)

        # ── Input row: Key Input + Eye + Test + Docs ─────────────────────────
        input_row = QHBoxLayout()
        input_row.setSpacing(6)

        self.input_field = QLineEdit(current_val)
        self.input_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_field.setPlaceholderText(f"Introduce tu clave ({env_var})...")
        self.input_field.setFont(QFont("Consolas", 9))
        self.input_field.setFixedHeight(34)
        self.input_field.setStyleSheet(f"""
            QLineEdit {{
                background: rgba(2, 6, 12, 0.85);
                color: #e0f2fe;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 6px;
                padding: 0 10px;
            }}
            QLineEdit:focus {{
                border: 1.5px solid {C_CYAN};
                background: rgba(0, 229, 255, 0.05);
            }}
        """)
        self.input_field.textChanged.connect(self._on_text_changed)
        input_row.addWidget(self.input_field, 1)

        # Show / Hide password button
        self.btn_eye = QPushButton("👁")
        self.btn_eye.setFixedSize(34, 34)
        self.btn_eye.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_eye.setToolTip("Mostrar / Ocultar caracteres de la clave")
        self.btn_eye.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 6px;
                color: #94a3b8;
                font-size: 13px;
            }
            QPushButton:hover {
                background: rgba(0, 229, 255, 0.15);
                border-color: #00e5ff;
                color: #ffffff;
            }
        """)
        self.btn_eye.clicked.connect(self._toggle_echo_mode)
        input_row.addWidget(self.btn_eye)

        # Validate button
        if self.validator_func:
            self.btn_validate = QPushButton("Validar")
            self.btn_validate.setFixedHeight(34)
            self.btn_validate.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
            self.btn_validate.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.btn_validate.setToolTip("Comprobar en vivo si la clave es válida y responde")
            self.btn_validate.setStyleSheet("""
                QPushButton {
                    background: rgba(16, 185, 129, 0.12);
                    border: 1px solid rgba(16, 185, 129, 0.4);
                    border-radius: 6px;
                    color: #10b981;
                    padding: 0 12px;
                }
                QPushButton:hover {
                    background: rgba(16, 185, 129, 0.28);
                    border-color: #34d399;
                    color: #ffffff;
                }
            """)
            self.btn_validate.clicked.connect(self.validate_in_background)
            input_row.addWidget(self.btn_validate)

        # Documentation link button
        if self.doc_url:
            self.btn_link = QPushButton("Obtener Clave ↗")
            self.btn_link.setFixedHeight(34)
            self.btn_link.setFont(QFont("Segoe UI", 8))
            self.btn_link.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.btn_link.setToolTip(f"Abrir portal oficial para obtener la clave ({self.doc_url})")
            self.btn_link.setStyleSheet("""
                QPushButton {
                    background: rgba(0, 229, 255, 0.08);
                    border: 1px solid rgba(0, 229, 255, 0.25);
                    border-radius: 6px;
                    color: #38bdf8;
                    padding: 0 10px;
                }
                QPushButton:hover {
                    background: rgba(0, 229, 255, 0.22);
                    border-color: #00e5ff;
                    color: #ffffff;
                }
            """)
            self.btn_link.clicked.connect(lambda: webbrowser.open(self.doc_url))
            input_row.addWidget(self.btn_link)

        lay.addLayout(input_row)

        # ── Diagnostic / Validation feedback banner ──────────────────────────
        self.feedback_lbl = QLabel("")
        self.feedback_lbl.setFont(QFont("Segoe UI", 8))
        self.feedback_lbl.setStyleSheet("background: transparent;")
        self.feedback_lbl.hide()
        lay.addWidget(self.feedback_lbl)

    def _toggle_echo_mode(self):
        if self.input_field.echoMode() == QLineEdit.EchoMode.Password:
            self.input_field.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_eye.setText("🔒")
        else:
            self.input_field.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_eye.setText("👁")

    def _on_text_changed(self, text: str):
        val = text.strip()
        if not val:
            self._update_status_style("empty")
            self.status_lbl.setText("○ No configurada")
        else:
            self._update_status_style("dirty")
            self.status_lbl.setText("● Modificada (Sin guardar)")
        self.feedback_lbl.hide()

    def _update_status_style(self, status: str):
        if status == "valid" or status == "saved":
            col, bg = "#10b981", "rgba(16, 185, 129, 0.15)"
        elif status == "invalid":
            col, bg = "#ef4444", "rgba(239, 68, 68, 0.20)"
        elif status == "testing":
            col, bg = "#38bdf8", "rgba(56, 189, 248, 0.15)"
        elif status == "dirty":
            col, bg = "#f59e0b", "rgba(245, 158, 11, 0.15)"
        else:
            col, bg = "#94a3b8", "rgba(148, 163, 184, 0.10)"

        self.status_lbl.setStyleSheet(f"""
            color: {col};
            background: {bg};
            border: 1px solid {col};
            border-radius: 4px;
            padding: 2px 7px;
        """)

    def validate_in_background(self):
        val = self.input_field.text().strip()
        if not val:
            self.set_feedback(False, "Por favor introduce una clave antes de validar.")
            return

        if not self.validator_func:
            return

        self._update_status_style("testing")
        self.status_lbl.setText("⏳ Validando...")
        self.feedback_lbl.setText("Comprobando conexión con el servidor...")
        self.feedback_lbl.setStyleSheet("color: #38bdf8;")
        self.feedback_lbl.show()

        def _worker():
            ok, msg = self.validator_func(val)
            QTimer.singleShot(0, lambda: self.set_feedback(ok, msg))

        threading.Thread(target=_worker, daemon=True).start()

    def set_feedback(self, ok: bool, msg: str):
        if ok:
            self._update_status_style("valid")
            self.status_lbl.setText("● ACTIVA / VÁLIDA")
            self.feedback_lbl.setText(f"✓ {msg}")
            self.feedback_lbl.setStyleSheet("color: #34d399; font-weight: bold;")
        else:
            self._update_status_style("invalid")
            self.status_lbl.setText("✕ INVÁLIDA")
            self.feedback_lbl.setText(f"⚠ {msg}")
            self.feedback_lbl.setStyleSheet("color: #f87171; font-weight: bold;")
        self.feedback_lbl.show()

    def get_value(self) -> str:
        return self.input_field.text().strip()


# ── Live Validation Functions ────────────────────────────────────────────────

def _validate_gemini(key: str) -> Tuple[bool, str]:
    if not key:
        return False, "La clave no puede estar vacía."
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={urllib.parse.quote(key)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Viernes-Validator/1.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode())
            models = len(data.get("models", []))
            return True, f"Conexión con Google Gemini exitosa ({models} modelos accesibles)."
    except urllib.error.HTTPError as e:
        if e.code == 400 or e.code == 403:
            return False, "Google rechazó la API Key (Clave inválida o sin permisos de Generative Language)."
        return False, f"Error de respuesta de Google Gemini (Código HTTP {e.code})."
    except Exception as exc:
        return False, f"Fallo al conectar con Gemini: {exc}"


def _validate_elevenlabs(key: str) -> Tuple[bool, str]:
    if not key:
        return False, "La clave no puede estar vacía."
    url = "https://api.elevenlabs.io/v1/user"
    try:
        req = urllib.request.Request(
            url,
            headers={"xi-api-key": key, "User-Agent": "Viernes-Validator/1.0"}
        )
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode())
            sub = data.get("subscription", {}).get("tier", "free")
            chars = data.get("subscription", {}).get("character_count", 0)
            limit = data.get("subscription", {}).get("character_limit", 0)
            return True, f"ElevenLabs conectado. Plan: {sub.upper()} ({chars}/{limit} caracteres usados)."
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return False, "Clave de ElevenLabs rechazada (xi-api-key inválida)."
        return False, f"Error del servidor ElevenLabs (Código {e.code})."
    except Exception as exc:
        return False, f"Error de conexión con ElevenLabs: {exc}"


def _validate_serpapi(key: str) -> Tuple[bool, str]:
    if not key:
        return False, "La clave no puede estar vacía."
    url = f"https://serpapi.com/account?api_key={urllib.parse.quote(key)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Viernes-Validator/1.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode())
            searches = data.get("plan_searches_left", "N/A")
            return True, f"SerpAPI verificado. Búsquedas restantes este mes: {searches}."
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return False, "Clave SerpAPI inválida o cuenta inactiva."
        return False, f"Error SerpAPI (Código {e.code})."
    except Exception as exc:
        return False, f"Error al validar SerpAPI: {exc}"


def _validate_virustotal(key: str) -> Tuple[bool, str]:
    if not key:
        return False, "La clave no puede estar vacía."
    url = f"https://www.virustotal.com/api/v3/users/{urllib.parse.quote(key)}"
    try:
        req = urllib.request.Request(
            url,
            headers={"x-apikey": key, "User-Agent": "Viernes-Validator/1.0"}
        )
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode())
            uid = data.get("data", {}).get("id", "Usuario")
            return True, f"VirusTotal conectado. Cuenta activa: {uid}."
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return False, "Clave VirusTotal rechazada (x-apikey inválida)."
        return False, f"Error VirusTotal (Código {e.code})."
    except Exception as exc:
        return False, f"Error al conectar con VirusTotal: {exc}"


def _validate_weather(key: str) -> Tuple[bool, str]:
    if not key:
        return False, "La clave no puede estar vacía."
    url = f"https://api.weatherapi.com/v1/current.json?key={urllib.parse.quote(key)}&q=London"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Viernes-Validator/1.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode())
            loc = data.get("location", {}).get("name", "OK")
            return True, f"WeatherAPI verificado y respondiendo correctamente (Ubicación de prueba: {loc})."
    except Exception as e:
        return False, f"Clave WeatherAPI rechazada o sin conexión: {e}"


# ── Main Modal Dialog ────────────────────────────────────────────────────────

class ApiKeysGeneralDialog(QDialog):
    """
    Production-grade Unified API Keys & Credentials Management Center for VIERNES.
    Categorizes Mandatory vs Optional APIs with real-time test validation and persistent storage.
    """

    credentials_updated = pyqtSignal()
    keys_saved = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("VIERNES — Claves API General & Credenciales de Producción")
        self.setModal(True)
        self.resize(840, 640)
        self.setMinimumSize(780, 560)

        self.setStyleSheet(f"""
            QDialog {{
                background: {C_PANEL};
                color: {C_TEXT};
                border: 1px solid {C_BORDER};
                border-radius: 14px;
            }}
            QTabWidget::pane {{
                border: 1px solid {C_BORDER};
                background: {C_BG};
                border-radius: 10px;
                padding: 10px;
            }}
            QTabBar::tab {{
                background: {C_PANEL_ALT};
                color: {C_TEXT_MUTED};
                padding: 9px 18px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 11px;
                font-weight: 600;
            }}
            QTabBar::tab:selected {{
                background: #1E1D36;
                color: #6E6AF6;
                border-bottom: 2px solid #6E6AF6;
            }}
            QTabBar::tab:hover:!selected {{
                background: #272730;
                color: #FAF9F6;
            }}
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QScrollBar:vertical {{
                background: transparent;
                width: 6px;
                border-radius: 3px;
            }}
            QScrollBar::handle:vertical {{
                background: #353542;
                border-radius: 3px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #6E6AF6;
            }}
        """)

        self._rows: Dict[str, ApiKeyEntryRow] = {}
        self._load_current_credentials()
        self._setup_ui()
        self._refresh_summary_counters()

    def _load_current_credentials(self):
        cfg = load_api_keys()
        self._current_cfg = cfg

        # Gmail credentials
        self._gmail_email = ""
        self._gmail_pass = ""
        try:
            from integrations.gmail.gmail_client import gmail
            self._gmail_email = getattr(gmail, "_account_email", "") or ""
            self._gmail_pass = getattr(gmail, "_app_password", "") or ""
        except Exception:
            pass

        # Home assistant credentials
        self._ha_url = ""
        self._ha_token = ""
        try:
            from integrations.smarthome.adapters.home_assistant import ha_client
            self._ha_url = getattr(ha_client, "base_url", "") or ""
            self._ha_token = getattr(ha_client, "token", "") or ""
        except Exception:
            pass

        # Elevenlabs
        el_cfg = get_elevenlabs_config()
        self._el_key = el_cfg.get("api_key", "")
        self._el_voice = el_cfg.get("voice_id", "")

        # Spotify
        sp_cfg = get_spotify_config()
        self._sp_client_id = sp_cfg.get("client_id", "")
        self._sp_client_secret = sp_cfg.get("client_secret", "")

    def _setup_ui(self):
        root_lay = QVBoxLayout(self)
        root_lay.setContentsMargins(20, 18, 20, 16)
        root_lay.setSpacing(12)

        # ── 1. DIALOG HEADER ─────────────────────────────────────────────────
        hdr_lay = QHBoxLayout()
        hdr_lay.setSpacing(12)

        icon_box = QLabel("🔑")
        icon_box.setFont(QFont("Segoe UI", 20))
        icon_box.setStyleSheet("background: transparent;")
        hdr_lay.addWidget(icon_box)

        title_v = QVBoxLayout()
        title_v.setSpacing(2)

        main_title = QLabel("Claves API y credenciales")
        main_title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        main_title.setStyleSheet("color: #FAF9F6;")
        title_v.addWidget(main_title)

        sub_title = QLabel("Centro unificado de configuración de llaves y servicios externos.")
        sub_title.setFont(QFont("Segoe UI", 9))
        sub_title.setStyleSheet("color: #A0A0AB;")
        title_v.addWidget(sub_title)
        hdr_lay.addLayout(title_v)

        hdr_lay.addStretch(1)

        # Close button
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(28, 28)
        btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_close.setStyleSheet("""
            QPushButton {
                background: #1F1F26;
                border: 1px solid #272730;
                border-radius: 8px;
                color: #A0A0AB;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #3A1F24;
                color: #F87171;
                border-color: #F87171;
            }
        """)
        btn_close.clicked.connect(self.reject)
        hdr_lay.addWidget(btn_close)

        root_lay.addLayout(hdr_lay)

        # ── 2. SUMMARY METRICS BAR ───────────────────────────────────────────
        self.summary_bar = QFrame(self)
        self.summary_bar.setStyleSheet("""
            QFrame {
                background: #1F1F26;
                border: 1px solid #272730;
                border-radius: 8px;
                padding: 4px 8px;
            }
        """)
        s_lay = QHBoxLayout(self.summary_bar)
        s_lay.setContentsMargins(12, 6, 12, 6)
        s_lay.setSpacing(16)

        self.lbl_req_stat = QLabel("🔴 Obligatorio: 0 / 1")
        self.lbl_req_stat.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        s_lay.addWidget(self.lbl_req_stat)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.VLine)
        sep.setStyleSheet("color: rgba(255, 255, 255, 0.15);")
        s_lay.addWidget(sep)

        self.lbl_opt_stat = QLabel("🟢 Opcionales: 0 / 7 Activas")
        self.lbl_opt_stat.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        s_lay.addWidget(self.lbl_opt_stat)

        s_lay.addStretch(1)

        self.lbl_core_health = QLabel("● ESTADO DEL NÚCLEO: OPERATIVO")
        self.lbl_core_health.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.lbl_core_health.setStyleSheet("color: #10b981;")
        s_lay.addWidget(self.lbl_core_health)

        root_lay.addWidget(self.summary_bar)

        # ── 3. TABS CONTAINER ────────────────────────────────────────────────
        self.tabs = QTabWidget(self)

        # Tab 1: IA, Búsqueda y Núcleo
        self.tabs.addTab(self._build_core_ai_tab(), "🧠  IA, Búsqueda y Núcleo")

        # Tab 2: Servicios & Domótica
        self.tabs.addTab(self._build_services_tab(), "⚡  Integraciones y Domótica")

        # Tab 3: Guía y Requisitos
        self.tabs.addTab(self._build_guide_tab(), "📋  Guía de Producción")

        root_lay.addWidget(self.tabs, 1)

        # ── 4. BOTTOM ACTION BUTTONS ─────────────────────────────────────────
        bot_lay = QHBoxLayout()
        bot_lay.setSpacing(10)

        btn_test_all = QPushButton("🔄  Validar Todas las Conexiones")
        btn_test_all.setFixedHeight(38)
        btn_test_all.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))
        btn_test_all.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_test_all.setStyleSheet("""
            QPushButton {
                background: rgba(0, 229, 255, 0.12);
                border: 1px solid rgba(0, 229, 255, 0.35);
                border-radius: 6px;
                color: #00e5ff;
                padding: 0 16px;
            }
            QPushButton:hover {
                background: rgba(0, 229, 255, 0.28);
                color: #ffffff;
                border-color: #ffffff;
            }
        """)
        btn_test_all.clicked.connect(self._validate_all_keys)
        bot_lay.addWidget(btn_test_all)

        bot_lay.addStretch(1)

        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setFixedHeight(38)
        btn_cancel.setFont(QFont("Segoe UI", 9))
        btn_cancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_cancel.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid rgba(148, 163, 184, 0.3);
                border-radius: 6px;
                color: #94a3b8;
                padding: 0 18px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.08);
                color: #ffffff;
            }
        """)
        btn_cancel.clicked.connect(self.reject)
        bot_lay.addWidget(btn_cancel)

        btn_save = QPushButton("Guardar y aplicar credenciales")
        btn_save.setFixedHeight(36)
        btn_save.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))
        btn_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_save.setStyleSheet("""
            QPushButton {
                background: #6E6AF6;
                border: none;
                border-radius: 8px;
                color: #FAF9F6;
                padding: 0 22px;
            }
            QPushButton:hover {
                background: #5652D4;
            }
        """)
        btn_save.clicked.connect(self._save_credentials)
        bot_lay.addWidget(btn_save)

        root_lay.addLayout(bot_lay)

    def _build_core_ai_tab(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        lay = QVBoxLayout(container)
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setSpacing(12)

        # 1. Google Gemini (OBLIGATORIO)
        row_gemini = ApiKeyEntryRow(
            service_name="Google Gemini AI (LLM, Visión y Herramientas)",
            env_var="GEMINI_API_KEY",
            description="Cerebro neuronal central de VIERNES. Requerido para procesar preguntas, razonamiento lógico en español, análisis multimodal de pantalla y ejecución de herramientas.",
            current_val=get_gemini_key() or "",
            is_required=True,
            doc_url="https://aistudio.google.com/app/apikey",
            validator_func=_validate_gemini,
            parent=self,
        )
        self._rows["gemini_api_key"] = row_gemini
        lay.addWidget(row_gemini)

        # 2. ElevenLabs (OPCIONAL)
        row_eleven = ApiKeyEntryRow(
            service_name="ElevenLabs (Síntesis de Voz Ultra-Realista)",
            env_var="ELEVENLABS_API_KEY",
            description="Motor de voz neuronal hiperrealista con clonación de voz. Opcional: Si no se configura, VIERNES utiliza las voces nativas oficiales de Gemini Live.",
            current_val=self._el_key,
            is_required=False,
            doc_url="https://elevenlabs.io/",
            validator_func=_validate_elevenlabs,
            parent=self,
        )
        self._rows["elevenlabs_api_key"] = row_eleven
        lay.addWidget(row_eleven)

        # Voice ID subfield
        el_voice_box = QFrame()
        el_voice_box.setStyleSheet(f"background: {C_PANEL_ALT}; border: 1px solid rgba(255,255,255,0.06); border-radius: 6px;")
        v_lay = QHBoxLayout(el_voice_box)
        v_lay.setContentsMargins(12, 6, 12, 6)
        v_lay.addWidget(QLabel("ElevenLabs Voice ID (ID de Voz Opcional):"))
        self.input_el_voice = QLineEdit(self._el_voice)
        self.input_el_voice.setPlaceholderText("Ejemplo: 21m00Tcm4TlvDq8ikWAM (dejar vacío para voz predeterminada)")
        self.input_el_voice.setStyleSheet("background: #02060d; color: #e2e8f0; border: 1px solid rgba(255,255,255,0.12); border-radius: 4px; padding: 4px 8px;")
        v_lay.addWidget(self.input_el_voice, 1)
        lay.addWidget(el_voice_box)

        # 3. SerpAPI (OPCIONAL)
        row_serp = ApiKeyEntryRow(
            service_name="SerpAPI (Búsqueda en Google & Galería Visual HD)",
            env_var="SERPAPI_API_KEY",
            description="Potencia las búsquedas web profundas en tiempo real y la obtención de imágenes en alta resolución para la Tarjeta de Inteligencia Visual de VIERNES.",
            current_val=get_serpapi_key() or "",
            is_required=False,
            doc_url="https://serpapi.com/",
            validator_func=_validate_serpapi,
            parent=self,
        )
        self._rows["serpapi_api_key"] = row_serp
        lay.addWidget(row_serp)

        # 4. VirusTotal (OPCIONAL)
        row_vt = ApiKeyEntryRow(
            service_name="VirusTotal (Escaneo de Archivos & Inteligencia de Amenazas)",
            env_var="VIRUSTOTAL_API_KEY",
            description="Permite al plugin de seguridad analizar ejecutables y descargas sospechosas contra más de 70 motores antivirus simultáneamente.",
            current_val=get_virustotal_key() or "",
            is_required=False,
            doc_url="https://www.virustotal.com/gui/my-apikey",
            validator_func=_validate_virustotal,
            parent=self,
        )
        self._rows["virustotal_api_key"] = row_vt
        lay.addWidget(row_vt)

        # 5. WeatherAPI (OPCIONAL)
        row_weather = ApiKeyEntryRow(
            service_name="WeatherAPI (Radares Satelitales Extendidos)",
            env_var="WEATHER_API_KEY",
            description="Radares meteorológicos satelitales e índice UV extendido. Opcional: Por defecto VIERNES opera de forma nativa con Open-Meteo sin necesidad de clave.",
            current_val=get_weather_key() or "",
            is_required=False,
            doc_url="https://www.weatherapi.com/",
            validator_func=_validate_weather,
            parent=self,
        )
        self._rows["weather_api_key"] = row_weather
        lay.addWidget(row_weather)

        lay.addStretch(1)
        scroll.setWidget(container)
        return scroll

    def _build_services_tab(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        lay = QVBoxLayout(container)
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setSpacing(14)

        # ── 1. GMAIL SMTP / IMAP ─────────────────────────────────────────────
        gmail_box = QFrame()
        gmail_box.setStyleSheet(f"background: {C_PANEL}; border: 1px solid rgba(255,255,255,0.08); border-radius: 8px;")
        g_lay = QVBoxLayout(gmail_box)
        g_lay.setContentsMargins(14, 12, 14, 12)
        g_lay.setSpacing(8)

        g_hdr = QHBoxLayout()
        g_title = QLabel("Google Gmail (SMTP & IMAP Seguro)")
        g_title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        g_title.setStyleSheet("color: #ffffff;")
        g_hdr.addWidget(g_title)
        g_hdr.addWidget(_create_badge("🟢 OPCIONAL", is_required=False))
        g_hdr.addStretch(1)
        g_lay.addLayout(g_hdr)

        g_desc = QLabel(
            "Monitoreo en vivo de correos entrantes, alertas y redacción de emails por voz. "
            "Requiere tu correo de Gmail y una Contraseña de Aplicación de 16 letras generada en tu cuenta de Google."
        )
        g_desc.setFont(QFont("Segoe UI", 8))
        g_desc.setStyleSheet(f"color: {C_TEXT_MUTED};")
        g_desc.setWordWrap(True)
        g_lay.addWidget(g_desc)

        g_fields = QHBoxLayout()
        self.input_gmail_email = QLineEdit(self._gmail_email)
        self.input_gmail_email.setPlaceholderText("tu_correo@gmail.com")
        self.input_gmail_email.setStyleSheet("background: #02060d; color: #e2e8f0; border: 1px solid rgba(255,255,255,0.12); border-radius: 4px; padding: 6px 10px;")
        g_fields.addWidget(self.input_gmail_email, 1)

        self.input_gmail_pass = QLineEdit(self._gmail_pass)
        self.input_gmail_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_gmail_pass.setPlaceholderText("Contraseña de Aplicación (16 letras)")
        self.input_gmail_pass.setStyleSheet("background: #02060d; color: #e2e8f0; border: 1px solid rgba(255,255,255,0.12); border-radius: 4px; padding: 6px 10px;")
        g_fields.addWidget(self.input_gmail_pass, 1)

        btn_gmail_link = QPushButton("Generar Contraseña ↗")
        btn_gmail_link.setStyleSheet("background: rgba(0, 229, 255, 0.08); border: 1px solid rgba(0, 229, 255, 0.25); border-radius: 4px; color: #38bdf8; padding: 6px 10px;")
        btn_gmail_link.clicked.connect(lambda: webbrowser.open("https://myaccount.google.com/apppasswords"))
        g_fields.addWidget(btn_gmail_link)
        g_lay.addLayout(g_fields)

        lay.addWidget(gmail_box)

        # ── 2. HOME ASSISTANT ────────────────────────────────────────────────
        ha_box = QFrame()
        ha_box.setStyleSheet(f"background: {C_PANEL}; border: 1px solid rgba(255,255,255,0.08); border-radius: 8px;")
        ha_lay = QVBoxLayout(ha_box)
        ha_lay.setContentsMargins(14, 12, 14, 12)
        ha_lay.setSpacing(8)

        ha_hdr = QHBoxLayout()
        ha_title = QLabel("Home Assistant (Domótica & Hogar Inteligente)")
        ha_title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        ha_title.setStyleSheet("color: #ffffff;")
        ha_hdr.addWidget(ha_title)
        ha_hdr.addWidget(_create_badge("🟢 OPCIONAL", is_required=False))
        ha_hdr.addStretch(1)
        ha_lay.addLayout(ha_hdr)

        ha_desc = QLabel(
            "Control domótico de luces, enchufes, cerraduras, clima y sensores en tu servidor local o en la nube."
        )
        ha_desc.setFont(QFont("Segoe UI", 8))
        ha_desc.setStyleSheet(f"color: {C_TEXT_MUTED};")
        ha_lay.addWidget(ha_desc)

        ha_fields = QHBoxLayout()
        self.input_ha_url = QLineEdit(self._ha_url)
        self.input_ha_url.setPlaceholderText("http://homeassistant.local:8123 o IP local")
        self.input_ha_url.setStyleSheet("background: #02060d; color: #e2e8f0; border: 1px solid rgba(255,255,255,0.12); border-radius: 4px; padding: 6px 10px;")
        ha_fields.addWidget(self.input_ha_url, 1)

        self.input_ha_token = QLineEdit(self._ha_token)
        self.input_ha_token.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_ha_token.setPlaceholderText("Long-Lived Access Token")
        self.input_ha_token.setStyleSheet("background: #02060d; color: #e2e8f0; border: 1px solid rgba(255,255,255,0.12); border-radius: 4px; padding: 6px 10px;")
        ha_fields.addWidget(self.input_ha_token, 1)
        ha_lay.addLayout(ha_fields)

        lay.addWidget(ha_box)

        # ── 3. SPOTIFY DEVELOPER ─────────────────────────────────────────────
        sp_box = QFrame()
        sp_box.setStyleSheet(f"background: {C_PANEL}; border: 1px solid rgba(255,255,255,0.08); border-radius: 8px;")
        sp_lay = QVBoxLayout(sp_box)
        sp_lay.setContentsMargins(14, 12, 14, 12)
        sp_lay.setSpacing(8)

        sp_hdr = QHBoxLayout()
        sp_title = QLabel("Spotify Web API (Control Musical Avanzado)")
        sp_title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        sp_title.setStyleSheet("color: #ffffff;")
        sp_hdr.addWidget(sp_title)
        sp_hdr.addWidget(_create_badge("🟢 OPCIONAL", is_required=False))
        sp_hdr.addStretch(1)
        sp_lay.addLayout(sp_hdr)

        sp_desc = QLabel(
            "Integración de Spotify para desarrolladores: búsqueda de álbumes, playlists automáticas y control remoto de reproducción."
        )
        sp_desc.setFont(QFont("Segoe UI", 8))
        sp_desc.setStyleSheet(f"color: {C_TEXT_MUTED};")
        sp_lay.addWidget(sp_desc)

        sp_fields = QHBoxLayout()
        self.input_sp_id = QLineEdit(self._sp_client_id)
        self.input_sp_id.setPlaceholderText("Spotify Client ID")
        self.input_sp_id.setStyleSheet("background: #02060d; color: #e2e8f0; border: 1px solid rgba(255,255,255,0.12); border-radius: 4px; padding: 6px 10px;")
        sp_fields.addWidget(self.input_sp_id, 1)

        self.input_sp_secret = QLineEdit(self._sp_client_secret)
        self.input_sp_secret.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_sp_secret.setPlaceholderText("Spotify Client Secret")
        self.input_sp_secret.setStyleSheet("background: #02060d; color: #e2e8f0; border: 1px solid rgba(255,255,255,0.12); border-radius: 4px; padding: 6px 10px;")
        sp_fields.addWidget(self.input_sp_secret, 1)

        btn_sp_link = QPushButton("Dashboard ↗")
        btn_sp_link.setStyleSheet("background: rgba(30, 215, 96, 0.12); border: 1px solid rgba(30, 215, 96, 0.4); border-radius: 4px; color: #1ed760; padding: 6px 10px;")
        btn_sp_link.clicked.connect(lambda: webbrowser.open("https://developer.spotify.com/dashboard"))
        sp_fields.addWidget(btn_sp_link)
        sp_lay.addLayout(sp_fields)

        lay.addWidget(sp_box)

        lay.addStretch(1)
        scroll.setWidget(container)
        return scroll

    def _build_guide_tab(self) -> QWidget:
        container = QWidget()
        lay = QVBoxLayout(container)
        lay.setContentsMargins(16, 14, 16, 14)
        lay.setSpacing(12)

        title = QLabel("Arquitectura de Credenciales & Despliegue en Producción")
        title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        title.setStyleSheet("color: #00e5ff;")
        lay.addWidget(title)

        info_text = QLabel(
            "<b>1. Requisito Obligatorio del Sistema:</b><br>"
            "• <b>Google Gemini API Key:</b> Es el único requisito mandatorio para operar VIERNES. "
            "Proporciona la inteligencia artificial que comprende tus peticiones, ejecuta plugins, "
            "analiza la pantalla e interactúa mediante voz en tiempo real. Es 100% gratuita para uso individual.<br><br>"
            "<b>2. Servicios Opcionales:</b><br>"
            "• <b>ElevenLabs:</b> Síntesis de voz avanzada con clonación. Si está vacío, se usan las voces nativas de Gemini Live sin costo adicional.<br>"
            "• <b>SerpAPI:</b> Búsquedas web exhaustivas con tarjetas visuales de imágenes HD.<br>"
            "• <b>VirusTotal:</b> Auditoría criptográfica y escaneo de virus con 70 motores antivirus.<br>"
            "• <b>Gmail SMTP/IMAP:</b> Alertas y envío seguro de correos.<br>"
            "• <b>Home Assistant:</b> Control físico de domótica inteligente.<br><br>"
            "<b>3. Seguridad y Cifrado:</b><br>"
            "Todas las claves se almacenan localmente en tu equipo dentro de <code>config/api_keys.json</code> y "
            "los conectores bancarios/domóticos se protegen mediante cifrado simétrico AES-256 (Fernet). "
            "Ninguna credencial se envía a servidores de terceros ni intermediarios ajenos a los servicios oficiales."
        )
        info_text.setFont(QFont("Segoe UI", 9))
        info_text.setStyleSheet("color: #cbd5e1; line-height: 1.5;")
        info_text.setWordWrap(True)
        lay.addWidget(info_text)

        lay.addStretch(1)
        return container

    def _refresh_summary_counters(self):
        gemini_k = self._rows.get("gemini_api_key").get_value() if "gemini_api_key" in self._rows else ""
        if gemini_k:
            self.lbl_req_stat.setText("🔴 Obligatorio: 1 / 1 Configurada (100%)")
            self.lbl_req_stat.setStyleSheet("color: #34d399; font-weight: bold;")
            self.lbl_core_health.setText("● NÚCLEO OPERATIVO")
            self.lbl_core_health.setStyleSheet("color: #10b981; font-weight: bold;")
        else:
            self.lbl_req_stat.setText("🔴 Obligatorio: 0 / 1 (Gemini Pendiente)")
            self.lbl_req_stat.setStyleSheet("color: #ef4444; font-weight: bold;")
            self.lbl_core_health.setText("⚠ NÚCLEO INCOMPLETO (Falta Gemini)")
            self.lbl_core_health.setStyleSheet("color: #ef4444; font-weight: bold;")

        # Count optionals
        opt_count = 0
        total_opt = 7
        if self._rows.get("elevenlabs_api_key") and self._rows["elevenlabs_api_key"].get_value():
            opt_count += 1
        if self._rows.get("serpapi_api_key") and self._rows["serpapi_api_key"].get_value():
            opt_count += 1
        if self._rows.get("virustotal_api_key") and self._rows["virustotal_api_key"].get_value():
            opt_count += 1
        if self._rows.get("weather_api_key") and self._rows["weather_api_key"].get_value():
            opt_count += 1
        if hasattr(self, "input_gmail_email") and self.input_gmail_email.text().strip():
            opt_count += 1
        if hasattr(self, "input_ha_url") and self.input_ha_url.text().strip():
            opt_count += 1
        if hasattr(self, "input_sp_id") and self.input_sp_id.text().strip():
            opt_count += 1

        self.lbl_opt_stat.setText(f"🟢 Opcionales: {opt_count} / {total_opt} Conectadas")
        self.lbl_opt_stat.setStyleSheet("color: #38bdf8; font-weight: bold;")

    def _validate_all_keys(self):
        """Trigger background validation across all configured services simultaneously."""
        for row in self._rows.values():
            if row.get_value():
                row.validate_in_background()

    def _save_credentials(self):
        # 1. Enforce Mandatory Gemini API Key
        gemini_val = self._rows["gemini_api_key"].get_value() if "gemini_api_key" in self._rows else ""
        if not gemini_val:
            QMessageBox.critical(
                self,
                "Requisito Obligatorio Faltante",
                "La clave de Google Gemini es estrictamente obligatoria para que VIERNES funcione.\n\n"
                "Por favor introduce tu clave de Google Gemini en la primera casilla antes de guardar."
            )
            self.tabs.setCurrentIndex(0)
            self._rows["gemini_api_key"].input_field.setFocus()
            return

        # 2. Gather values for batch update
        update_dict = {
            "gemini_api_key": gemini_val,
            "elevenlabs_api_key": self._rows["elevenlabs_api_key"].get_value() if "elevenlabs_api_key" in self._rows else "",
            "elevenlabs_voice_id": self.input_el_voice.text().strip() if hasattr(self, "input_el_voice") else "",
            "serpapi_api_key": self._rows["serpapi_api_key"].get_value() if "serpapi_api_key" in self._rows else "",
            "virustotal_api_key": self._rows["virustotal_api_key"].get_value() if "virustotal_api_key" in self._rows else "",
            "weather_api_key": self._rows["weather_api_key"].get_value() if "weather_api_key" in self._rows else "",
            "spotify_client_id": self.input_sp_id.text().strip() if hasattr(self, "input_sp_id") else "",
            "spotify_client_secret": self.input_sp_secret.text().strip() if hasattr(self, "input_sp_secret") else "",
        }

        save_all_api_keys(update_dict)

        # 3. Synchronize environment variables for live subprocesses/plugins
        os.environ["GEMINI_API_KEY"] = gemini_val
        if update_dict["serpapi_api_key"]:
            os.environ["SERPAPI_API_KEY"] = update_dict["serpapi_api_key"]
        if update_dict["virustotal_api_key"]:
            os.environ["VIRUSTOTAL_API_KEY"] = update_dict["virustotal_api_key"]
        if update_dict["elevenlabs_api_key"]:
            os.environ["ELEVENLABS_API_KEY"] = update_dict["elevenlabs_api_key"]

        # 4. Save Gmail if provided
        gmail_saved_msg = ""
        if hasattr(self, "input_gmail_email") and hasattr(self, "input_gmail_pass"):
            g_email = self.input_gmail_email.text().strip()
            g_pass = self.input_gmail_pass.text().strip()
            if g_email and g_pass:
                try:
                    from integrations.gmail.gmail_client import gmail
                    ok, g_res = gmail.save_credentials(g_email, g_pass)
                    if ok:
                        gmail_saved_msg = "\n• Cuenta de Gmail sincronizada y cifrada con éxito."
                except Exception as e:
                    gmail_saved_msg = f"\n• Nota en Gmail: {e}"

        # 5. Save Home Assistant if provided
        ha_saved_msg = ""
        if hasattr(self, "input_ha_url") and hasattr(self, "input_ha_token"):
            h_url = self.input_ha_url.text().strip()
            h_tok = self.input_ha_token.text().strip()
            if h_url and h_tok:
                try:
                    from integrations.smarthome.adapters.home_assistant import ha_client
                    ha_client.save_credentials(h_url, h_tok)
                    ha_saved_msg = "\n• Home Assistant vinculado exitosamente."
                except Exception as e:
                    ha_saved_msg = f"\n• Nota en Home Assistant: {e}"

        self._refresh_summary_counters()
        self.credentials_updated.emit()
        self.keys_saved.emit(update_dict)

        QMessageBox.information(
            self,
            "Credenciales Guardadas",
            f"¡Todas las claves y credenciales de producción han sido guardadas y aplicadas exitosamente!{gmail_saved_msg}{ha_saved_msg}\n\nVIERNES continuará operando con la nueva configuración en tiempo real."
        )
        self.accept()
