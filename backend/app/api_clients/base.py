"""Base API client"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import httpx


class BaseClient(ABC):
    def __init__(self, api_key: Optional[str] = None, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)

    @abstractmethod
    async def search(self, query: str, filters: Dict[str, Any], limit: int) -> Dict[str, Any]:
        pass

    def _normalize_article(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'title': raw.get('title', ''),
            'authors': raw.get('authors', []),
            'year': raw.get('year'),
            'journal': raw.get('journal', ''),
            'doi': raw.get('doi', ''),
            'pmid': raw.get('pmid', ''),
            'abstract': raw.get('abstract', ''),
            'citation_count': raw.get('citation_count', 0) or 0,
            'url': raw.get('url', ''),
            'type': raw.get('type', 'article'),
            'open_access': bool(raw.get('open_access', False)),
            'raw': raw
        }

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()