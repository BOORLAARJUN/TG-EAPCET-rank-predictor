from datetime import datetime

from sqlalchemy import DateTime, Float, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.core.database import Base

JsonType = JSON().with_variant(JSONB, "postgresql")


class StudentTrainingData(Base):
    __tablename__ = "student_training_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exam_year: Mapped[int] = mapped_column(Integer, index=True)
    exam_type: Mapped[str] = mapped_column(String(40), index=True)
    category: Mapped[str] = mapped_column(String(20), index=True)
    total_marks: Mapped[float] = mapped_column(Float)
    subject_1_marks: Mapped[float | None] = mapped_column(Float)
    subject_2_marks: Mapped[float | None] = mapped_column(Float)
    subject_3_marks: Mapped[float | None] = mapped_column(Float)
    actual_rank: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CollegeCutoff(Base):
    __tablename__ = "college_cutoffs"
    __table_args__ = (Index("ix_cutoffs_lookup", "exam_year", "exam_type", "category", "closing_rank"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exam_year: Mapped[int] = mapped_column(Integer, index=True)
    exam_type: Mapped[str] = mapped_column(String(40), index=True)
    college_name: Mapped[str] = mapped_column(String(160))
    branch_name: Mapped[str] = mapped_column(String(120))
    category: Mapped[str] = mapped_column(String(20), index=True)
    opening_rank: Mapped[int] = mapped_column(Integer)
    closing_rank: Mapped[int] = mapped_column(Integer, index=True)
    location: Mapped[str | None] = mapped_column(String(120))


class ModelRegistry(Base):
    __tablename__ = "model_registry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    model_name: Mapped[str] = mapped_column(String(80))
    model_version: Mapped[str] = mapped_column(String(40), index=True)
    file_path: Mapped[str] = mapped_column(Text)
    normalization_method: Mapped[str] = mapped_column(String(40))
    normalization_params_json: Mapped[dict] = mapped_column(JsonType)
    feature_columns_json: Mapped[dict] = mapped_column(JsonType)
    metrics_json: Mapped[dict] = mapped_column(JsonType)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_json: Mapped[dict] = mapped_column(JsonType)
    normalized_score: Mapped[float] = mapped_column(Float)
    predicted_rank: Mapped[int] = mapped_column(Integer, index=True)
    response_json: Mapped[dict] = mapped_column(JsonType)
    model_version: Mapped[str] = mapped_column(String(40), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
