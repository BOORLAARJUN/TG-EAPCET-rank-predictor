import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import joblib
import pandas as pd

from app.core.config import Settings


@dataclass
class ModelBundle:
    model: object
    normalization: dict
    metrics: dict
    feature_columns: list[str]
    cutoff_frame: pd.DataFrame
    model_version: str


def _read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _apply_college_priority(cutoff_frame: pd.DataFrame, priority_path: Path) -> pd.DataFrame:
    cutoff_frame = cutoff_frame.copy()
    cutoff_frame["college_priority"] = 9999
    if not priority_path.exists() or "institute_code" not in cutoff_frame.columns:
        return cutoff_frame

    priority_frame = pd.read_csv(priority_path, header=None, names=["institute_code"], dtype=str)
    priority_frame["institute_code"] = priority_frame["institute_code"].str.strip().str.upper()
    priority_frame = priority_frame[priority_frame["institute_code"].notna() & (priority_frame["institute_code"] != "")]
    priority_map = {code: index + 1 for index, code in enumerate(priority_frame["institute_code"].tolist())}
    cutoff_frame["college_priority"] = (
        cutoff_frame["institute_code"].astype(str).str.strip().str.upper().map(priority_map).fillna(9999).astype(int)
    )
    return cutoff_frame


def _ensure_artifacts(settings: Settings) -> None:
    required = [
        settings.artifacts_dir / "model.joblib",
        settings.artifacts_dir / "normalization.json",
        settings.artifacts_dir / "metrics.json",
        settings.artifacts_dir / "feature_columns.json",
    ]
    if all(path.exists() for path in required):
        return

    subprocess.run(
        [sys.executable, "training/train_model.py"],
        cwd=Path(__file__).resolve().parents[2],
        check=True,
    )


def load_model_bundle(settings: Settings) -> ModelBundle:
    _ensure_artifacts(settings)
    artifacts_dir = settings.artifacts_dir
    cutoff_path = settings.seed_cutoffs_csv
    if not cutoff_path.exists():
        fallback = Path("data/seed_college_cutoffs.csv")
        cutoff_path = fallback
    cutoff_frame = pd.read_csv(cutoff_path)
    cutoff_frame = _apply_college_priority(cutoff_frame, settings.college_priority_csv)
    feature_payload = _read_json(artifacts_dir / "feature_columns.json")
    return ModelBundle(
        model=joblib.load(artifacts_dir / "model.joblib"),
        normalization=_read_json(artifacts_dir / "normalization.json"),
        metrics=_read_json(artifacts_dir / "metrics.json"),
        feature_columns=feature_payload["feature_columns"],
        cutoff_frame=cutoff_frame,
        model_version=settings.model_version,
    )
