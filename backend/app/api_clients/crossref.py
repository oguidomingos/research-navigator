"""Crossref API client"""

from typing import Dict, Any, Optional
from app.api_clients.base import BaseClient


class CrossRefClient(BaseClient):
    BASE_URL = "https://api.crossref.org"

    def __init__(self, api_key: Optional[str] = None, timeout: int = 30):
        super().__init__(api_key, timeout)
        self.headers = {"Accept": "application/json"}

    async def search(self, query: str, filters: Dict[str, Any], limit: int) -> Dict[str, Any]:
        params = {"query": query, "rows": min(limit, 100)}

        try:
            response = await self.client.get(f"{self.BASE_URL}/works", params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            articles = [self._normalize_article(self._extract(item)) for item in data.get('message', {}).get('items', [])]
            return {'articles': articles}
        except Exception as e:
            print(f"Crossref error: {e}")
            return {'articles': []}

    def _extract(self, raw: Dict) -> Dict:
        pub_date = raw.get('published', {}).get('date-parts', [[]])
        year = pub_date[0][0] if pub_date and pub_date[0] else None
        authors = raw.get('author', [])
        return {
            'title': raw.get('title', [''])[0] if raw.get('title') else '',
            'authors': [{'name': f"{a.get('given', '')} {a.get('family', '')}".strip()} for a in authors],
            'year': year,
            'journal': raw.get('container-title', [''])[0] if raw.get('container-title') else '',
            'doi': raw.get('DOI') or '',
            'url': f"https://doi.org/{raw.get('DOI')}" if raw.get('DOI') else '',
            'type': raw.get('type', 'journal-article').lower()
        }