from dataclasses import dataclass

SHIFT_LABELS = {
    "2025-05-02-S1": "May 2 Shift 1",
    "2025-05-02-S2": "May 2 Shift 2",
    "2025-05-03-S1": "May 3 Shift 1",
    "2025-05-03-S2": "May 3 Shift 2",
    "2025-05-04-S1": "May 4 Shift 1",
    "2025-05-04-S2": "May 4 Shift 2",
}

SHIFT_DIFFICULTY_MAP = {
    "2025-05-02-S1": "moderate",
    "2025-05-02-S2": "tough",
    "2025-05-03-S1": "easy_moderate",
    "2025-05-03-S2": "easy",
    "2025-05-04-S1": "moderate",
    "2025-05-04-S2": "tough",
}

ADJUSTMENT_RULES = {
    "very_tough": (2.5, 5.0),
    "tough": (1.5, 3.5),
    "moderate": (0.0, 1.0),
    "easy_moderate": (-0.5, 0.5),
    "easy": (-2.0, -0.5),
}


@dataclass
class EstimatedNormalizationResult:
    shift_id: str
    shift_label: str
    difficulty: str
    adjustment_min: float
    adjustment_max: float
    adjusted_marks_min: float
    adjusted_marks_max: float
    adjusted_marks_mid: float


def clamp_marks(value: float) -> float:
    return max(0.0, min(160.0, round(value, 2)))


def estimate_normalized_marks(raw_marks: float, shift_id: str) -> EstimatedNormalizationResult:
    difficulty = SHIFT_DIFFICULTY_MAP.get(shift_id, "moderate")
    adj_min, adj_max = ADJUSTMENT_RULES.get(difficulty, (0.0, 1.0))

    adjusted_min = clamp_marks(raw_marks + adj_min)
    adjusted_max = clamp_marks(raw_marks + adj_max)
    adjusted_mid = clamp_marks((adjusted_min + adjusted_max) / 2)

    return EstimatedNormalizationResult(
        shift_id=shift_id,
        shift_label=SHIFT_LABELS.get(shift_id, shift_id),
        difficulty=difficulty,
        adjustment_min=adj_min,
        adjustment_max=adj_max,
        adjusted_marks_min=adjusted_min,
        adjusted_marks_max=adjusted_max,
        adjusted_marks_mid=adjusted_mid,
    )
