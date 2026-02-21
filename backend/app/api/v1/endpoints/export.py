"""Export endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from app.schemas import ExportRequest, ExportResponse
from app.services.export_service import ExportService
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
export_service = ExportService()


@router.post("/", response_model=ExportResponse)
async def export_articles(request: ExportRequest, db: AsyncSession = Depends(get_db)):
    result = await export_service.export_articles(request.article_ids, request.format, db)
    if not result:
        raise HTTPException(status_code=400, detail="Export failed")
    return ExportResponse(format=request.format, content=result, filename=f"references.{request.format}", exported_at=datetime.utcnow())