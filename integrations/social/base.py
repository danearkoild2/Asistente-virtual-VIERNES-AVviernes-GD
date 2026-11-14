"""
Social Media Adapter Interface for VIERNES
===========================================
Defines the base contract for all external social network integrations.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class SocialAdapter(ABC):
    """Abstract base class for social media platform integrations."""

    def __init__(self, platform_id: str, platform_name: str):
        self.platform_id = platform_id
        self.platform_name = platform_name
        self.is_enabled = False

    @abstractmethod
    def is_connected(self) -> bool:
        """Return True if valid API credentials/tokens are configured."""
        pass

    @abstractmethod
    def get_metrics(self) -> Dict[str, Any]:
        """Fetch platform overview metrics (followers, impressions, engagement, reach)."""
        pass

    @abstractmethod
    def get_recent_posts(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Fetch recent publications with likes, comments, and shares."""
        pass

    @abstractmethod
    def create_post(self, content: str, media_urls: Optional[List[str]] = None) -> Dict[str, Any]:
        """Publish a new post if the API allows."""
        pass

    @abstractmethod
    def get_comments_requiring_attention(self) -> List[Dict[str, Any]]:
        """Analyze recent comments to detect inquiries, support requests, or negative sentiment."""
        pass
