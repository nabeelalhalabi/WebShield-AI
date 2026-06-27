import json
from pathlib import Path

from app.common.enums import PageStatus
from app.domain.entities.moderation_result import ContentDecision
from app.domain.entities.page_analysis import PageSummary
from app.domain.value_objects.action_type import ActionType
from app.domain.value_objects.risk_label import RiskLabel


class SafetyScoreEngine:
    def __init__(self, weights_path: Path) -> None:
        payload = json.loads(weights_path.read_text(encoding="utf-8"))
        self.weights: dict[str, float] = payload.get("weights", {})

    @staticmethod
    def _severity_factor(risk_level: RiskLabel) -> float:
        return {
            RiskLabel.SAFE: 0.0,
            RiskLabel.LOW: 0.2,
            RiskLabel.MODERATE: 0.45,
            RiskLabel.HIGH: 0.75,
            RiskLabel.CRITICAL: 1.0,
        }[risk_level]

    def score(self, decisions: list[ContentDecision], *, blocklisted: bool = False) -> tuple[int, PageStatus]:
        if blocklisted:
            return 0, PageStatus.BLOCKED

        score = 100.0
        blocked = 0
        warned = 0

        for decision in decisions:
            if decision.action == ActionType.ALLOW:
                continue
            if decision.action == ActionType.BLOCK:
                blocked += 1
            if decision.action in {ActionType.WARN, ActionType.BLUR, ActionType.HIDE, ActionType.REPLACE}:
                warned += 1
            weight = self.weights.get(decision.primary_category or "default", 10.0)
            score -= weight * self._severity_factor(decision.risk_level) * max(decision.confidence, 0.4)

        score = max(0.0, min(100.0, score))
        if blocked > 0 or score < 25:
            status = PageStatus.BLOCKED
        elif score < 50:
            status = PageStatus.RESTRICTED
        elif warned > 0 or score < 80:
            status = PageStatus.WARNING
        else:
            status = PageStatus.SAFE
        return int(round(score)), status
