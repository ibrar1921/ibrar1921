# MLOps Model Service

A small reproducible **Iris classification** baseline with FastAPI serving, input validation, Docker and pytest. The service trains and caches a model at first access.

## Quick start
```bash
pip install -r requirements.txt
pytest -q
uvicorn api:app --reload
```

Then open `http://localhost:8000/docs` for interactive API documentation.

## Docker
```bash
docker build -t iris-service .
docker run -p 8000:8000 iris-service
```

The Iris dataset is a simple engineering benchmark; this project is not a medical model. Future MLOps work: model artifact registry, automated drift checks, CI validation and explicit model-version promotion.
