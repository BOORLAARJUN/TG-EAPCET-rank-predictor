import re
from pathlib import Path

import pandas as pd
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_PATH = DATA_DIR / "college_cutoffs_imported.csv"

CATEGORY_COLUMNS = [
    ("OC", "BOYS"),
    ("OC", "GIRLS"),
    ("BC_A", "BOYS"),
    ("BC_A", "GIRLS"),
    ("BC_B", "BOYS"),
    ("BC_B", "GIRLS"),
    ("BC_C", "BOYS"),
    ("BC_C", "GIRLS"),
    ("BC_D", "BOYS"),
    ("BC_D", "GIRLS"),
    ("BC_E", "BOYS"),
    ("BC_E", "GIRLS"),
    ("SC_I", "BOYS"),
    ("SC_I", "GIRLS"),
    ("SC_II", "BOYS"),
    ("SC_II", "GIRLS"),
    ("SC_III", "BOYS"),
    ("SC_III", "GIRLS"),
    ("ST", "BOYS"),
    ("ST", "GIRLS"),
    ("EWS", "BOYS"),
    ("EWS", "GIRLS"),
]

COLLEGE_TYPES = {"PVT", "GOV", "UNIV", "SF", "AIDED"}
COED_MARKERS = {"COED", "GIRLS", "BOYS"}


def _phase_from_name(path: Path) -> str:
    name = path.stem.upper()
    if "FINAL" in name:
        return "FINAL"
    if "SECOND" in name:
        return "SECOND"
    if "FIRST" in name:
        return "FIRST"
    return "UNKNOWN"


def _extract_records(pdf_path: Path) -> list[str]:
    reader = PdfReader(str(pdf_path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    records: list[str] = []
    current: list[str] = []
    for line in lines:
        if re.match(r"^[A-Z0-9]{4}\s+", line):
            if current:
                records.append(" ".join(current))
            current = [line]
        elif current:
            current.append(line)
    if current:
        records.append(" ".join(current))
    return records


def _parse_record(record: str, phase: str) -> list[dict]:
    tokens = record.split()
    numeric_positions = [idx for idx, token in enumerate(tokens) if token.isdigit()]
    if len(numeric_positions) < len(CATEGORY_COLUMNS):
        return []

    rank_positions = numeric_positions[-len(CATEGORY_COLUMNS) :]
    rank_start = rank_positions[0]
    rank_end = rank_positions[-1]
    if rank_positions != list(range(rank_start, rank_end + 1)):
        return []

    prefix = tokens[:rank_start]
    ranks = [int(value) for value in tokens[rank_start : rank_end + 1]]
    affiliated_to = " ".join(tokens[rank_end + 1 :]) or None
    if len(prefix) < 8:
        return []

    inst_code = prefix[0]
    type_idx = None
    for idx, token in enumerate(prefix):
        if token in COLLEGE_TYPES:
            type_idx = idx
    if type_idx is None or type_idx + 2 >= len(prefix):
        return []

    branch_code = prefix[type_idx + 1]
    branch_name = " ".join(prefix[type_idx + 2 :])
    coed_idx = next((idx for idx, token in enumerate(prefix[:type_idx]) if token in COED_MARKERS), None)
    if coed_idx is None or coed_idx < 3:
        return []

    place = prefix[coed_idx - 2]
    district = prefix[coed_idx - 1]
    college_name = " ".join(prefix[1 : coed_idx - 2])
    college_type = prefix[type_idx]

    rows = []
    for (category, gender), closing_rank in zip(CATEGORY_COLUMNS, ranks):
        rows.append(
            {
                "exam_year": 2025,
                "exam_type": "TS_EAMCET",
                "phase": phase,
                "institute_code": inst_code,
                "college_name": college_name,
                "branch_code": branch_code,
                "branch_name": branch_name,
                "category": category,
                "gender": gender,
                "opening_rank": closing_rank,
                "closing_rank": closing_rank,
                "location": place,
                "district": district,
                "college_type": college_type,
                "affiliated_to": affiliated_to,
            }
        )
    return rows


def import_cutoffs() -> pd.DataFrame:
    rows = []
    for pdf_path in sorted(DATA_DIR.glob("TGEAPCET_2025*LASTRANKS*.pdf")):
        phase = _phase_from_name(pdf_path)
        for record in _extract_records(pdf_path):
            rows.extend(_parse_record(record, phase))

    if not rows:
        raise RuntimeError("No cutoff rows could be parsed from the TGEAPCET PDFs.")

    frame = pd.DataFrame(rows)
    frame = frame.drop_duplicates(
        subset=["phase", "institute_code", "branch_code", "category", "gender", "closing_rank"]
    )
    frame.to_csv(OUTPUT_PATH, index=False)
    return frame


def main() -> None:
    frame = import_cutoffs()
    print(f"Wrote {len(frame)} cutoff rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
