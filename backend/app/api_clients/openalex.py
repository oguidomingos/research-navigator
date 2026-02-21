"""OpenAlex API client"""

from typing import Dict, Any, Optional, List
from app.api_clients.base import BaseClient


class OpenAlexClient(BaseClient):
    BASE_URL = "https://api.openalex.org"

    def __init__(self, api_key: Optional[str] = None, timeout: int = 30):
        super().__init__(api_key, timeout)
        self.headers = {"User-Agent": "Research-Navigator/1.0 (mailto:contact@iibpr.org.br)", "Accept": "application/json"}
        if api_key: self.headers["api_key"] = api_key

    async def search(self, query: str, filters: Dict[str, Any], limit: int) -> Dict[str, Any]:
        params = {"search": query, "per-page": min(limit, 200)}

        year = filters.get('year')
        if year:
            if isinstance(year, (tuple, list)) and len(year) == 2:
                params['filter'] = f"from_publication_date:{year[0]}-01-01,to_publication_date:{year[1]}-12-31"
            else:
                params['filter'] = f"publication_year:{year}"

        try:
            response = await self.client.get(f"{self.BASE_URL}/works", params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            articles = [self._normalize_article(self._extract(work)) for work in data.get('results', [])]
            return {'articles': articles}
        except Exception as e:
            print(f"OpenAlex error: {e}")
            return {'articles': []}

    def _extract(self, raw: Dict) -> Dict:
        location = raw.get('primary_location') or {}
        source = location.get('source') or {}
        return {
            'title': raw.get('title') or '',
            'authors': [{'name': a.get('author', {}).get('display_name', '')} for a in raw.get('authorships', [])],
            'year': raw.get('publication_year'),
            'journal': source.get('display_name', ''),
            'doi': location.get('doi') or raw.get('doi') or '',
            'abstract': self._reconstruct_abstract(raw.get('abstract_inverted_index')) or '',
            'citation_count': raw.get('cited_by_count', 0) or 0,
            'url': location.get('landing_url') or '',
            'type': raw.get('type') or 'article',
            'open_access': bool(location.get('is_oa', False))
        }

    def _reconstruct_abstract(self, inverted):
        if not inverted: return ''
        try:
            words = [''] * (max(max(v) for v in inverted.values()) + 1)
            for word, positions in inverted.items():
                for pos in positions: words[pos] = word
            return ' '.join(words).strip()
        except: return ''
