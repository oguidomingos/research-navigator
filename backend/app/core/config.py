"""Application configuration"""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Research Navigator"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://research:research123@localhost:5432/research_navigator"
    DATABASE_URL_SYNC: str = "postgresql://research:research123@localhost:5432/research_navigator"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # LLM
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4-turbo-preview"
    LLM_MAX_TOKENS: int = 4000
    
    # API Keys
    OPENALEX_API_KEY: str = ""
    SEMANTIC_SCHOLAR_API_KEY: str = ""
    CORE_API_KEY: str = ""
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()