# Homework 5 — Deploying Machine Learning Models

A reproducible solution for [ML Zoomcamp 2026 Homework 5](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/cohorts/2026/homework/05-deployment/homework.md): load the frozen lead-scoring model, serve predictions with FastAPI, and verify the same prediction in Docker.

## Answers and solution

See [SOLUTION.md](SOLUTION.md) for the six answers, verification notes, and detailed reproduction commands. The same answer values are recorded in [answers.json](answers.json).

## Files

| Files | Purpose |
| --- | --- |
| `q3.py`, `q3_result.json` | Load the frozen model and record the Question 3 prediction |
| `predict.py`, `model.py` | FastAPI service and shared model loading |
| `verify_api.py`, `local_api_result.json`, `docker_result.json` | Check API health, predictions, and artifact checksums |
| `Dockerfile`, `pyproject.toml`, `uv.lock`, `.python-version` | Pinned container and Python environment |
| `pipeline.bin`, `feature_defaults.json`, `model_metadata.json` | Official frozen model, missing-value defaults, and release metadata |
| `smoke_test.py`, `q6_test.py` | Official model and API test clients |
| `train.py`, `homework.md`, `homework.yaml` | Official training reference and homework specification |

The model, Dockerfile, and lockfile are unchanged from the official release. The API accepts eight observable fields. Missing numeric values use the training medians in `feature_defaults.json`; missing categories use `NA`. The model does not need to be retrained to reproduce the homework answers.

## Local run

From this folder, with Python 3.11.15 and `uv` available:

```bash
uv sync --locked
uv run python smoke_test.py
uv run python q3.py
uv run uvicorn predict:app --host 0.0.0.0 --port 9696
```

In another terminal:

```bash
uv run python q6_test.py
```

## Container run

Stop the local API before reusing port `9696`:

```bash
docker build -t zoomcamp-model:2026-hw5 .
docker run --rm -p 9696:9696 zoomcamp-model:2026-hw5
```

In another terminal:

```bash
uv run python q6_test.py
```

The API exposes `GET /health` and `POST /predict`. Its health response reports the model and feature-default checksums, allowing local and container inference to be compared with the recorded release metadata. For the separate-port comparison and saved verification results, see [SOLUTION.md](SOLUTION.md).
