"""Summary endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from app.schemas import SummaryRequest, SummaryResponse, CollectionSummaryRequest, CollectionSummaryResponse
from app.services.summary_service import SummaryService
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
summary_service = SummaryService()


@router.post("/article", response_model=SummaryResponse)
async def generate_article_summary(request: SummaryRequest, db: AsyncSession = Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database disabled in current environment")
    summary = await summary_service.generate_article_summary(request, db)
    if not summary:
        raise HTTPException(status_code=404, detail="Article not found or cannot be summarized")
    return summary


@router.post("/collection", response_model=CollectionSummaryResponse)
async def generate_collection_summary(request: CollectionSummaryRequest, db: AsyncSession = Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database disabled in current environment")
    summary = await summary_service.generate_collection_summary(request, db)
    if not summary:
        raise HTTPException(status_code=404, detail="Collection not found or empty")
    return summary
