from enum import Enum


class ContentKind(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    PROMOTION = "promotion"
    HEADING = "heading"


class PageStatus(str, Enum):
    SAFE = "safe"
    WARNING = "warning"
    RESTRICTED = "restricted"
    BLOCKED = "blocked"


class ProviderStatus(str, Enum):
    READY = "ready"
    FALLBACK = "fallback"
    ERROR = "error"
