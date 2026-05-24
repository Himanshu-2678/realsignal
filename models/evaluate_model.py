import joblib
import pandas as pd

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
)


MODEL_PATH = "models/registry/isolation_forest_v1.pkl"

DATASET_PATH = (
    "dataset/processed/transactions_dataset.csv"
)

REPORT_PATH = (
    "evaluation/classification_report.txt"
)

CONFUSION_MATRIX_PATH = (
    "evaluation/confusion_matrix.txt"
)


FEATURE_COLUMNS = [
    "amount",
    "velocity_1m",
    "avg_amount_1m",
    "merchant_diversity_1m",
]


if __name__ == "__main__":

    df = pd.read_csv(DATASET_PATH)

    X = df[FEATURE_COLUMNS]

    y_true = df["is_fraud"].astype(int)

    model = joblib.load(MODEL_PATH)

    predictions = model.predict(X)

    y_pred = [
        1 if pred == -1 else 0
        for pred in predictions
    ]

    report = classification_report(
        y_true,
        y_pred,
    )

    matrix = confusion_matrix(
        y_true,
        y_pred,
    )

    print("\nClassification Report:\n")
    print(report)

    print("\nConfusion Matrix:\n")
    print(matrix)

    with open(REPORT_PATH, "w") as f:
        f.write(report)

    with open(CONFUSION_MATRIX_PATH, "w") as f:
        f.write(str(matrix))

    print("\nEvaluation artifacts saved.")