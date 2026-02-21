"""Search service - orchestrates parallel search across multiple academic APIs"""

import asyncio
from typing import List, Dict, Any, Optional
import hashlib

from app.api_clients.openalex import OpenAlexClient
from app.api_clients.semantic_scholar import SemanticScholarClient
from app.api_clients.core import CoreClient
from app.api_clients.pubmed import PubMedClient
from app.api_clients.crossref import CrossRefClient
from app.api_clients.arxiv import ArxivClient
from app.core.config import settings


class SearchService:
    def __init__(self):
        self.clients = {
            'openalex': OpenAlexClient(api_key=settings.OPENALEX_API_KEY),
            'semantic_scholar': SemanticScholarClient(api_key=settings.SEMANTIC_SCHOLAR_API_KEY),
            'core': CoreClient(api_key=settings.CORE_API_KEY),
            'pubmed': PubMedClient(),
            'crossref': CrossRefClient(),
            'arxiv': ArxivClient(),
        }

    async def search(self, query: str, filters: Optional[Dict] = None, limit: int = 20, offset: int = 0, sort_by: str = 'relevance') -> Dict:
        filters = filters or {}
        sources_to_query = filters.get('sources')

        if sources_to_query:
            clients_to_query = {k: v for k, v in self.clients.items() if k in sources_to_query}
        else:
            clients_to_query = self.clients

        tasks = [self._search_single_api(client, name, query, filters, limit) for name, client in clients_to_query.items()]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_articles = []
        sources_used = []

        for name, result in zip(clients_to_query.keys(), results):
            if isinstance(result, Exception) or not result:
                continue
            if result.get('articles'):
                for article in result['articles']:
                    article['sources'] = article.get('sources', [])
                    if name not in article['sources']:
                        article['sources'].append(name)
                all_articles.extend(result['articles'])
                sources_used.append(name)

        deduplicated = self._deduplicate_articles(all_articles)
        ranked = self._rank_articles(deduplicated, sort_by, query)
        paginated = ranked[offset:offset + limit]

        return {'total': len(ranked), 'articles': paginated, 'sources_used': sources_used}

    async def _search_single_api(self, client, name: str, query: str, filters: Dict, limit: int):
        try:
            return await client.search(query, filters, limit)
        except Exception as e:
            print(f"Error in {name}: {e}")
            return None

    def _deduplicate_articles(self, articles: List[Dict]) -> List[Dict]:
        seen_dois = set()
        seen_signatures = set()
        deduplicated = []

        for article in articles:
            doi = article.get('doi')
            if doi and doi.lower() in seen_dois:
                continue
            if doi:
                seen_dois.add(doi.lower())

            title = article.get('title', '').lower().strip()
            authors = article.get('authors', [])
            year = article.get('year')

            if title and authors and year:
                author_names = ','.join([a.get('name', '') for a in authors if isinstance(a, dict)])
                signature = hashlib.md5(f"{title}{author_names}{year}".encode()).hexdigest()
                if signature in seen_signatures:
                    continue
                seen_signatures.add(signature)

            deduplicated.append(article)

        return deduplicated

    def _rank_articles(self, articles: List[Dict], sort_by: str, query: str) -> List[Dict]:
        if not articles:
            return articles

        if sort_by == 'recency':
            return sorted(articles, key=lambda x: (x.get('year') or 0), reverse=True)
        elif sort_by == 'citations':
            return sorted(articles, key=lambda x: (x.get('citation_count') or 0), reverse=True)
        else:
            query_terms = set(query.lower().split())
            def calc_score(article):
                score = 0
                title = article.get('title', '').lower()
                abstract = article.get('abstract', '').lower()
                for term in query_terms:
                    if term in title: score += 10
                    if term in abstract: score += 5
                if article.get('year', 0) >= 2020: score += 2
                if article.get('citation_count', 0) >= 100: score += 3
                return score
            return sorted(articles, key=calc_score, reverse=True)

    async def get_suggestions(self, query: str, limit: int = 10) -> List[str]:
        suggestions = []
        common_terms = ["machine learning", "artificial intelligence", "psychomotor", "child development", "autism", "motor skills", "sensory integration"]
        for term in common_terms:
            if query.lower() in term.lower():
                suggestions.append(term)
                if len(suggestions) >= limit: break
        return suggestions