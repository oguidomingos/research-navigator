"""Database configuration"""

from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import settings

async_engine = None
AsyncSessionLocal = None

if not settings.DISABLE_DB:
    async_engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
    AsyncSessionLocal = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db() -> AsyncGenerator[Optional[AsyncSession], None]:
    if settings.DISABLE_DB or AsyncSessionLocal is None:
        yield None
        return

    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db():
    if settings.DISABLE_DB or async_engine is None:
        print("⚠️ Database disabled (DISABLE_DB=true)")
        return
    async with async_engine.connect() as conn:
        print("✅ Database connected")


async def close_db():
    if settings.DISABLE_DB or async_engine is None:
        return
    await async_engine.dispose()
    print("👋 Database disconnected")
