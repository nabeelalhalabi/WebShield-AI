from typing import Any

from pydantic import BaseModel, Field

from app.domain.entities.page_analysis import PageAnalysis
from app.domain.entities.user_preferences import UserPreferences


class PromoItemInput(BaseModel):
    item_id: str
    text: str
    tag_name: str | None = None
    role: str | None = None
    class_name: str | None = None
    page_url: str | None = None
    meta: dict[str, Any] = Field(default_factory=dict)


class HeadingItemInput(BaseModel):
    item_id: str
    text: str
    level: int = 1
    page_url: str | None = None
    meta: dict[str, Any] = Field(default_factory=dict)


class PageAnalysisRequest(BaseModel):
    url: str
    title: str
    text_items: list[dict] = Field(default_factory=list)
    image_items: list[dict] = Field(default_factory=list)
    promo_items: list[dict] = Field(default_factory=list)
    headings: list[dict] = Field(default_factory=list)
    preferences: UserPreferences | None = None


class PageAnalysisResponse(BaseModel):
    analysis: PageAnalysis
