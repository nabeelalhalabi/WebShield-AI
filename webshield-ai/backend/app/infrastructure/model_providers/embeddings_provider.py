from __future__ import annotations

import math
from collections import Counter

from app.common.utils.text_cleaning import normalize_text
from app.config.settings import Settings
from app.infrastructure.model_providers.base import BaseProvider


class EmbeddingsProvider(BaseProvider):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings, settings.embeddings_model)
        self._model = None

    def _load(self) -> None:
        if self._model is not None:
            return
        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
            self._mark_ready()
        except Exception as exc:  # pragma: no cover
            self._model = None
            self._mark_fallback(exc)

    @staticmethod
    def _fallback_vector(text: str) -> Counter[str]:
        cleaned = normalize_text(text).lower()
        return Counter(cleaned.split())

    @staticmethod
    def _cosine_counts(left: Counter[str], right: Counter[str]) -> float:
        if not left or not right:
            return 0.0
        shared = set(left) & set(right)
        numerator = sum(left[token] * right[token] for token in shared)
        left_norm = math.sqrt(sum(value * value for value in left.values()))
        right_norm = math.sqrt(sum(value * value for value in right.values()))
        if not left_norm or not right_norm:
            return 0.0
        return numerator / (left_norm * right_norm)

    def compare(self, source: str, candidate: str) -> float:
        self._load()
        if self._model is None:
            return self._cosine_counts(self._fallback_vector(source), self._fallback_vector(candidate))

        try:
            source_vec = self._model.encode(source, normalize_embeddings=True)
            candidate_vec = self._model.encode(candidate, normalize_embeddings=True)
            return float(source_vec @ candidate_vec)
        except Exception as exc:  # pragma: no cover
            self._mark_fallback(exc)
            return self._cosine_counts(self._fallback_vector(source), self._fallback_vector(candidate))

    def compare_many(self, source: str, candidates: list[str]) -> dict[str, float]:
        return {candidate: max(0.0, self.compare(source, candidate)) for candidate in candidates}

    def health(self) -> dict[str, str]:
        self._load()
        return {"provider": "embeddings", "model_name": self.model_name, "status": self.status.value}
