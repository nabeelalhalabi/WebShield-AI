from pydantic import BaseModel, Field

from app.domain.entities.content_item import ContentItem
from app.domain.entities.user_preferences import UserPreferences


class AnalyzeTextBlocksInput(BaseModel):
    items: list[ContentItem] = Field(default_factory=list)
    preferences: UserPreferences


class AnalyzeImagesInput(BaseModel):
    items: list[ContentItem] = Field(default_factory=list)
    preferences: UserPreferences


class AnalyzePromotionsInput(BaseModel):
    items: list[ContentItem] = Field(default_factory=list)
    preferences: UserPreferences


class AnalyzePageInput(BaseModel):
    url: str
    title: str
    text_items: list[ContentItem] = Field(default_factory=list)
    image_items: list[ContentItem] = Field(default_factory=list)
    promo_items: list[ContentItem] = Field(default_factory=list)
    heading_items: list[ContentItem] = Field(default_factory=list)
    preferences: UserPreferences
