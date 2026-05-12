import json
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.core.rank_models import IsotonicRankRegressor

REAL_DATA_PATH = ROOT / "data" / "marks and ranks.csv"
SEED_DATA_PATH = ROOT / "data" / "seed_training_data.csv"
ARTIFACTS_DIR = ROOT / "artifacts"
FEATURE_COLUMNS = ["total_marks", "normalized_marks"]


def _clean_number_series(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series.astype(str).str.replace(",", "", regex=False).str.strip(), errors="coerce")


def load_training_data() -> pd.DataFrame:
    if REAL_DATA_PATH.exists():
        raw = pd.read_csv(REAL_DATA_PATH)
        frame = pd.DataFrame(
            {
                "student_id": range(1, len(raw) + 1),
                "exam_year": 2025,
                "exam_type": "TS_EAMCET",
                "session_id": raw.get("session_id", raw.get("Session", "ALL")),
                "category": "OC",
                "total_marks": _clean_number_series(raw["Total marks"]),
                "actual_rank": _clean_number_series(raw["Expected rank"]),
                "rank_min": _clean_number_series(raw["lowest rank probable"]),
                "rank_max": _clean_number_series(raw["probable highest rank"]),
            }
        )
    else:
        frame = pd.read_csv(SEED_DATA_PATH)
        frame["session_id"] = "ALL"
        frame["rank_min"] = frame["actual_rank"]
        frame["rank_max"] = frame["actual_rank"]

    frame = frame.dropna(subset=["total_marks", "actual_rank"])
    frame = frame[(frame["total_marks"] >= 0) & (frame["total_marks"] <= 160)].copy()
    return frame


def _top_average(values: pd.Series) -> float:
    count = max(1, int(round(len(values) * 0.001)))
    return float(values.sort_values(ascending=False).head(count).mean())


def add_normalized_marks(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Apply the EAMCET-style normalization formula.

    Formula:
    GASD + ((GTA - GASD) / (STA - SASD)) * (candidate_marks - SASD)
    where ASD is average + standard deviation and TA is top 0.1 percent average.
    With one available session this intentionally reduces to raw marks.
    """
    frame = frame.copy()
    cohorts = {}
    global_stats = {}

    for (exam_type, exam_year), exam_group in frame.groupby(["exam_type", "exam_year"]):
        exam_key = f"{exam_type}:{int(exam_year)}"
        global_mean = float(exam_group["total_marks"].mean())
        global_std = float(exam_group["total_marks"].std(ddof=0))
        gasd = global_mean + global_std
        gta = _top_average(exam_group["total_marks"])
        global_stats[exam_key] = {
            "mean": global_mean,
            "std": global_std,
            "asd": gasd,
            "top_average": gta,
            "count": int(len(exam_group)),
        }

        for session_id, session_group in exam_group.groupby("session_id"):
            session_key = f"{exam_key}:{session_id}"
            session_mean = float(session_group["total_marks"].mean())
            session_std = float(session_group["total_marks"].std(ddof=0))
            sasd = session_mean + session_std
            sta = _top_average(session_group["total_marks"])
            denominator = sta - sasd
            scale = 1.0 if abs(denominator) < 1e-9 else (gta - gasd) / denominator
            mask = (
                (frame["exam_type"] == exam_type)
                & (frame["exam_year"] == exam_year)
                & (frame["session_id"] == session_id)
            )
            frame.loc[mask, "normalized_marks"] = gasd + scale * (frame.loc[mask, "total_marks"] - sasd)
            cohorts[session_key] = {
                "exam_key": exam_key,
                "session_id": str(session_id),
                "mean": session_mean,
                "std": session_std,
                "asd": sasd,
                "top_average": sta,
                "scale": scale,
                "count": int(len(session_group)),
            }

    fallback_key = max(cohorts.items(), key=lambda item: item[1]["count"])[0]
    normalization = {
        "method": "eamcet_official",
        "formula": "GASD + ((GTA - GASD) / (STA - SASD)) * (candidate_marks - SASD)",
        "global_stats": global_stats,
        "cohorts": cohorts,
        "fallback_cohort": fallback_key,
    }
    return frame, normalization


def evaluate(name: str, model: object, x_valid: pd.DataFrame, y_valid: pd.Series) -> dict:
    predictions = model.predict(x_valid)
    absolute_errors = (predictions - y_valid).abs()
    return {
        "name": name,
        "mae": float(mean_absolute_error(y_valid, predictions)),
        "rmse": float(root_mean_squared_error(y_valid, predictions)),
        "r2": float(r2_score(y_valid, predictions)),
        "within_500": float((absolute_errors <= 500).mean()),
        "within_1000": float((absolute_errors <= 1000).mean()),
        "within_2000": float((absolute_errors <= 2000).mean()),
    }


def main() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    frame = load_training_data()
    frame, normalization = add_normalized_marks(frame)
    x = frame[FEATURE_COLUMNS]
    y = frame["actual_rank"]
    test_size = 0.25 if len(frame) >= 12 else max(1, int(len(frame) * 0.2))
    x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=test_size, random_state=42)

    candidates = [
        ("linear_regression", LinearRegression()),
        ("polynomial_ridge", make_pipeline(PolynomialFeatures(degree=2, include_bias=False), Ridge(alpha=1.0))),
        ("random_forest", RandomForestRegressor(n_estimators=180, random_state=42, min_samples_leaf=2)),
        ("gradient_boosting", GradientBoostingRegressor(random_state=42, max_depth=2, learning_rate=0.05, n_estimators=160)),
        ("isotonic_rank_curve", IsotonicRankRegressor()),
    ]
    scored = []
    for name, model in candidates:
        model.fit(x_train, y_train)
        scored.append((evaluate(name, model, x_valid, y_valid), model))

    best_metrics, best_model = min(scored, key=lambda item: item[0]["mae"])
    all_metrics = {"selected_model": best_metrics["name"], "validation": best_metrics, "candidates": [item[0] for item in scored]}

    joblib.dump(best_model, ARTIFACTS_DIR / "model.joblib")
    frame.to_csv(ARTIFACTS_DIR / "training_data_normalized.csv", index=False)
    (ARTIFACTS_DIR / "normalization.json").write_text(json.dumps(normalization, indent=2), encoding="utf-8")
    (ARTIFACTS_DIR / "metrics.json").write_text(json.dumps(all_metrics, indent=2), encoding="utf-8")
    (ARTIFACTS_DIR / "feature_columns.json").write_text(
        json.dumps({"feature_columns": FEATURE_COLUMNS}, indent=2),
        encoding="utf-8",
    )
    print(f"Saved {best_metrics['name']} model with MAE {best_metrics['mae']:.2f}")


if __name__ == "__main__":
    main()
