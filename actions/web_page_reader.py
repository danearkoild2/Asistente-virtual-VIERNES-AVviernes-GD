"""
Action: web_fetch
=================
Fetches, sanitizes, and extracts readable content from a specific public URL.
Useful when the user asks: "Lee esta página", "resume este enlace", or provides a URL.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from core.research import WebReader

logger = logging.getLogger("Viernes.Actions.WebFetch")


def web_fetch(
    parameters: Optional[Dict[str, Any]] = None,
    player=None,
    speak: Optional[Any] = None,
    **kwargs,
) -> str:
    params = parameters or {}
    url = str(params.get("url") or "").strip()

    if not url:
        return "Por favor proporciona la URL de la página que deseas consultar."

    if player:
        player.write_log(f"🌐 [Lectura Web] Extrayendo contenido de: {url[:50]}...")

    reader = WebReader()
    page = reader.fetch_page(url, try_playwright_if_empty=True)

    if page.error:
        return f"No se pudo acceder a la página ({url}): {page.error}"

    if not page.text or page.word_count < 10:
        return f"La página no contiene texto legible accesible ({url})."

    # Summarize with Gemini if available, or return clean excerpt
    summary_text = ""
    try:
        from core import gemini
        prompt = (
            f"Lee el siguiente contenido extraído de la página web '{page.title}' ({url}):\n\n"
            f"{page.text[:4000]}\n\n"
            f"Elabora un resumen conciso, estructurado y directo en español destacando las ideas principales y datos clave."
        )
        resp = gemini.call(prompt, tier=gemini.FAST, timeout_ms=15_000)
        if resp and resp.text:
            summary_text = resp.text.strip()
    except Exception:
        pass

    if not summary_text:
        summary_text = page.text[:800] + ("..." if len(page.text) > 800 else "")

    if player and hasattr(player, "show_content"):
        player.show_content(f"PÁGINA: {page.title[:30]}", f"URL: {url}\n\n{summary_text}")

    return f"Contenido de '{page.title}' ({page.word_count} palabras):\n\n{summary_text}"


TOOL = {
    "name": "web_fetch",
    "description": (
        "Lee, extrae y analiza el contenido de una página web específica a partir de su URL pública. "
        "Elimina publicidad y elementos no esenciales para resumir o responder preguntas sobre dicho enlace."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "url": {
                "type": "STRING",
                "description": "La dirección URL pública completa de la página web a leer (http:// o https://)."
            }
        },
        "required": ["url"]
    },
    "handler": web_fetch,
}
