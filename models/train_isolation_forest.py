import joblib
import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
)

from settings import MODEL_PATH, N_ESTIMATORS, CONTAMINATION

TRAIN_DATASET_PATH = "dataset/processed/transactions_dataset.csv"
EVAL_DATASET_PATH = "dataset/processed/current_transactions.csv"

FEATURE_COLUMNS = [
    "amount",
    "velocity_1m",
    "avg_amount_1m",
    "merchant_diversity_1m",
]

train_df = pd.read_csv(TRAIN_DATASET_PATH)
eval_df = pd.read_csv(EVAL_DATASET_PATH)

X_train = train_df[FEATURE_COLUMNS]
X_eval = eval_df[FEATURE_COLUMNS]
y_true = eval_df["is_fraud"].astype(int)

mlflow.set_experiment("RealSignal-Anomaly-Detection")

with mlflow.start_run():
    model = IsolationForest(
        n_estimators=N_ESTIMATORS,
        contamination=CONTAMINATION,
        random_state=42,
    )

    model.fit(X_train)

    predictions = model.predict(X_eval)

    y_pred = [1 if p == -1 else 0 for p in predictions]

    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    accuracy = accuracy_score(y_true, y_pred)

    report = classification_report(y_true, y_pred)
    matrix = confusion_matrix(y_true, y_pred)

    print("\nClassification Report:\n")
    print(report)

    print("\nConfusion Matrix:\n")
    print(matrix)

    mlflow.log_param("n_estimators", N_ESTIMATORS)
    mlflow.log_param("contamination", CONTAMINATION)

    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)
    mlflow.log_metric("accuracy", accuracy)

    with open("evaluation/classification_report.txt", "w") as f:
        f.write(report)

    with open("evaluation/confusion_matrix.txt", "w") as f:
        f.write(str(matrix))

    mlflow.log_artifact("evaluation/classification_report.txt")
    mlflow.log_artifact("evaluation/confusion_matrix.txt")

    if pd.io.common.file_exists("monitoring/drift_report.json"):
        mlflow.log_artifact("monitoring/drift_report.json")

    joblib.dump(model, MODEL_PATH)

    mlflow.sklearn.log_model(sk_model=model, name="isolation_forest_model",)

    print("\nMLflow tracking completed.")