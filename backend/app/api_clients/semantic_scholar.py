"""Semantic Scholar API client"""

from typing import Dict, Any, Optional
from app.api_clients.base import BaseClient


class SemanticScholarClient(BaseClient):
    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def __init__(self, api_key: Optional[str] = None, timeout: int = 30):
        super().__init__(api_key, timeout)
        self.headers = {"Accept": "application/json"}
        if api_key: self.headers["x-api-key"] = api_key

    async def search(self, query: str, filters: Dict[str, Any], limit: int) -> Dict[str, Any]:
        params = {
            "query": query, "limit": min(limit, 100),
            "fields": "paperId,title,abstract,authors,year,venue,citationCount,openAccessPdf,externalIds,url,publicationDate"
        }

        try:
            response = await self.client.get(f"{self.BASE_URL}/paper/search", params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            articles = [self._normalize_article(self._extract(paper)) for paper in data.get('data', [])]
            return {'articles': articles}
        except Exception as e:
            print(f"Semantic Scholar error: {e}")
            return {'articles': []}

    def _extract(self, raw: Dict) -> Dict:
        return {
            'title': raw.get('title') or '',
            'authors': [{'name': a.get('name', '')} for a in raw.get('authors', [])],
            'year': raw.get('year'),
            'journal': raw.get('venue') or '',
            'doi': raw.get('externalIds', {}).get('DOI', '') or '',
            'pmid': raw.get('externalIds', {}).get('PubMed', '') or '',
            'abstract': raw.get('abstract') or (f"[AI Summary] {raw.get('tldr', {}).get('text', '')}" if raw.get('tldr') else ''),
            'citation_count': raw.get('citationCount', 0) or 0,
            'url': raw.get('url') or raw.get('openAccessPdf', {}).get('url', '') or '',
            'type': (raw.get('publicationTypes') or ['article'])[0].lower() if raw.get('publicationTypes') else 'article',
            'open_access': bool(raw.get('openAccessPdf'))
        }