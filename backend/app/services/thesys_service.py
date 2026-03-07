"""Thesys.dev chat service for research-oriented conversational answers."""

from __future__ import annotations

from typing import List

from app.core.config import settings
from app.schemas import LLMArticleInput, ThesysChatMessage

try:
    from openai import AsyncOpenAI
    OPENAI_IMPORT_ERROR = None
except Exception as exc:  # pragma: no cover
    AsyncOpenAI = None
    OPENAI_IMPORT_ERROR = str(exc)


class ThesysService:
    def __init__(self) -> None:
        self.client = None
        self._init_client()

    def _init_client(self) -> None:
        if self.client is not None:
            return
        if not AsyncOpenAI:
            return
        if not settings.THESYS_API_KEY:
            return
        self.client = AsyncOpenAI(
            api_key=settings.THESYS_API_KEY,
            base_url=settings.THESYS_BASE_URL,
        )

    @property
    def is_configured(self) -> bool:
        self._init_client()
        return self.client is not None

    @property
    def configuration_issue(self) -> str:
        if self.client is not None:
            return ""
        if OPENAI_IMPORT_ERROR:
            return f"openai import failed: {OPENAI_IMPORT_ERROR}"
        if not settings.THESYS_API_KEY:
            return "missing THESYS_API_KEY"
        return "unknown configuration issue"

    async def chat(
        self,
        prompt: str,
        language: str,
        search_query: str | None,
        history: List[ThesysChatMessage],
        results: List[LLMArticleInput],
        saved_articles: List[LLMArticleInput],
    ) -> str:
        if not self.client:
            raise RuntimeError("Thesys is not configured")

        messages = [
            {
                "role": "system",
                "content": self._build_system_prompt(
                    language=language,
                    search_query=search_query,
                    results=results,
                    saved_articles=saved_articles,
                ),
            }
        ]

        for message in history[-10:]:
            messages.append({"role": message.role, "content": message.content})

        messages.append({"role": "user", "content": prompt})

        response = await self.client.chat.completions.create(
            model=settings.THESYS_MODEL,
            messages=messages,
        )
        return (response.choices[0].message.content or "").strip()

    def _build_system_prompt(
        self,
        language: str,
        search_query: str | None,
        results: List[LLMArticleInput],
        saved_articles: List[LLMArticleInput],
    ) -> str:
        result_context = self._serialize_articles(results[:10])
        saved_context = self._serialize_articles(saved_articles[:10])

        return (
            f"You are an expert scientific research copilot for the Research Navigator app. "
            f"Answer in {language}. Use TheSys C1 format so the frontend can render rich responses. "
            f"Prefer concise structure, highlight evidence quality, limitations, conflicting findings, "
            f"and next research steps. If the available context is insufficient, say so clearly and ask "
            f"for a tighter question or more search results.\n\n"
            f"Current search query: {search_query or 'none'}\n\n"
            f"Current search results context:\n{result_context}\n\n"
            f"Saved collection context:\n{saved_context}\n\n"
            f"When citing papers, mention title, year, journal and DOI if available. "
            f"Do not invent studies. If the user asks for recommendations, rank them explicitly."
        )

    def _serialize_articles(self, articles: List[LLMArticleInput]) -> str:
        if not articles:
            return "No articles available."

        lines = []
        for index, article in enumerate(articles, start=1):
            lines.append(
                f"{index}. {article.title} | "
                f"authors={', '.join(article.authors) if article.authors else 'N/A'} | "
                f"year={article.year or 'N/A'} | "
                f"journal={article.journal or 'N/A'} | "
                f"doi={article.doi or 'N/A'} | "
                f"abstract={(article.abstract or 'N/A')[:700]}"
            )
        return "\n".join(lines)
