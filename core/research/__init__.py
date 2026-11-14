"""
Viernes — Advanced Web Research Subsystem
"""

from core.research.serpapi_client import SerpApiClient, SearchResultItem
from core.research.web_reader import WebReader, ExtractedPage
from core.research.researcher import ResearchEngine, ResearchReport

__all__ = [
    "SerpApiClient",
    "SearchResultItem",
    "WebReader",
    "ExtractedPage",
    "ResearchEngine",
    "ResearchReport",
]
