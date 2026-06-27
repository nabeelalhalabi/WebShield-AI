from app.domain.value_objects.action_type import ActionType


ESCALATION_ORDER = {
    ActionType.ALLOW: ActionType.WARN,
    ActionType.WARN: ActionType.BLUR,
    ActionType.BLUR: ActionType.HIDE,
    ActionType.HIDE: ActionType.HIDE,
    ActionType.REPLACE: ActionType.HIDE,
    ActionType.BLOCK: ActionType.BLOCK,
}


def escalate_action(action: ActionType) -> ActionType:
    return ESCALATION_ORDER[action]
