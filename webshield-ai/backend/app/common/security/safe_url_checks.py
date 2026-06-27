from urllib.parse import urlparse


SAFE_SCHEMES = {"http", "https", "data"}


def is_safe_web_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in SAFE_SCHEMES
