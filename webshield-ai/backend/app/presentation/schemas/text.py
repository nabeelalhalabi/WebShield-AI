from typing import Any

from pydantic import BaseModel, Field

from app.domain.entities.user_preferences import UserPreferences
from app.domain.entities.moderation_result import ContentDecision


class TextItemInput(BaseModel):
    item_id: str
    text: str
    tag_name: str | None = None
    page_url: str | None = None
    meta: dict[str, Any] = Field(default_factory=dict)


class TextModerationRequest(BaseModel):
    items: list[TextItemInput] = Field(default_factory=list)
    preferences: UserPreferences


class TextModerationResponse(BaseModel):
    results: list[ContentDecision] = Field(default_factory=list)
