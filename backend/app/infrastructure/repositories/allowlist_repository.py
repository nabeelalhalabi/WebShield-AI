from __future__ import annotations

from pathlib import Path

from app.infrastructure.storage.local_json_store import LocalJsonStore


class AllowlistRepository:
    def __init__(self, path: Path) -> None:
        self.store = LocalJsonStore(path, default_factory=lambda: {"allowlist": [], "blocklist": []})

    def get_rules(self) -> dict[str, list[str]]:
        payload = self.store.read()
        return {
            "allowlist": payload.get("allowlist", []),
            "blocklist": payload.get("blocklist", []),
        }

    def save_rules(self, *, allowlist: list[str], blocklist: list[str]) -> dict[str, list[str]]:
        payload = {"allowlist": allowlist, "blocklist": blocklist}
        self.store.write(payload)
        return payload
