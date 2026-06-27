from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.common.enums import PageStatus
from app.domain.entities.content_item import ContentItem
from app.domain.entities.moderation_result import ContentDecision


class PreferenceMatch(BaseModel):
    score: float = 0.0
    top_interests: list[str] = Field(default_factory=list)
    compared_text: str = ""


class PageSummary(BaseModel):
    url: str
    title: str
    status: PageStatus = PageStatus.SAFE
    safety_score: int = 100
    preference_match: PreferenceMatch = Field(default_factory=PreferenceMatch)
    flagged_items: int = 0
    explanation: str = ""
    created_at: datetime


class PageAnalysis(BaseModel):
    summary: PageSummary
    items: list[ContentItem] = Field(default_factory=list)
    decisions: list[ContentDecision] = Field(default_factory=list)
    allowlisted: bool = False
    blocklisted: bool = False
    domain: str = ""
    meta: dict[str, Any] = Field(default_factory=dict)
