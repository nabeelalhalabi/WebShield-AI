from __future__ import annotations

import requests

from app.config.settings import Settings


class LLMClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @property
    def is_enabled(self) -> bool:
        return (
            self.settings.enable_remote_llm
            and bool(self.settings.llm_api_base)
            and bool(self.settings.llm_api_key)
            and bool(self.settings.llm_model_name)
        )

    def complete(self, prompt: str) -> str | None:
        if not self.is_enabled:
            return None

        try:
            response = requests.post(
                self.settings.llm_api_base.rstrip("/") + "/chat/completions",
                timeout=self.settings.request_timeout_seconds,
                headers={
                    "Authorization": f"Bearer {self.settings.llm_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.settings.llm_model_name,
                    "messages": [
                        {"role": "system", "content": "You are a concise content moderation explainer."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.2,
                },
            )
            response.raise_for_status()
            payload = response.json()
            choices = payload.get("choices", [])
            if not choices:
                return None
            return choices[0]["message"]["content"].strip()
        except Exception:
            return None
