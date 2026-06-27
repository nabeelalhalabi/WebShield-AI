from app.domain.entities.moderation_result import ContentDecision, ModuleSignal
from app.domain.entities.user_preferences import UserPreferences
from app.domain.services.policy_engine import PolicyEngine
from app.domain.value_objects.action_type import ActionType
from app.domain.value_objects.risk_label import RiskLabel


def test_policy_engine_uses_category_action():
    engine = PolicyEngine()
    preferences = UserPreferences(
        thresholds={"toxicity": 0.2},
        category_actions={"toxicity": "warn"},
    )
    decision = ContentDecision(
        item_id="1",
        content_kind="text",
        module_results=[
            ModuleSignal(
                category="toxicity",
                label="toxic",
                confidence=0.9,
                risk_level=RiskLabel.HIGH,
            )
        ],
    )

    result = engine.apply([decision], preferences)
    assert result[0].action == ActionType.WARN
    assert result[0].primary_category == "toxicity"
