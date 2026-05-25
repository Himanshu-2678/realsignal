import json
import os
import joblib

from pydantic import BaseModel

from models.inference import predict_anomaly
from services.explainability_service import generate_anomaly_reasons

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI(title="RealSignal Metrics API")

app.mount("/static", StaticFiles(directory="frontend/static"), name="static",)
templates = Jinja2Templates(directory="frontend/templates")


DRIFT_REPORT_PATH = "monitoring/drift_report.json"
MODEL_PATH = "models/registry/isolation_forest_v1.pkl"


model = joblib.load(MODEL_PATH)

class TransactionRequest(BaseModel):
    amount: float
    velocity_1m: float
    avg_amount_1m: float
    merchant_diversity_1m: float


@app.get("/", response_class=HTMLResponse,)

def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,},)

@app.get("/health")
def health_check():
    model_exists = os.path.exists(MODEL_PATH)

    return {
        "status": "healthy",
        "model_loaded": model_exists,
    }


@app.get("/drift-report")
def get_drift_report():
    if not os.path.exists(DRIFT_REPORT_PATH):
        return {
            "message": "No drift report found."
        }

    with open(DRIFT_REPORT_PATH, "r") as f:
        drift_report = json.load(f)

    return drift_report


@app.get("/metrics")
def get_metrics():
    return {
        "anomaly_detection_system": "active",
        "drift_monitoring": "enabled",
        "retraining_pipeline": "enabled",
        "dlq_support": "enabled",
    }

@app.post("/predict")
def predict_transaction(request: TransactionRequest):

    feature_vector = {
        "amount": request.amount,
        "velocity_1m": request.velocity_1m,
        "avg_amount_1m": request.avg_amount_1m,
        "merchant_diversity_1m":
        request.merchant_diversity_1m,
    }

    prediction_result = predict_anomaly(feature_vector)

    reasons = generate_anomaly_reasons(feature_vector)

    return {
        "prediction": prediction_result["prediction"],
        "anomaly_score": prediction_result["anomaly_score"],
        "reasons": reasons,
    }