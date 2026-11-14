"""
Viernes — Secure Web Content Reader & Extractor
================================================
Fetches, sanitizes, and extracts structured readable text from public URLs.
Includes:
- Anti-SSRF protection (blocks private IP ranges and local files)
- Semantic HTML cleaning (removes ads, headers, nav, cookies, scripts)
- Headless browser fallback via Playwright for JavaScript SPAs (React/Vue)
- Anti-Prompt-Injection defense and strict containment
"""

from __future__ import annotations

import ipaddress
import logging
import re
import socket
import threading
from dataclasses import dataclass
from typing import Optional, Tuple
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger("Viernes.WebReader")

# Security: Prompt injection patterns to neutralize
_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+(instructions|prompts)", re.IGNORECASE),
    re.compile(r"disregard\s+(all\s+)?(previous|prior)\s+(instructions|prompts)", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+(a|an)?\s*", re.IGNORECASE),
    re.compile(r"<\|im_start\|>|<\|im_end\|>|\[INST\]|\[/INST\]|<<SYS>>|<system>", re.IGNORECASE),
    re.compile(r"(system|human|assistant)\s*:\s*", re.IGNORECASE),
]

_PLAYWRIGHT_LOCK = threading.Lock()


@dataclass
class ExtractedPage:
    url: str
    title: str
    text: str
    word_count: int
    content_type: str = "text/html"
    is_dynamic: bool = False
    error: Optional[str] = None

    def to_safe_context(self, max_chars: int = 4000) -> str:
        """Format as untrusted, isolated context with clear containment."""
        safe_text = self.text[:max_chars].strip()
        return (
            f"<untrusted_web_source url=\"{self.url}\" title=\"{self.title}\">\n"
            f"{safe_text}\n"
            f"</untrusted_web_source>"
        )


def _is_safe_public_url(url: str) -> Tuple[bool, str]:
    """Validate that the URL is public and does not point to internal networks (anti-SSRF)."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False, f"Unsupported scheme: {parsed.scheme}"

        hostname = parsed.hostname
        if not hostname:
            return False, "Missing hostname"

        if hostname.lower() in ("localhost", "127.0.0.1", "0.0.0.0", "::1"):
            return False, "Access to localhost is blocked"

        # Resolve IP to verify it's not a private subnet
        try:
            ip_str = socket.gethostbyname(hostname)
            ip_obj = ipaddress.ip_address(ip_str)
            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved or ip_obj.is_link_local:
                return False, f"Access to private IP {ip_str} is blocked"
        except Exception:
            pass  # DNS resolution failed or unavailable, continue with URL check

        return True, ""
    except Exception as e:
        return False, str(e)


def _sanitize_for_prompt(text: str) -> str:
    """Neutralize potential prompt injection attack vectors."""
    cleaned = text
    for pattern in _INJECTION_PATTERNS:
        cleaned = pattern.sub("[REDACTED_INSTRUCTION]", cleaned)
    # Collapse excess whitespace
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
    return cleaned.strip()


class WebReader:
    """Secure web page extractor with static HTTP and Playwright JS fallback."""

    def __init__(self, timeout: float = 12.0, max_size_bytes: int = 2_500_000):
        self.timeout = timeout
        self.max_size_bytes = max_size_bytes
        self._headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
        }

    def fetch_page(self, url: str, try_playwright_if_empty: bool = True) -> ExtractedPage:
        """Fetch and extract readable text from a URL."""
        url = url.strip()
        safe, reason = _is_safe_public_url(url)
        if not safe:
            return ExtractedPage(
                url=url,
                title="Acceso Bloqueado",
                text="",
                word_count=0,
                error=f"Seguridad: {reason}",
            )

        # 1. Fast static fetch via httpx
        try:
            with httpx.Client(
                timeout=self.timeout,
                headers=self._headers,
                follow_redirects=True,
                max_redirects=5,
            ) as client:
                resp = client.get(url)

            if resp.status_code >= 400:
                return ExtractedPage(
                    url=url,
                    title=f"Error HTTP {resp.status_code}",
                    text="",
                    word_count=0,
                    error=f"HTTP {resp.status_code}",
                )

            # Cap content size
            html_content = resp.text[:self.max_size_bytes]
            page = self._parse_html(url, html_content)

            # 2. Check if page appears empty or client-side rendered (SPA)
            if try_playwright_if_empty and (page.word_count < 60 or self._is_spa_stub(html_content)):
                dynamic_page = self._fetch_playwright(url)
                if dynamic_page and dynamic_page.word_count > page.word_count:
                    return dynamic_page

            return page

        except Exception as e:
            logger.warning(f"Static fetch failed for {url}: {e}")
            if try_playwright_if_empty:
                dynamic_page = self._fetch_playwright(url)
                if dynamic_page and not dynamic_page.error:
                    return dynamic_page
            return ExtractedPage(
                url=url,
                title="Error de Lectura",
                text="",
                word_count=0,
                error=str(e),
            )

    def _is_spa_stub(self, html: str) -> bool:
        """Detect common client-side rendered Single Page Application stubs."""
        low = html.lower()
        if '<div id="root"></div>' in low or '<div id="app"></div>' in low or '<div id="__next">' in low:
            return True
        if 'you need to enable javascript to run this app' in low:
            return True
        return False

    def _parse_html(self, url: str, html: str) -> ExtractedPage:
        """Extract title, metadata, and main body text using BeautifulSoup."""
        soup = BeautifulSoup(html, "html.parser")

        # 1. Extract Title
        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        elif soup.find("h1"):
            title = soup.find("h1").get_text(strip=True)
        if not title:
            parsed = urlparse(url)
            title = parsed.netloc + parsed.path

        # 2. Remove noise and non-article elements
        for tag in soup.find_all([
            "script", "style", "svg", "noscript", "iframe", "canvas",
            "nav", "footer", "header", "aside", "form", "button",
            "dialog", "menu", "select", "option", "textarea"
        ]):
            tag.decompose()

        # Remove common ad/cookie overlay containers
        for noisy_class in [
            "cookie-banner", "consent", "cookie-notice", "advertisement",
            "ad-banner", "sidebar", "social-share", "popup", "newsletter"
        ]:
            for tag in soup.find_all(class_=re.compile(noisy_class, re.I)):
                tag.decompose()

        # 3. Locate Main Content container
        main_container = (
            soup.find("article")
            or soup.find("main")
            or soup.find(id=re.compile(r"content|main|article|body", re.I))
            or soup.find(class_=re.compile(r"content|article-body|post-content|entry-content", re.I))
            or soup.body
            or soup
        )

        # 4. Extract structured text preserving headers and lists
        lines = []
        for el in main_container.find_all(["h1", "h2", "h3", "h4", "p", "li", "pre", "blockquote"]):
            txt = el.get_text(strip=True)
            if not txt:
                continue
            if el.name in ("h1", "h2"):
                lines.append(f"\n## {txt}\n")
            elif el.name in ("h3", "h4"):
                lines.append(f"\n### {txt}\n")
            elif el.name == "li":
                lines.append(f"- {txt}")
            elif el.name == "blockquote":
                lines.append(f"> {txt}")
            else:
                lines.append(txt)

        if not lines:
            raw_text = main_container.get_text(separator="\n", strip=True)
        else:
            raw_text = "\n".join(lines)

        cleaned_text = _sanitize_for_prompt(raw_text)
        word_count = len(cleaned_text.split())

        return ExtractedPage(
            url=url,
            title=title,
            text=cleaned_text,
            word_count=word_count,
            content_type="text/html",
            is_dynamic=False,
        )

    def _fetch_playwright(self, url: str) -> Optional[ExtractedPage]:
        """Headless browser rendering for complex JavaScript pages."""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            logger.info("Playwright not available; skipping dynamic render.")
            return None

        with _PLAYWRIGHT_LOCK:
            try:
                with sync_playwright() as p:
                    # Launch lightweight headless chromium
                    browser = p.chromium.launch(
                        headless=True,
                        args=[
                            "--no-sandbox",
                            "--disable-setuid-sandbox",
                            "--disable-dev-shm-usage",
                            "--disable-gpu",
                            "--disable-images",
                        ],
                    )
                    context = browser.new_context(
                        user_agent=self._headers["User-Agent"],
                        viewport={"width": 1280, "height": 800},
                        java_script_enabled=True,
                    )
                    # Block unnecessary image, font, and stylesheet downloads for speed
                    def route_handler(route):
                        req = route.request
                        if req.resource_type in ("image", "font", "media"):
                            route.abort()
                        else:
                            route.continue_()

                    page = context.new_page()
                    page.route("**/*", route_handler)

                    try:
                        page.goto(url, wait_until="domcontentloaded", timeout=12000)
                        page.wait_for_timeout(1000)  # Brief grace period for client hydration
                        content = page.content()
                        title = page.title()
                    finally:
                        browser.close()

                    extracted = self._parse_html(url, content)
                    if title and not extracted.title:
                        extracted.title = title
                    extracted.is_dynamic = True
                    return extracted

            except Exception as e:
                logger.warning(f"Playwright render failed for {url}: {e}")
                return None
