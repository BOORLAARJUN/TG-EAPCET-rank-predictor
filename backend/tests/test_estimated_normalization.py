from app.core.estimated_normalization import clamp_marks, estimate_normalized_marks


def test_tough_shift_adjusts_marks_up() -> None:
    result = estimate_normalized_marks(70, "2026-05-09-S2")

    assert result.difficulty == "tough"
    assert result.adjusted_marks_min == 71.5
    assert result.adjusted_marks_max == 73.5
    assert result.adjusted_marks_mid == 72.5


def test_extremely_tough_shift_adjusts_marks_up() -> None:
    result = estimate_normalized_marks(70, "2026-05-10-S1")

    assert result.difficulty == "extremely_tough"
    assert result.adjusted_marks_min == 73.0
    assert result.adjusted_marks_max == 76.0
    assert result.adjusted_marks_mid == 74.5


def test_all_configured_shifts_return_an_estimate() -> None:
    expected_difficulties = {
        "2026-05-09-S1": "moderate_tough",
        "2026-05-09-S2": "tough",
        "2026-05-10-S1": "extremely_tough",
        "2026-05-10-S2": "moderate_tough",
        "2026-05-11-S1": "moderate_tough",
        "2026-05-11-S2": "tough",
    }

    for shift_id, difficulty in expected_difficulties.items():
        result = estimate_normalized_marks(70, shift_id)

        assert result.difficulty == difficulty
        assert 0 <= result.adjusted_marks_min <= 160
        assert 0 <= result.adjusted_marks_mid <= 160
        assert 0 <= result.adjusted_marks_max <= 160


def test_invalid_shift_id_falls_back_to_moderate() -> None:
    result = estimate_normalized_marks(70, "invalid-shift")

    assert result.difficulty == "moderate"
    assert result.shift_label == "invalid-shift"
    assert result.adjusted_marks_min == 70.0
    assert result.adjusted_marks_max == 71.0


def test_marks_clamped_at_160() -> None:
    assert clamp_marks(170.25) == 160.0
    assert estimate_normalized_marks(159, "2026-05-09-S2").adjusted_marks_max == 160.0


def test_marks_clamped_at_0() -> None:
    assert clamp_marks(-5.5) == 0.0
    assert estimate_normalized_marks(-1, "invalid-shift").adjusted_marks_min == 0.0
