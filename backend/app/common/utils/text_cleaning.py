import re
from collections import Counter


WHITESPACE_RE = re.compile(r"\s+")
REPEATED_CHAR_RE = re.compile(r"(.)\1{3,}")


def normalize_text(text: str) -> str:
    return WHITESPACE_RE.sub(" ", (text or "").strip())


def uppercase_ratio(text: str) -> float:
    letters = [char for char in text if char.isalpha()]
    if not letters:
        return 0.0
    upper = [char for char in letters if char.isupper()]
    return len(upper) / len(letters)


def repeated_character_ratio(text: str) -> float:
    if not text:
        return 0.0
    repeated = sum(len(match.group(0)) for match in REPEATED_CHAR_RE.finditer(text))
    return repeated / max(len(text), 1)


def keyword_overlap_score(text: str, keywords: list[str]) -> float:
    cleaned = normalize_text(text).lower()
    tokens = cleaned.split()
    if not tokens or not keywords:
        return 0.0
    token_counts = Counter(tokens)
    hits = 0
    for keyword in keywords:
        key = keyword.lower().strip()
        if not key:
            continue
        if " " in key and key in cleaned:
            hits += 1
        elif token_counts[key] > 0:
            hits += 1
    return hits / max(len(keywords), 1)


def truncate_text(text: str, max_length: int = 280) -> str:
    text = normalize_text(text)
    if len(text) <= max_length:
        return text
    return text[: max_length - 1].rstrip() + "…"
