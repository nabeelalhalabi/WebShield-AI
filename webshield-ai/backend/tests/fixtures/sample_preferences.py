PREFERENCES = {
    "enabled": True,
    "child_safe_mode": False,
    "scan_on_load": True,
    "history_enabled": False,
    "interests": ["cars", "technology"],
    "detectors": {
        "toxicity": True,
        "profanity": True,
        "hate_speech": True,
        "nsfw": True,
        "violence": True,
        "promotions": True,
        "preference_match": True,
        "explanations": True
    },
    "thresholds": {
        "toxicity": 0.1,
        "profanity": 0.1,
        "hate_speech": 0.1,
        "nsfw": 0.5,
        "violence": 0.5,
        "promotions": 0.1
    },
    "category_actions": {
        "toxicity": "warn",
        "profanity": "warn",
        "hate_speech": "hide",
        "nsfw": "blur",
        "violence": "blur",
        "promotions": "warn"
    },
    "allowlist": [],
    "blocklist": [],
    "max_text_items": 40,
    "max_image_items": 12,
    "max_promo_items": 12
}
