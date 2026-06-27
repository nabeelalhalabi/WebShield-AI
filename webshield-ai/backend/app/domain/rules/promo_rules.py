import json
import re
from pathlib import Path

from app.common.utils.text_cleaning import normalize_text, repeated_character_ratio, uppercase_ratio


class PromoRules:
    def __init__(self, path: Path) -> None:
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.keywords = payload.get("keywords", [])
        self.patterns = [re.compile(pattern, re.IGNORECASE) for pattern in payload.get("regex_patterns", [])]

    def evaluate(self, text: str) -> tuple[float, list[str]]:
        cleaned = normalize_text(text)
        lowered = cleaned.lower()
        hits: list[str] = []
        score = 0.0

        for keyword in self.keywords:
            if keyword.lower() in lowered:
                hits.append(keyword)
                score += 0.12

        for pattern in self.patterns:
            if pattern.search(cleaned):
                hits.append(pattern.pattern)
                score += 0.18

        score += min(uppercase_ratio(cleaned) * 0.35, 0.2)
        score += min(repeated_character_ratio(cleaned) * 0.5, 0.2)

        exclamations = cleaned.count("!")
        if exclamations >= 3:
            score += 0.12
            hits.append("excessive_exclamation")

        if any(token in lowered for token in ["free", "won", "winner", "claim now", "urgent", "limited time"]):
            score += 0.15

        return min(score, 1.0), sorted(set(hits))
