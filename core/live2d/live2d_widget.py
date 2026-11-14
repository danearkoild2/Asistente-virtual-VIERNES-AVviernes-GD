"""
Edith Live2D Pro Engine Widget
==============================
Native PyQt6 WebEngine wrapper hosting the PixiJS + Live2D Cubism Core real-time avatar.
High-performance 60 FPS continuous mesh deformation and physics with zero photo-by-photo overhead.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
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


class Live2DWidget(QWidget):
    """Host widget for Edith Live2D avatar rendered in real time with PixiJS & Cubism 4 Core."""

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
        self._last_sent_amp = -1.0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        if not WEBENGINE_AVAILABLE:
            err_lbl = QLabel("WebGL/QtWebEngine no disponible en este entorno.")
            err_lbl.setStyleSheet("color: #ff4466; background: transparent; font-family: monospace;")
            layout.addWidget(err_lbl)
            self._view = None
            return

        self._view = QWebEngineView(self)
        self._view.setStyleSheet("background: transparent;")
        self._view.page().setBackgroundColor(QColor(0, 0, 0, 0))
        self._view.loadFinished.connect(self._on_load_finished)

        # Enable local file and WebGL access
        settings = self._view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)

        layout.addWidget(self._view)

        # Load Edith viewer HTML with current skin parameter
        html_file = Path(__file__).resolve().parent / "viewer.html"
        if html_file.exists():
            try:
                from memory.config_manager import get_live2d_skin
                from core.live2d.skin_manager import get_skin_model_url
                cur_skin = get_live2d_skin()
                model_url = get_skin_model_url(cur_skin)
            except Exception:
                model_url = "../../edith/edith.model3.json"

            url = QUrl.fromLocalFile(str(html_file))
            if model_url:
                url.setQuery(f"model={model_url}")
            self._view.setUrl(url)
        else:
            self.model_error.emit("Archivo core/live2d/viewer.html no encontrado.")

        self._active = True

    def _on_load_finished(self, ok: bool) -> None:
        self._page_loaded = bool(ok)
        if ok and self._view and self._active:
            for js in self._pending_js:
                self._view.page().runJavaScript(js)
            self._pending_js.clear()
            try:
                from memory.config_manager import get_edith_autonomy_enabled, get_edith_spontaneity_level
                auto = get_edith_autonomy_enabled()
                lvl = get_edith_spontaneity_level()
                self._view.page().runJavaScript(
                    f"if (window.live2dApp) {{ window.live2dApp.setAutonomyEnabled({'true' if auto else 'false'}); window.live2dApp.setSpontaneityLevel({lvl:.2f}); }}"
                )
            except Exception:
                pass

    def _run_js(self, js: str) -> None:
        if not self._view or not self._active:
            return
        if self._page_loaded:
            self._view.page().runJavaScript(js)
        else:
            self._pending_js.append(js)

    def load_model(self, model_url: str) -> None:
        """Load a new Live2D model into the active WebEngine runtime."""
        self._run_js(f"if (window.live2dApp) window.live2dApp.loadModel('{model_url}');")

    def play_native_motion(self, motion_name: str) -> None:
        """Play a native Live2D Cubism motion (e.g. haoqi, qizi, linghun, keshui, yaotou, zhentou)."""
        self._run_js(f"if (window.live2dApp) window.live2dApp.playNativeMotion('{motion_name}');")

    def set_speaking(self, speaking: bool) -> None:
        self._is_speaking = bool(speaking)
        self._run_js(f"if (window.live2dApp) window.live2dApp.setSpeaking({'true' if self._is_speaking else 'false'});")

    def set_level(self, amp: float) -> None:
        if abs(amp - self._last_sent_amp) < 0.02:
            return
        self._amplitude = max(0.0, min(1.0, float(amp)))
        self._last_sent_amp = self._amplitude
        self._run_js(f"if (window.live2dApp) window.live2dApp.setAmplitude({self._amplitude:.3f});")

    def set_state(self, state: str) -> None:
        self._state = str(state).strip().upper()
        self._run_js(f"if (window.live2dApp) window.live2dApp.setState('{self._state}');")
        if self._state in ("THINKING", "SEARCHING"):
            self.set_prop_state("hologram_rings", True, duration=6.0)
        elif self._state == "SLEEPING":
            self.set_prop_state("flameAura", False)
            self.set_prop_state("hologramRings", False)
            self.set_prop_state("grimoire", False)

    def glance(self, dx: float, dy: float, hold: float = 0.0) -> None:
        self._run_js(f"if (window.live2dApp) window.live2dApp.glance({float(dx):.2f}, {float(dy):.2f});")

    def set_expression(self, name: str) -> None:
        self._run_js(f"if (window.live2dApp) window.live2dApp.setExpression('{name}');")

    def set_emotion(self, name: str, intensity: float = 1.0, duration: float = 0.0) -> None:
        """Trigger an emotional state for Edith/HuoHuo (e.g. happy, sad, angry, shy, surprised, curious, bored, confused, proud, sleepy, enthusiastic, relieved)."""
        self._run_js(f"if (window.live2dApp) window.live2dApp.setEmotion('{name}', {float(intensity):.2f}, {float(duration):.2f});")

    def trigger_action(self, name: str) -> None:
        """Trigger an autonomous spontaneous action."""
        self._run_js(f"if (window.live2dApp) window.live2dApp.triggerAction('{name}');")

    def set_semantic_intent(self, intent: str, metadata: dict | None = None) -> None:
        meta_json = json.dumps(metadata or {})
        self._run_js(f"if (window.live2dApp) window.live2dApp.setSemanticIntent('{intent}', {meta_json});")

    def trigger_gesture(self, name: str, duration: float = 0.0, intensity: float = 1.0) -> None:
        """Trigger a specific expressive arm, shoulder, or posture gesture from the GestureLibrary or native motion."""
        self._run_js(f"if (window.live2dApp) window.live2dApp.triggerGesture('{name}', {float(duration):.2f}, {float(intensity):.2f});")

    def interrupt_gestures(self) -> None:
        self._run_js("if (window.live2dApp) window.live2dApp.interruptGestures();")

    def set_float_mode(self, mode: str) -> None:
        self._run_js(f"if (window.live2dApp) window.live2dApp.setFloatMode('{mode}');")

    def set_float_params(self, speed: float = 1.0, amplitude: float = 1.0) -> None:
        self._run_js(f"if (window.live2dApp) window.live2dApp.setFloatParams({float(speed):.2f}, {float(amplitude):.2f});")

    def set_autonomy_enabled(self, enabled: bool) -> None:
        self._run_js(f"if (window.live2dApp) window.live2dApp.setAutonomyEnabled({'true' if enabled else 'false'});")

    def set_spontaneity_level(self, level: float) -> None:
        self._run_js(f"if (window.live2dApp) window.live2dApp.setSpontaneityLevel({float(level):.2f});")

    def set_mood(self, mood: str) -> None:
        self._run_js(f"if (window.live2dApp) window.live2dApp.setMood('{mood}');")

    def set_debug_mode(self, enabled: bool) -> None:
        self._run_js(f"if (window.live2dApp) window.live2dApp.setDebugMode({'true' if enabled else 'false'});")

    def set_presentation_mode(self, active: bool) -> None:
        self._run_js(f"if (window.live2dApp) window.live2dApp.setPresentationMode({'true' if active else 'false'});")

    def interact(self, interaction_type: str = "headpat") -> None:
        self._run_js(f"if (window.live2dApp) window.live2dApp.interact('{interaction_type}');")

    def set_prop_state(self, prop_name: str, enabled: bool, duration: float = 0.0) -> None:
        self._run_js(f"if (window.live2dApp) window.live2dApp.setPropState('{prop_name}', {'true' if enabled else 'false'}, {float(duration):.2f});")

    def set_game_mode(self, mode: str) -> None:
        self._run_js(f"if (window.live2dApp) window.live2dApp.setGameMode('{mode}');")

    def trigger_game_gesture(self, gesture_name: str, duration: float = 0.0, intensity: float = 1.0) -> None:
        self._run_js(f"if (window.live2dApp) window.live2dApp.triggerGameGesture('{gesture_name}', {float(duration):.2f}, {float(intensity):.2f});")

    def notify_task_completed(self) -> None:
        """Reaction when a task/tool successfully finishes: victory celebration, HUD rings & pride!"""
        self.set_emotion("proud", intensity=0.95, duration=3.8)
        self.trigger_game_gesture("GAME_VICTORY_CELEBRATE", duration=3.8, intensity=1.0)
        self.set_prop_state("hologram_rings", True, duration=3.5)

    def notify_task_error(self, error_msg: str = "") -> None:
        """Reaction when an error occurs: mild confusion or concern."""
        self.set_emotion("confused", intensity=0.8, duration=3.0)

    def get_status(self, callback=None) -> None:
        """Query runtime status of the Live2D autonomy engine."""
        if self._view and self._active and callback:
            self._view.page().runJavaScript("window.live2dApp ? window.live2dApp.getStatus() : null;", callback)

    def wake(self) -> None:
        self.set_state("LISTENING")

    def sleep(self) -> None:
        self.set_state("SLEEPING")

    def pause(self) -> None:
        """Pause Live2D animation loop to release CPU/GPU when hidden."""
        if self._view and self._active:
            self._view.page().runJavaScript("if (window.live2dApp) window.live2dApp.pauseRendering();")

    def resume(self) -> None:
        """Resume Live2D animation loop when avatar is visible."""
        if self._view and self._active:
            self._view.page().runJavaScript("if (window.live2dApp) window.live2dApp.resumeRendering();")

    def cleanup(self) -> None:
        """Unload and clean up WebGL resources."""
        self.pause()
        self._active = False
        if self._view:
            self._view.setUrl(QUrl("about:blank"))
