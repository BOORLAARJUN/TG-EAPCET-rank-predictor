from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


Category = Literal["OC", "BC_A", "BC_B", "BC_C", "BC_D", "BC_E", "SC_I", "SC_II", "SC_III", "ST", "EWS"]


class PredictionRequest(BaseModel):
    exam_type: Literal["TS_EAMCET"] = "TS_EAMCET"
    exam_year: Literal[2026] = 2026
    category: Category = "OC"
    total_marks: float = Field(..., ge=0, le=160)
    branch_preference: str | None = None
    shift_id: str | None = None
    use_estimated_normalization: bool = False

    @field_validator("branch_preference")
    @classmethod
    def clean_branch(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None


class RankBand(BaseModel):
    min: int
    max: int


class CollegeSuggestion(BaseModel):
    college_name: str
    branch_name: str
    closing_rank: int
    opening_rank: int | None = None
    location: str | None = None
    chance: str
    college_priority: int | None = None


class EstimatedNormalizationOut(BaseModel):
    shift_id: str
    shift_label: str
    difficulty: str
    adjustment_min: float
    adjustment_max: float
    adjusted_marks_min: float
    adjusted_marks_max: float
    adjusted_marks_mid: float
    disclaimer: str


class EstimatedNormalizedRankBand(BaseModel):
    best_case: int
    likely: int
    worst_case: int


class PredictionResponse(BaseModel):
    normalized_score: float
    predicted_rank: int
    rank_band: RankBand
    colleges: list[CollegeSuggestion]
    model_version: str
    is_qualified: bool
    qualification_message: str

    raw_score: float | None = None
    raw_predicted_marks: float | None = None
    raw_predicted_rank: int | None = None
    raw_rank_band: RankBand | None = None

    estimated_normalization: EstimatedNormalizationOut | None = None
    estimated_normalized_rank: int | None = None
    estimated_normalized_rank_band: EstimatedNormalizedRankBand | None = None


class BulkPredictionRow(BaseModel):
    row: int
    prediction: PredictionResponse


class BulkPredictionError(BaseModel):
    row: int
    error: str


class BulkPredictionResponse(BaseModel):
    results: list[BulkPredictionRow]
    errors: list[BulkPredictionError]
