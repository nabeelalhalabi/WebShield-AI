from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable


class LocalJsonStore:
    def __init__(self, path: Path, default_factory: Callable[[], Any] | None = None) -> None:
        self.path = Path(path)
        self.default_factory = default_factory or (lambda: {})

    def read(self) -> Any:
        if not self.path.exists():
            return self.default_factory()
        return json.loads(self.path.read_text(encoding="utf-8"))

    def write(self, value: Any) -> Any:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(value, indent=2), encoding="utf-8")
        return value
