"""CORE API client"""

from typing import Dict, Any, Optional
from app.api_clients.base import BaseClient


class CoreClient(BaseClient):
    BASE_URL = "https://api.core.ac.uk/v3"

    def __init__(self, api_key: Optional[str] = None, timeout: int = 30):
        super().__init__(api_key, timeout)
        self.headers = {"Accept": "application/json"}
        if api_key: self.headers["Authorization"] = f"Bearer {api_key}"

    async def search(self, query: str, filters: Dict[str, Any], limit: int) -> Dict[str, Any]:
        params = {"q": query, "limit": min(limit, 100)}

        try:
            response = await self.client.get(f"{self.BASE_URL}/search/works", params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            articles = [self._normalize_article(self._extract(work)) for work in data.get('results', [])]
            return {'articles': articles}
        except Exception as e:
            print(f"CORE error: {e}")
            return {'articles': []}

    def _extract(self, raw: Dict) -> Dict:
        return {
            'title': raw.get('title') or '',
            'authors': [{'name': a.get('name', '')} for a in raw.get('authors', [])],
            'year': int(raw.get('publishedDate', '').split('-')[0]) if raw.get('publishedDate') else None,
            'journal': raw.get('journal') or '',
            'doi': next((id.get('id', '') for id in raw.get('identifiers', []) if id.get('type') == 'doi'), ''),
            'abstract': raw.get('abstract') or '',
            'citation_count': raw.get('citationCount', 0) or 0,
            'url': raw.get('downloadUrl') or raw.get('hostPageUrl') or '',
            'open_access': bool(raw.get('downloadUrl'))
        }