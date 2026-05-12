# TS EAMCET Rank and College Predictor

A compact full-stack predictor for TS EAMCET marks. The backend normalizes marks, predicts an expected rank with a saved sklearn model, and maps the rank to likely colleges from historical cutoff data. The frontend provides single prediction and CSV upload flows.

## Project Layout

```text
backend/
  app/                 FastAPI app, schemas, services, SQLAlchemy models
  data/                Demo TS EAMCET training and cutoff CSVs
  training/            Offline model training script
  artifacts/           Generated model files after training
frontend/
  src/                 React + Vite app
```

## Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python training/train_model.py
uvicorn app.main:app --reload
```

If you have the official TGEAPCET last-rank PDFs in `backend/data`, import them before starting the backend:

```bash
python training/import_cutoffs_from_pdfs.py
python training/train_model.py
```

Useful endpoints:

- `GET /health`
- `GET /model-info`
- `POST /predict`
- `POST /predict-bulk`

Example request:

```json
{
  "exam_type": "TS_EAMCET",
  "exam_year": 2026,
  "category": "OC",
  "total_marks": 124,
  "branch_preference": "Computer Science"
}
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_BASE_URL` when the backend is not running on `http://localhost:8000`.

## Environment Variables

Backend:

- `DATABASE_URL`
- `MODEL_PATH`
- `MODEL_VERSION`
- `CORS_ORIGINS`
- `PORT`

Frontend:

- `VITE_API_BASE_URL`

## Tests

```bash
cd backend
pytest
```

## Notes

The included seed data is demo data for development and smoke testing. Replace `backend/data/seed_training_data.csv` and `backend/data/seed_college_cutoffs.csv` with verified historical TS EAMCET data before relying on predictions.
