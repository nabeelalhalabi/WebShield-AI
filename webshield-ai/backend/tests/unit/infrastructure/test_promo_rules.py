from app.config.settings import get_settings
from app.domain.rules.promo_rules import PromoRules


def test_promo_rules_detects_spammy_copy():
    rules = PromoRules(get_settings().defaults_dir / "promo_patterns.json")
    score, hits = rules.evaluate("YOU WON 100000 DOLLARS!!! CLAIM NOW!!!")
    assert score > 0.3
    assert hits
