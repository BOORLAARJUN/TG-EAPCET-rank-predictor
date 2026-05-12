from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_predict_success() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/predict",
            json={
                "exam_type": "TS_EAMCET",
                "exam_year": 2026,
                "category": "OC",
                "total_marks": 124,
            },
        )
        assert response.status_code == 200
        body = response.json()
        assert body["predicted_rank"] > 0
        assert "colleges" in body


def test_predict_validation_failure() -> None:
    with TestClient(app) as client:
        response = client.post("/predict", json={"total_marks": -1})
        assert response.status_code == 422


def test_predict_rejects_unsupported_year_and_category() -> None:
    with TestClient(app) as client:
        year_response = client.post("/predict", json={"exam_year": 2035, "category": "OC", "total_marks": 80})
        category_response = client.post("/predict", json={"exam_year": 2026, "category": "INVALID", "total_marks": 80})

        assert year_response.status_code == 422
        assert category_response.status_code == 422
