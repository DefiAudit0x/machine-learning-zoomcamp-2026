"""Reproduce the answers for DataTalks.Club ML Zoomcamp 2026 Homework 6."""

from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


DATA_URL = (
    "https://raw.githubusercontent.com/DataTalksClub/machine-learning-zoomcamp/"
    "main/cohorts/2026/data/car_fuel_efficiency_2026.csv"
)
EXPECTED_SHA256 = "00a5cab178a8b7cd6e9157ee71dabc236ba7f20b1832336d358b07af14ba431f"
CACHE_PATH = (
    Path.home()
    / ".cache"
    / "ml-zoomcamp-2026"
    / "car_fuel_efficiency_2026.csv"
)
TARGET = "fuel_efficiency_mpg"


def load_data() -> pd.DataFrame:
    """Load the pinned course CSV, downloading it to the user cache if needed."""
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CACHE_PATH.exists():
        with urllib.request.urlopen(DATA_URL, timeout=60) as response:
            data = response.read()
        actual_sha256 = hashlib.sha256(data).hexdigest()
        if actual_sha256 != EXPECTED_SHA256:
            raise ValueError(
                "Downloaded dataset checksum does not match the pinned course release: "
                f"{actual_sha256}"
            )
        CACHE_PATH.write_bytes(data)

    actual_sha256 = hashlib.sha256(CACHE_PATH.read_bytes()).hexdigest()
    if actual_sha256 != EXPECTED_SHA256:
        raise ValueError(
            "Cached dataset checksum does not match the pinned course release: "
            f"{actual_sha256}"
        )

    frame = pd.read_csv(CACHE_PATH)
    if len(frame) != 10_000:
        raise ValueError(f"Expected 10,000 rows, found {len(frame)}")
    return frame


def rmse(actual: pd.Series | np.ndarray, predicted: np.ndarray) -> float:
    return float(mean_squared_error(actual, predicted) ** 0.5)


def main() -> None:
    df = load_data()

    # Follow the assignment's preparation rule and exact split calls.
    df = df.fillna(0)
    df_full_train, df_test = train_test_split(
        df, test_size=0.2, random_state=1
    )
    df_train, df_val = train_test_split(
        df_full_train, test_size=0.25, random_state=1
    )

    y_train = df_train[TARGET]
    y_val = df_val[TARGET]
    X_train_dicts = df_train.drop(columns=[TARGET]).to_dict(orient="records")
    X_val_dicts = df_val.drop(columns=[TARGET]).to_dict(orient="records")

    dv = DictVectorizer(sparse=True)
    X_train = dv.fit_transform(X_train_dicts)
    X_val = dv.transform(X_val_dicts)

    # Question 1: depth-one decision tree; map one-hot names to source columns.
    tree = DecisionTreeRegressor(max_depth=1, random_state=1)
    tree.fit(X_train, y_train)
    split_name = dv.feature_names_[tree.tree_.feature[0]]
    q1_feature = split_name.split("=", 1)[0]

    # Questions 2 and 3: forest size; Question 2 is the 10-tree result.
    forest_scores: dict[int, float] = {}
    for n_estimators in [10, 50, 100, 150]:
        model = RandomForestRegressor(
            n_estimators=n_estimators, random_state=1, n_jobs=-1
        )
        model.fit(X_train, y_train)
        forest_scores[n_estimators] = rmse(y_val, model.predict(X_val))

    # Question 4: average validation RMSE across the four forest sizes.
    depth_scores: dict[int, float] = {}
    for depth in [10, 15, 20, 25]:
        scores = []
        for n_estimators in [10, 50, 100, 150]:
            model = RandomForestRegressor(
                n_estimators=n_estimators,
                max_depth=depth,
                random_state=1,
                n_jobs=-1,
            )
            model.fit(X_train, y_train)
            scores.append(rmse(y_val, model.predict(X_val)))
        depth_scores[depth] = float(np.mean(scores))

    # Question 5: most important feature among the four named candidates.
    importance_model = RandomForestRegressor(
        n_estimators=10, max_depth=20, random_state=1, n_jobs=-1
    )
    importance_model.fit(X_train, y_train)
    importances = dict(zip(dv.feature_names_, importance_model.feature_importances_))
    candidates = [
        "vehicle_weight",
        "horsepower",
        "acceleration",
        "engine_displacement",
    ]
    q5_importances = {name: float(importances.get(name, 0.0)) for name in candidates}

    # Question 6: compare the two eta values with the assignment's XGBoost setup.
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_val, label=y_val)
    watchlist = [(dtrain, "train"), (dval, "validation")]
    xgb_scores: dict[str, float] = {}
    for eta in [0.3, 0.1]:
        params = {
            "eta": eta,
            "max_depth": 6,
            "min_child_weight": 1,
            "objective": "reg:squarederror",
            "nthread": 8,
            "seed": 1,
            "verbosity": 1,
        }
        model = xgb.train(
            params,
            dtrain,
            num_boost_round=100,
            evals=watchlist,
            verbose_eval=False,
        )
        xgb_scores[str(eta)] = rmse(y_val, model.predict(dval))

    q6_eta = min(xgb_scores, key=xgb_scores.get)
    answers = {
        "q1_split_feature": q1_feature,
        "q2_random_forest_rmse": forest_scores[10],
        "q2_selected_option": f"{forest_scores[10]:.3f}",
        "q3_best_n_estimators": min(forest_scores, key=forest_scores.get),
        "q3_validation_rmse_by_n_estimators": {
            str(n): score for n, score in forest_scores.items()
        },
        "q4_best_max_depth": min(depth_scores, key=depth_scores.get),
        "q4_mean_rmse_by_max_depth": {
            str(depth): score for depth, score in depth_scores.items()
        },
        "q5_most_important_feature": max(q5_importances, key=q5_importances.get),
        "q5_candidate_importances": q5_importances,
        "q6_best_eta": float(q6_eta),
        "q6_validation_rmse_by_eta": xgb_scores,
        "dataset_sha256": EXPECTED_SHA256,
        "rows": len(df),
        "split_sizes": {
            "train": len(df_train),
            "validation": len(df_val),
            "test": len(df_test),
        },
        "versions": {
            "pandas": pd.__version__,
            "scikit_learn": __import__("sklearn").__version__,
            "xgboost": xgb.__version__,
        },
    }
    print(json.dumps(answers, indent=2))


if __name__ == "__main__":
    main()
