"""
Viernes — Advanced SerpApi Universal Search Client
===================================================
Robust, cached, rate-limited and multi-engine client for SerpApi with fallback support.
Supports: Google Search, Google News, Google Scholar, Google Images, YouTube,
Google Maps/Local, Google Shopping, and GitHub.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import httpx

from memory.config_manager import get_base_dir, get_serpapi_key

logger = logging.getLogger("Viernes.SerpApi")

SERPAPI_ENDPOINT = "https://serpapi.com/search.json"
CACHE_DIR = get_base_dir() / "config" / "serp_cache"


@dataclass
class SearchResultItem:
    title: str
    link: str
    snippet: str
    source: str = ""
    date: str = ""
    thumbnail: str = ""
    score: float = 0.0
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "link": self.link,
            "snippet": self.snippet,
            "source": self.source,
            "date": self.date,
            "thumbnail": self.thumbnail,
            "score": self.score,
            "extra": self.extra,
        }


class SerpApiClient:
    """Enterprise-grade, cached, rate-limited SerpApi client."""

    _instance: Optional[SerpApiClient] = None
    _lock = threading.Lock()

    def __init__(self, api_key: Optional[str] = None):
        self._custom_key = api_key
        self._cache_lock = threading.Lock()
        self._mem_cache: Dict[str, tuple[float, Dict[str, Any]]] = {}
        self._quota_exceeded_until = 0.0
        self._last_req_time = 0.0
        self._min_interval = 0.25  # Minimum 250ms between remote calls
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_instance(cls) -> SerpApiClient:
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    @property
    def api_key(self) -> str:
        if self._custom_key:
            return self._custom_key
        return get_serpapi_key()

    def is_configured(self) -> bool:
        key = self.api_key
        return bool(key and len(key) >= 16)

    def _cache_key(self, engine: str, params: Dict[str, Any]) -> str:
        norm = {k: v for k, v in sorted(params.items()) if k != "api_key"}
        raw = f"{engine}:{json.dumps(norm, sort_keys=True)}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _get_from_cache(self, key: str, max_age_sec: float = 3600.0) -> Optional[Dict[str, Any]]:
        now = time.time()
        with self._cache_lock:
            if key in self._mem_cache:
                ts, data = self._mem_cache[key]
                if (now - ts) < max_age_sec:
                    return data
                del self._mem_cache[key]

        disk_file = CACHE_DIR / f"{key}.json"
        if disk_file.exists():
            try:
                stat = disk_file.stat()
                if (now - stat.st_mtime) < max_age_sec:
                    data = json.loads(disk_file.read_text(encoding="utf-8"))
                    with self._cache_lock:
                        self._mem_cache[key] = (stat.st_mtime, data)
                    return data
            except Exception:
                pass
        return None

    def _save_to_cache(self, key: str, data: Dict[str, Any]) -> None:
        now = time.time()
        with self._cache_lock:
            self._mem_cache[key] = (now, data)
        disk_file = CACHE_DIR / f"{key}.json"
        try:
            disk_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    def search(
        self,
        query: str,
        engine: str = "google",
        num: int = 10,
        hl: str = "es",
        gl: str = "es",
        extra_params: Optional[Dict[str, Any]] = None,
        use_cache: bool = True,
        cache_ttl: float = 3600.0,
    ) -> List[SearchResultItem]:
        """
        Execute universal search via SerpApi.
        Supported engines: 'google', 'google_news', 'google_scholar', 'google_images',
        'youtube', 'google_maps', 'google_shopping', 'github'.
        """
        query = (query or "").strip()
        if not query:
            return []

        # Circuit breaker check
        now = time.time()
        if now < self._quota_exceeded_until:
            wait_m = int((self._quota_exceeded_until - now) / 60)
            logger.warning(f"SerpApi quota circuit open. Waiting {wait_m}m before retry.")
            return self._fallback_search(query, engine=engine, num=num)

        params: Dict[str, Any] = {
            "q": query,
            "engine": engine,
            "num": min(max(num, 1), 20),
            "hl": hl,
            "gl": gl,
        }
        if extra_params:
            params.update(extra_params)

        # Check Cache
        ck = self._cache_key(engine, params)
        if use_cache:
            cached = self._get_from_cache(ck, max_age_sec=cache_ttl)
            if cached is not None:
                return self._parse_engine_results(engine, cached)

        key = self.api_key
        if not key:
            logger.info("No SerpApi key configured. Falling back to alternative search.")
            return self._fallback_search(query, engine=engine, num=num)

        params["api_key"] = key

        # Respect minimum interval between calls
        with self._cache_lock:
            elapsed = time.time() - self._last_req_time
            if elapsed < self._min_interval:
                time.sleep(self._min_interval - elapsed)
            self._last_req_time = time.time()

        # Execute HTTP Request with retry & backoff
        for attempt in range(3):
            try:
                with httpx.Client(timeout=22.0) as client:
                    resp = client.get(SERPAPI_ENDPOINT, params=params)

                if resp.status_code == 200:
                    data = resp.json()
                    if "error" in data:
                        err_msg = str(data.get("error", ""))
                        if "run out of searches" in err_msg.lower() or "invalid api key" in err_msg.lower():
                            logger.error(f"SerpApi error: {err_msg}")
                            self._quota_exceeded_until = time.time() + 1800  # 30 min cooldown
                            return self._fallback_search(query, engine=engine, num=num)
                    if use_cache:
                        self._save_to_cache(ck, data)
                    return self._parse_engine_results(engine, data)

                elif resp.status_code in (429, 401, 403):
                    logger.warning(f"SerpApi returned {resp.status_code}. Setting circuit cooldown.")
                    self._quota_exceeded_until = time.time() + 1800
                    return self._fallback_search(query, engine=engine, num=num)
                else:
                    time.sleep(0.5 * (attempt + 1))

            except Exception as e:
                logger.warning(f"SerpApi request failed (attempt {attempt+1}/3): {e}")
                time.sleep(0.5 * (attempt + 1))

        return self._fallback_search(query, engine=engine, num=num)

    def _parse_engine_results(self, engine: str, data: Dict[str, Any]) -> List[SearchResultItem]:
        items: List[SearchResultItem] = []

        # Knowledge graph or answer box if present
        if "answer_box" in data and isinstance(data["answer_box"], dict):
            ab = data["answer_box"]
            ans = ab.get("answer") or ab.get("snippet") or ab.get("result") or ""
            link = ab.get("link") or ab.get("displayed_link") or ""
            title = ab.get("title") or "Respuesta directa"
            if ans:
                items.append(SearchResultItem(
                    title=f"[Destacado] {title}",
                    link=link,
                    snippet=ans,
                    source="Google Answer Box",
                    score=1.5
                ))

        if "knowledge_graph" in data and isinstance(data["knowledge_graph"], dict):
            kg = data["knowledge_graph"]
            kg_title = kg.get("title", "")
            kg_desc = kg.get("description", "")
            kg_source = kg.get("source", {}).get("name", "Knowledge Graph") if isinstance(kg.get("source"), dict) else "Knowledge Graph"
            kg_link = kg.get("source", {}).get("link", "") if isinstance(kg.get("source"), dict) else ""
            if kg_desc:
                items.append(SearchResultItem(
                    title=f"[Ficha] {kg_title}",
                    link=kg_link,
                    snippet=kg_desc,
                    source=kg_source,
                    score=1.4
                ))

        # 1. Google Web / Organic
        if engine == "google":
            for r in data.get("organic_results", []):
                if not isinstance(r, dict):
                    continue
                title = r.get("title", "")
                link = r.get("link", "")
                snippet = r.get("snippet", "") or r.get("snippet_highlighted_words", "")
                if isinstance(snippet, list):
                    snippet = " ... ".join(str(s) for s in snippet)
                source = r.get("source") or r.get("displayed_link", "")
                date = r.get("date", "")
                thumb = r.get("thumbnail", "")
                if link and (title or snippet):
                    items.append(SearchResultItem(
                        title=title,
                        link=link,
                        snippet=snippet,
                        source=source,
                        date=date,
                        thumbnail=thumb,
                        score=1.0
                    ))

        # 2. Google News
        elif engine == "google_news":
            for n in data.get("news_results", []):
                if not isinstance(n, dict):
                    continue
                title = n.get("title", "")
                link = n.get("link", "")
                snippet = n.get("snippet", "")
                source_obj = n.get("source")
                source = source_obj.get("name", "") if isinstance(source_obj, dict) else str(source_obj or "")
                date = n.get("date", "")
                thumb = n.get("thumbnail", "")
                if link and title:
                    items.append(SearchResultItem(
                        title=title,
                        link=link,
                        snippet=snippet,
                        source=source,
                        date=date,
                        thumbnail=thumb,
                        score=1.1
                    ))

        # 3. Google Scholar
        elif engine == "google_scholar":
            for s in data.get("organic_results", []):
                if not isinstance(s, dict):
                    continue
                title = s.get("title", "")
                link = s.get("link", "")
                snippet = s.get("snippet", "")
                info = s.get("publication_info", {})
                authors = info.get("summary", "") if isinstance(info, dict) else ""
                resources = s.get("resources", [])
                pdf_link = resources[0].get("link", "") if resources and isinstance(resources[0], dict) else ""
                items.append(SearchResultItem(
                    title=f"[Paper] {title}",
                    link=pdf_link or link,
                    snippet=f"{snippet} (Autores/Citas: {authors})",
                    source="Google Scholar",
                    score=1.2,
                    extra={"pdf": pdf_link, "citations": s.get("inline_links", {}).get("cited_by", {})}
                ))

        # 4. YouTube / Videos
        elif engine in ("youtube", "google_videos"):
            results_key = "video_results" if engine == "google_videos" else "video_results"
            for v in data.get(results_key, []) or data.get("organic_results", []):
                if not isinstance(v, dict):
                    continue
                title = v.get("title", "")
                link = v.get("link", "")
                snippet = v.get("description", "") or v.get("snippet", "")
                channel = v.get("channel", {}).get("name", "") if isinstance(v.get("channel"), dict) else v.get("channel", "")
                duration = v.get("length", "") or v.get("duration", "")
                views = v.get("views", "")
                thumb = v.get("thumbnail", {}).get("static", "") if isinstance(v.get("thumbnail"), dict) else v.get("thumbnail", "")
                items.append(SearchResultItem(
                    title=f"▶ {title} [{duration}]",
                    link=link,
                    snippet=f"{snippet} — Canal: {channel} • Vistas: {views}",
                    source=f"YouTube ({channel})" if channel else "YouTube",
                    thumbnail=thumb,
                    score=1.0,
                    extra={"duration": duration, "views": views}
                ))

        # 5. Google Images
        elif engine == "google_images":
            for img in data.get("images_results", []):
                if not isinstance(img, dict):
                    continue
                title = img.get("title", "")
                link = img.get("original", "") or img.get("link", "")
                source = img.get("source", "")
                thumb = img.get("thumbnail", "")
                items.append(SearchResultItem(
                    title=title,
                    link=link,
                    snippet=f"Imagen original de {source}",
                    source=source,
                    thumbnail=thumb,
                    score=0.9
                ))

        # 6. Google Shopping / Products
        elif engine == "google_shopping":
            for p in data.get("shopping_results", []):
                if not isinstance(p, dict):
                    continue
                title = p.get("title", "")
                price = p.get("price", "")
                link = p.get("link", "")
                merchant = p.get("source", "")
                rating = p.get("rating", "")
                items.append(SearchResultItem(
                    title=f"🏷 {title} ({price})",
                    link=link,
                    snippet=f"Vendedor: {merchant} • Calificación: {rating}/5",
                    source=merchant,
                    thumbnail=p.get("thumbnail", ""),
                    score=1.0,
                    extra={"price": price, "rating": rating}
                ))

        # 7. Google Maps / Local Businesses
        elif engine == "google_maps":
            for pl in data.get("local_results", []):
                if not isinstance(pl, dict):
                    continue
                title = pl.get("title", "")
                addr = pl.get("address", "")
                rating = pl.get("rating", "")
                reviews = pl.get("reviews", "")
                phone = pl.get("phone", "")
                link = pl.get("link", "") or pl.get("website", "")
                items.append(SearchResultItem(
                    title=f"📍 {title} ({rating}★ - {reviews} reseñas)",
                    link=link,
                    snippet=f"Dirección: {addr} • Tel: {phone}",
                    source="Google Maps",
                    score=1.0
                ))

        # 8. GitHub Repos
        elif engine == "github":
            # GitHub search via SerpApi or organic github search
            for r in data.get("organic_results", []):
                if not isinstance(r, dict):
                    continue
                title = r.get("title", "")
                link = r.get("link", "")
                snippet = r.get("snippet", "")
                if "github.com" in link:
                    items.append(SearchResultItem(
                        title=f"💻 {title}",
                        link=link,
                        snippet=snippet,
                        source="GitHub",
                        score=1.1
                    ))

        # Default fallback to any organic results
        if not items and "organic_results" in data:
            for r in data["organic_results"]:
                if isinstance(r, dict):
                    items.append(SearchResultItem(
                        title=r.get("title", ""),
                        link=r.get("link", ""),
                        snippet=r.get("snippet", ""),
                        source=r.get("displayed_link", ""),
                        score=0.8
                    ))

        return items

    def _fallback_search(self, query: str, engine: str = "google", num: int = 8) -> List[SearchResultItem]:
        """
        Graceful zero-config fallback using DuckDuckGo HTML / Instant Answers when
        SerpApi key is not set or quota is exhausted.
        """
        logger.info(f"Executing fallback search for: {query!r}")
        items: List[SearchResultItem] = []
        try:
            # Try DuckDuckGo Lite / HTML endpoint with realistic browser headers
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            }
            with httpx.Client(timeout=10.0, headers=headers, follow_redirects=True) as client:
                resp = client.post(
                    "https://html.duckduckgo.com/html/",
                    data={"q": query, "b": ""},
                )
                if resp.status_code == 200:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(resp.text, "html.parser")
                    links = soup.select(".result")
                    for el in links[:num]:
                        title_el = el.select_one(".result__title a")
                        snip_el = el.select_one(".result__snippet")
                        if title_el and title_el.get("href"):
                            raw_href = title_el["href"]
                            # Clean DDG redirect URL if needed
                            if "uddg=" in raw_href:
                                import urllib.parse
                                try:
                                    parsed = urllib.parse.parse_qs(urllib.parse.urlparse(raw_href).query)
                                    clean_url = parsed.get("uddg", [raw_href])[0]
                                except Exception:
                                    clean_url = raw_href
                            else:
                                clean_url = raw_href

                            title = title_el.get_text(strip=True)
                            snippet = snip_el.get_text(strip=True) if snip_el else ""
                            items.append(SearchResultItem(
                                title=title,
                                link=clean_url,
                                snippet=snippet,
                                source="Web Search (Fallback)",
                                score=0.8
                            ))
        except Exception as e:
            logger.warning(f"Fallback search failed: {e}")

        return items
