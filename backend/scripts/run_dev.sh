#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="${PYTHONPATH:-}:$(pwd)"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
