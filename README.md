# RealSignal

**Adaptive Real-Time Fraud Detection & ML Monitoring System**

RealSignal is a streaming-first anomaly detection system built for real-time fraud monitoring, operational observability, and adaptive ML lifecycle management. The project simulates how production fraud monitoring infrastructure behaves in real-world ML systems environments — prioritizing operational engineering over benchmark chasing.

## System Overview

RealSignal is designed to simulate the operational lifecycle of a real-time anomaly detection system deployed in streaming environments.

The system focuses on:
- low-latency streaming inference
- online behavioral feature engineering
- anomaly detection under shifting distributions
- explainable operational predictions
- drift-aware adaptive retraining
- ML observability and lifecycle tracking

Rather than optimizing only for offline evaluation metrics, the project emphasizes production-oriented ML systems behavior including monitoring, maintainability, operational reliability, and retraining workflows.



## System Architecture

```
Transaction Generator
        ↓
Kafka Producer
        ↓
Kafka Consumer
        ↓
Online Feature Engineering
        ↓
Isolation Forest Inference
        ↓
Explainability Layer
        ↓
Drift Detection (PSI)
        ↓
Adaptive Retraining Pipeline
        ↓
MLflow Lifecycle Tracking
```


## Demo

Watch the video demo: [RealSignal Demo](https://youtu.be/zqPcyIgDgqU)

**Landing Page**
![Landing Page](assets/landing-page.png)

**Demo Section**
![Demo Section](assets/demo-section.png)

**MLflow Tracking**
![MLflow Tracking](assets/mlflow.png)


## Key Operational Metrics

- Processed and monitored 5000+ streaming transaction events using Kafka-driven online feature engineering pipelines
- Reduced false positive anomaly predictions by 97% (1261 → 36) through feature distribution stabilization and contamination threshold tuning
- Implemented PSI-based drift monitoring across 4 behavioral features with adaptive retraining workflows
- Integrated MLflow lifecycle tracking for experiment monitoring, evaluation artifacts, and retraining visibility


## Operational Capabilities

### Streaming Inference
Kafka-based producer-consumer pipeline for real-time transaction processing with event-driven inference.

### Online Feature Engineering
Behavioral features computed dynamically per transaction:
- Transaction velocity (1-minute window)
- Average transaction amount (1-minute window)
- Merchant diversity (1-minute window)

### Anomaly Detection
Isolation Forest model trained on behavioral transaction distributions. Classifies transactions as `normal` or `anomaly` based on statistical density patterns — not hardcoded rules.

### Explainability Layer
Rule-based signal explanations attached to every prediction:
- `high_transaction_velocity`
- `large_transaction_amount`
- `high_average_transaction_amount`
- `high_merchant_diversity`

Designed intentionally for low-latency streaming inference without introducing computationally expensive attribution methods.

### Drift Detection
Population Stability Index (PSI) monitors feature distribution shifts across windows:

| PSI Range | Status |
|---|---|
| < 0.1 | Stable |
| 0.1 – 0.2 | Moderate Drift |
| > 0.2 | Significant Drift |

### Adaptive Retraining
Significant drift automatically triggers the retraining pipeline — no manual intervention required.

### MLflow Tracking
Full lifecycle visibility: experiment tracking, metric logging, drift reports, retraining artifacts.

### Fault Tolerance
Dead Letter Queue (DLQ) isolates malformed events. Consumer crashes are prevented; failed messages are logged separately for inspection.



## Technology Stack

| Component | Technology |
|---|---|
| Backend API | FastAPI |
| Streaming | Apache Kafka |
| ML Model | Isolation Forest (scikit-learn) |
| Deep Learning | AutoEncoder (Pytorch) |
| Experiment Tracking | MLflow |
| Frontend | HTML / CSS / JavaScript |
| Data Processing | Pandas |
| Model Persistence | Joblib |
| Drift Monitoring | PSI (custom implementation) |



## Project Structure

```
realsignal/
├── api/
│   └── metrics_api.py          # FastAPI endpoints
├── features/
│   └── online_features.py      # Runtime feature engineering
├── models/
│   ├── generate_dataset.py
│   ├── train_isolation_forest.py
│   ├── retrain_pipeline.py
│   └── inference.py
├── monitoring/
│   └── drift_detector.py       # PSI-based drift detection
├── services/
│   └── explainability_service.py
├── streaming/                  # Kafka producer/consumer
├── streaming_pipeline/
├── frontend/
│   ├── static/
│   └── templates/
├── dataset/
│   └── processed/
├── evaluation/
├── utils/
├── experiments/
│   └── autoencoder_comparison.ipynb
└── requirements.txt
```



## Setup & Running

### Prerequisites
- Python 3.9+
- Docker (for Kafka)
- pip

### Installation

```bash
git clone <repository-url>
cd realsignal

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
```

### Start Kafka

```bash
docker-compose up
```

### Train the Model

```bash
# Generate synthetic dataset
python -m models.generate_dataset

# Train Isolation Forest
python -m models.train_isolation_forest \
  --train_data dataset/processed/transactions_dataset.csv \
  --eval_data dataset/processed/transactions_dataset.csv
```

### Start the API Server

```bash
uvicorn api.metrics_api:app --reload
```



## API Reference

### Health Check
```http
GET /health
```

### Drift Report
```http
GET /drift-report
```

### Predict Transaction
```http
POST /predict
Content-Type: application/json

{
    "amount": 1500,
    "velocity_1m": 20,
    "avg_amount_1m": 4500,
    "merchant_diversity_1m": 3
}
```

**Response:**
```json
{
    "prediction": "normal",
    "anomaly_score": -0.0842,
    "reasons": []
}
```



## Model Performance

| Metric | Value |
|---|---|
| Accuracy | 96% |
| Precision | 64% |
| Recall | 26% |
| F1 Score | 0.37 |

The precision-recall tradeoff here is intentional. Isolation Forest is optimized for catching rare behavioral anomalies, not maximizing F1. In production fraud systems, a low recall model with high precision is often preferred to reduce false positive fatigue for analysts.



## Design Decisions 

**Why Isolation Forest over supervised models?**
No labeled fraud data is available in most real-world deployments early on. Isolation Forest provides unsupervised anomaly detection based purely on behavioral density — it generalizes to novel fraud patterns rather than overfitting to known ones.

**Why rule-based explainability instead of SHAP?**
SHAP adds significant per-inference compute overhead. In a streaming system processing thousands of transactions per second, that latency is unacceptable. Rule-based signals are O(1) and interpretable enough for operational use.

**Why PSI for drift detection?**
PSI is well-understood in financial services, lightweight to compute, and interpretable without statistical background. It fits the streaming context better than more complex distribution tests.


## Architecture Evaluation

An experimental comparison between Isolation Forest and a lightweight PyTorch AutoEncoder was conducted to evaluate:
- inference latency
- operational complexity
- preprocessing overhead
- deployment suitability
- retraining maintainability

Although the AutoEncoder achieved lower raw inference latency in isolated benchmarks, Isolation Forest remained the preferred production choice due to lower operational complexity, simpler retraining workflows, and lightweight deployment requirements.


## Known Limitations

- Transaction data is synthetically generated — real fraud distributions are noisier
- Feature space is intentionally small (3 behavioral signals)
- No ground truth fraud labels — evaluation is approximate
- Streaming simulation does not replicate true Kafka throughput at scale
- Retraining is triggered by drift, not by confirmed fraud signals

These are acknowledged tradeoffs, not oversights.


## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software with proper attribution.

See the [MIT License](LICENSE) file for full details.