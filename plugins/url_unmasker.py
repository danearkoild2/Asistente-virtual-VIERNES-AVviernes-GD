"""
URL Unmasker & Link Safety Inspector Plugin for MARK LV / Viernes.
Expands shortened URLs (bit.ly, t.co, tinyurl) and inspects redirects before opening.
"""
from __future__ import annotations
import urllib.request
from memory.config_manager import get_plugin_setting

PLUGIN = {
    "name": "url_unmasker",
    "description": (
        "Unmasks shortened links (bit.ly, t.co, tinyurl) and reveals the real final destination URL. "
        "Use when user asks 'a dónde lleva este link', 'desenmascara esta url', or 'es seguro este link'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "url": {
                "type": "STRING",
                "description": "The short or suspicious URL to inspect.",
            }
        },
        "required": ["url"],
    },
}

PLUGIN_SETTINGS = {
    "title": "Desenmascarador de Enlaces",
    "fields": [
        {
            "key": "timeout_seconds",
            "label": "Tiempo de Espera (segundos)",
            "type": "text",
            "default": "5",
            "placeholder": "5",
        },
    ],
}

class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Stop automatic redirect

def run(parameters: dict, player=None, session_memory=None) -> str:
    url = str(parameters.get("url", "")).strip()
    if not url:
        return "Sir, ingresa la URL que deseas inspeccionar."

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        # Follow redirects with standard opener to find final URL
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            final_url = resp.geturl()
            status = resp.status

        is_redirected = (final_url != url)
        if is_redirected:
            msg = f"🔍 ENLACE DESENMASCARADO: {url} ➔ Destino Real: {final_url} (HTTP {status})"
            report = f"El enlace acortado redirige a: {final_url} con código de respuesta {status}."
        else:
            msg = f"🔍 ENLACE DIRECTO: {url} responde con estado HTTP {status}"
            report = f"El enlace no redirige. Su destino directo es {final_url}."

        if player:
            try:
                player.write_log(msg)
            except Exception:
                pass

        return report

    except Exception as e:
        return f"No se pudo resolver el enlace '{url}': {e}"
