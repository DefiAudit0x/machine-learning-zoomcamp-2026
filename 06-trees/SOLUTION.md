# Homework 6 — Trees: Solution

## Answers

| Question | Answer | Validation result |
| --- | --- | --- |
| 1. Decision-tree split (`max_depth=1`) | `model_year` | Root split feature |
| 2. Random-forest RMSE (`n_estimators=10`) | `1.837` | `1.837054` |
| 3. Best `n_estimators` | `100` | Lowest RMSE among 10, 50, 100, and 150 trees |
| 4. Best `max_depth` | `10` | Lowest mean RMSE across the four tested forest sizes |
| 5. Most important candidate feature | `vehicle_weight` | Highest candidate `feature_importances_` |
| 6. Best XGBoost `eta` | `0.1` | Validation RMSE: `1.724810` (`eta=0.3`: `1.826458`) |

## Validation details

The script uses the official 10,000-row dataset, fills missing values with zero, makes the two exact `train_test_split` calls specified in the assignment with `random_state=1`, and vectorizes features with `DictVectorizer(sparse=True)`. The resulting split sizes are 6,000 training rows, 2,000 validation rows, and 2,000 test rows. Model selection uses the validation set; the test set is held out.

The dataset SHA-256 is `00a5cab178a8b7cd6e9157ee71dabc236ba7f20b1832336d358b07af14ba431f`, matching the [published 2026 data release](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/cohorts/2026/data/README.md). The results were reproduced with Python 3.11.15, NumPy 2.3.3, pandas 2.3.2, scikit-learn 1.7.2, and XGBoost 3.2.0, the versions stated for the course reference replay.

The preprocessing, split, model settings, and selected options were cross-checked against the course's [official homework reference validator](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/cohorts/2026/data/validate_homework.py). The XGBoost validation RMSE comparison was run directly using the assignment's specified parameters and 100 boosting rounds.

## Sources

- [Official Homework 6 instructions](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/cohorts/2026/homework/06-trees/homework.md)
- [Pinned 2026 car fuel-efficiency dataset](https://raw.githubusercontent.com/DataTalksClub/machine-learning-zoomcamp/main/cohorts/2026/data/car_fuel_efficiency_2026.csv)
- [2026 data release notes and checksums](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/cohorts/2026/data/README.md)
- [Official homework answer validator](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/cohorts/2026/data/validate_homework.py)
