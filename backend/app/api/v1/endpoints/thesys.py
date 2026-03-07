"""Thesys.dev chat endpoint."""

from fastapi import APIRouter, HTTPException

from app.schemas import ThesysChatRequest, ThesysChatResponse
from app.services.thesys_service import ThesysService

router = APIRouter()
thesys_service = ThesysService()


@router.post("/chat", response_model=ThesysChatResponse)
async def chat(request: ThesysChatRequest):
    if not thesys_service.is_configured:
        raise HTTPException(
            status_code=503,
            detail=f"Thesys is not configured: {thesys_service.configuration_issue}",
        )

    try:
        c1_response = await thesys_service.chat(
            prompt=request.prompt,
            language=request.language,
            search_query=request.search_query,
            history=request.history,
            results=request.results,
            saved_articles=request.saved_articles,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Thesys provider error: {exc}") from exc

    return ThesysChatResponse(
        c1_response=c1_response,
        model="thesys",
    )
