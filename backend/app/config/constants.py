from app.domain.value_objects.action_type import ActionType

APP_DESCRIPTION = "WebShield AI moderation API"

SUPPORTED_CATEGORIES = [
    "toxicity",
    "profanity",
    "hate_speech",
    "nsfw",
    "violence",
    "promotions",
]

DEFAULT_THRESHOLDS = {
    "toxicity": 0.60,
    "profanity": 0.50,
    "hate_speech": 0.60,
    "nsfw": 0.60,
    "violence": 0.55,
    "promotions": 0.55,
}

DEFAULT_CATEGORY_ACTIONS = {
    "toxicity": ActionType.WARN.value,
    "profanity": ActionType.WARN.value,
    "hate_speech": ActionType.HIDE.value,
    "nsfw": ActionType.BLUR.value,
    "violence": ActionType.BLUR.value,
    "promotions": ActionType.WARN.value,
}
