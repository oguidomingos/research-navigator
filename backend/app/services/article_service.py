"""Article service"""

from typing import List, Optional, Dict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Paper
from app.schemas import ArticleUpdate


class ArticleService:
    async def get_article(self, article_id: int, db: AsyncSession) -> Optional[Paper]:
        result = await db.execute(select(Paper).where(Paper.id == article_id))
        return result.scalar_one_or_none()

    async def get_article_by_doi(self, doi: str, db: AsyncSession) -> Optional[Paper]:
        result = await db.execute(select(Paper).where(Paper.doi == doi))
        return result.scalar_one_or_none()

    async def generate_citation(self, article_id: int, style: str) -> Optional[Dict]:
        return {"citation": f"Citation for article {article_id} in {style} style", "bibkey": f"article_{article_id}"}

    async def get_related_articles(self, article_id: int, limit: int, db: AsyncSession) -> List[Paper]:
        result = await db.execute(select(Paper).where(Paper.id != article_id).limit(limit))
        return result.scalars().all()

    async def save_article(self, article_data: Dict, db: AsyncSession) -> Paper:
        paper = Paper(
            title=article_data.get('title'),
            abstract=article_data.get('abstract'),
            authors=article_data.get('authors'),
            year=article_data.get('year'),
            journal=article_data.get('journal'),
            doi=article_data.get('doi'),
            pmid=article_data.get('pmid'),
            paper_type=article_data.get('type'),
            open_access=article_data.get('open_access', False),
            citation_count=article_data.get('citation_count', 0),
            url=article_data.get('url'),
            sources=article_data.get('sources', [])
        )
        db.add(paper)
        await db.commit()
        await db.refresh(paper)
        return paper