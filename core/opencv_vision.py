"""
core/opencv_vision.py — Motor nativo de Visión por Computadora con OpenCV (cv2) para VIERNES.

Sustituye al antiguo modo visión genérico por un pipeline OpenCV nativo:
- Captura continua de cámara web y captura de pantalla con cv2 / mss.
- Detección local en tiempo real (0 tokens): rostros (Haar Cascade), movimiento (absdiff/contornos),
  códigos QR (QRCodeDetector) y métricas de iluminación.
- Enlace inteligente con Gemini/IA local solo cuando hay eventos relevantes o petición directa,
  minimizando el consumo de tokens.
"""
from __future__ import annotations

import base64
import json
import sys
import threading
import time
from collections import deque
from pathlib import Path
from typing import Callable, Optional

import cv2
import numpy as np

try:
    import mss
    _MSS_AVAILABLE = True
except ImportError:
    _MSS_AVAILABLE = False


def _get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


BASE_DIR = _get_base_dir()
CONFIG_PATH = BASE_DIR / "config" / "api_keys.json"


class OpenCVContextMemory:
    """Memoria temporal en RAM de detecciones OpenCV y contexto visual."""

    def __init__(self, max_history: int = 8):
        self._lock = threading.Lock()
        self.scene_summary: str = "OpenCV en espera."
        self.elements_in_view: list[str] = []
        self.last_observation_time: float = 0.0
        self.last_metrics: dict = {
            "faces": 0,
            "motion_pct": 0.0,
            "brightness": 0.0,
            "qr": [],
        }
        self.history: deque = deque(maxlen=max_history)

    def update_metrics(self, metrics: dict) -> None:
        with self._lock:
            self.last_metrics = dict(metrics)
            self.last_observation_time = time.time()

    def update_observation(self, summary: str, elements: list[str] | None = None) -> None:
        with self._lock:
            self.last_observation_time = time.time()
            self.scene_summary = summary.strip()
            if elements is not None:
                self.elements_in_view = list(elements)
            self.history.append({
                "time": self.last_observation_time,
                "summary": self.scene_summary,
                "metrics": dict(self.last_metrics),
            })

    def record_event(self, event_text: str) -> None:
        with self._lock:
            self.history.append({"time": time.time(), "event": event_text})

    def get_context_prompt(self) -> str:
        with self._lock:
            m = self.last_metrics
            age = int(time.time() - self.last_observation_time) if self.last_observation_time else -1
            if age < 0:
                return "[OPENCV VISION] Cámara OpenCV inactiva."
            qr_str = f", QR={m['qr']}" if m.get("qr") else ""
            return (
                f"[OPENCV VISION — hace {age}s] "
                f"Rostros={m.get('faces', 0)}, Movimiento={m.get('motion_pct', 0.0):.1f}%, "
                f"Brillo={m.get('brightness', 0):.0f}/255{qr_str}. "
                f"Escena: {self.scene_summary}"
            )


class _RoomSentinelCompat:
    """Compatibilidad con hooks de main.py / ui.py usando el motor OpenCV."""

    def __init__(self, owner: "OpenCVVisionCoordinator"):
        self._owner = owner

    def stop(self) -> None:
        self._owner.stop_continuous_vision()


class OpenCVVisionCoordinator:
    """Coordinador singleton de visión nativa con OpenCV (cv2)."""

    _instance: Optional["OpenCVVisionCoordinator"] = None
    _inst_lock = threading.Lock()

    def __new__(cls):
        with cls._inst_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self.visual_memory = OpenCVContextMemory()
        self.room_sentinel = _RoomSentinelCompat(self)
        self.main_window_ref = None
        self.ui_ref = None

        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._subscribers: list[Callable[[bytes], None]] = []
        self._sub_lock = threading.Lock()

        self._latest_jpeg: Optional[bytes] = None
        self._latest_bgr: Optional[np.ndarray] = None
        self._prev_gray: Optional[np.ndarray] = None
        self._frame_lock = threading.Lock()
        self._is_analyzing = False
        self._last_ai_ts = 0.0

        cascade_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
        self._face_cascade = cv2.CascadeClassifier(str(cascade_path)) if cascade_path.exists() else None
        self._qr_detector = cv2.QRCodeDetector()

    # ── Configuración ────────────────────────────────────────────────────────
    def get_config(self) -> dict:
        defaults = {
            "camera_index": 0,
            "preview_mode": "pip",
            "draw_hud_boxes": True,
            "motion_threshold_pct": 3.5,
            "analysis_interval_sec": 30.0,
            "auto_ai_on_event": False,  # Ahorro de tokens por defecto
            "prefer_local_vision": False,
        }
        try:
            if CONFIG_PATH.exists():
                data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
                defaults.update(data.get("opencv_vision", {}))
        except Exception:
            pass
        return defaults

    def is_active(self) -> bool:
        return self._running

    def register_frame_subscriber(self, cb: Callable[[bytes], None]) -> None:
        with self._sub_lock:
            if cb not in self._subscribers:
                self._subscribers.append(cb)

    def unregister_frame_subscriber(self, cb: Callable[[bytes], None]) -> None:
        with self._sub_lock:
            if cb in self._subscribers:
                self._subscribers.remove(cb)

    def _emit_frame(self, jpeg_bytes: bytes) -> None:
        with self._sub_lock:
            subs = list(self._subscribers)
        for cb in subs:
            try:
                cb(jpeg_bytes)
            except Exception:
                pass

    # ── Ciclo continuo OpenCV ────────────────────────────────────────────────
    def start_continuous_vision(self) -> bool:
        if self._running:
            return True
        self._running = True
        self._thread = threading.Thread(target=self._capture_loop, daemon=True, name="OpenCVVisionLoop")
        self._thread.start()
        return True

    def stop_continuous_vision(self) -> None:
        self._running = False
        self._prev_gray = None

    def toggle_opencv_vision(self) -> bool:
        if self._running:
            self.stop_continuous_vision()
            return False
        self.start_continuous_vision()
        return True

    def toggle_room_sentinel(self) -> bool:
        return self.toggle_opencv_vision()

    def _capture_loop(self) -> None:
        cfg = self.get_config()
        cam_idx = int(cfg.get("camera_index", 0))
        cap = cv2.VideoCapture(cam_idx, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(cam_idx)
        if not cap.isOpened():
            self._running = False
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

        try:
            frame_i = 0
            while self._running:
                ok, frame = cap.read()
                if not ok or frame is None:
                    time.sleep(0.1)
                    continue

                frame_i += 1
                annotated = frame
                if frame_i % 3 == 0:
                    metrics, annotated = self.analyze_bgr_local(
                        frame, draw_boxes=bool(cfg.get("draw_hud_boxes", True))
                    )
                    self.visual_memory.update_metrics(metrics)
                    if (
                        cfg.get("auto_ai_on_event", False)
                        and metrics["motion_pct"] >= float(cfg.get("motion_threshold_pct", 3.5))
                        and (time.time() - self._last_ai_ts) >= float(cfg.get("analysis_interval_sec", 30.0))
                    ):
                        self._last_ai_ts = time.time()
                        threading.Thread(target=self.analyze_current_scene, daemon=True).start()

                ok_jpg, buf = cv2.imencode(".jpg", annotated, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                if ok_jpg:
                    jpg = buf.tobytes()
                    with self._frame_lock:
                        self._latest_bgr = frame
                        self._latest_jpeg = jpg
                    self._emit_frame(jpg)

                time.sleep(0.05)
        finally:
            cap.release()

    # ── Análisis local OpenCV (0 tokens) ─────────────────────────────────────
    def analyze_bgr_local(self, frame: np.ndarray, draw_boxes: bool = False) -> tuple[dict, np.ndarray]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = float(np.mean(gray))

        motion_pct = 0.0
        blur = cv2.GaussianBlur(gray, (15, 15), 0)
        if self._prev_gray is not None and self._prev_gray.shape == blur.shape:
            diff = cv2.absdiff(self._prev_gray, blur)
            _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
            motion_pct = float(np.count_nonzero(thresh) * 100.0 / thresh.size)
        self._prev_gray = blur

        faces_boxes = []
        if self._face_cascade is not None:
            detected = self._face_cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=5, minSize=(40, 40))
            faces_boxes = [(int(x), int(y), int(w), int(h)) for (x, y, w, h) in detected]

        qr_list = []
        try:
            data, pts, _ = self._qr_detector.detectAndDecode(frame)
            if data:
                qr_list.append(data)
        except Exception:
            pts = None

        out = frame.copy() if draw_boxes else frame
        if draw_boxes:
            for (x, y, w, h) in faces_boxes:
                cv2.rectangle(out, (x, y), (x + w, y + h), (0, 230, 180), 2)
                cv2.putText(out, "FACE", (x, max(16, y - 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 230, 180), 1)
            cv2.putText(
                out,
                f"OpenCV | Faces:{len(faces_boxes)} Mov:{motion_pct:.1f}%",
                (10, 22),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 230, 180),
                1,
            )

        metrics = {
            "faces": len(faces_boxes),
            "face_boxes": faces_boxes,
            "motion_pct": round(motion_pct, 2),
            "brightness": round(brightness, 1),
            "qr": qr_list,
            "resolution": f"{frame.shape[1]}x{frame.shape[0]}",
        }
        return metrics, out

    def get_latest_jpeg_frame(self) -> Optional[bytes]:
        with self._frame_lock:
            return self._latest_jpeg

    def capture_single_bgr(self, source: str = "camera", image_path: str = "") -> Optional[np.ndarray]:
        if image_path and Path(image_path).is_file():
            return cv2.imread(image_path)
        if source == "screen" and _MSS_AVAILABLE:
            with mss.mss() as sct:
                mon = sct.monitors[1]
                raw = np.array(sct.grab(mon))
                return cv2.cvtColor(raw, cv2.COLOR_BGRA2BGR)
        with self._frame_lock:
            if self._running and self._latest_bgr is not None:
                return self._latest_bgr.copy()
        cap = cv2.VideoCapture(int(self.get_config().get("camera_index", 0)), cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None
        try:
            for _ in range(3):
                cap.read()
            ok, frame = cap.read()
            return frame if ok else None
        finally:
            cap.release()

    def capture_frame_for_query(self, source: str = "camera") -> tuple[bytes, str]:
        bgr = self.capture_single_bgr(source=source)
        if bgr is not None:
            ok, buf = cv2.imencode(".jpg", bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
            if ok:
                return buf.tobytes(), "image/jpeg"
        if source == "camera":
            from actions.screen_processor import _capture_camera
            return _capture_camera()
        from actions.screen_processor import _capture_screen
        return _capture_screen()

    def analyze_current_scene(self) -> dict:
        if self._is_analyzing:
            return {"status": "busy"}
        self._is_analyzing = True
        try:
            frame_bytes = self.get_latest_jpeg_frame()
            if not frame_bytes:
                frame_bytes, _ = self.capture_frame_for_query("camera")
            if not frame_bytes:
                return {"status": "no_frame"}
            from core import gemini
            b64 = base64.b64encode(frame_bytes).decode("ascii")
            resp = gemini.ask_image(
                ladder=gemini.FAST,
                image_data=b64,
                mime_type="image/jpeg",
                prompt="Describe en 1-2 oraciones breves en español lo que ves en la escena.",
                timeout=12.0,
            )
            if resp:
                self.visual_memory.update_observation(resp)
                return {"status": "ok", "summary": resp}
        except Exception:
            pass
        finally:
            self._is_analyzing = False
        return {"status": "failed"}

    def get_visual_context_prompt(self) -> str:
        return self.visual_memory.get_context_prompt()

    def get_sensory_context_prompt(self) -> str:
        return self.visual_memory.get_context_prompt()


def get_opencv_vision() -> OpenCVVisionCoordinator:
    return OpenCVVisionCoordinator()


def get_vision_coordinator() -> OpenCVVisionCoordinator:
    return OpenCVVisionCoordinator()
