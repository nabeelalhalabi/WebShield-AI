from __future__ import annotations

from typing import Any

from PIL import Image

from app.config.settings import Settings
from app.infrastructure.model_providers.base import BaseProvider


class ViolenceProvider(BaseProvider):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings, settings.violence_model)
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
        return {
            "label": "non-violent",
            "score": 0.02,
            "scores": {"violent": 0.02, "non-violent": 0.98},
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
            violence_score = max(
                score_map.get("violent", 0.0),
                score_map.get("violence", 0.0),
                score_map.get("graphic_violence", 0.0),
            )
            return {
                "label": "violent" if violence_score >= 0.5 else "non-violent",
                "score": violence_score,
                "scores": score_map,
                "provider_status": self.status.value,
            }
        except Exception as exc:  # pragma: no cover
            self._mark_fallback(exc)
            return self._fallback(image)

    def health(self) -> dict[str, Any]:
        self._load()
        return {"provider": "violence", "model_name": self.model_name, "status": self.status.value}
