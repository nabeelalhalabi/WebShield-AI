from pydantic import BaseModel, Field, field_validator


class ConfidenceScore(BaseModel):
    value: float = Field(ge=0.0, le=1.0)

    @field_validator("value")
    @classmethod
    def clamp(cls, value: float) -> float:
        return max(0.0, min(1.0, float(value)))
