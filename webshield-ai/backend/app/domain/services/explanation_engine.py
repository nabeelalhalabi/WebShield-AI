from collections import Counter

from app.domain.entities.moderation_result import ContentDecision
from app.domain.entities.page_analysis import PreferenceMatch
from app.infrastructure.model_providers.explanation_provider import ExplanationProvider


class ExplanationEngine:
    def __init__(self, provider: ExplanationProvider) -> None:
        self.provider = provider

    def build(
        self,
        *,
        title: str,
        url: str,
        safety_score: int,
        decisions: list[ContentDecision],
        preference_match: PreferenceMatch,
    ) -> str:
        category_counts = Counter(
            decision.primary_category for decision in decisions if decision.primary_category
        )
        return self.provider.generate(
            title=title,
            url=url,
            safety_score=safety_score,
            category_counts=dict(category_counts),
            preference_score=preference_match.score,
            top_interests=preference_match.top_interests,
            decisions=decisions,
        )
