from __future__ import annotations

from app.domain.entities.moderation_result import ModuleSignal
from app.domain.rules.profanity_rules import ProfanityRules
from app.domain.value_objects.risk_label import RiskLabel


class ProfanityDetector:
    def __init__(self, rules: ProfanityRules) -> None:
        self.rules = rules

    def detect(self, text: str) -> ModuleSignal:
        matches = self.rules.match(text)
        confidence = min(1.0, 0.35 + (0.15 * len(matches))) if matches else 0.0
        risk = RiskLabel.from_score(confidence)
        return ModuleSignal(
            category="profanity",
            label="profanity" if matches else "clean",
            confidence=confidence,
            risk_level=risk,
            reason=f"Matched profanity terms: {', '.join(matches)}" if matches else "No profanity terms matched.",
            matched_rules=matches,
            raw_scores={"profanity": confidence},
            model_name="rule-list",
            provider_status="ok",
        )
