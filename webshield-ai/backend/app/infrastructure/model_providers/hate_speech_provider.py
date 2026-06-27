from __future__ import annotations

from typing import Any

from app.common.utils.text_cleaning import keyword_overlap_score, normalize_text
from app.config.settings import Settings
from app.infrastructure.model_providers.base import BaseProvider


class HateSpeechProvider(BaseProvider):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings, settings.hate_speech_model)
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
        except Exception as exc:  # pragma: no cover
            self._pipeline = None
            self._mark_fallback(exc)

    def _fallback(self, text: str) -> dict[str, Any]:
        cleaned = normalize_text(text).lower()
        score = keyword_overlap_score(
            cleaned,
            ["go back", "subhuman", "dirty", "vermin", "kill them", "race traitor"],
        )
        return {
            "label": "hate" if score >= 0.2 else "nothate",
            "score": min(max(score * 1.75, 0.0), 1.0),
            "scores": {"hate": min(max(score * 1.75, 0.0), 1.0)},
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
            hate_score = 0.0
            for label, score in score_map.items():
                if "hate" in label and "not" not in label and "non" not in label:
                    hate_score = max(hate_score, score)
            return {
                "label": "hate" if hate_score >= 0.5 else "nothate",
                "score": hate_score,
                "scores": score_map,
                "provider_status": self.status.value,
            }
        except Exception as exc:  # pragma: no cover
            self._mark_fallback(exc)
            return self._fallback(text)

    def health(self) -> dict[str, Any]:
        self._load()
        return {"provider": "hate_speech", "model_name": self.model_name, "status": self.status.value}
