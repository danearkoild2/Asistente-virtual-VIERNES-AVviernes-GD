"""
core/crawl4ai_engine.py — Integración nativa de Crawl4AI para VIERNES.
Extrae contenido web limpio en Markdown, enlaces y metadatos optimizados para bajo consumo de tokens.
"""
from __future__ import annotations

import asyncio
from typing import Any


async def _crawl_async(
    url: str,
    word_count_threshold: int = 10,
    max_chars: int = 4500,
    include_links: bool = False,
) -> dict[str, Any]:
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

    browser_cfg = BrowserConfig(headless=True, verbose=False)
    run_cfg = CrawlerRunConfig(word_count_threshold=word_count_threshold, verbose=False)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(url=url, config=run_cfg)

    if not result or not getattr(result, "success", False):
        return {
            "ok": False,
            "url": url,
            "error": getattr(result, "error_message", "No se pudo rastrear la URL."),
        }

    md_obj = getattr(result, "markdown", None)
    if hasattr(md_obj, "raw_markdown"):
        md = md_obj.raw_markdown or ""
    else:
        md = str(md_obj or "")

    md = md.strip()
    truncated = len(md) > max_chars
    if truncated:
        md = md[:max_chars].rstrip() + "\n...[recortado para ahorrar tokens]"

    meta = getattr(result, "metadata", None) or {}
    out: dict[str, Any] = {
        "ok": True,
        "url": getattr(result, "url", url),
        "title": meta.get("title", ""),
        "markdown": md,
        "truncated": truncated,
    }
    if include_links:
        links = getattr(result, "links", None) or {}
        internal = [x.get("href") for x in (links.get("internal") or [])[:15] if isinstance(x, dict) and x.get("href")]
        external = [x.get("href") for x in (links.get("external") or [])[:15] if isinstance(x, dict) and x.get("href")]
        out["links"] = {"internal": internal, "external": external}
    return out


def crawl_url(
    url: str,
    max_chars: int = 4500,
    include_links: bool = False,
) -> dict[str, Any]:
    """Ejecuta Crawl4AI de forma síncrona segura desde cualquier hilo."""
    try:
        return asyncio.run(_crawl_async(url, max_chars=max_chars, include_links=include_links))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(_crawl_async(url, max_chars=max_chars, include_links=include_links))
        finally:
            loop.close()
    except Exception as exc:
        return {"ok": False, "url": url, "error": str(exc)}
