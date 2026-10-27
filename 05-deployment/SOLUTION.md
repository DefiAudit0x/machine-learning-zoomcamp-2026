# Homework 5 — Deploying Machine Learning Models

A practical solution to **ML Zoomcamp 2026 — Deploying Machine Learning Models**, using the official cohort files and the frozen model without retraining it or modifying the lockfile.

## Answers

| Question | Answer |
|---|---|
| 1 — Local uv version | `0.12.13` |
| 2 — Locked Scikit-Learn version | `1.7.2` |
| 3 — Conversion probability from the model | `0.533` |
| 4 — Conversion probability via the API | `0.770` |
| 5 — Python base image | `python:3.11.15-slim-bookworm` |
| 6 — Conversion probability from the container | `0.770` |

The unrounded value for Question 3 is `0.5329944186432507`. The API and container returned exactly the same value: `0.769799` with `conversion: true`.

The local `uv` version differs from the version installed inside Docker, which is `0.10.11`. Question 1 asks for the local version; the official instructions describe this question as a setup check.

## What Was Verified

- Running the locked environment with Python `3.11.15` and `uv sync --locked`.
- Passing the reference `smoke_test.py` test.
- Loading the model with `pickle` after matching the official SHA-256 fingerprint.
- Running the FastAPI locally and testing `/health` and `/predict`.
- Building the official Dockerfile and running an actual container, then passing `q6_test.py`.
- Matching predictions, model fingerprints, and imputation values between the local API and the container.
- No modifications to `Dockerfile`, `uv.lock`, or the official model.

Model fingerprint:

```text
1646bbdcd38d4f044da6b630c5b332c93a314245a8c21929011c42de51f629f1
```

## Re-running

From inside the project directory, with `uv` and Docker installed:

```bash
uv sync --locked
uv run python smoke_test.py
uv run python q3.py
```

In a first terminal window, run the local API on a separate port so it can be compared with the container:

```bash
uv run uvicorn predict:app --host 127.0.0.1 --port 9697
```

In a second window:

```bash
uv run python verify_api.py --runtime local_api --base-url http://127.0.0.1:9697
```

To build and run the container:

```bash
docker build -t zoomcamp-model:2026-hw5 .
docker run --rm -p 9696:9696 zoomcamp-model:2026-hw5
```

Then, from another window:

```bash
uv run python verify_api.py --runtime docker --base-url http://127.0.0.1:9696
uv run python q6_test.py
```

The scripts write their results to `q3_result.json`, `local_api_result.json`, and `docker_result.json`. `answers.json` contains a summary of the answers and verification. `--network=host` was used when building and running the container in the isolated execution environment; the Dockerfile was not changed.

## Sources

- [Official Homework 5 instructions](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/cohorts/2026/homework/05-deployment/homework.md)
- [Official release files](https://github.com/DataTalksClub/machine-learning-zoomcamp/tree/main/cohorts/2026/homework/05-deployment)
- [Homework submission page](https://courses.datatalks.club/ml-zoomcamp-2026/homework/hw05)
