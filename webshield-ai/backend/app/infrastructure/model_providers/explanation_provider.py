from __future__ import annotations

from app.domain.entities.moderation_result import ContentDecision
from app.infrastructure.external.llm_client import LLMClient


class ExplanationProvider:
    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm_client = llm_client

    def generate(
        self,
        *,
        title: str,
        url: str,
        safety_score: int,
        category_counts: dict[str, int],
        preference_score: float,
        top_interests: list[str],
        decisions: list[ContentDecision],
    ) -> str:
        if self.llm_client and self.llm_client.is_enabled:
            prompt = self._build_prompt(
                title=title,
                url=url,
                safety_score=safety_score,
                category_counts=category_counts,
                preference_score=preference_score,
                top_interests=top_interests,
            )
            response = self.llm_client.complete(prompt)
            if response:
                return response

        if not category_counts:
            explanation = f'The page "{title}" looks mostly safe based on the enabled detectors.'
        else:
            parts = [f"{count} {category.replace('_', ' ')} item(s)" for category, count in category_counts.items()]
            explanation = (
                f'The page "{title}" triggered ' + ", ".join(parts) +
                f". Its safety score is {safety_score}/100."
            )
        if top_interests:
            explanation += f" It is most related to: {', '.join(top_interests)}."
        if preference_score:
            explanation += f" Preference match score: {preference_score:.1f}%."
        return explanation

    @staticmethod
    def _build_prompt(
        *,
        title: str,
        url: str,
        safety_score: int,
        category_counts: dict[str, int],
        preference_score: float,
        top_interests: list[str],
    ) -> str:
        return (
            f"Explain a browsing safety analysis in 3 sentences. "
            f"Title: {title}. URL: {url}. Safety score: {safety_score}. "
            f"Category counts: {category_counts}. Preference score: {preference_score}. "
            f"Top interests: {top_interests}."
        )
