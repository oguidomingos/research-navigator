"""Collection service"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Collection, SavedPaper, Paper
from app.schemas import CollectionCreate


class CollectionService:
    async def list_collections(self, user_id: int, db: AsyncSession) -> List[Collection]:
        result = await db.execute(
            select(Collection).where(Collection.user_id == user_id)
            .options(selectinload(Collection.saved_papers))
            .order_by(Collection.created_at.desc())
        )
        return result.scalars().all()

    async def get_collection(self, collection_id: int, db: AsyncSession) -> Optional[Collection]:
        result = await db.execute(
            select(Collection).where(Collection.id == collection_id)
            .options(selectinload(Collection.saved_papers))
        )
        return result.scalar_one_or_none()

    async def create_collection(self, user_id: int, collection: CollectionCreate, db: AsyncSession) -> Collection:
        new_collection = Collection(user_id=user_id, name=collection.name, description=collection.description)
        db.add(new_collection)
        await db.commit()
        await db.refresh(new_collection)
        return new_collection

    async def delete_collection(self, collection_id: int, db: AsyncSession) -> bool:
        collection = await self.get_collection(collection_id, db)
        if not collection: return False
        await db.delete(collection)
        await db.commit()
        return True

    async def add_articles(self, collection_id: int, article_ids: List[int], notes: Optional[str], db: AsyncSession) -> bool:
        collection = await self.get_collection(collection_id, db)
        if not collection: return False

        for article_id in article_ids:
            paper_result = await db.execute(select(Paper).where(Paper.id == article_id))
            paper = paper_result.scalar_one_or_none()
            if not paper: continue

            existing = await db.execute(
                select(SavedPaper).where(SavedPaper.collection_id == collection_id, SavedPaper.paper_id == article_id)
            )
            if existing.scalar_one_or_none(): continue

            saved_paper = SavedPaper(user_id=collection.user_id, paper_id=article_id, collection_id=collection_id, notes=notes)
            db.add(saved_paper)

        await db.commit()
        return True

    async def remove_article(self, collection_id: int, article_id: int, db: AsyncSession) -> bool:
        result = await db.execute(
            select(SavedPaper).where(SavedPaper.collection_id == collection_id, SavedPaper.paper_id == article_id)
        )
        saved_paper = result.scalar_one_or_none()
        if not saved_paper: return False
        await db.delete(saved_paper)
        await db.commit()
        return True
