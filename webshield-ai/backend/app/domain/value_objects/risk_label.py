from enum import IntEnum


class RiskLabel(IntEnum):
    SAFE = 0
    LOW = 1
    MODERATE = 2
    HIGH = 3
    CRITICAL = 4

    @classmethod
    def from_score(cls, score: float) -> "RiskLabel":
        if score >= 0.9:
            return cls.CRITICAL
        if score >= 0.75:
            return cls.HIGH
        if score >= 0.5:
            return cls.MODERATE
        if score >= 0.25:
            return cls.LOW
        return cls.SAFE
