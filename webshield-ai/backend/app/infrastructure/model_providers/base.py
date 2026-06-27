from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

from app.common.enums import ProviderStatus
from app.config.settings import Settings


class BaseProvider(ABC):
    def __init__(self, settings: Settings, model_name: str) -> None:
        self.settings = settings
        self.model_name = model_name
        self.logger = logging.getLogger(self.__class__.__name__)
        self._loaded = False
        self._status = ProviderStatus.FALLBACK
        self._error: str | None = None

    @property
    def status(self) -> ProviderStatus:
        return self._status

    @property
    def last_error(self) -> str | None:
        return self._error

    def _mark_ready(self) -> None:
        self._loaded = True
        self._status = ProviderStatus.READY
        self._error = None

    def _mark_fallback(self, error: Exception | str) -> None:
        self._loaded = False
        self._status = ProviderStatus.FALLBACK
        self._error = str(error)
        self.logger.warning("%s using fallback mode: %s", self.__class__.__name__, error)

    @abstractmethod
    def health(self) -> dict[str, Any]:
        raise NotImplementedError
