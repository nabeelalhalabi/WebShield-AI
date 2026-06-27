from __future__ import annotations

from app.domain.entities.content_item import ContentItem
from app.domain.entities.moderation_result import ContentDecision, ModuleSignal
from app.domain.value_objects.action_type import ActionType
from app.domain.value_objects.risk_label import RiskLabel
from app.infrastructure.external.image_downloader import ImageDownloader
from app.infrastructure.model_providers.nsfw_provider import NsfwProvider
from app.infrastructure.model_providers.violence_provider import ViolenceProvider


class ImageDetector:
    def __init__(
        self,
        *,
        downloader: ImageDownloader,
        nsfw_provider: NsfwProvider,
        violence_provider: ViolenceProvider,
    ) -> None:
        self.downloader = downloader
        self.nsfw_provider = nsfw_provider
        self.violence_provider = violence_provider

    def detect(self, item: ContentItem) -> ContentDecision:
        if not item.source_url:
            unavailable = ModuleSignal(
                category="nsfw",
                label="unavailable",
                confidence=0.0,
                risk_level=RiskLabel.SAFE,
                reason="Image item had no source URL.",
                provider_status="error",
                raw_scores={},
            )
            return ContentDecision(
                item_id=item.item_id,
                content_kind=item.kind.value,
                action=ActionType.ALLOW,
                explanation=unavailable.reason,
                categories=[],
                primary_category=None,
                confidence=0.0,
                risk_level=RiskLabel.SAFE,
                module_results=[unavailable],
                meta={"source_url": item.source_url or "", "download_status": "missing_url"},
            )

        try:
            image = self.downloader.fetch(item.source_url)
            nsfw = self.nsfw_provider.predict(image)
            violence = self.violence_provider.predict(image)

            signals = [
                ModuleSignal(
                    category="nsfw",
                    label=nsfw["label"],
                    confidence=float(nsfw["score"]),
                    risk_level=RiskLabel.from_score(float(nsfw["score"])),
                    reason=f'NSFW model predicted {nsfw["label"]}.',
                    raw_scores=nsfw.get("scores", {}),
                    model_name=self.nsfw_provider.model_name,
                    provider_status=nsfw.get("provider_status", "ok"),
                ),
                ModuleSignal(
                    category="violence",
                    label=violence["label"],
                    confidence=float(violence["score"]),
                    risk_level=RiskLabel.from_score(float(violence["score"])),
                    reason=f'Violence model predicted {violence["label"]}.',
                    raw_scores=violence.get("scores", {}),
                    model_name=self.violence_provider.model_name,
                    provider_status=violence.get("provider_status", "ok"),
                ),
            ]

            download_status = "ok"
        except Exception as exc:
            signals = [
                ModuleSignal(
                    category="nsfw",
                    label="unavailable",
                    confidence=0.0,
                    risk_level=RiskLabel.SAFE,
                    reason=f"Image download failed: {exc}",
                    provider_status="error",
                    raw_scores={},
                )
            ]
            download_status = "failed"

        strongest = max(signals, key=lambda signal: (int(signal.risk_level), signal.confidence))
        nsfw_signal = next((signal for signal in signals if signal.category == "nsfw"), None)
        violence_signal = next((signal for signal in signals if signal.category == "violence"), None)

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
            meta={
                "source_url": item.source_url,
                "download_status": download_status,
                "nsfw_score": nsfw_signal.confidence if nsfw_signal else 0.0,
                "nsfw_label": nsfw_signal.label if nsfw_signal else "unknown",
                "violence_score": violence_signal.confidence if violence_signal else 0.0,
                "violence_label": violence_signal.label if violence_signal else "unknown",
            },
        )

    def analyze_items(self, items: list[ContentItem]) -> list[ContentDecision]:
        return [self.detect(item) for item in items]