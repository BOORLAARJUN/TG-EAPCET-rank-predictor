from app.core.preprocessing import normalize_marks


def test_normalize_marks_uses_saved_cohort() -> None:
    normalization = {
        "method": "z_score",
        "fallback_cohort": "TS_EAMCET:2026",
        "cohorts": {"TS_EAMCET:2026": {"mean": 100.0, "std": 20.0, "count": 2}},
    }

    z_score, display = normalize_marks(120.0, "TS_EAMCET", 2026, normalization)

    assert z_score == 1.0
    assert display == 60.0


def test_eamcet_official_normalization_single_session_preserves_marks() -> None:
    normalization = {
        "method": "eamcet_official",
        "fallback_cohort": "TS_EAMCET:2025:ALL",
        "global_stats": {
            "TS_EAMCET:2025": {
                "asd": 100.0,
                "top_average": 125.0,
            }
        },
        "cohorts": {
            "TS_EAMCET:2025:ALL": {
                "exam_key": "TS_EAMCET:2025",
                "asd": 100.0,
                "top_average": 125.0,
            }
        },
    }

    normalized, display = normalize_marks(110.0, "TS_EAMCET", 2025, normalization)

    assert normalized == 110.0
    assert display == 110.0
