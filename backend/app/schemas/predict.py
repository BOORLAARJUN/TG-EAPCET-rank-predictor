from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


Category = Literal["OC", "BC_A", "BC_B", "BC_C", "BC_D", "BC_E", "SC_I", "SC_II", "SC_III", "ST", "EWS"]


class PredictionRequest(BaseModel):
    exam_type: Literal["TS_EAMCET"] = "TS_EAMCET"
    exam_year: Literal[2026] = 2026
    category: Category = "OC"
    total_marks: float = Field(..., ge=0, le=160)
    branch_preference: str | None = None

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


class PredictionResponse(BaseModel):
    normalized_score: float
    predicted_rank: int
    rank_band: RankBand
    colleges: list[CollegeSuggestion]
    model_version: str
    is_qualified: bool
    qualification_message: str


class BulkPredictionRow(BaseModel):
    row: int
    prediction: PredictionResponse


class BulkPredictionError(BaseModel):
    row: int
    error: str


class BulkPredictionResponse(BaseModel):
    results: list[BulkPredictionRow]
    errors: list[BulkPredictionError]
