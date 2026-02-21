"""Search endpoints"""

from fastapi import APIRouter, Depends
import time
from app.schemas import SearchRequest, SearchResponse, ArticleResponse
from app.services.search_service import SearchService
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
search_service = SearchService()


@router.post("/articles", response_model=SearchResponse)
async def search_articles(request: SearchRequest, db: AsyncSession = Depends(get_db)):
    start_time = time.time()

    results = await search_service.search(
        query=request.query,
        filters=request.filters.model_dump() if request.filters else {},
        limit=request.limit,
        offset=request.offset,
        sort_by=request.sort_by
    )

    search_time = (time.time() - start_time) * 1000

    return SearchResponse(
        query=request.query,
        total=results['total'],
        results=[ArticleResponse(**article) for article in results['articles']],
        sources_used=results['sources_used'],
        cached=False,
        search_time_ms=search_time
    )


@router.get("/suggestions")
async def get_suggestions(query: str, limit: int = 10):
    suggestions = await search_service.get_suggestions(query, limit)
    return {"suggestions": suggestions}