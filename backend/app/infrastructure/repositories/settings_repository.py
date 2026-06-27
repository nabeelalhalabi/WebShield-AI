from __future__ import annotations

import json
from pathlib import Path

from app.domain.entities.user_preferences import UserPreferences
from app.infrastructure.repositories.base import SettingsRepositoryBase
from app.infrastructure.storage.local_json_store import LocalJsonStore


class SettingsRepository(SettingsRepositoryBase):
    def __init__(self, defaults_path: Path, target_path: Path) -> None:
        self.defaults_path = defaults_path
        self.store = LocalJsonStore(target_path, default_factory=self._load_defaults)

    def _load_defaults(self) -> dict:
        return json.loads(self.defaults_path.read_text(encoding="utf-8"))

    def get(self) -> UserPreferences:
        payload = self.store.read()
        return UserPreferences.model_validate(payload)

    def save(self, preferences: UserPreferences) -> UserPreferences:
        self.store.write(preferences.model_dump(mode="json"))
        return preferences
