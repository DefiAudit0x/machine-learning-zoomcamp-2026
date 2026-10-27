# Homework 4 — Lead-scoring dataset

This folder contains the public, synthetic lead-scoring dataset used by ML Zoomcamp 2026 Homework 4. It comes from the [official course data release](https://github.com/DataTalksClub/machine-learning-zoomcamp/tree/main/cohorts/2026/data), which generates the data from a reviewed plan. It is not private customer data.

## Files

- `course_lead_scoring_2026.csv`: 5,000 rows and nine columns.
- `course_lead_scoring_2026_report.json`: the course release's data-generation and quality report, including feature distributions, relationships, and missingness rates.

## Columns

The input features are `lead_source`, `industry`, `employment_status`, `location`, `annual_income`, `number_of_courses_viewed`, `interaction_count`, and `lead_score`. The target is `converted`.

The data represents a marketing funnel: acquisition and employment categories influence engagement, which relates to interactions and lead score. Conversion is sampled from a logistic probability rather than assigned by a hard threshold. Some feature values are intentionally missing. See the [homework solution](../README.md) for the assignment's preprocessing and evaluation procedure.

## Source and integrity

The checked-in CSV matches the [official CSV](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/cohorts/2026/data/course_lead_scoring_2026.csv) byte for byte. Its pinned SHA-256 is:

```text
2d9da196bdefd2a45aa0a17ca21c19f06a5d9d56af628be1f04bbb3531cc12e9  course_lead_scoring_2026.csv
```

Verify it from this folder with:

```bash
sha256sum course_lead_scoring_2026.csv
```

The report includes a measured generation time, so its checksum is not used as the dataset identity. The CSV checksum identifies the fixed release used for the homework.
