from io import StringIO

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.predict import BulkPredictionResponse, PredictionRequest, PredictionResponse
from app.services.predictor import persist_prediction_log, predict_one

router = APIRouter(tags=["prediction"])


@router.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest, request: Request, db: Session | None = Depends(get_db)) -> PredictionResponse:
    response = predict_one(payload, request.app.state.model_bundle)
    persist_prediction_log(db, payload, response)
    return response


@router.post("/predict-bulk", response_model=BulkPredictionResponse)
async def predict_bulk(request: Request, file: UploadFile = File(...)) -> BulkPredictionResponse:
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a CSV file.")

    content = (await file.read()).decode("utf-8-sig")
    try:
        frame = pd.read_csv(StringIO(content))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not parse CSV: {exc}") from exc

    results = []
    errors = []
    for index, row in frame.iterrows():
        try:
            payload = PredictionRequest(
                exam_type=row.get("exam_type", "TS_EAMCET"),
                exam_year=int(row.get("exam_year", 2026)),
                category=row.get("category", "OC"),
                total_marks=float(row["total_marks"]),
                branch_preference=row.get("branch_preference") if pd.notna(row.get("branch_preference")) else None,
            )
            results.append({"row": int(index) + 1, "prediction": predict_one(payload, request.app.state.model_bundle)})
        except Exception as exc:
            errors.append({"row": int(index) + 1, "error": str(exc)})

    return BulkPredictionResponse(results=results, errors=errors)
