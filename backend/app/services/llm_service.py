"""LLM service using OpenRouter for MVP summarization, QA and synthesis."""

from __future__ import annotations

import json
import re
from typing import List

from app.core.config import settings
from app.schemas import (
    LLMArticleInput,
    LLMQuickSummaryResponse,
    LLMAskArticleResponse,
    LLMSynthesisResponse,
    LLMRecommendedArticle,
    LLMRecommendResultsResponse,
)

try:
    from openai import AsyncOpenAI
except Exception:  # pragma: no cover
    AsyncOpenAI = None


class LLMService:
    def __init__(self):
        self.client = None
        if AsyncOpenAI and settings.OPENROUTER_API_KEY:
            self.client = AsyncOpenAI(
                api_key=settings.OPENROUTER_API_KEY,
                base_url=settings.OPENROUTER_BASE_URL,
            )

    @property
    def is_configured(self) -> bool:
        return self.client is not None

    async def _complete(self, prompt: str) -> str:
        if not self.client:
            raise RuntimeError("OpenRouter not configured")

        response = await self.client.chat.completions.create(
            model=settings.OPENROUTER_MODEL,
            messages=[
                {"role": "system", "content": "You are a precise academic assistant. Follow formatting strictly."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return (response.choices[0].message.content or "").strip()

    async def quick_summary(self, article: LLMArticleInput, language: str) -> LLMQuickSummaryResponse:
        prompt = f"""
Generate a structured academic summary in {language}.

Article metadata:
Title: {article.title}
Authors: {', '.join(article.authors) if article.authors else 'N/A'}
Year: {article.year or 'N/A'}
Journal: {article.journal or 'N/A'}
DOI: {article.doi or 'N/A'}
Abstract: {article.abstract or 'N/A'}
Methodology hints: {article.methodology or 'N/A'}
Conclusions hints: {'; '.join(article.conclusions) if article.conclusions else 'N/A'}
Limitations hints: {'; '.join(article.limitations) if article.limitations else 'N/A'}

Return exactly with these headings (one paragraph each):
OBJETIVO:
METODOLOGIA:
PRINCIPAIS_ACHADOS:
LIMITACOES:
IMPLICACOES_PRATICAS:
""".strip()

        raw = await self._complete(prompt)

        return LLMQuickSummaryResponse(
            objetivo=self._extract_section(raw, "OBJETIVO"),
            metodologia=self._extract_section(raw, "METODOLOGIA"),
            principais_achados=self._extract_section(raw, "PRINCIPAIS_ACHADOS"),
            limitacoes=self._extract_section(raw, "LIMITACOES"),
            implicacoes_praticas=self._extract_section(raw, "IMPLICACOES_PRATICAS"),
            raw=raw,
        )

    async def ask_article(self, article: LLMArticleInput, question: str, language: str) -> LLMAskArticleResponse:
        prompt = f"""
Answer this question about the article in {language}.
Question: {question}

Article:
Title: {article.title}
Authors: {', '.join(article.authors) if article.authors else 'N/A'}
Year: {article.year or 'N/A'}
DOI: {article.doi or 'N/A'}
Abstract: {article.abstract or 'N/A'}
Methodology hints: {article.methodology or 'N/A'}
Conclusions hints: {'; '.join(article.conclusions) if article.conclusions else 'N/A'}

Format:
ANSWER:
CITATION:
""".strip()

        raw = await self._complete(prompt)
        return LLMAskArticleResponse(
            answer=self._extract_section(raw, "ANSWER"),
            citation=self._extract_section(raw, "CITATION"),
        )

    async def synthesize(self, articles: List[LLMArticleInput], synthesis_type: str, size: str, language: str) -> LLMSynthesisResponse:
        papers_text = []
        for idx, article in enumerate(articles, start=1):
            papers_text.append(
                f"Paper {idx}: {article.title} ({article.year or 'N/A'})\\n"
                f"Authors: {', '.join(article.authors) if article.authors else 'N/A'}\\n"
                f"Journal: {article.journal or 'N/A'}\\n"
                f"DOI: {article.doi or 'N/A'}\\n"
                f"Abstract: {article.abstract or 'N/A'}"
            )

        prompt = f"""
Create an academic synthesis in {language}.
Synthesis type: {synthesis_type}
Size: {size}

Articles:
{chr(10).join(papers_text)}

Return exactly with these headings:
INTRODUCAO:
CONVERGENCIAS:
DIVERGENCIAS:
LACUNAS:
RECOMENDACOES:
REFERENCIAS_APA:
- reference 1
- reference 2
""".strip()

        raw = await self._complete(prompt)
        refs_raw = self._extract_section(raw, "REFERENCIAS_APA")
        refs = [line.strip().lstrip("- ").strip() for line in refs_raw.splitlines() if line.strip()]

        return LLMSynthesisResponse(
            introducao=self._extract_section(raw, "INTRODUCAO"),
            convergencias=self._extract_section(raw, "CONVERGENCIAS"),
            divergencias=self._extract_section(raw, "DIVERGENCIAS"),
            lacunas=self._extract_section(raw, "LACUNAS"),
            recomendacoes=self._extract_section(raw, "RECOMENDACOES"),
            referencias_apa=refs,
            raw=raw,
        )

    async def recommend_results(self, instruction: str, articles: List[LLMArticleInput], language: str) -> LLMRecommendResultsResponse:
        condensed = []
        for article in articles:
            condensed.append({
                "local_id": article.local_id,
                "title": article.title,
                "authors": article.authors,
                "year": article.year,
                "journal": article.journal,
                "doi": article.doi,
                "abstract": (article.abstract or "")[:800],
                "methodology": article.methodology,
            })

        prompt = f"""
You are ranking articles by user intent. Language: {language}.
Instruction: {instruction}

Articles (JSON):
{json.dumps(condensed, ensure_ascii=False)}

Return STRICT JSON only with this shape:
{{
  "summary": "short explanation in {language}",
  "recommendations": [
    {{"local_id": 1, "reason": "why this matches"}},
    {{"local_id": 3, "reason": "why this matches"}}
  ],
  "suggested_filters": {{
    "year_min": 2018,
    "year_max": 2026,
    "open_access_only": false,
    "types": ["Revisao", "Artigo"],
    "journal_contains": "",
    "author_contains": ""
  }}
}}
Rules:
- Use only local_id values that exist in input.
- Return 1 to 8 recommendations.
- Keep reasons objective and concise.
""".strip()

        raw = await self._complete(prompt)
        parsed = self._extract_json(raw)

        valid_ids = {item.local_id for item in articles if item.local_id is not None}
        recommendations = []
        for rec in parsed.get("recommendations", []):
            local_id = rec.get("local_id")
            if isinstance(local_id, int) and local_id in valid_ids:
                recommendations.append(
                    LLMRecommendedArticle(local_id=local_id, reason=str(rec.get("reason", "")).strip() or "Aderente ao pedido.")
                )

        return LLMRecommendResultsResponse(
            recommendations=recommendations,
            summary=str(parsed.get("summary", "")).strip(),
            suggested_filters=parsed.get("suggested_filters", {}) if isinstance(parsed.get("suggested_filters"), dict) else {},
            raw=raw,
        )

    def _extract_section(self, text: str, name: str) -> str:
        pattern = rf"(?:^|\n)\s*\**{re.escape(name)}\**\s*:\s*(.*?)(?=(?:\n\s*\**[A-Z_]+\**\s*:)|\Z)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def _extract_json(self, text: str) -> dict:
        try:
            return json.loads(text)
        except Exception:
            pass

        first = text.find("{")
        last = text.rfind("}")
        if first != -1 and last != -1 and last > first:
            candidate = text[first : last + 1]
            try:
                return json.loads(candidate)
            except Exception:
                return {}
        return {}
