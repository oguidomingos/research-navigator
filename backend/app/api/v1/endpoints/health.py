"""Health endpoints"""

from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/status")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected" if settings.REDIS_URL else "disabled"
    }


@router.get("/apis")
async def list_apis():
    return {
        "apis": [
            {"name": "OpenAlex", "coverage": ">450M works", "focus": "Global multidisciplinary"},
            {"name": "Semantic Scholar", "coverage": ">250M papers", "focus": "AI-powered relevance"},
            {"name": "CORE", "coverage": ">300M full-texts", "focus": "Open access"},
            {"name": "PubMed", "coverage": ">35M biomedical", "focus": "Health, clinical, biomedical"},
            {"name": "Crossref", "coverage": ">170M DOIs", "focus": "Global metadata"},
            {"name": "arXiv", "coverage": ">2M preprints", "focus": "Preprints, CS, physics"}
        ]
    }