"""Article endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from app.schemas import ArticleResponse, CitationRequest, CitationResponse
from app.services.article_service import ArticleService
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
article_service = ArticleService()


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int, db: AsyncSession = Depends(get_db)):
    article = await article_service.get_article(article_id, db)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleResponse.model_validate(article)


@router.post("/{article_id}/cite", response_model=CitationResponse)
async def generate_citation(article_id: int, request: CitationRequest):
    citation = await article_service.generate_citation(article_id, request.style)
    if not citation:
        raise HTTPException(status_code=404, detail="Article not found")
    return CitationResponse(article_id=article_id, style=request.style, citation=citation['citation'], bibkey=citation.get('bibkey'))