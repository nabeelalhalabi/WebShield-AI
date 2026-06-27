from __future__ import annotations

from app.application.dto.moderation_requests import (
    AnalyzePageInput,
    AnalyzePromotionsInput,
    AnalyzeTextBlocksInput,
)
from app.application.use_cases.analyze_promotions import analyze_promotions
from app.application.use_cases.analyze_text_blocks import analyze_text_blocks
from app.common.enums import PageStatus
from app.common.utils.dom_normalization import dedupe_texts
from app.common.utils.time_utils import utc_now
from app.domain.entities.content_item import ContentItem
from app.domain.entities.moderation_result import ContentDecision
from app.domain.entities.page_analysis import PageAnalysis, PageSummary
from app.domain.services.explanation_engine import ExplanationEngine
from app.domain.services.policy_engine import PolicyEngine
from app.domain.services.preference_similarity_engine import PreferenceSimilarityEngine
from app.domain.services.safety_score_engine import SafetyScoreEngine
from app.domain.rules.domain_rules import extract_domain, match_domain
from app.infrastructure.detectors.image_detector import ImageDetector
from app.infrastructure.detectors.promo_detector import PromoDetector
from app.infrastructure.detectors.text_detector import TextDetector
from app.infrastructure.repositories.allowlist_repository import AllowlistRepository
from app.infrastructure.repositories.history_repository import HistoryRepository


class PageAnalysisOrchestrator:
    def __init__(
        self,
        *,
        text_detector: TextDetector,
        image_detector: ImageDetector,
        promo_detector: PromoDetector,
        policy_engine: PolicyEngine,
        safety_score_engine: SafetyScoreEngine,
        preference_engine: PreferenceSimilarityEngine,
        explanation_engine: ExplanationEngine,
        allowlist_repository: AllowlistRepository,
        history_repository: HistoryRepository,
    ) -> None:
        self.text_detector = text_detector
        self.image_detector = image_detector
        self.promo_detector = promo_detector
        self.policy_engine = policy_engine
        self.safety_score_engine = safety_score_engine
        self.preference_engine = preference_engine
        self.explanation_engine = explanation_engine
        self.allowlist_repository = allowlist_repository
        self.history_repository = history_repository

    def analyze(self, input_data: AnalyzePageInput) -> PageAnalysis:
        rules = self.allowlist_repository.get_rules()
        merged_allowlist = sorted(set(rules.get("allowlist", []) + input_data.preferences.allowlist))
        merged_blocklist = sorted(set(rules.get("blocklist", []) + input_data.preferences.blocklist))
        domain = extract_domain(input_data.url)

        allowlisted = match_domain(domain, merged_allowlist)
        blocklisted = match_domain(domain, merged_blocklist)

        decisions: list[ContentDecision] = []
        items: list[ContentItem] = []

        text_items = [*input_data.text_items, *input_data.heading_items]
        image_items = input_data.image_items
        promo_items = input_data.promo_items

        if input_data.preferences.enabled and not allowlisted:
            decisions.extend(
                analyze_text_blocks(
                    AnalyzeTextBlocksInput(items=text_items, preferences=input_data.preferences),
                    self.text_detector,
                ).decisions
            )

            # Use raw image detector results here.
            # Page-level policy is applied once later to all decisions together.
            decisions.extend(self.image_detector.analyze_items(image_items))

            decisions.extend(
                analyze_promotions(
                    AnalyzePromotionsInput(items=promo_items, preferences=input_data.preferences),
                    self.promo_detector,
                ).decisions
            )

        items.extend(text_items)
        items.extend(image_items)
        items.extend(promo_items)

        final_decisions = self.policy_engine.apply(decisions, input_data.preferences)

        analysis_text = " ".join(
            dedupe_texts(
                [input_data.title]
                + [item.text or "" for item in input_data.heading_items]
                + [item.text or "" for item in input_data.text_items[:15]]
            )
        )

        preference_match = self.preference_engine.match(
            input_data.preferences.interests if input_data.preferences.detectors.preference_match else [],
            analysis_text,
        )

        safety_score, status = self.safety_score_engine.score(final_decisions, blocklisted=blocklisted)
        if allowlisted:
            status = PageStatus.SAFE
            safety_score = 100

        summary = PageSummary(
            url=input_data.url,
            title=input_data.title or input_data.url,
            status=status,
            safety_score=safety_score,
            preference_match=preference_match,
            flagged_items=sum(1 for decision in final_decisions if decision.action.value != "allow"),
            explanation="",
            created_at=utc_now(),
        )

        summary.explanation = self.explanation_engine.build(
            title=summary.title,
            url=summary.url,
            safety_score=summary.safety_score,
            decisions=final_decisions,
            preference_match=preference_match,
        )

        analysis = PageAnalysis(
            summary=summary,
            items=items,
            decisions=final_decisions,
            allowlisted=allowlisted,
            blocklisted=blocklisted,
            domain=domain,
            meta={"allowlist": merged_allowlist, "blocklist": merged_blocklist},
        )

        if input_data.preferences.history_enabled:
            self.history_repository.add(summary)

        return analysis