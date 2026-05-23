import json

from fastapi import FastAPI, Request

from api.schemas import PredictionRequest
from models.inference import predict_anomaly
from utils.logger import logger


app = FastAPI()

metrics = {
    "total_predictions": 0,
    "anomaly_predictions": 0,
}


with open("models/registry/metadata.json", "r") as file:
    model_metadata = json.load(file)


@app.middleware("http")
async def log_requests(request: Request, call_next):

    logger.info(
        f"{request.method} {request.url.path}"
    )

    response = await call_next(request)

    return response


@app.get("/")
def root():

    return {
        "message": "RealSignal API Running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model_loaded": True,
    }


@app.get("/metrics")
def get_metrics():

    total = metrics["total_predictions"]

    anomalies = metrics["anomaly_predictions"]

    anomaly_rate = (
        anomalies / total
        if total > 0
        else 0
    )

    return {
        "total_predictions": total,
        "anomaly_predictions": anomalies,
        "anomaly_rate": round(
            anomaly_rate,
            4,
        ),
    }


@app.get("/model-info")
def get_model_info():

    return model_metadata


@app.post("/predict")
def predict(
    transaction_features: PredictionRequest
):

    result = predict_anomaly(
        transaction_features.model_dump()
    )

    metrics["total_predictions"] += 1

    if result["prediction"] == "anomaly":
        metrics["anomaly_predictions"] += 1

    return result