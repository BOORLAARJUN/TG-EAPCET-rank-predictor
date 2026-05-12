import pandas as pd
import math

def safe_str(value, default=""):
    if value is None:
        return default
    if isinstance(value, float) and math.isnan(value):
        return default
    return str(value)

def safe_int(value, default=0):
    if value is None:
        return default
    if pd.isna(value):
        return default
    return int(value)

def classify_chance(predicted_rank: int, closing_rank: int) -> str:
    if predicted_rank <= 0 or closing_rank <= 0:
        return "Reach"
    if predicted_rank <= closing_rank * 0.90:
        return "Safe"
    if closing_rank * 0.90 < predicted_rank <= closing_rank * 1.10:
        return "Possible"
    if closing_rank * 1.10 < predicted_rank <= closing_rank * 1.15:
        return "Ambitious"
    return "Reach"


def match_colleges(
    cutoffs: pd.DataFrame,
    predicted_rank: int,
    exam_type: str,
    category: str,
    branch_preference: str | None = None,
    limit: int = 25,
) -> list[dict]:
    category_upper = category.upper()
    frame = cutoffs[
        (cutoffs["exam_type"].str.upper() == exam_type.upper())
    ].copy()
    if category_upper == "SC":
        frame = frame[frame["category"].str.upper().str.startswith("SC_")].copy()
    else:
        frame = frame[frame["category"].str.upper() == category_upper].copy()
    if "phase" in frame.columns and (frame["phase"].str.upper() == "FINAL").any():
        frame = frame[frame["phase"].str.upper() == "FINAL"].copy()
    if branch_preference:
        branch_mask = frame["branch_name"].str.contains(branch_preference, case=False, na=False)
        if branch_mask.any():
            frame = frame[branch_mask].copy()

    if frame.empty:
        return []

    frame = frame[frame["closing_rank"].notna()].copy()
    frame["chance"] = frame["closing_rank"].apply(lambda value: classify_chance(predicted_rank, int(value)))
    frame = frame[frame["chance"].isin(["Safe", "Possible", "Ambitious"])].copy()
    frame = frame[
        ((frame["chance"] == "Safe") & (predicted_rank <= frame["closing_rank"] * 0.90))
        | ((frame["chance"] == "Possible") & (predicted_rank > frame["closing_rank"] * 0.90) & (predicted_rank <= frame["closing_rank"] * 1.10))
        | ((frame["chance"] == "Ambitious") & (predicted_rank > frame["closing_rank"] * 1.10) & (predicted_rank <= frame["closing_rank"] * 1.15))
    ].copy()
    if frame.empty:
        return []

    chance_order = {"Safe": 0, "Possible": 1, "Ambitious": 2}
    frame["chance_order"] = frame["chance"].map(chance_order)
    frame["distance"] = (frame["closing_rank"] - predicted_rank).abs()
    if "college_priority" not in frame.columns:
        frame["college_priority"] = 9999
    frame = frame.sort_values(["college_priority", "chance_order", "distance", "closing_rank"])
    frame = frame.drop_duplicates(subset=["college_name", "branch_name", "closing_rank"]).head(limit)
    return [
    {
        "college_name": safe_str(row.college_name, "Unknown"),
        "branch_name": safe_str(row.branch_name, ""),
        "closing_rank": safe_int(row.closing_rank),
        "opening_rank": safe_int(row.opening_rank),
        "location": safe_str(row.location, ""),
        "chance": safe_str(row.chance, "Reach"),
        "college_priority": None if safe_int(row.college_priority, 9999) == 9999 else safe_int(row.college_priority),
    }
        for row in frame.itertuples(index=False)
    ]
