from fastapi import APIRouter, Request

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/model-info")
def model_info(request: Request) -> dict:
    bundle = request.app.state.model_bundle
    return {
        "model_version": bundle.model_version,
        "model_name": bundle.metrics.get("selected_model", "unknown"),
        "feature_columns": bundle.feature_columns,
        "metrics": bundle.metrics,
        "normalization_method": bundle.normalization.get("method", "z_score"),
    }
