from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.page_analysis import PageSummary
from app.domain.entities.user_preferences import UserPreferences


class SettingsRepositoryBase(ABC):
    @abstractmethod
    def get(self) -> UserPreferences:
        raise NotImplementedError

    @abstractmethod
    def save(self, preferences: UserPreferences) -> UserPreferences:
        raise NotImplementedError


class HistoryRepositoryBase(ABC):
    @abstractmethod
    def add(self, summary: PageSummary) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self, limit: int = 50) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError
