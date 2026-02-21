"""Application configuration"""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache
from pathlib import Path

ROOT_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    APP_NAME: str = "Research Navigator"
    DEBUG: bool = False
    DISABLE_DB: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://research:research123@localhost:5432/research_navigator"
    DATABASE_URL_SYNC: str = "postgresql://research:research123@localhost:5432/research_navigator"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # LLM
    OPENAI_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "openai/gpt-5.1-mini"
    LLM_MODEL: str = "gpt-4-turbo-preview"
    LLM_MAX_TOKENS: int = 4000
    
    # API Keys
    OPENALEX_API_KEY: str = ""
    SEMANTIC_SCHOLAR_API_KEY: str = ""
    CORE_API_KEY: str = ""
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        env_file = str(ROOT_ENV_FILE)
        case_sensitive = True
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


def get_cors_origins() -> List[str]:
    return [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
