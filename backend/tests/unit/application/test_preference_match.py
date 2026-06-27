from app.config.settings import get_settings
from app.domain.services.preference_similarity_engine import PreferenceSimilarityEngine
from app.infrastructure.model_providers.embeddings_provider import EmbeddingsProvider


def test_preference_match_returns_score(monkeypatch):
    provider = EmbeddingsProvider(get_settings())
    monkeypatch.setattr(provider, "_load", lambda: provider._mark_fallback("forced"))
    provider._model = None
    engine = PreferenceSimilarityEngine(provider)

    result = engine.match(["cars", "science"], "This article discusses electric cars and engines.")
    assert result.score >= 0
    assert isinstance(result.top_interests, list)
