"""API clients for academic research sources"""

from app.api_clients.base import BaseClient
from app.api_clients.openalex import OpenAlexClient
from app.api_clients.semantic_scholar import SemanticScholarClient
from app.api_clients.core import CoreClient
from app.api_clients.pubmed import PubMedClient
from app.api_clients.crossref import CrossRefClient
from app.api_clients.arxiv import ArxivClient

__all__ = ["BaseClient", "OpenAlexClient", "SemanticScholarClient", "CoreClient", "PubMedClient", "CrossRefClient", "ArxivClient"]