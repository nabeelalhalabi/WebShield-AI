from pathlib import Path
import json

BASE = Path(__file__).resolve().parents[1]
runtime_dir = BASE / ".runtime"
runtime_dir.mkdir(parents=True, exist_ok=True)

defaults_path = BASE / "app" / "data" / "defaults" / "default_preferences.json"
target_path = runtime_dir / "user_preferences.json"

if not target_path.exists():
    target_path.write_text(defaults_path.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Seeded {target_path}")
else:
    print(f"{target_path} already exists")
