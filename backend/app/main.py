from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_health import router as health_router
from app.api.routes_predict import router as predict_router
from app.core.config import get_settings
from app.core.database import Base, engine
from app.core.model_loader import load_model_bundle

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if engine is not None:
        Base.metadata.create_all(bind=engine)

    app.state.model_bundle = load_model_bundle(settings)

    yield


app = FastAPI(
    title="TS EAMCET Rank Predictor",
    version=settings.model_version,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "ok"}


app.include_router(health_router)
app.include_router(predict_router)