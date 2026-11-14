from __future__ import annotations

import os
import subprocess
import sys
import threading
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from PyQt6.QtCore import Qt, QUrl, pyqtSignal
from PyQt6.QtGui import QDesktopServices, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

PAYPAL_DONATE_URL = "https://www.paypal.com/ncp/payment/NE56HM9KTAQRQ"


class ViernesInstaller(QWidget):
    """Instalador Oficial de Viernes — Creado por Groovi Developer."""

    _log_sig = pyqtSignal(str)
    _deps_done_sig = pyqtSignal(bool)
    _key_check_sig = pyqtSignal(bool, str)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Instalador Oficial de Viernes · Groovi Developer")
        self.resize(840, 650)
        self.setMinimumSize(760, 580)
        self.setStyleSheet("QWidget { background: #0B0D12; color: #F1F5F9; font-family: 'Segoe UI', sans-serif; }")

        self._log_sig.connect(self._append_log)
        self._deps_done_sig.connect(self._on_deps_done)
        self._key_check_sig.connect(self._on_key_checked)

        self._step_btns: list[QPushButton] = []
        self._build_ui()
        self._set_step(0)

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        # Header
        hdr = QHBoxLayout()
        badge = QLabel("V")
        badge.setFixedSize(40, 40)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        badge.setStyleSheet(
            "background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #6366F1,stop:1 #38BDF8);"
            "color: #FFFFFF; border-radius: 10px;"
        )
        hdr.addWidget(badge)

        t_col = QVBoxLayout()
        t_col.setSpacing(1)
        t1 = QLabel("VIERNES — Instalador Oficial")
        t1.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        t2 = QLabel("Edición Gratuita Open-Source · Creado por Groovi Developer")
        t2.setStyleSheet("color: #38BDF8; font-size: 11px;")
        t_col.addWidget(t1)
        t_col.addWidget(t2)
        hdr.addLayout(t_col)
        hdr.addStretch()

        doc_btn = QPushButton("📖 Documentación Oficial")
        doc_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        doc_btn.setFixedHeight(32)
        doc_btn.setStyleSheet(
            "QPushButton { background: #151C2B; color: #E2E8F0; border: 1px solid #242B3D; border-radius: 8px; padding: 0 12px; }"
            "QPushButton:hover { border-color: #38BDF8; }"
        )
        doc_btn.clicked.connect(self._open_docs)
        hdr.addWidget(doc_btn)
        root.addLayout(hdr)

        # Stepper
        steps_row = QHBoxLayout()
        steps_row.setSpacing(6)
        labels = [
            "1. Dependencias",
            "2. Tu Nombre",
            "3. APIs (Gemini)",
            "4. Voz & Skin",
            "5. Donación & Fin",
        ]
        for idx, lbl in enumerate(labels):
            b = QPushButton(lbl)
            b.setFixedHeight(32)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda _=False, i=idx: self._set_step(i))
            self._step_btns.append(b)
            steps_row.addWidget(b)
        root.addLayout(steps_row)

        self._stack = QStackedWidget()
        self._stack.addWidget(self._page_deps())
        self._stack.addWidget(self._page_identity())
        self._stack.addWidget(self._page_apis())
        self._stack.addWidget(self._page_voice_skin())
        self._stack.addWidget(self._page_finish())
        root.addWidget(self._stack, stretch=1)

        # Navigation Footer
        nav = QHBoxLayout()
        self._prev_btn = QPushButton("← Anterior")
        self._prev_btn.setFixedHeight(36)
        self._prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._prev_btn.setStyleSheet(
            "QPushButton { background: #151C2B; color: #CBD5E1; border: 1px solid #242B3D; border-radius: 8px; padding: 0 18px; }"
        )
        self._prev_btn.clicked.connect(lambda: self._set_step(max(0, self._stack.currentIndex() - 1)))
        nav.addWidget(self._prev_btn)

        nav.addStretch()

        self._next_btn = QPushButton("Siguiente →")
        self._next_btn.setFixedHeight(36)
        self._next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._next_btn.setStyleSheet(
            "QPushButton { background: #6366F1; color: #FFFFFF; border: none; border-radius: 8px; padding: 0 22px; font-weight: 700; }"
            "QPushButton:hover { background: #4F46E5; }"
        )
        self._next_btn.clicked.connect(self._on_next)
        nav.addWidget(self._next_btn)
        root.addLayout(nav)

    def _set_step(self, idx: int) -> None:
        self._stack.setCurrentIndex(idx)
        for i, b in enumerate(self._step_btns):
            if i == idx:
                b.setStyleSheet(
                    "QPushButton { background: #1C1F3B; color: #38BDF8; border: 1px solid #6366F1; border-radius: 8px; font-weight: 700; }"
                )
            else:
                b.setStyleSheet(
                    "QPushButton { background: #121620; color: #94A3B8; border: 1px solid #242B3D; border-radius: 8px; }"
                )
        self._prev_btn.setVisible(idx > 0)
        self._next_btn.setText("Guardar y Lanzar Viernes ✓" if idx == 4 else "Siguiente →")

    def _on_next(self) -> None:
        cur = self._stack.currentIndex()
        if cur < 4:
            self._set_step(cur + 1)
        else:
            self._save_and_launch()

    def _card(self) -> tuple[QFrame, QVBoxLayout]:
        f = QFrame()
        f.setStyleSheet("QFrame { background: #121620; border: 1px solid #242B3D; border-radius: 12px; }")
        l = QVBoxLayout(f)
        l.setContentsMargins(16, 14, 16, 14)
        l.setSpacing(10)
        return f, l

    def _input_style(self) -> str:
        return (
            "QLineEdit { background: #07090D; color: #F1F5F9; border: 1px solid #242B3D; "
            "border-radius: 8px; padding: 6px 10px; font-size: 13px; }"
            "QLineEdit:focus { border-color: #6366F1; }"
        )

    # ── Page 1: Dependencies ───────────────────────────────────────────────
    def _page_deps(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        card, cl = self._card()

        title = QLabel("Instalación de Dependencias del Sistema")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        cl.addWidget(title)

        desc = QLabel(
            f"Python detectado: {sys.version.split()[0]} ({sys.executable})\n"
            "Pulsa el botón para instalar o verificar todas las librerías necesarias desde requirements.txt."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #94A3B8;")
        cl.addWidget(desc)

        self._deps_btn = QPushButton("Instalar / Verificar Dependencias")
        self._deps_btn.setFixedHeight(36)
        self._deps_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._deps_btn.setStyleSheet(
            "QPushButton { background: #10B981; color: #FFFFFF; border: none; border-radius: 8px; font-weight: 700; padding: 0 16px; }"
        )
        self._deps_btn.clicked.connect(self._install_deps)
        cl.addWidget(self._deps_btn)

        self._deps_bar = QProgressBar()
        self._deps_bar.setRange(0, 100)
        self._deps_bar.setValue(0)
        cl.addWidget(self._deps_bar)

        self._deps_log = QTextEdit()
        self._deps_log.setReadOnly(True)
        self._deps_log.setStyleSheet(
            "QTextEdit { background: #07090D; color: #CBD5E1; border: 1px solid #242B3D; border-radius: 8px; font-family: Consolas; font-size: 12px; }"
        )
        cl.addWidget(self._deps_log, stretch=1)

        lay.addWidget(card)
        return w

    def _install_deps(self) -> None:
        self._deps_btn.setEnabled(False)
        self._deps_bar.setRange(0, 0)
        self._deps_log.clear()
        self._append_log("Iniciando instalación de dependencias...")

        def _worker():
            req = BASE_DIR / "requirements.txt"
            cmd = (
                [sys.executable, "-m", "pip", "install", "-r", str(req)]
                if req.exists()
                else [
                    sys.executable, "-m", "pip", "install",
                    "PyQt6", "PyQt6-WebEngine", "google-genai", "requests",
                    "beautifulsoup4", "edge-tts", "miniaudio", "sounddevice",
                    "numpy", "psutil", "adblock", "opencv-python",
                ]
            )
            try:
                proc = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding="utf-8", errors="replace",
                )
                for line in proc.stdout:
                    self._log_sig.emit(line.rstrip())
                proc.wait()
                self._deps_done_sig.emit(proc.returncode == 0)
            except Exception as exc:
                self._log_sig.emit(f"ERROR: {exc}")
                self._deps_done_sig.emit(False)

        threading.Thread(target=_worker, daemon=True).start()

    def _append_log(self, msg: str) -> None:
        self._deps_log.append(msg)

    def _on_deps_done(self, ok: bool) -> None:
        self._deps_btn.setEnabled(True)
        self._deps_bar.setRange(0, 100)
        self._deps_bar.setValue(100 if ok else 0)
        self._append_log("\n✓ Dependencias instaladas correctamente." if ok else "\n⚠ Algunas dependencias reportaron advertencias.")

    # ── Page 2: User & Assistant Identity ──────────────────────────────────
    def _page_identity(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        card, cl = self._card()

        t = QLabel("Identidad y Trato Personalizado")
        t.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        cl.addWidget(t)

        d = QLabel(
            "Dile a Viernes cómo te llamas para que adapte sus respuestas, saludos y memoria personal."
        )
        d.setWordWrap(True)
        d.setStyleSheet("color: #94A3B8;")
        cl.addWidget(d)

        cl.addWidget(QLabel("Tu nombre (¿Cómo quieres que te llame Viernes?):"))
        self._user_name_in = QLineEdit()
        self._user_name_in.setPlaceholderText("Ej. Daniel")
        self._user_name_in.setStyleSheet(self._input_style())
        cl.addWidget(self._user_name_in)

        cl.addWidget(QLabel("Nombre del asistente (por defecto: Viernes):"))
        self._assistant_name_in = QLineEdit("Viernes")
        self._assistant_name_in.setStyleSheet(self._input_style())
        cl.addWidget(self._assistant_name_in)

        cl.addStretch()
        lay.addWidget(card)
        return w

    # ── Page 3: APIs (Mandatory vs Optional) ───────────────────────────────
    def _page_apis(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        inner = QWidget()
        il = QVBoxLayout(inner)
        il.setSpacing(12)

        # Mandatory Gemini Card
        c1, l1 = self._card()
        h1 = QLabel("1. Google Gemini API Key — [OBLIGATORIA]")
        h1.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        h1.setStyleSheet("color: #10B981;")
        l1.addWidget(h1)

        guide = QLabel(
            "Cómo crear tu cuenta y obtener tu API Key gratuita:\n"
            "  1) Haz clic en 'Abrir Google AI Studio' e inicia sesión con tu cuenta Google.\n"
            "  2) Pulsa 'Create API key' y selecciona o crea un proyecto.\n"
            "  3) Copia la clave (empieza por AIza...) y pégala aquí abajo."
        )
        guide.setWordWrap(True)
        guide.setStyleSheet("color: #CBD5E1; font-size: 12px;")
        l1.addWidget(guide)

        g_row = QHBoxLayout()
        self._gemini_in = QLineEdit()
        self._gemini_in.setPlaceholderText("Pega aquí tu Gemini API Key (AIza...)")
        self._gemini_in.setEchoMode(QLineEdit.EchoMode.Password)
        self._gemini_in.setStyleSheet(self._input_style())
        g_row.addWidget(self._gemini_in, stretch=1)

        open_ai_btn = QPushButton("Abrir Google AI Studio")
        open_ai_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        open_ai_btn.setFixedHeight(32)
        open_ai_btn.setStyleSheet("QPushButton { background: #191F2E; color: #38BDF8; border: 1px solid #38BDF8; border-radius: 8px; padding: 0 12px; }")
        open_ai_btn.clicked.connect(lambda: webbrowser.open("https://aistudio.google.com/apikey"))
        g_row.addWidget(open_ai_btn)

        chk_btn = QPushButton("Verificar Key")
        chk_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        chk_btn.setFixedHeight(32)
        chk_btn.setStyleSheet("QPushButton { background: #6366F1; color: #FFF; border: none; border-radius: 8px; padding: 0 12px; font-weight: 600; }")
        chk_btn.clicked.connect(self._verify_gemini_key)
        g_row.addWidget(chk_btn)
        l1.addLayout(g_row)

        self._key_status = QLabel("Estado: Sin verificar")
        self._key_status.setStyleSheet("color: #94A3B8; font-size: 12px;")
        l1.addWidget(self._key_status)
        il.addWidget(c1)

        # Optional APIs Card
        c2, l2 = self._card()
        h2 = QLabel("2. APIs Opcionales (Puedes dejarlas en blanco)")
        h2.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        h2.setStyleSheet("color: #F59E0B;")
        l2.addWidget(h2)

        l2.addWidget(QLabel("ElevenLabs API Key (Opcional — solo si eliges voz ElevenLabs Flash):"))
        self._el_key_in = QLineEdit()
        self._el_key_in.setPlaceholderText("sk_... (opcional)")
        self._el_key_in.setStyleSheet(self._input_style())
        l2.addWidget(self._el_key_in)

        l2.addWidget(QLabel("SerpAPI Key (Opcional — búsqueda web y vuelos avanzados):"))
        self._serp_in = QLineEdit()
        self._serp_in.setPlaceholderText("Opcional")
        self._serp_in.setStyleSheet(self._input_style())
        l2.addWidget(self._serp_in)

        l2.addWidget(QLabel("OpenWeather API Key (Opcional — widget de clima local):"))
        self._weather_in = QLineEdit()
        self._weather_in.setPlaceholderText("Opcional")
        self._weather_in.setStyleSheet(self._input_style())
        l2.addWidget(self._weather_in)

        il.addWidget(c2)
        il.addStretch()
        scroll.setWidget(inner)
        lay.addWidget(scroll)
        return w

    def _verify_gemini_key(self) -> None:
        key = self._gemini_in.text().strip()
        if not key:
            self._key_status.setText("Estado: Pega una Gemini API Key primero.")
            self._key_status.setStyleSheet("color: #F59E0B;")
            return
        self._key_status.setText("Estado: Verificando con Google Gemini...")
        self._key_status.setStyleSheet("color: #38BDF8;")

        def _worker():
            try:
                from google import genai
                client = genai.Client(api_key=key)
                list(client.models.list())
                self._key_check_sig.emit(True, "API Key válida y activa ✓")
            except Exception as exc:
                self._key_check_sig.emit(False, f"Error verificando: {exc}")

        threading.Thread(target=_worker, daemon=True).start()

    def _on_key_checked(self, ok: bool, msg: str) -> None:
        self._key_status.setText(f"Estado: {msg}")
        self._key_status.setStyleSheet(f"color: {'#10B981' if ok else '#F43F5E'}; font-weight: 600;")

    # ── Page 4: Voice & Live2D Skin ────────────────────────────────────────
    def _page_voice_skin(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        card, cl = self._card()

        t = QLabel("Motor de Voz (TTS) y Skin Live2D")
        t.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        cl.addWidget(t)

        combo_ss = (
            "QComboBox { background: #07090D; color: #F1F5F9; border: 1px solid #242B3D; border-radius: 8px; padding: 6px 10px; }"
            "QComboBox QAbstractItemView { background: #121620; color: #F1F5F9; selection-background-color: #1C1F3B; }"
        )

        cl.addWidget(QLabel("Motor de voz principal:"))
        self._tts_combo = QComboBox()
        self._tts_combo.setStyleSheet(combo_ss)
        self._tts_combo.addItem("Gemini Live (Nativo · Recomendado)", "gemini")
        self._tts_combo.addItem("Edge Neural (Microsoft · Gratuito sin GPU)", "edgetts")
        self._tts_combo.addItem("ElevenLabs Flash v2.5 (Requiere API Key)", "elevenlabs")
        self._tts_combo.addItem("Coqui XTTS-v2 (Local · Clonación de voz)", "coqui_xtts")
        self._tts_combo.currentIndexChanged.connect(self._refresh_voice_choices)
        cl.addWidget(self._tts_combo)

        cl.addWidget(QLabel("Voz / Hablante:"))
        self._voice_combo = QComboBox()
        self._voice_combo.setStyleSheet(combo_ss)
        cl.addWidget(self._voice_combo)
        self._refresh_voice_choices()

        cl.addWidget(QLabel("Skin / Modelo Live2D del Asistente:"))
        self._skin_combo = QComboBox()
        self._skin_combo.setStyleSheet(combo_ss)
        try:
            from core.live2d.skin_manager import discover_live2d_skins
            skins = discover_live2d_skins()
            for sname in skins.keys():
                self._skin_combo.addItem(sname, sname)
        except Exception:
            self._skin_combo.addItem("Edith", "Edith")
        cl.addWidget(self._skin_combo)

        cl.addStretch()
        lay.addWidget(card)
        return w

    def _refresh_voice_choices(self) -> None:
        self._voice_combo.clear()
        eng = self._tts_combo.currentData()
        try:
            from memory.config_manager import (
                AVAILABLE_VOICES,
                COQUI_XTTS_SPEAKERS,
                EDGE_SPANISH_VOICES,
                ELEVENLABS_PRESET_VOICES,
            )
            if eng == "gemini":
                for v in AVAILABLE_VOICES:
                    self._voice_combo.addItem(v, v)
            elif eng == "edgetts":
                for vid, (vname, gen, desc) in EDGE_SPANISH_VOICES.items():
                    self._voice_combo.addItem(f"{vname} ({gen}) — {desc}", vid)
            elif eng == "elevenlabs":
                for vid, (vname, gen, desc) in ELEVENLABS_PRESET_VOICES.items():
                    self._voice_combo.addItem(f"{vname} ({gen}) — {desc}", vid)
            else:
                for spk in COQUI_XTTS_SPEAKERS:
                    self._voice_combo.addItem(spk, spk)
        except Exception:
            self._voice_combo.addItem("Aoede", "Aoede")

    # ── Page 5: Donation & Credits ─────────────────────────────────────────
    def _page_finish(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        card, cl = self._card()

        t = QLabel("¡Todo listo para producción!")
        t.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        t.setStyleSheet("color: #10B981;")
        cl.addWidget(t)

        credits = QLabel(
            "Creado con dedicación por Groovi Developer.\n"
            "Viernes se distribuye de forma 100% gratuita para la comunidad.\n\n"
            "Si deseas apoyar el desarrollo continuo, nuevas integraciones y mantenimiento, "
            "puedes hacer una donación voluntaria a través de PayPal:"
        )
        credits.setWordWrap(True)
        credits.setStyleSheet("color: #CBD5E1; font-size: 13px;")
        cl.addWidget(credits)

        pay_btn = QPushButton("💛 Apoyar proyecto vía PayPal (Groovi Developer)")
        pay_btn.setFixedHeight(40)
        pay_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        pay_btn.setStyleSheet(
            "QPushButton { background: rgba(251,191,36,0.16); color: #FBBF24; border: 1px solid #FBBF24; "
            "border-radius: 9px; font-weight: 700; font-size: 13px; }"
            "QPushButton:hover { background: rgba(251,191,36,0.28); }"
        )
        pay_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(PAYPAL_DONATE_URL)))
        cl.addWidget(pay_btn)

        doc_btn = QPushButton("📖 Abrir Documentación Oficial Interactiva")
        doc_btn.setFixedHeight(36)
        doc_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        doc_btn.setStyleSheet(
            "QPushButton { background: #191F2E; color: #38BDF8; border: 1px solid #36415C; border-radius: 9px; font-weight: 600; }"
        )
        doc_btn.clicked.connect(self._open_docs)
        cl.addWidget(doc_btn)

        cl.addStretch()
        lay.addWidget(card)
        return w

    def _open_docs(self) -> None:
        doc_path = BASE_DIR / "documentación Oficial" / "index.html"
        if doc_path.exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(doc_path)))

    def _save_and_launch(self) -> None:
        gemini_key = self._gemini_in.text().strip()
        if not gemini_key:
            QMessageBox.warning(
                self,
                "API Key obligatoria",
                "Debes ingresar tu Google Gemini API Key en el paso 3 para que Viernes pueda funcionar.",
            )
            self._set_step(2)
            return

        from memory.config_manager import (
            save_api_keys,
            save_assistant_config,
            save_coqui_config,
            save_edge_voice,
            save_elevenlabs_config,
            save_live2d_skin,
            save_serpapi_key,
            save_tts_engine,
            save_voice,
            save_weather_key,
        )

        save_api_keys(gemini_key)
        save_assistant_config(
            self._assistant_name_in.text().strip() or "Viernes",
            self._user_name_in.text().strip(),
        )
        if self._serp_in.text().strip():
            save_serpapi_key(self._serp_in.text().strip())
        if self._weather_in.text().strip():
            save_weather_key(self._weather_in.text().strip())

        eng = str(self._tts_combo.currentData() or "gemini")
        voice = str(self._voice_combo.currentData() or "")
        save_tts_engine(eng)
        if eng == "gemini" and voice:
            save_voice(voice)
        elif eng == "edgetts" and voice:
            save_edge_voice(voice)
        elif eng == "elevenlabs":
            save_elevenlabs_config(self._el_key_in.text().strip(), voice or "21m00Tcm4TlvDq8ikWAM")
        elif eng == "coqui_xtts":
            save_coqui_config(voice or "Ana Florence", "", "es")

        skin = str(self._skin_combo.currentData() or "Edith")
        save_live2d_skin(skin)

        subprocess.Popen([sys.executable, str(BASE_DIR / "main.py")], cwd=str(BASE_DIR))
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ViernesInstaller()
    win.show()
    sys.exit(app.exec())
