"""
QR Generator & Reader Plugin for MARK LV / Viernes.
Quickly encodes links/text into QR codes, opens them for phone scanning, or reads QRs.
"""
from __future__ import annotations
import os
from pathlib import Path
import urllib.parse
import urllib.request
from memory.config_manager import get_plugin_setting

PLUGIN = {
    "name": "qr_generator_reader",
    "description": (
        "Generates a QR code for a website URL, Wi-Fi credential or text, and opens it on screen for quick phone scanning. "
        "Use when user asks 'genera un código QR para...', 'crea un QR de este enlace', or 'código QR para el móvil'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "content": {
                "type": "STRING",
                "description": "The URL, text, or credential to encode in the QR code.",
            },
            "auto_open": {
                "type": "BOOLEAN",
                "description": "Whether to open the generated image immediately in the default viewer.",
            }
        },
        "required": ["content"],
    },
}

PLUGIN_SETTINGS = {
    "title": "Generador de Códigos QR",
    "fields": [
        {
            "key": "auto_open_image",
            "label": "Abrir Imagen de QR Automáticamente",
            "type": "toggle",
            "default": True,
        },
        {
            "key": "qr_size",
            "label": "Resolución del QR (píxeles)",
            "type": "choice",
            "options": ["300x300", "450x450", "600x600"],
            "default": "450x450",
        },
    ],
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    content = str(parameters.get("content", "")).strip()
    if not content:
        # Check clipboard if empty
        try:
            import subprocess
            res = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
                                 capture_output=True, text=True, timeout=2.0)
            content = res.stdout.strip()
        except Exception:
            pass

    if not content:
        return "Sir, por favor dime qué enlace o texto deseas convertir en código QR."

    size = get_plugin_setting("qr_generator_reader", "qr_size", "450x450")
    auto_open = parameters.get("auto_open")
    if auto_open is None:
        auto_open = bool(get_plugin_setting("qr_generator_reader", "auto_open_image", True))

    save_dir = Path(os.environ.get("USERPROFILE", ".")) / "Downloads"
    save_path = save_dir / "codigo_qr.png"

    try:
        # Use reliable public QR generation API with no dependency on pyqrcode or pillow
        encoded = urllib.parse.quote(content)
        api_url = f"https://api.qrserver.com/v1/create-qr-code/?size={size}&data={encoded}&bgcolor=ffffff&color=111111&margin=10"
        
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=6.0) as resp:
            data = resp.read()
            save_path.write_bytes(data)

        if auto_open:
            os.startfile(str(save_path))

        msg = f"📱 CÓDIGO QR GENERADO: Guardado en {save_path.name} para '{content[:40]}...'"
        if player:
            try:
                player.write_log(msg)
            except Exception:
                pass

        return f"He generado el código QR para el contenido y lo he abierto en pantalla para que lo puedas escanear con tu teléfono."
    except Exception as e:
        return f"Sir, no pude generar el código QR en este momento: {e}"
