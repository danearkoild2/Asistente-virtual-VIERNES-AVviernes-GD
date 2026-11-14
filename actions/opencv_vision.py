"""
actions/opencv_vision.py — Herramienta nativa OpenCV para VIERNES.
"""
from __future__ import annotations

from core.opencv_vision import get_opencv_vision


def opencv_vision_action(
    parameters: dict,
    response=None,
    player=None,
    session_memory=None,
    speak=None,
) -> str:
    p = parameters or {}
    mode = (p.get("mode") or "analyze").strip().lower()
    source = (p.get("source") or "camera").strip().lower()
    image_path = (p.get("image_path") or "").strip()

    ov = get_opencv_vision()

    if mode in ("start", "start_stream"):
        ok = ov.start_continuous_vision()
        return "OpenCV activo en tiempo real." if ok else "No se pudo abrir la cámara con OpenCV."

    if mode in ("stop", "stop_stream"):
        ov.stop_continuous_vision()
        return "OpenCV en tiempo real detenido."

    bgr = ov.capture_single_bgr(source=source, image_path=image_path)
    if bgr is None:
        return f"No se pudo capturar imagen OpenCV desde '{source}'."

    metrics, _ = ov.analyze_bgr_local(bgr, draw_boxes=False)

    if mode == "read_qr":
        qrs = metrics.get("qr") or []
        return f"QR detectados: {qrs}" if qrs else "No se detectaron códigos QR en la imagen."

    if mode == "detect_faces":
        return (
            f"Rostros detectados con OpenCV: {metrics['faces']} "
            f"(resolución {metrics['resolution']}, brillo {metrics['brightness']}/255)."
        )

    if mode == "ai_describe":
        res = ov.analyze_current_scene()
        return res.get("summary") or f"Métricas OpenCV: {metrics}"

    return (
        f"Análisis OpenCV ({source}): resolución={metrics['resolution']}, "
        f"rostros={metrics['faces']}, movimiento={metrics['motion_pct']}%, "
        f"brillo={metrics['brightness']}/255, qr={metrics['qr']}."
    )


TOOL = {
    "name": "opencv_vision",
    "description": "Visión por computadora nativa con OpenCV (cv2): detección de rostros, movimiento, códigos QR, brillo/escena en cámara, pantalla o archivo local sin gastar tokens innecesarios.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "mode": {
                "type": "STRING",
                "description": "Modo: analyze, detect_faces, read_qr, ai_describe, start, stop"
            },
            "source": {
                "type": "STRING",
                "description": "Origen de captura: camera o screen (default: camera)"
            },
            "image_path": {
                "type": "STRING",
                "description": "Ruta opcional a imagen local para analizar con OpenCV"
            }
        },
        "required": ["mode"]
    },
    "handler": opencv_vision_action,
}
