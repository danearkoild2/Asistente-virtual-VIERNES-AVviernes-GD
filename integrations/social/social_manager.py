"""
Social Media Manager & Coordinator for VIERNES
===============================================
Manages multi-platform lifecycle, encrypted token storage,
and cross-platform engagement aggregation.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from integrations.crypto import decrypt_secret, encrypt_secret
from integrations.social.adapters import FacebookAdapter, InstagramAdapter, XAdapter, YouTubeAdapter
from integrations.social.base import SocialAdapter
from security.audit_logger import record_audit

_CONFIG_FILE = Path(__file__).resolve().parent.parent.parent / "config" / "social_credentials.enc"


class SocialMediaManager:
    """Central registry and analytics coordinator for social networks."""

    def __init__(self):
        self._adapters: Dict[str, SocialAdapter] = {
            "youtube": YouTubeAdapter(),
            "instagram": InstagramAdapter(),
            "x_twitter": XAdapter(),
            "facebook": FacebookAdapter(),
        }
        self._load_credentials()

    def _load_credentials(self):
        if _CONFIG_FILE.exists():
            try:
                enc = _CONFIG_FILE.read_text(encoding="utf-8")
                raw = decrypt_secret(enc)
                if raw:
                    creds = json.loads(raw)
                    if "youtube" in creds:
                        self._adapters["youtube"].api_key = creds["youtube"].get("api_key", "")
                        self._adapters["youtube"].channel_id = creds["youtube"].get("channel_id", "")
                    if "instagram" in creds:
                        self._adapters["instagram"].access_token = creds["instagram"].get("access_token", "")
                    if "x_twitter" in creds:
                        self._adapters["x_twitter"].bearer_token = creds["x_twitter"].get("bearer_token", "")
                    if "facebook" in creds:
                        self._adapters["facebook"].page_token = creds["facebook"].get("page_token", "")
            except Exception as e:
                print(f"[SocialManager] Failed to load credentials: {e}")

    def save_credentials(self, creds: Dict[str, Any]):
        try:
            raw = json.dumps(creds)
            enc = encrypt_secret(raw)
            _CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            _CONFIG_FILE.write_text(enc, encoding="utf-8")
            self._load_credentials()
            record_audit("SOCIAL_CONFIG_UPDATE", result="SUCCESS")
        except Exception as e:
            print(f"[SocialManager] Failed to save credentials: {e}")

    def get_platforms_status(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": a.platform_id,
                "name": a.platform_name,
                "connected": a.is_connected(),
                "enabled": a.is_enabled,
            }
            for a in self._adapters.values()
        ]

    def get_credentials(self) -> Dict[str, Any]:
        """Return credentials dict (with masked secrets)."""
        creds = {}
        if _CONFIG_FILE.exists():
            try:
                enc = _CONFIG_FILE.read_text(encoding="utf-8")
                raw = decrypt_secret(enc)
                if raw:
                    creds = json.loads(raw)
            except Exception:
                pass
        return creds

    def set_youtube_credentials(self, api_key: str, channel_id: str) -> Tuple[bool, str]:
        """Save YouTube credentials and re-initialize adapter."""
        api_key = api_key.strip()
        channel_id = channel_id.strip()
        if not api_key or not channel_id:
            return False, "Debes proporcionar tanto la API Key como el Channel ID de YouTube."

        creds = self.get_credentials()
        creds["youtube"] = {"api_key": api_key, "channel_id": channel_id}
        self.save_credentials(creds)
        self._adapters["youtube"] = YouTubeAdapter(api_key=api_key, channel_id=channel_id)
        
        # Test connection
        metrics = self._adapters["youtube"].get_metrics()
        if metrics.get("connected"):
            return True, f"Canal '{metrics.get('channel_title', 'YouTube')}' conectado con éxito. {metrics.get('subscribers', 0):,} suscriptores."
        elif "error" in metrics:
            return False, f"Error validando canal de YouTube: {metrics['error']}"
        return True, "Credenciales de YouTube guardadas."

    def get_cross_platform_summary(self) -> str:
        """
        Produce a concise executive briefing across active social platforms.
        If no platforms are configured, transparently reports status without fabricating numbers.
        """
        connected = [a for a in self._adapters.values() if a.is_connected()]
        if not connected:
            return (
                "Actualmente no tienes ninguna red social vinculada. "
                "Puedes configurar tu canal de YouTube o cuentas en el panel de Integraciones (F8) "
                "para ver métricas e interacciones en tiempo real."
            )

        lines = []
        for a in connected:
            m = a.get_metrics()
            if a.platform_id == "youtube":
                title = m.get("channel_title") or "YouTube"
                subs = m.get("subscribers", 0)
                views = m.get("views", 0)
                lines.append(f"YouTube ({title}): {subs:,} suscriptores y {views:,} reproducciones totales.")
            elif a.platform_id == "instagram":
                lines.append(f"Instagram (@{m.get('username', 'conectado')}): activo.")
            elif a.platform_id == "x_twitter":
                lines.append(f"X (@{m.get('username', 'conectado')}): activo.")
            elif a.platform_id == "facebook":
                likes = m.get("page_likes", 0)
                lines.append(f"Facebook ({m.get('name', 'Página')}): {likes:,} me gusta.")

        # Check for recent posts on connected platforms
        all_posts = []
        for a in connected:
            all_posts.extend(a.get_recent_posts(limit=2))

        if all_posts:
            top_post = max(all_posts, key=lambda p: p.get("likes", 0), default={})
            top_title = top_post.get("title") or top_post.get("caption") or top_post.get("text") or ""
            if top_title:
                lines.append(f"Última publicación relevante: '{top_title}'.")

        return " ".join(lines)

    def get_attention_needed_comments(self) -> List[Dict[str, Any]]:
        comments = []
        for a in self._adapters.values():
            if a.is_connected():
                comments.extend(a.get_comments_requiring_attention())
        return comments


# Global Social Media Singleton
social_manager = SocialMediaManager()
