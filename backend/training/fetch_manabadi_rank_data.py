import csv
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "marks and ranks.csv"
API_URL = "https://www.manabadi.co.in/Entrance-Exams/eamcet/PredictRank-2026.aspx"


def split_subject_marks(total_marks: int) -> tuple[int, int, int]:
    """Create a valid engineering subject split for a total-only rank curve."""
    maths = min(80, round(total_marks * 0.5))
    physics = min(40, round(total_marks * 0.25))
    chemistry = total_marks - maths - physics

    if chemistry > 40:
        overflow = chemistry - 40
        chemistry = 40
        maths = min(80, maths + overflow)

    if maths + physics + chemistry != total_marks:
        chemistry += total_marks - (maths + physics + chemistry)

    return maths, physics, chemistry


def fetch_prediction(total_marks: int, attempts: int = 3) -> dict:
    payload = json.dumps({"totalMarks": total_marks}).encode("utf-8")
    request = Request(
        API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "rank-predictor-data-refresh/1.0",
        },
        method="POST",
    )

    for attempt in range(1, attempts + 1):
        try:
            with urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8").strip())
        except (TimeoutError, URLError, json.JSONDecodeError):
            if attempt == attempts:
                raise
            time.sleep(1.5 * attempt)

    raise RuntimeError(f"Could not fetch prediction for {total_marks} marks")


def build_row(total_marks: int, prediction: dict) -> dict:
    maths, physics, chemistry = split_subject_marks(total_marks)
    return {
        "maths score": maths,
        "physics score": physics,
        "Chemistry score": chemistry,
        "Total marks": total_marks,
        "lowest rank probable": int(prediction["minRank"]),
        "probable highest rank": int(prediction["maxRank"]),
        "Expected rank": int(prediction["expectedRank"]),
    }


def main() -> None:
    totals = range(1, 161)
    rows = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(fetch_prediction, total): total for total in totals}
        for future in as_completed(futures):
            total = futures[future]
            rows.append(build_row(total, future.result()))

    rows.sort(key=lambda row: row["Total marks"])
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
