# WebShield backend

FastAPI backend for page analysis, policy evaluation, history persistence, and explanation generation.

## Main commands

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
pytest -q
```
