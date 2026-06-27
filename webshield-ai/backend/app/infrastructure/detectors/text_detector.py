from __future__ import annotations

from app.domain.entities.content_item import ContentItem
from app.domain.entities.moderation_result import ContentDecision, ModuleSignal
from app.domain.value_objects.action_type import ActionType
from app.domain.value_objects.risk_label import RiskLabel
from app.infrastructure.detectors.profanity_detector import ProfanityDetector
from app.infrastructure.model_providers.hate_speech_provider import HateSpeechProvider
from app.infrastructure.model_providers.text_toxicity_provider import TextToxicityProvider


class TextDetector:
    def __init__(
        self,
        *,
        toxicity_provider: TextToxicityProvider,
        hate_provider: HateSpeechProvider,
        profanity_detector: ProfanityDetector,
    ) -> None:
        self.toxicity_provider = toxicity_provider
        self.hate_provider = hate_provider
        self.profanity_detector = profanity_detector

    def detect(self, item: ContentItem) -> ContentDecision:
        text = item.text or ""
        toxic = self.toxicity_provider.predict(text)
        hate = self.hate_provider.predict(text)
        profanity = self.profanity_detector.detect(text)

        signals = [
            ModuleSignal(
                category="toxicity",
                label=toxic["label"],
                confidence=float(toxic["score"]),
                risk_level=RiskLabel.from_score(float(toxic["score"])),
                reason=f'Toxicity model predicted {toxic["label"]}.',
                raw_scores=toxic.get("scores", {}),
                model_name=self.toxicity_provider.model_name,
                provider_status=toxic.get("provider_status", "ok"),
            ),
            ModuleSignal(
                category="hate_speech",
                label=hate["label"],
                confidence=float(hate["score"]),
                risk_level=RiskLabel.from_score(float(hate["score"])),
                reason=f'Hate-speech model predicted {hate["label"]}.',
                raw_scores=hate.get("scores", {}),
                model_name=self.hate_provider.model_name,
                provider_status=hate.get("provider_status", "ok"),
            ),
            profanity,
        ]

        strongest = max(signals, key=lambda signal: (int(signal.risk_level), signal.confidence))
        return ContentDecision(
            item_id=item.item_id,
            content_kind=item.kind.value,
            action=ActionType.ALLOW,
            risk_level=strongest.risk_level,
            confidence=strongest.confidence,
            explanation=strongest.reason,
            categories=[signal.category for signal in signals if signal.confidence > 0],
            primary_category=strongest.category if strongest.confidence > 0 else None,
            module_results=signals,
        )

    def analyze_items(self, items: list[ContentItem]) -> list[ContentDecision]:
        return [self.detect(item) for item in items]
