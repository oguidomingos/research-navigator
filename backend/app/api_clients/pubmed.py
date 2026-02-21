"""PubMed API client"""

from typing import Dict, Any, Optional
from app.api_clients.base import BaseClient


class PubMedClient(BaseClient):
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    async def search(self, query: str, filters: Dict[str, Any], limit: int) -> Dict[str, Any]:
        search_params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": min(limit, 100)}

        try:
            search_response = await self.client.get(f"{self.BASE_URL}/esearch.fcgi", params=search_params)
            search_response.raise_for_status()
            search_data = search_response.json()
            pmids = search_data.get('esearchresult', {}).get('idlist', [])
            if not pmids: return {'articles': []}

            summary_params = {"db": "pubmed", "id": ','.join(pmids), "retmode": "json"}
            summary_response = await self.client.get(f"{self.BASE_URL}/esummary.fcgi", params=summary_params)
            summary_response.raise_for_status()
            summary_data = summary_response.json()

            articles = []
            for pmid in pmids:
                article_data = summary_data.get('result', {}).get(pmid, {})
                if article_data:
                    article_data['pmid'] = pmid
                    articles.append(self._normalize_article(self._extract(article_data)))
            return {'articles': articles}
        except Exception as e:
            print(f"PubMed error: {e}")
            return {'articles': []}

    def _extract(self, raw: Dict) -> Dict:
        return {
            'title': raw.get('title') or '',
            'authors': [{'name': f"{a.get('name', {}).get('lastname', '')} {a.get('name', {}).get('initials', '')}"} for a in raw.get('authors', [])],
            'year': int(raw.get('pubdate', '').split()[0]) if raw.get('pubdate') else None,
            'journal': raw.get('source') or '',
            'pmid': raw.get('pmid') or '',
            'url': f"https://pubmed.ncbi.nlm.nih.gov/{raw.get('pmid')}/" if raw.get('pmid') else '',
            'open_access': False
        }