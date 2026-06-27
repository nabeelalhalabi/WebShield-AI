from app.common.utils.text_cleaning import normalize_text


def clean_block_text(text: str) -> str:
    return normalize_text(text).replace("\u200b", "")


def dedupe_texts(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        cleaned = clean_block_text(value)
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            output.append(cleaned)
    return output
