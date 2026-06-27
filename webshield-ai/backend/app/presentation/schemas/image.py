from typing import Any

from pydantic import BaseModel, Field

from app.domain.entities.user_preferences import UserPreferences
from app.domain.entities.moderation_result import ContentDecision


class ImageItemInput(BaseModel):
    item_id: str
    src: str
    alt_text: str | None = None
    tag_name: str | None = None
    page_url: str | None = None
    width: int = 0
    height: int = 0
    meta: dict[str, Any] = Field(default_factory=dict)


class ImageModerationRequest(BaseModel):
    items: list[ImageItemInput] = Field(default_factory=list)
    preferences: UserPreferences


class ImageModerationResponse(BaseModel):
    results: list[ContentDecision] = Field(default_factory=list)
