from functools import lru_cache
import os
from pathlib import Path


class Settings:
    def __init__(self) -> None:
        self.app_env = os.getenv("APP_ENV", "development")
        self.database_url = os.getenv("DATABASE_URL") or None
        self.model_path = Path(os.getenv("MODEL_PATH", "artifacts/model.joblib"))
        self.artifacts_dir = Path(os.getenv("ARTIFACTS_DIR", "artifacts"))
        self.seed_training_csv = Path(os.getenv("SEED_TRAINING_CSV", "data/seed_training_data.csv"))
        self.seed_cutoffs_csv = Path(os.getenv("SEED_CUTOFFS_CSV", "data/college_cutoffs_imported.csv"))
        self.college_priority_csv = Path(os.getenv("COLLEGE_PRIORITY_CSV", "data/Clgpriority.csv"))
        self.model_version = os.getenv("MODEL_VERSION", "v1")
        self.cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
