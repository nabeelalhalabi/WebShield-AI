from __future__ import annotations

from typing import Any

from app.common.utils.text_cleaning import keyword_overlap_score, normalize_text
from app.config.settings import Settings
from app.infrastructure.model_providers.base import BaseProvider


class TextToxicityProvider(BaseProvider):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings, settings.text_toxicity_model)
        self._pipeline = None

    def _load(self) -> None:
        if self._pipeline is not None:
            return
        try:
            from transformers import pipeline

            self._pipeline = pipeline(
                "text-classification",
                model=self.model_name,
                top_k=None,
                truncation=True,
            )
            self._mark_ready()
        except Exception as exc:  # pragma: no cover - exercised when model unavailable
            self._pipeline = None
            self._mark_fallback(exc)

    def _fallback(self, text: str) -> dict[str, Any]:
        cleaned = normalize_text(text).lower()
        score = keyword_overlap_score(
            cleaned,
            ["idiot", "stupid", "disgusting", "trash", "hate", "moron", "shut up"],
        )
        return {
            "label": "toxic" if score >= 0.2 else "non_toxic",
            "score": min(max(score * 1.6, 0.0), 1.0),
            "scores": {"toxic": min(max(score * 1.6, 0.0), 1.0)},
            "provider_status": self.status.value,
        }

    def predict(self, text: str) -> dict[str, Any]:
        self._load()
        if self._pipeline is None:
            return self._fallback(text)

        try:
            raw = self._pipeline(text)
            candidates = raw[0] if raw and isinstance(raw[0], list) else raw
            score_map: dict[str, float] = {}
            for item in candidates:
                label = str(item["label"]).lower()
                score_map[label] = float(item["score"])
            toxic_score = max(
                score_map.get("toxic", 0.0),
                score_map.get("severe_toxic", 0.0),
                score_map.get("obscene", 0.0) * 0.5,
                score_map.get("insult", 0.0) * 0.75,
                score_map.get("threat", 0.0) * 0.9,
            )
            return {
                "label": "toxic" if toxic_score >= 0.5 else "non_toxic",
                "score": toxic_score,
                "scores": score_map,
                "provider_status": self.status.value,
            }
        except Exception as exc:  # pragma: no cover
            self._mark_fallback(exc)
            return self._fallback(text)

    def health(self) -> dict[str, Any]:
        self._load()
        return {"provider": "text_toxicity", "model_name": self.model_name, "status": self.status.value}
