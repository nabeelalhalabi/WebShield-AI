from app.domain.entities.page_analysis import PreferenceMatch
from app.infrastructure.model_providers.embeddings_provider import EmbeddingsProvider


class PreferenceSimilarityEngine:
    def __init__(self, provider: EmbeddingsProvider) -> None:
        self.provider = provider

    def match(self, interests: list[str], text: str) -> PreferenceMatch:
        cleaned_interests = [item.strip() for item in interests if item.strip()]
        if not cleaned_interests or not text.strip():
            return PreferenceMatch(score=0.0, top_interests=[], compared_text=text[:500])

        score_map = self.provider.compare_many(text, cleaned_interests)
        ordered = sorted(score_map.items(), key=lambda pair: pair[1], reverse=True)
        top = ordered[:3]
        if not top:
            return PreferenceMatch(score=0.0, top_interests=[], compared_text=text[:500])

        top_score = max(value for _, value in top)
        top_interests = [interest for interest, value in top if value >= max(top_score - 0.1, 0.15)]
        return PreferenceMatch(score=round(top_score * 100, 2), top_interests=top_interests, compared_text=text[:500])
