import json
import re
from pathlib import Path

from app.common.utils.text_cleaning import normalize_text


class ProfanityRules:
    def __init__(self, path: Path) -> None:
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.words: list[str] = [word.lower() for word in payload.get("words", [])]
        self.regexes = [re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE) for word in self.words]

    def match(self, text: str) -> list[str]:
        cleaned = normalize_text(text)
        matches: list[str] = []
        for word, regex in zip(self.words, self.regexes):
            if regex.search(cleaned):
                matches.append(word)
        return sorted(set(matches))
