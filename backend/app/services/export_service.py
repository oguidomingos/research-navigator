"""Export service"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Paper


class ExportService:
    async def export_articles(self, article_ids: List[int], format: str, db: Optional[AsyncSession] = None) -> Optional[str]:
        if not db:
            return self._generate_placeholder_citations(article_ids, format)

        papers = []
        for article_id in article_ids:
            result = await db.execute(select(Paper).where(Paper.id == article_id))
            paper = result.scalar_one_or_none()
            if paper: papers.append(paper)

        if not papers: return None

        if format == 'bibtex': return self._export_bibtex(papers)
        elif format == 'apa': return self._export_apa(papers)
        elif format == 'abnt': return self._export_abnt(papers)
        return self._export_apa(papers)

    def _export_bibtex(self, papers: List[Paper]) -> str:
        entries = []
        for paper in papers:
            key = f"{(paper.authors[0].get('name', 'unknown').split()[-1] if paper.authors else 'unknown').lower()}{paper.year or ''}"
            entry = f"@article{{{key},\n  title = {{{paper.title}}},\n"
            if paper.authors:
                entry += f"  author = {{{' and '.join([a.get('name', '') for a in paper.authors])}}},\n"
            if paper.year: entry += f"  year = {{{paper.year}}},\n"
            if paper.journal: entry += f"  journal = {{{paper.journal}}},\n"
            if paper.doi: entry += f"  doi = {{{paper.doi}}},\n"
            entry += "}\n"
            entries.append(entry)
        return '\n'.join(entries)

    def _export_apa(self, papers: List[Paper]) -> str:
        citations = []
        for paper in papers:
            parts = []
            if paper.authors:
                parts.append(', '.join([a.get('name', '') for a in paper.authors]))
            if paper.year: parts.append(f"({paper.year})")
            if paper.title: parts.append(paper.title)
            if paper.journal: parts.append(f"*{paper.journal}*")
            if paper.doi: parts.append(f"https://doi.org/{paper.doi}")
            citations.append('. '.join(parts) + '.')
        return '\n\n'.join(citations)

    def _export_abnt(self, papers: List[Paper]) -> str:
        citations = []
        for paper in papers:
            parts = []
            if paper.authors:
                authors_upper = [a.get('name', '').upper() for a in paper.authors[:3]]
                if len(paper.authors) > 3: authors_upper.append("et al.")
                parts.append('; '.join(authors_upper))
            if paper.title: parts.append(paper.title)
            if paper.journal: parts.append(f"*{paper.journal}*")
            if paper.year: parts.append(str(paper.year))
            if paper.doi: parts.append(f"DOI: {paper.doi}")
            citations.append('. '.join(parts) + '.')
        return '\n\n'.join(citations)

    def _generate_placeholder_citations(self, article_ids: List[int], format: str) -> str:
        return '\n\n'.join([f"Article {aid}. Citation in {format.upper()} format." for aid in article_ids])