# Smart Food — Backend

FastAPI service.

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Layout

- `app/main.py` — app entrypoint
- `app/models/` — ORM / data models
- `app/schemas/` — Pydantic request & response schemas
- `app/services/` — business logic
- `app/routes/` — API endpoints
- `app/data/` — static data / seed files
- `app/utils/` — helpers
