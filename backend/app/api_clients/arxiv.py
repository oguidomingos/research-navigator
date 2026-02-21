"""arXiv API client"""

from typing import Dict, Any, Optional
from app.api_clients.base import BaseClient
import feedparser


class ArxivClient(BaseClient):
    BASE_URL = "https://export.arxiv.org/api/query"

    async def search(self, query: str, filters: Dict[str, Any], limit: int) -> Dict[str, Any]:
        params = {"search_query": f"all:{query}", "max_results": min(limit, 100)}

        try:
            response = await self.client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            feed = feedparser.parse(response.text)
            articles = [self._normalize_article(self._extract(entry)) for entry in feed.entries]
            return {'articles': articles}
        except Exception as e:
            print(f"arXiv error: {e}")
            return {'articles': []}

    def _extract(self, raw: Dict) -> Dict:
        return {
            'title': raw.get('title') or '',
            'authors': [{'name': a.get('name', '')} for a in raw.get('authors', [])],
            'year': int(raw.get('published', '').split('-')[0]) if raw.get('published') else None,
            'journal': 'arXiv',
            'abstract': ' '.join(raw.get('summary', '').split()) if raw.get('summary') else '',
            'url': next((l.get('href', '') for l in raw.get('links', []) if 'arxiv.org/abs' in l.get('href', '')), ''),
            'type': 'preprint',
            'open_access': True
        }
