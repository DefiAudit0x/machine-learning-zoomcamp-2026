# Homework 6 — Trees

A reproducible solution for [DataTalks.Club ML Zoomcamp 2026 Homework 6](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/cohorts/2026/homework/06-trees/homework.md). It uses the official pinned car fuel-efficiency dataset and follows the assignment's preprocessing and train/validation/test split.

## Run

Use Python 3.11.15, then install the pinned dependencies and run the solution:

```bash
python -m pip install -r requirements.txt
python homework.py
```

The script downloads the dataset to `~/.cache/ml-zoomcamp-2026/` if it is not already cached, verifies the official SHA-256 checksum, and prints the answers with supporting validation metrics. It does not write the dataset into this folder.

## Files

| File | Purpose |
| --- | --- |
| `homework.py` | Reproduces the split, models, validation scores, and six answers |
| `answers.json` | Machine-readable answers, metrics, dataset checksum, split sizes, and runtime versions |
| `SOLUTION.md` | Answers and concise validation notes |
| `requirements.txt` | Reference package versions for the 2026 release |
