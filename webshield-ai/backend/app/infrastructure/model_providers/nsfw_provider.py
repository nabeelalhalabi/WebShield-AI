from __future__ import annotations

from typing import Any

from PIL import Image

from app.config.settings import Settings
from app.infrastructure.model_providers.base import BaseProvider


class NsfwProvider(BaseProvider):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings, settings.nsfw_model)
        self._pipeline = None

    def _load(self) -> None:
        if self._pipeline is not None:
            return
        try:
            from transformers import pipeline

            self._pipeline = pipeline("image-classification", model=self.model_name, top_k=None)
            self._mark_ready()
        except Exception as exc:  # pragma: no cover
            self._pipeline = None
            self._mark_fallback(exc)

    def _fallback(self, image: Image.Image) -> dict[str, Any]:
        width, height = image.size
        score = 0.05 + (0.05 if width < 96 or height < 96 else 0.0)
        return {
            "label": "normal",
            "score": score,
            "scores": {"normal": 1.0 - score, "nsfw": score},
            "provider_status": self.status.value,
        }

    def predict(self, image: Image.Image) -> dict[str, Any]:
        self._load()
        if self._pipeline is None:
            return self._fallback(image)
        try:
            candidates = self._pipeline(image)
            score_map: dict[str, float] = {}
            for item in candidates:
                label = str(item["label"]).lower()
                score_map[label] = float(item["score"])
            nsfw_score = max(score_map.get("nsfw", 0.0), score_map.get("porn", 0.0), score_map.get("sexy", 0.0))
            return {
                "label": "nsfw" if nsfw_score >= 0.5 else "normal",
                "score": nsfw_score,
                "scores": score_map,
                "provider_status": self.status.value,
            }
        except Exception as exc:  # pragma: no cover
            self._mark_fallback(exc)
            return self._fallback(image)

    def health(self) -> dict[str, Any]:
        self._load()
        return {"provider": "nsfw", "model_name": self.model_name, "status": self.status.value}
