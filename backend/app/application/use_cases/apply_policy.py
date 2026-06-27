from app.application.dto.decision_requests import ApplyPolicyInput
from app.domain.services.policy_engine import PolicyEngine


def apply_policy(input_data: ApplyPolicyInput, engine: PolicyEngine):
    return engine.apply(input_data.decisions, input_data.preferences)
