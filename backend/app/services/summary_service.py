"""Summary service"""

from typing import Optional, List, Dict
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Paper, Collection, SavedPaper
from app.schemas import SummaryRequest, SummaryResponse, CollectionSummaryRequest, CollectionSummaryResponse
from app.core.config import settings
from openai import AsyncOpenAI


class SummaryService:
    def __init__(self):
        self.openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

    async def generate_article_summary(self, request: SummaryRequest, db: AsyncSession) -> Optional[SummaryResponse]:
        result = await db.execute(select(Paper).where(Paper.id == request.article_id))
        paper = result.scalar_one_or_none()
        if not paper: return None

        if not self.openai:
            return SummaryResponse(article_id=request.article_id, summary="LLM service not configured", generated_at=datetime.utcnow())

        prompt = f"""Summarize this academic article in {request.language}:

Title: {paper.title}
Authors: {', '.join([a.get('name', '') for a in (paper.authors or [])])}
Year: {paper.year or 'Unknown'}

Abstract:
{paper.abstract or 'No abstract available.'}

Provide:
1. SUMMARY: Overall summary (2-3 paragraphs)
2. OBJECTIVES: Main objectives/research questions
3. METHODOLOGY: Key methodological aspects
4. RESULTS: Main findings
5. LIMITATIONS: Study limitations
"""

        try:
            response = await self.openai.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=settings.LLM_MAX_TOKENS
            )
            content = response.choices[0].message.content

            paper.summary = content
            await db.commit()

            return SummaryResponse(article_id=request.article_id, summary=content, generated_at=datetime.utcnow())
        except Exception as e:
            print(f"Error generating summary: {e}")
            return None

    async def generate_collection_summary(self, request: CollectionSummaryRequest, db: AsyncSession) -> Optional[CollectionSummaryResponse]:
        result = await db.execute(select(Collection).where(Collection.id == request.collection_id))
        collection = result.scalar_one_or_none()
        if not collection: return None

        saved_papers_result = await db.execute(select(SavedPaper).where(SavedPaper.collection_id == request.collection_id))
        saved_papers = saved_papers_result.scalars().all()
        if not saved_papers: return None

        papers = []
        for sp in saved_papers:
            paper_result = await db.execute(select(Paper).where(Paper.id == sp.paper_id))
            paper = paper_result.scalar_one_or_none()
            if paper: papers.append(paper)

        if not self.openai:
            return CollectionSummaryResponse(
                collection_id=request.collection_id, collection_name=collection.name,
                article_count=len(papers), synthesis="LLM service not configured",
                comparisons=[], gaps=[], next_steps=[], generated_at=datetime.utcnow()
            )

        papers_info = "\n\n".join([
            f"Paper {i+1}: {p.title} ({p.year or 'Unknown'})\n{p.abstract or 'No abstract'}"
            for i, p in enumerate(papers)
        ])

        prompt = f"""Synthesize these {len(papers)} academic articles in {request.language}:

{papers_info}

Provide:
1. SYNTHESIS: Comprehensive synthesis (3-4 paragraphs)
2. COMPARISONS: Key comparisons between papers
3. GAPS: Research gaps identified
4. NEXT STEPS: Suggested future research directions
"""

        try:
            response = await self.openai.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=settings.LLM_MAX_TOKENS
            )
            content = response.choices[0].message.content

            return CollectionSummaryResponse(
                collection_id=request.collection_id, collection_name=collection.name,
                article_count=len(papers), synthesis=content,
                comparisons=[], gaps=[], next_steps=[], generated_at=datetime.utcnow()
            )
        except Exception as e:
            print(f"Error generating collection summary: {e}")
            return None