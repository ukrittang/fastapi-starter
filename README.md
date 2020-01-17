# FastAPI Starter

This git is just for my study on the full stack example of https://github.com/tiangolo/full-stack-fastapi-postgresql.

```bash
celery worker -A app.worker -l info -Q main-queue -c 1
# Run in separated window
```

```bash
pipenv shell
pipenv install
alembic upgrade head
uvicorn app.main:app --reload
```
