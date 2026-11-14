"""
core/sports_web_view.py — Native Ad-Blocked Sports Web Player for VIERNES.

Loads the ORIGINAL sports channel page (e.g. https://futbolenvivo.top/en-vivo/espn-2/)
inside an isolated QWebEngineView protected by Brave's adblock-rust engine:
- Preserves genuine Origin / Referer so stream CDNs do not drop the signal.
- Blocks ad scripts, trackers, popunders and third-party ad frames at the network layer.
- Blocks popup windows via createWindow -> None.
- Injects Brave cosmetic CSS and isolates #embedIframe fullscreen inside the HUD
  without detaching it from the original page DOM.
"""
from __future__ import annotations

import json
import re
import threading
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional

from PyQt6.QtCore import QUrl, pyqtSignal
from PyQt6.QtWebEngineCore import (
    QWebEnginePage,
    QWebEngineProfile,
    QWebEngineSettings,
    QWebEngineUrlRequestInfo,
    QWebEngineUrlRequestInterceptor,
)
from PyQt6.QtWebEngineWidgets import QWebEngineView

from core.sports_tv import UA, get_adblocker, load_settings

_RESOURCE_TYPE_NAMES = {
    QWebEngineUrlRequestInfo.ResourceType.ResourceTypeMainFrame: "mainframe",
    QWebEngineUrlRequestInfo.ResourceType.ResourceTypeSubFrame: "subframe",
    QWebEngineUrlRequestInfo.ResourceType.ResourceTypeStylesheet: "stylesheet",
    QWebEngineUrlRequestInfo.ResourceType.ResourceTypeScript: "script",
    QWebEngineUrlRequestInfo.ResourceType.ResourceTypeImage: "image",
    QWebEngineUrlRequestInfo.ResourceType.ResourceTypeFontResource: "font",
    QWebEngineUrlRequestInfo.ResourceType.ResourceTypeSubResource: "other",
    QWebEngineUrlRequestInfo.ResourceType.ResourceTypeObject: "object",
    QWebEngineUrlRequestInfo.ResourceType.ResourceTypeMedia: "media",
    QWebEngineUrlRequestInfo.ResourceType.ResourceTypeXhr: "xhr",
    QWebEngineUrlRequestInfo.ResourceType.ResourceTypePing: "ping",
    QWebEngineUrlRequestInfo.ResourceType.ResourceTypeFavicon: "favicon",
    QWebEngineUrlRequestInfo.ResourceType.ResourceTypeCspReport: "csp",
}

_ISOLATE_JS = r"""
(() => {
  try {
    const css = %COSMETIC_CSS%;
    if (css && !document.getElementById('__viernes_cosmetic')) {
      const st = document.createElement('style');
      st.id = '__viernes_cosmetic';
      st.textContent = css;
      (document.head || document.documentElement).appendChild(st);
    }
    if (!%ISOLATE%) return;
    if (!document.getElementById('__viernes_isolate')) {
      const iso = document.createElement('style');
      iso.id = '__viernes_isolate';
      iso.textContent = `
        html, body {
          margin: 0 !important; padding: 0 !important;
          width: 100%% !important; height: 100%% !important;
          overflow: hidden !important; background: #000 !important;
        }
        header, footer, nav, aside, [class*="ad-"], [id*="ad-"], .ads, .banner {
          display: none !important;
        }
        iframe#embedIframe, iframe#playerFrame, iframe[name="player"], iframe[src*="canal"], iframe[src*="vivo"], iframe[src*="stream"], iframe[src*="player"] {
          position: fixed !important;
          inset: 0 !important;
          width: 100vw !important;
          height: 100vh !important;
          max-width: none !important;
          max-height: none !important;
          border: none !important;
          z-index: 2147483647 !important;
          background: #000 !important;
          display: block !important;
          visibility: visible !important;
        }
      `;
      (document.head || document.documentElement).appendChild(iso);
    }
    const targetSrc = %TARGET_FRAME_SRC%;
    const frame = document.getElementById('embedIframe')
      || document.getElementById('playerFrame')
      || document.querySelector('iframe[name="player"], iframe[src*="canal"], iframe[src*="vivo"], iframe[src*="stream"], iframe[src*="player"]');
    if (frame && targetSrc) {
      const btn = Array.from(document.querySelectorAll('button.option[data-src]'))
        .find((b) => b.getAttribute('data-src') === targetSrc);
      if (btn) {
        try { btn.click(); } catch (_) {}
      }
      if (frame.getAttribute('src') !== targetSrc) {
        frame.setAttribute('src', targetSrc);
      }
    }
    if (frame) {
      let cur = frame.parentElement;
      while (cur && cur !== document.body && cur !== document.documentElement) {
        cur.style.setProperty('overflow', 'visible', 'important');
        cur.style.setProperty('transform', 'none', 'important');
        cur = cur.parentElement;
      }
      Array.from(document.body ? document.body.children : []).forEach((el) => {
        if (!el.contains(frame) && el.tagName !== 'STYLE' && el.tagName !== 'SCRIPT') {
          el.style.setProperty('display', 'none', 'important');
        }
      });
    }
    if (%AUTOPLAY%) {
      document.querySelectorAll('video').forEach((v) => {
        try { v.play().catch(() => {}); } catch (_) {}
      });
    }
  } catch (_) {}
})();
"""


class _HlsProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if not parsed.path.startswith(("/hls", "/stream", "/seg")):
            self.send_error(404)
            return
        qs = urllib.parse.parse_qs(parsed.query)
        target = (qs.get("u") or [""])[0]
        ref = (qs.get("ref") or ["https://la18hd.su/"])[0]
        if not target.startswith(("http://", "https://")):
            self.send_error(400)
            return
        ref_p = urllib.parse.urlparse(ref)
        origin = f"{ref_p.scheme}://{ref_p.netloc}" if ref_p.scheme and ref_p.netloc else ""
        headers = {"User-Agent": UA, "Referer": ref}
        if origin:
            headers["Origin"] = origin
        try:
            req = urllib.request.Request(target, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                ctype = resp.headers.get("Content-Type", "application/octet-stream")
                data = resp.read()
                final_url = resp.geturl()
        except Exception as exc:
            self.send_error(502, str(exc))
            return

        is_m3u8 = (
            "mpegurl" in ctype.lower()
            or ".m3u8" in final_url.lower()
            or data.lstrip()[:7] == b"#EXTM3U"
        )
        if is_m3u8:
            port = self.server.server_address[1]
            text = data.decode("utf-8", "replace")
            rewritten = []

            def _prox(u: str) -> str:
                abs_u = urllib.parse.urljoin(final_url, u.strip())
                ext = ".m3u8" if ".m3u8" in abs_u.lower() else ".ts"
                return (
                    f"http://127.0.0.1:{port}/seg{ext}?u="
                    f"{urllib.parse.quote(abs_u, safe='')}"
                    f"&ref={urllib.parse.quote(ref, safe='')}"
                )

            for line in text.splitlines():
                s = line.strip()
                if not s:
                    rewritten.append(line)
                elif s.startswith("#"):
                    rewritten.append(
                        re.sub(r'URI="([^"]+)"', lambda m: f'URI="{_prox(m.group(1))}"', line)
                    )
                else:
                    rewritten.append(_prox(s))
            data = ("\n".join(rewritten) + "\n").encode("utf-8")
            ctype = "application/vnd.apple.mpegurl"

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)


_HLS_PROXY_SERVER: Optional[ThreadingHTTPServer] = None
_HLS_PROXY_LOCK = threading.Lock()


def get_hls_proxy_url(stream_url: str, referer: str) -> str:
    global _HLS_PROXY_SERVER
    with _HLS_PROXY_LOCK:
        if _HLS_PROXY_SERVER is None:
            _HLS_PROXY_SERVER = ThreadingHTTPServer(("127.0.0.1", 0), _HlsProxyHandler)
            _HLS_PROXY_SERVER.daemon_threads = True
            t = threading.Thread(target=_HLS_PROXY_SERVER.serve_forever, daemon=True)
            t.start()
        port = _HLS_PROXY_SERVER.server_address[1]
    return (
        f"http://127.0.0.1:{port}/stream.m3u8?u="
        f"{urllib.parse.quote(stream_url, safe='')}"
        f"&ref={urllib.parse.quote(referer, safe='')}"
    )


class _SportsAdBlockInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._blocker = get_adblocker()
        self.frame_host = ""
        self.referer_url = "https://futbolenvivo.top/"
        self.on_m3u8 = None

    def interceptRequest(self, info: QWebEngineUrlRequestInfo) -> None:
        cfg = load_settings()
        url = info.requestUrl().toString()
        if not url.startswith(("http://", "https://")):
            return
        if ".m3u8" in url.lower() and self.on_m3u8 is not None:
            try:
                self.on_m3u8(url)
            except Exception:
                pass
        if not cfg.get("adblock_enabled", True):
            return
        src = info.firstPartyUrl().toString() or self.referer_url or url
        rtype = _RESOURCE_TYPE_NAMES.get(info.resourceType(), "other")
        if self._blocker.should_block(url, src, rtype):
            info.block(True)


class _SportsWebPage(QWebEnginePage):
    def __init__(self, profile: QWebEngineProfile, parent=None) -> None:
        super().__init__(profile, parent)
        self.block_popups = True

    def createWindow(self, _win_type):
        if self.block_popups:
            return None
        return super().createWindow(_win_type)


class SportsWebPlayer(QWebEngineView):
    """Embedded ad-blocked web player for live sports channels."""

    blocked_popup = pyqtSignal(str)
    stream_detected = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._profile = QWebEngineProfile("ViernesSportsProfile", self)
        self._profile.setHttpUserAgent(UA)
        self._interceptor = _SportsAdBlockInterceptor(self._profile)
        self._interceptor.on_m3u8 = self._handle_m3u8
        self._profile.setUrlRequestInterceptor(self._interceptor)

        self._page = _SportsWebPage(self._profile, self)
        self.setPage(self._page)

        s = self.settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
        s.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, False)
        s.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)

        self._current_url = ""
        self._current_frame_src = ""
        self._current_frame_host = ""
        self._muted = False
        self._stream_emitted = False
        self.loadFinished.connect(self._on_load_finished)

    def _handle_m3u8(self, stream_url: str) -> None:
        if self._stream_emitted or not self._current_url:
            return
        self._stream_emitted = True
        ref_src = self._current_frame_src or self._current_url
        p = urllib.parse.urlparse(ref_src)
        ref = f"{p.scheme}://{p.netloc}/" if p.scheme and p.netloc else ref_src
        proxied = get_hls_proxy_url(stream_url, ref)
        self.stream_detected.emit(proxied)

    def load_channel(self, url: str, frame_src: str = "", frame_host: str = "", muted: bool = False) -> None:
        cfg = load_settings()
        self._page.block_popups = bool(cfg.get("block_popups", True))
        if frame_host:
            get_adblocker().allow_frame_host(frame_host)
        self._interceptor.frame_host = (frame_host or "").lower()
        self._interceptor.referer_url = url or "https://futbolenvivo.top/"
        self._current_url = url
        self._current_frame_src = frame_src
        self._current_frame_host = frame_host
        self._stream_emitted = False
        self.set_muted(muted)

        # tvporinternet.org requires loading the original channel page so Referer and window.top !== window.self hold
        if "tvporinternet.org" in (url or "").lower():
            target_url = url
        else:
            target_url = frame_src or url
        if target_url:
            self.setUrl(QUrl(target_url))

    def reload_channel(self) -> None:
        if self._current_url:
            self.load_channel(
                self._current_url,
                frame_src=self._current_frame_src,
                frame_host=self._current_frame_host,
                muted=self.is_muted(),
            )

    def stop_channel(self) -> None:
        self._current_url = ""
        self._stream_emitted = False
        try:
            self._page.setAudioMuted(True)
            self._page.triggerAction(QWebEnginePage.WebAction.Stop)
        except Exception:
            pass

    def set_muted(self, muted: bool) -> None:
        self._muted = bool(muted)
        try:
            self._page.setAudioMuted(self._muted)
        except Exception:
            pass

    def is_muted(self) -> bool:
        try:
            return bool(self._page.isAudioMuted())
        except Exception:
            return self._muted

    def _on_load_finished(self, ok: bool) -> None:
        if not ok or not self._current_url or self._current_url == "about:blank":
            return
        cfg = load_settings()
        cosmetic = ""
        if cfg.get("adblock_enabled", True):
            cosmetic = get_adblocker().cosmetic_css(self._current_url)
        js = (
            _ISOLATE_JS
            .replace("%COSMETIC_CSS%", json.dumps(cosmetic))
            .replace("%ISOLATE%", "true" if cfg.get("isolate_player", True) else "false")
            .replace("%AUTOPLAY%", "true" if cfg.get("autoplay", True) else "false")
            .replace("%TARGET_FRAME_SRC%", json.dumps(self._current_frame_src or ""))
        )
        try:
            self._page.runJavaScript(js)
        except Exception:
            pass
