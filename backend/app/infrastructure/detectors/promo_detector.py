from __future__ import annotations

from app.domain.entities.content_item import ContentItem
from app.domain.entities.moderation_result import ContentDecision, ModuleSignal
from app.domain.rules.promo_rules import PromoRules
from app.domain.value_objects.action_type import ActionType
from app.domain.value_objects.risk_label import RiskLabel


class PromoDetector:
    def __init__(self, rules: PromoRules) -> None:
        self.rules = rules

    def detect(self, item: ContentItem) -> ContentDecision:
        score, hits = self.rules.evaluate(item.text or "")
        signal = ModuleSignal(
            category="promotions",
            label="suspicious" if score >= 0.4 else "normal",
            confidence=score,
            risk_level=RiskLabel.from_score(score),
            reason="Matched suspicious promotional patterns." if hits else "No suspicious promotional pattern matched.",
            matched_rules=hits,
            raw_scores={"promotions": score},
            model_name="rule-assisted",
        )
        return ContentDecision(
            item_id=item.item_id,
            content_kind=item.kind.value,
            action=ActionType.ALLOW,
            risk_level=signal.risk_level,
            confidence=signal.confidence,
            explanation=signal.reason,
            categories=["promotions"] if score > 0 else [],
            primary_category="promotions" if score > 0 else None,
            module_results=[signal],
        )

    def analyze_items(self, items: list[ContentItem]) -> list[ContentDecision]:
        return [self.detect(item) for item in items]
