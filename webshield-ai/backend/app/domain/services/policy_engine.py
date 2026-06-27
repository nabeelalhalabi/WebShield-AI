from collections import Counter

from app.domain.entities.moderation_result import ContentDecision
from app.domain.entities.policy import Policy
from app.domain.entities.user_preferences import UserPreferences
from app.domain.rules.child_safe_rules import escalate_action
from app.domain.value_objects.action_type import ActionType
from app.domain.value_objects.risk_label import RiskLabel


class PolicyEngine:
    def build_policy(self, preferences: UserPreferences) -> Policy:
        return Policy(
            category_actions=preferences.category_actions,
            thresholds=preferences.thresholds,
            child_safe_mode=preferences.child_safe_mode,
            default_action=ActionType.WARN,
        )

    def _apply_page_level_nsfw_reinforcement(
        self,
        decisions: list[ContentDecision],
        policy: Policy,
    ) -> None:
        image_decisions = [decision for decision in decisions if decision.content_kind == "image"]
        if not image_decisions:
            return

        strong_nsfw_images = 0
        for decision in image_decisions:
            for signal in decision.module_results:
                if signal.category == "nsfw" and signal.confidence >= 0.70:
                    strong_nsfw_images += 1
                    break

        # If the page clearly contains multiple strong-NSFW images,
        # also blur borderline article images with moderate NSFW scores.
        if strong_nsfw_images < 2:
            return

        reinforced_action = policy.category_actions.get("nsfw", ActionType.BLUR)
        if reinforced_action == ActionType.ALLOW:
            reinforced_action = ActionType.BLUR

        for decision in image_decisions:
            if decision.action != ActionType.ALLOW:
                continue

            nsfw_signal = next(
                (signal for signal in decision.module_results if signal.category == "nsfw"),
                None,
            )
            if nsfw_signal is None:
                continue

            if nsfw_signal.confidence >= 0.35:
                decision.action = reinforced_action
                decision.risk_level = max(decision.risk_level, nsfw_signal.risk_level)
                decision.confidence = max(decision.confidence, nsfw_signal.confidence)
                decision.primary_category = "nsfw"
                decision.categories = sorted(set([*decision.categories, "nsfw"]))
                decision.explanation = (
                    "Blurred due to page-level NSFW reinforcement: multiple strong NSFW images "
                    "were detected on this page."
                )

    def apply(self, decisions: list[ContentDecision], preferences: UserPreferences) -> list[ContentDecision]:
        policy = self.build_policy(preferences)
        enabled_map = preferences.detectors.model_dump()

        final_decisions: list[ContentDecision] = []
        for decision in decisions:
            active_signals = [
                signal
                for signal in decision.module_results
                if enabled_map.get(signal.category, True)
                and signal.confidence >= policy.thresholds.get(signal.category, 0.5)
            ]

            if not active_signals:
                decision.action = ActionType.ALLOW
                decision.risk_level = RiskLabel.SAFE
                decision.confidence = 0.0
                decision.primary_category = None
                decision.categories = []
                decision.explanation = "No enabled detector exceeded its configured threshold."
                final_decisions.append(decision)
                continue

            primary = max(active_signals, key=lambda item: (int(item.risk_level), item.confidence))
            action = policy.category_actions.get(primary.category, policy.default_action)

            if policy.child_safe_mode and primary.category in {
                "toxicity",
                "profanity",
                "hate_speech",
                "nsfw",
                "violence",
            }:
                action = escalate_action(action)

            decision.action = action
            decision.risk_level = primary.risk_level
            decision.confidence = primary.confidence
            decision.primary_category = primary.category
            decision.categories = sorted({signal.category for signal in active_signals})
            decision.explanation = primary.reason or (
                f"Flagged as {primary.category} with confidence {primary.confidence:.2f}."
            )
            final_decisions.append(decision)

        self._apply_page_level_nsfw_reinforcement(final_decisions, policy)
        return final_decisions