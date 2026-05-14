import pandas as pd
from sqlalchemy.orm import Session  # type: ignore

from app.core.college_matcher import match_colleges
from app.core.model_loader import ModelBundle
from app.core.preprocessing import build_features
from app.core.estimated_normalization import estimate_normalized_marks
from app.models.db_models import PredictionLog
from app.schemas.predict import (
    EstimatedNormalizationOut,
    EstimatedNormalizedRankBand,
    PredictionRequest,
    PredictionResponse,
    RankBand,
)

QUALIFYING_MARKS = 40
SC_ST_PREFIXES = ("SC", "ST")
OPEN_CATEGORY_VALUES = {"OC", "GENERAL", "BC", "OBC", "BC_A", "BC_B", "BC_C", "BC_D", "BC_E"}
ESTIMATED_NORMALIZATION_DISCLAIMER = (
    "This is an unofficial estimate based on TG EAPCET 2026 engineering shift difficulty reports, "
    "not the official TG EAPCET normalization formula."
)

def get_qualification_status(category: str, normalized_score: float) -> tuple[bool, str]:
    category_upper = category.strip().upper()

    if category_upper.startswith(SC_ST_PREFIXES):
        return True, "Qualified: SC/ST candidates have no minimum qualifying marks in TG EAPCET."

    if category_upper in OPEN_CATEGORY_VALUES or category_upper.startswith("BC"):
        if normalized_score >= QUALIFYING_MARKS:
            return True, f"Qualified: {category_upper} candidates need at least 40/160, and you scored {round(normalized_score, 2)}."
        return False, f"Not qualified: {category_upper} candidates need at least 40/160, and you scored {round(normalized_score, 2)}."

    if normalized_score >= QUALIFYING_MARKS:
        return True, f"Qualified: category treated as non-SC/ST, minimum required is 40/160 and you scored {round(normalized_score, 2)}."
    return False, f"Not qualified: category treated as non-SC/ST, minimum required is 40/160 and you scored {round(normalized_score, 2)}."


def predict_rank_for_marks(payload: PredictionRequest, bundle: ModelBundle, marks: float) -> int:
    adjusted_payload = payload.model_copy(update={"total_marks": marks})
    features, _ = build_features(adjusted_payload, bundle)
    feature_frame = pd.DataFrame([features], columns=bundle.feature_columns)
    return max(1, int(round(float(bundle.model.predict(feature_frame)[0]))))  # type: ignore


def predict_one(payload: PredictionRequest, bundle: ModelBundle) -> PredictionResponse:
    features, display_score = build_features(payload, bundle)
    feature_frame = pd.DataFrame([features], columns=bundle.feature_columns)
    predicted_rank = max(1, int(round(float(bundle.model.predict(feature_frame)[0]))))  # type: ignore
    spread = max(250, int(round(predicted_rank * 0.05)))

    raw_score = round(display_score, 2)
    raw_predicted_rank = predicted_rank
    raw_rank_band = RankBand(
        min=max(1, predicted_rank - spread),
        max=predicted_rank + spread,
    )

    estimated_normalization = None
    estimated_normalized_rank = None
    estimated_normalized_rank_band = None

    if payload.use_estimated_normalization and payload.shift_id:
        norm_result = estimate_normalized_marks(raw_score, payload.shift_id)

        likely_rank = predict_rank_for_marks(payload, bundle, norm_result.adjusted_marks_mid)
        best_rank = predict_rank_for_marks(payload, bundle, norm_result.adjusted_marks_max)
        worst_rank = predict_rank_for_marks(payload, bundle, norm_result.adjusted_marks_min)

        estimated_normalization = EstimatedNormalizationOut(
            shift_id=norm_result.shift_id,
            shift_label=norm_result.shift_label,
            difficulty=norm_result.difficulty,
            adjustment_min=norm_result.adjustment_min,
            adjustment_max=norm_result.adjustment_max,
            adjusted_marks_min=norm_result.adjusted_marks_min,
            adjusted_marks_max=norm_result.adjusted_marks_max,
            adjusted_marks_mid=norm_result.adjusted_marks_mid,
            disclaimer=ESTIMATED_NORMALIZATION_DISCLAIMER,
        )

        estimated_normalized_rank = likely_rank
        estimated_normalized_rank_band = EstimatedNormalizedRankBand(
            best_case=best_rank,
            likely=likely_rank,
            worst_case=worst_rank,
        )

    is_qualified, qualification_message = get_qualification_status(
        payload.category,
        round(display_score, 2),
    )

    colleges = match_colleges(
        bundle.cutoff_frame,
        predicted_rank=predicted_rank,
        exam_type=payload.exam_type,
        category=payload.category,
        branch_preference=payload.branch_preference,
    )

    return PredictionResponse(
        normalized_score=raw_score,
        predicted_rank=raw_predicted_rank,
        rank_band=raw_rank_band,
        colleges=colleges,
        model_version=bundle.model_version,
        is_qualified=is_qualified,
        qualification_message=qualification_message,

        raw_score=raw_score,
        raw_predicted_marks=raw_score,
        raw_predicted_rank=raw_predicted_rank,
        raw_rank_band=raw_rank_band,

        estimated_normalization=estimated_normalization,
        estimated_normalized_rank=estimated_normalized_rank,
        estimated_normalized_rank_band=estimated_normalized_rank_band,
    )

def persist_prediction_log(db: Session | None, payload: PredictionRequest, response: PredictionResponse) -> None:
    if db is None:
        return

    log = PredictionLog(
        request_json=payload.model_dump(),
        normalized_score=response.normalized_score,
        predicted_rank=response.predicted_rank,
        response_json=response.model_dump(),
        model_version=response.model_version,
    )
    db.add(log)
    db.commit()
