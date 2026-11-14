"""
Edith 3D VRM Engine Widget
===========================
High-performance 3D Humanoid VRM 1.0 Avatar controller hosted in QtWebEngine.
Integrates Three.js, @pixiv/three-vrm, SpringBone secondary physics,
procedural body kinetics, gaze tracking, emotion engine and conversational lip-sync.
Served via an embedded localhost server to ensure 100% compliant WebGL asset streaming and ES module imports.
"""

from __future__ import annotations

import json
import os
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional

from PyQt6.QtCore import QUrl, pyqtSignal, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebEngineCore import QWebEngineSettings
    WEBENGINE_AVAILABLE = True
except Exception:
    WEBENGINE_AVAILABLE = False
    QWebEngineView = QWidget


# ── EMBEDDED LOCAL SERVER FOR VRM / ES MODULES ──────────────────────────────
_VRM_SERVER = None
_VRM_SERVER_PORT = None
_VRM_SERVER_LOCK = threading.Lock()


class _VRMHTTPHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def log_message(self, format, *args):
        pass  # Quiet logging


def _get_or_start_vrm_server() -> int:
    global _VRM_SERVER, _VRM_SERVER_PORT
    with _VRM_SERVER_LOCK:
        if _VRM_SERVER_PORT is not None:
            return _VRM_SERVER_PORT

        vrm_dir = os.path.abspath(os.path.dirname(__file__))
        server = ThreadingHTTPServer(("127.0.0.1", 0), lambda *a, **k: _VRMHTTPHandler(*a, directory=vrm_dir, **k))
        _VRM_SERVER_PORT = server.server_address[1]
        _VRM_SERVER = server
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        print(f"[VRM 3D] Local HTTP server active on http://127.0.0.1:{_VRM_SERVER_PORT}/")
        return _VRM_SERVER_PORT


def discover_vrm_models() -> List[str]:
    """Descubre todos los archivos .vrm disponibles en core/vrm/models/."""
    models_dir = Path(__file__).resolve().parent / "models"
    if not models_dir.exists():
        return []
    return sorted([f.name for f in models_dir.glob("*.vrm") if f.is_file()])


class VRMWidget(QWidget):
    """
    Host widget for Edith VRM 3D humanoid avatar.
    Maintains exact API parity with Live2DWidget for zero-friction backend interchangeability.
    """

    model_error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet("background: transparent;")

        self._active = False
        self._page_loaded = False
        self._pending_js: list[str] = []
        self._is_speaking = False
        self._amplitude = 0.0
        self._state = "IDLE"
        self._current_model = "edithof.vrm"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        if not WEBENGINE_AVAILABLE:
            err_lbl = QLabel("WebGL/QtWebEngine no disponible para renderizado 3D.")
            err_lbl.setStyleSheet("color: #ff4466; background: transparent; font-family: monospace;")
            layout.addWidget(err_lbl)
            self._view = None
            return

        self._view = QWebEngineView(self)
        self._view.setStyleSheet("background: transparent;")
        self._view.page().setBackgroundColor(QColor(0, 0, 0, 0))
        self._view.loadFinished.connect(self._on_load_finished)

        # Enable WebGL and hardware acceleration
        settings = self._view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)

        layout.addWidget(self._view)

        # Iniciar servidor local y cargar viewer.html
        port = _get_or_start_vrm_server()

        # Determinar modelo activo (priorizando edithof.vrm)
        try:
            from memory.config_manager import get_vrm_model
            active_model = get_vrm_model()
        except Exception:
            active_model = "edithof.vrm"

        available = discover_vrm_models()
        if available and active_model not in available:
            if "edithof.vrm" in available:
                active_model = "edithof.vrm"
            else:
                active_model = available[0]

        self._current_model = active_model
        url = QUrl(f"http://127.0.0.1:{port}/viewer.html?model=./models/{active_model}")
        self._view.setUrl(url)
        self._active = True
        print(f"[VRM 3D] Inicializado con modelo '{self._current_model}' en puerto {port}.")

    def _on_load_finished(self, ok: bool) -> None:
        self._page_loaded = bool(ok)
        if ok and self._view and self._active:
            for js in self._pending_js:
                self._view.page().runJavaScript(js)
            self._pending_js.clear()

    def _run_js(self, js: str) -> None:
        if not self._view or not self._active:
            return
        if self._page_loaded:
            self._view.page().runJavaScript(js)
        else:
            self._pending_js.append(js)

    @property
    def current_model(self) -> str:
        return self._current_model

    def load_model(self, model_name: str) -> None:
        """Carga un nuevo modelo VRM en el motor 3D."""
        if not model_name:
            return
        clean_name = os.path.basename(model_name)
        if not clean_name.lower().endswith(".vrm"):
            clean_name = f"{clean_name}.vrm"

        self._current_model = clean_name
        try:
            from memory.config_manager import save_vrm_model
            save_vrm_model(clean_name)
        except Exception:
            pass

        self._run_js(f"if (window.vrmApp) window.vrmApp.loadModel('./models/{clean_name}');")

    def set_speaking(self, is_speaking: bool) -> None:
        """Indica si el asistente está emitiendo voz."""
        self._is_speaking = bool(is_speaking)
        self._run_js(f"if (window.vrmApp) window.vrmApp.setSpeaking({'true' if self._is_speaking else 'false'});")

    def set_level(self, amplitude: float) -> None:
        """Actualiza la amplitud acústica para el lip-sync continuo."""
        self._amplitude = max(0.0, min(1.0, float(amplitude)))
        self._run_js(f"if (window.vrmApp) window.vrmApp.setAmplitude({self._amplitude:.3f});")

    def set_state(self, state: str) -> None:
        """Actualiza el estado general (IDLE, LISTENING, THINKING, SPEAKING, SLEEPING)."""
        self._state = str(state or "IDLE").upper()
        self._run_js(f"if (window.vrmApp) window.vrmApp.setState('{self._state}');")

    def glance(self, dx: float, dy: float, hold: float = 1.5) -> None:
        """Orienta la mirada de Edith en el espacio 3D."""
        self._run_js(f"if (window.vrmApp) window.vrmApp.glance({float(dx):.2f}, {float(dy):.2f});")

    def set_emotion(self, name: str, intensity: float = 1.0, duration: float = 0.0) -> None:
        """Aplica una emoción con duración e intensidad."""
        self._run_js(f"if (window.vrmApp) window.vrmApp.setEmotion('{name}', {float(intensity):.2f}, {float(duration):.2f});")

    def trigger_gesture(self, gesture_name: str, duration: float = 3.5, intensity: float = 1.0) -> None:
        """Ejecuta un gesto corporal estructurado (WAVE_HELLO, EXPLAIN, THINKING, etc.)."""
        self._run_js(f"if (window.vrmApp) window.vrmApp.triggerGesture('{gesture_name}', {float(duration):.2f}, {float(intensity):.2f});")

    def set_semantic_intent(self, intent: str, metadata: Any = None) -> None:
        """Canal de intención semántica desde el SpeechAnimationController."""
        meta_json = json.dumps(metadata) if metadata else "{}"
        self._run_js(f"if (window.vrmApp) window.vrmApp.setSemanticIntent('{intent}', {meta_json});")

    def set_personality_params(self, params: Dict[str, Any]) -> None:
        """Configura dinámica corporal según la personalidad activa."""
        if params:
            self._run_js(f"if (window.vrmApp) window.vrmApp.setPersonalityParams({json.dumps(params)});")

    def set_camera_preset(self, preset: str) -> None:
        """Ajusta el encuadre de cámara ('full', 'upper', 'portrait')."""
        self._run_js(f"if (window.vrmApp) window.vrmApp.setCameraPreset('{preset}');")

    def sleep(self) -> None:
        """Pone el modelo 3D en modo reposo."""
        self.set_state("SLEEPING")

    def wake(self) -> None:
        """Despierta el modelo 3D a estado IDLE."""
        self.set_state("IDLE")

    def trigger_action(self, name: str) -> None:
        """Compatibilidad con Live2D trigger_action."""
        act_map = {
            "nod": "NOD_AGREE",
            "shake": "HEAD_SHAKE",
            "think": "THINKING",
            "wave": "WAVE_HELLO",
            "greeting": "WAVE_HELLO",
            "explain": "EXPLAIN",
            "curious": "THINKING",
        }
        mapped = act_map.get(str(name).lower(), name)
        self.trigger_gesture(mapped)

    def interrupt_gestures(self) -> None:
        """Interrumpe gestos en curso regresando a reposo."""
        self._run_js("if (window.vrmApp) window.vrmApp.currentGesture = null;")

    def set_float_mode(self, mode: Any) -> None:
        """Activa o desactiva la secuencia física de vuelo/levitación."""
        is_float = bool(mode) and str(mode).lower() not in ("false", "0", "off", "none")
        self._run_js(f"if (window.vrmApp) window.vrmApp.setFloatMode({'true' if is_float else 'false'});")

    def notify_task_completed(self) -> None:
        self.set_emotion("happy", 0.85, 2.5)
        self.trigger_gesture("NOD_AGREE", 2.0)

    def notify_task_error(self, error_msg: str = "") -> None:
        self.set_emotion("confused", 0.85, 2.5)
        self.trigger_gesture("HEAD_SHAKE", 2.0)

    def set_autonomy_enabled(self, enabled: bool) -> None:
        self._run_js(f"if (window.vrmApp) window.vrmApp.personality.spontaneity = {'1.0' if enabled else '0.0'};")

    def set_spontaneity_level(self, level: float) -> None:
        self._run_js(f"if (window.vrmApp) window.vrmApp.personality.spontaneity = {float(level):.2f};")

    def set_mood(self, mood: str) -> None:
        self.set_emotion(str(mood).lower(), 0.7, 4.0)

    def set_presentation_mode(self, enabled: bool) -> None:
        if enabled:
            self.set_camera_preset("upper")
            self.glance(0.48, -0.05, 3.5)
        else:
            self.set_camera_preset("full")

    def pause(self) -> None:
        if self._view and self._active:
            self._view.page().runJavaScript("if (window.vrmApp) window.vrmApp.isRunning = false;")

    def resume(self) -> None:
        if self._view and self._active:
            self._view.page().runJavaScript("if (window.vrmApp && !window.vrmApp.isRunning) { window.vrmApp.isRunning = true; window.vrmApp.animate(); }")
