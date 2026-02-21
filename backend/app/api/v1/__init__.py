"""API v1 routes"""

from fastapi import APIRouter
from app.api.v1.endpoints import search, articles, collections, summary, export, health

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(articles.router, prefix="/articles", tags=["Articles"])
api_router.include_router(collections.router, prefix="/collections", tags=["Collections"])
api_router.include_router(summary.router, prefix="/summary", tags=["Summary"])
api_router.include_router(export.router, prefix="/export", tags=["Export"])