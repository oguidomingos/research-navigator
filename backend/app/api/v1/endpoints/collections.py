"""Collection endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas import CollectionCreate, CollectionResponse, AddToCollectionRequest
from app.services.collection_service import CollectionService
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
collection_service = CollectionService()


@router.get("/", response_model=List[CollectionResponse])
async def list_collections(user_id: int, db: AsyncSession = Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database disabled in current environment")
    collections = await collection_service.list_collections(user_id, db)
    return [CollectionResponse(id=c.id, user_id=c.user_id, name=c.name, description=c.description,
                               paper_count=len(c.saved_papers) if c.saved_papers else 0,
                               created_at=c.created_at) for c in collections]


@router.post("/", response_model=CollectionResponse)
async def create_collection(collection: CollectionCreate, user_id: int, db: AsyncSession = Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database disabled in current environment")
    new_collection = await collection_service.create_collection(user_id, collection, db)
    return CollectionResponse(id=new_collection.id, user_id=new_collection.user_id, name=new_collection.name,
                             description=new_collection.description, paper_count=0, created_at=new_collection.created_at)


@router.get("/{collection_id}", response_model=CollectionResponse)
async def get_collection(collection_id: int, db: AsyncSession = Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database disabled in current environment")
    collection = await collection_service.get_collection(collection_id, db)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return CollectionResponse(id=collection.id, user_id=collection.user_id, name=collection.name,
                             description=collection.description,
                             paper_count=len(collection.saved_papers) if collection.saved_papers else 0,
                             created_at=collection.created_at)


@router.delete("/{collection_id}")
async def delete_collection(collection_id: int, db: AsyncSession = Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database disabled in current environment")
    success = await collection_service.delete_collection(collection_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Collection not found")
    return {"message": "Collection deleted"}


@router.post("/{collection_id}/articles")
async def add_to_collection(collection_id: int, request: AddToCollectionRequest, db: AsyncSession = Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database disabled in current environment")
    result = await collection_service.add_articles(collection_id, request.article_ids, request.notes, db)
    if not result:
        raise HTTPException(status_code=404, detail="Collection not found")
    return {"message": f"Added {len(request.article_ids)} articles to collection"}


@router.delete("/{collection_id}/articles/{article_id}")
async def remove_from_collection(collection_id: int, article_id: int, db: AsyncSession = Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database disabled in current environment")
    success = await collection_service.remove_article(collection_id, article_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Collection or article not found")
    return {"message": "Article removed from collection"}
