from cachetools import TTLCache


class ResultCache:
    def __init__(self, ttl_seconds: int = 600, maxsize: int = 512) -> None:
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl_seconds)

    def get(self, key: str):
        return self.cache.get(key)

    def set(self, key: str, value) -> None:
        self.cache[key] = value
