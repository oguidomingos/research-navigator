"""LLM endpoints backed by OpenRouter."""

from fastapi import APIRouter, HTTPException

from app.schemas import (
    LLMQuickSummaryRequest,
    LLMQuickSummaryResponse,
    LLMAskArticleRequest,
    LLMAskArticleResponse,
    LLMSynthesisRequest,
    LLMSynthesisResponse,
    LLMRecommendResultsRequest,
    LLMRecommendResultsResponse,
)
from app.services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()


@router.post("/quick-summary", response_model=LLMQuickSummaryResponse)
async def quick_summary(request: LLMQuickSummaryRequest):
    if not llm_service.is_configured:
        raise HTTPException(status_code=503, detail="OpenRouter is not configured")
    try:
        return await llm_service.quick_summary(request.article, request.language)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM provider error: {exc}") from exc


@router.post("/ask-article", response_model=LLMAskArticleResponse)
async def ask_article(request: LLMAskArticleRequest):
    if not llm_service.is_configured:
        raise HTTPException(status_code=503, detail="OpenRouter is not configured")
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question is required")
    try:
        return await llm_service.ask_article(request.article, request.question, request.language)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM provider error: {exc}") from exc


@router.post("/synthesize", response_model=LLMSynthesisResponse)
async def synthesize(request: LLMSynthesisRequest):
    if not llm_service.is_configured:
        raise HTTPException(status_code=503, detail="OpenRouter is not configured")
    if len(request.articles) < 2:
        raise HTTPException(status_code=400, detail="At least 2 articles are required")
    try:
        return await llm_service.synthesize(request.articles, request.synthesis_type, request.size, request.language)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM provider error: {exc}") from exc


@router.post("/recommend-results", response_model=LLMRecommendResultsResponse)
async def recommend_results(request: LLMRecommendResultsRequest):
    if not llm_service.is_configured:
        raise HTTPException(status_code=503, detail="OpenRouter is not configured")
    if not request.instruction.strip():
        raise HTTPException(status_code=400, detail="Instruction is required")
    if not request.articles:
        raise HTTPException(status_code=400, detail="Articles are required")
    try:
        return await llm_service.recommend_results(request.instruction, request.articles, request.language)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM provider error: {exc}") from exc
