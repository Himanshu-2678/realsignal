import json
import numpy as np
import pandas as pd

REFERENCE_DATASET = "dataset/processed/transactions_dataset.csv"
CURRENT_DATASET = "dataset/processed/current_transactions.csv"
DRIFT_REPORT_PATH = "monitoring/drift_report.json"

FEATURE_COLUMNS = [
    "amount",
    "velocity_1m",
    "avg_amount_1m",
    "merchant_diversity_1m",
]


def calculate_psi(expected, actual, bins=10):
    expected_counts, bin_edges = np.histogram(expected, bins=bins)
    actual_counts, _ = np.histogram(actual, bins=bin_edges)

    expected_percents = expected_counts / len(expected)
    actual_percents = actual_counts / len(actual)

    expected_percents = np.where(expected_percents == 0, 0.0001, expected_percents)
    actual_percents = np.where(actual_percents == 0, 0.0001, actual_percents)

    psi = np.sum(
        (actual_percents - expected_percents)
        * np.log(actual_percents / expected_percents)
    )

    return round(float(psi), 4)


def get_drift_status(psi_score):
    if psi_score < 0.1:
        return "stable"
    if psi_score < 0.25:
        return "moderate_drift"
    return "significant_drift"


if __name__ == "__main__":
    reference_df = pd.read_csv(REFERENCE_DATASET)
    current_df = pd.read_csv(CURRENT_DATASET)

    drift_report = {}

    for feature in FEATURE_COLUMNS:
        psi_score = calculate_psi(
            reference_df[feature],
            current_df[feature],
        )

        drift_report[feature] = {
            "psi_score": psi_score,
            "status": get_drift_status(psi_score),
        }

    with open(DRIFT_REPORT_PATH, "w") as f:
        json.dump(drift_report, f, indent=4)

    print("Drift report generated.")
    print(json.dumps(drift_report, indent=4))