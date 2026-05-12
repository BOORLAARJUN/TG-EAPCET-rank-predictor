import pandas as pd

from app.core.college_matcher import classify_chance, match_colleges


def test_classify_chance_labels() -> None:
    assert classify_chance(8000, 10000) == "Safe"
    assert classify_chance(10000, 10000) == "Possible"
    assert classify_chance(11200, 10000) == "Ambitious"


def test_match_colleges_filters_and_limits() -> None:
    frame = pd.DataFrame(
        [
            {"exam_type": "TS_EAMCET", "category": "OC", "college_name": "A", "branch_name": "CSE", "opening_rank": 1, "closing_rank": 10000, "location": "Hyd"},
            {"exam_type": "TS_EAMCET", "category": "SC", "college_name": "B", "branch_name": "CSE", "opening_rank": 1, "closing_rank": 20000, "location": "Hyd"},
        ]
    )

    colleges = match_colleges(frame, 9500, "TS_EAMCET", "OC")

    assert len(colleges) == 1
    assert colleges[0]["college_name"] == "A"


def test_match_colleges_uses_priority_before_closeness() -> None:
    frame = pd.DataFrame(
        [
            {"exam_type": "TS_EAMCET", "category": "OC", "college_name": "Lower Priority", "branch_name": "CSE", "opening_rank": 1, "closing_rank": 10100, "location": "Hyd", "college_priority": 2},
            {"exam_type": "TS_EAMCET", "category": "OC", "college_name": "Top Priority", "branch_name": "CSE", "opening_rank": 1, "closing_rank": 12000, "location": "Hyd", "college_priority": 1},
        ]
    )

    colleges = match_colleges(frame, 10000, "TS_EAMCET", "OC")

    assert colleges[0]["college_name"] == "Top Priority"
    assert colleges[0]["college_priority"] == 1


def test_high_rank_never_marks_low_cutoff_safe_or_suggested() -> None:
    frame = pd.DataFrame(
        [
            {"exam_type": "TS_EAMCET", "category": "OC", "college_name": "OUCE", "branch_name": "Computer Science", "opening_rank": 1, "closing_rank": 2547, "location": "Hyd", "college_priority": 1},
            {"exam_type": "TS_EAMCET", "category": "OC", "college_name": "Reachable", "branch_name": "Computer Science", "opening_rank": 1, "closing_rank": 160000, "location": "Hyd", "college_priority": 2},
        ]
    )

    colleges = match_colleges(frame, 157757, "TS_EAMCET", "OC")

    assert all(college["college_name"] != "OUCE" for college in colleges)
    assert colleges[0]["college_name"] == "Reachable"
    assert colleges[0]["chance"] == "Possible"
