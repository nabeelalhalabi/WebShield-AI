from urllib.parse import urlparse


def extract_domain(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc.lower().lstrip("www.")


def match_domain(domain: str, patterns: list[str]) -> bool:
    domain = domain.lower()
    for pattern in patterns:
        normalized = pattern.lower().strip()
        if not normalized:
            continue
        if domain == normalized or domain.endswith("." + normalized):
            return True
    return False
