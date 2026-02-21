"""Pydantic schemas"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime


class ArticleResponse(BaseModel):
    id: int
    title: str
    authors: List[Dict[str, str]] = []
    abstract: Optional[str] = None
    year: Optional[int] = None
    journal: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    paper_type: Optional[str] = None
    open_access: Optional[bool] = False
    citation_count: Optional[int] = 0
    url: Optional[str] = None
    sources: List[str] = []
    summary: Optional[str] = None

    class Config:
        from_attributes = True


class SearchFilters(BaseModel):
    year: Optional[Any] = None
    type: Optional[str] = None
    open_access: Optional[bool] = None
    sources: Optional[List[str]] = None


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    filters: Optional[SearchFilters] = None
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    sort_by: Literal['relevance', 'recency', 'citations'] = 'relevance'


class SearchResponse(BaseModel):
    query: str
    total: int
    results: List[ArticleResponse]
    sources_used: List[str]
    cached: bool = False
    search_time_ms: Optional[float] = None


class CollectionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class CollectionResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    paper_count: int = 0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AddToCollectionRequest(BaseModel):
    article_ids: List[int]
    notes: Optional[str] = None


class SummaryRequest(BaseModel):
    article_id: int
    language: str = "pt"


class SummaryResponse(BaseModel):
    article_id: int
    summary: str
    objectives: Optional[str] = None
    methodology: Optional[str] = None
    results: Optional[str] = None
    limitations: Optional[str] = None
    generated_at: datetime


class CollectionSummaryRequest(BaseModel):
    collection_id: int
    language: str = "pt"


class CollectionSummaryResponse(BaseModel):
    collection_id: int
    collection_name: str
    article_count: int
    synthesis: str
    comparisons: List[Dict[str, Any]]
    gaps: List[str]
    next_steps: List[str]
    generated_at: datetime


class ExportRequest(BaseModel):
    format: Literal['bibtex', 'apa', 'abnt']
    article_ids: List[int]


class ExportResponse(BaseModel):
    format: str
    content: str
    filename: str
    exported_at: datetime


class CitationRequest(BaseModel):
    article_id: int
    style: Literal['apa', 'abnt', 'bibtex']


class CitationResponse(BaseModel):
    article_id: int
    style: str
    citation: str
    bibkey: Optional[str] = None


class LLMArticleInput(BaseModel):
    local_id: Optional[int] = None
    title: str
    authors: List[str] = []
    year: Optional[int] = None
    journal: Optional[str] = None
    doi: Optional[str] = None
    abstract: Optional[str] = None
    methodology: Optional[str] = None
    limitations: List[str] = []
    conclusions: List[str] = []


class LLMQuickSummaryRequest(BaseModel):
    article: LLMArticleInput
    language: str = "pt-BR"


class LLMQuickSummaryResponse(BaseModel):
    objetivo: str
    metodologia: str
    principais_achados: str
    limitacoes: str
    implicacoes_praticas: str
    raw: str


class LLMAskArticleRequest(BaseModel):
    article: LLMArticleInput
    question: str
    language: str = "pt-BR"


class LLMAskArticleResponse(BaseModel):
    answer: str
    citation: str


class LLMSynthesisRequest(BaseModel):
    articles: List[LLMArticleInput]
    synthesis_type: str = "Revisao comparativa"
    size: str = "Medio"
    language: str = "pt-BR"


class LLMSynthesisResponse(BaseModel):
    introducao: str
    convergencias: str
    divergencias: str
    lacunas: str
    recomendacoes: str
    referencias_apa: List[str]
    raw: str


class LLMRecommendResultsRequest(BaseModel):
    instruction: str
    articles: List[LLMArticleInput]
    language: str = "pt-BR"


class LLMRecommendedArticle(BaseModel):
    local_id: int
    reason: str


class LLMRecommendResultsResponse(BaseModel):
    recommendations: List[LLMRecommendedArticle]
    summary: str
    suggested_filters: Dict[str, Any] = {}
    raw: str
