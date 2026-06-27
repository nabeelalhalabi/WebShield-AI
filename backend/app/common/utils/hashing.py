import hashlib


def stable_hash(value: str) -> str:
    """Return a stable SHA-256 hash for caching and element IDs."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
