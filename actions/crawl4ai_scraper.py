"""
actions/crawl4ai_scraper.py — Acción nativa de Crawl4AI para VIERNES.
"""
from __future__ import annotations

import json
from core.crawl4ai_engine import crawl_url


def crawl4ai_action(
    parameters: dict,
    response=None,
    player=None,
    session_memory=None,
    speak=None,
) -> str:
    p = parameters or {}
    url = (p.get("url") or "").strip()
    if not url:
        return "Proporciona una URL válida para analizar con Crawl4AI."
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    max_chars = int(p.get("max_chars", 4500))
    include_links = bool(p.get("include_links", False))
    res = crawl_url(url, max_chars=max(500, min(max_chars, 12000)), include_links=include_links)
    if not res.get("ok"):
        return f"Error de Crawl4AI en {url}: {res.get('error', 'desconocido')}"

    header = f"# {res.get('title') or url}\nURL: {res['url']}\n\n"
    body = res.get("markdown", "")
    if include_links and res.get("links"):
        body += "\n\nLinks:\n" + json.dumps(res["links"], ensure_ascii=False)
    return header + body


TOOL = {
    "name": "crawl4ai_scrape",
    "description": "Extrae contenido web limpio en Markdown estructurado y enlaces usando Crawl4AI (ideal para documentación, noticias y páginas con JavaScript).",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "url": {
                "type": "STRING",
                "description": "URL completa de la página web a rastrear"
            },
            "max_chars": {
                "type": "INTEGER",
                "description": "Límite máximo de caracteres Markdown devueltos (default: 4500)"
            },
            "include_links": {
                "type": "BOOLEAN",
                "description": "Incluir enlaces internos y externos principales (default: false)"
            }
        },
        "required": ["url"]
    },
    "handler": crawl4ai_action,
}
