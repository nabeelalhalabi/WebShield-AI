from typing import Any, Optional

from pydantic import BaseModel, Field

from app.common.enums import ContentKind


class BoundingBox(BaseModel):
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0


class ContentItem(BaseModel):
    item_id: str
    kind: ContentKind
    page_url: str | None = None
    text: str | None = None
    source_url: str | None = None
    alt_text: str | None = None
    tag_name: str | None = None
    role: str | None = None
    class_name: str | None = None
    visible: bool = True
    bounding_box: BoundingBox | None = None
    meta: dict[str, Any] = Field(default_factory=dict)
