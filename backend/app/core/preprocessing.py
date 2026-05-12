from app.core.model_loader import ModelBundle
from app.schemas.predict import PredictionRequest


def normalize_marks(total_marks: float, exam_type: str, exam_year: int, normalization: dict) -> tuple[float, float]:
    if normalization.get("method") == "eamcet_official":
        exam_key = f"{exam_type}:{exam_year}"
        fallback_key = normalization["fallback_cohort"]
        cohorts = normalization["cohorts"]
        params = cohorts.get(f"{exam_key}:ALL", cohorts[fallback_key])
        global_params = normalization["global_stats"].get(exam_key, normalization["global_stats"][params["exam_key"]])
        denominator = params["top_average"] - params["asd"]
        scale = 1.0 if abs(denominator) < 1e-9 else (global_params["top_average"] - global_params["asd"]) / denominator
        normalized = global_params["asd"] + scale * (total_marks - params["asd"])
        return normalized, max(0.0, min(160.0, normalized))

    cohorts = normalization["cohorts"]
    cohort_key = f"{exam_type}:{exam_year}"
    fallback_key = normalization["fallback_cohort"]
    params = cohorts.get(cohort_key, cohorts[fallback_key])
    std = params["std"] or 1.0
    z_score = (total_marks - params["mean"]) / std
    display_score = max(0.0, min(100.0, 50.0 + z_score * 10.0))
    return z_score, display_score


def build_features(payload: PredictionRequest, bundle: ModelBundle) -> tuple[list[float], float]:
    normalized_marks, display_score = normalize_marks(
        payload.total_marks,
        payload.exam_type,
        payload.exam_year,
        bundle.normalization,
    )
    raw = {
        "total_marks": payload.total_marks,
        "exam_year": payload.exam_year,
        "normalized_marks": normalized_marks,
    }
    return [float(raw[column]) for column in bundle.feature_columns], display_score
