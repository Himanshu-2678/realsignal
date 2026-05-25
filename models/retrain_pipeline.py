import subprocess
import sys
from monitoring.drift_detector import detect_drift

def retrain_model():
    print("\nStarting model retraining...\n")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "models.train_isolation_forest",

            "--train_data",
            "dataset/processed/current_transactions.csv",

            "--eval_data",
            "dataset/processed/current_transactions.csv",
        ],
        check=True,
    )

    print("\nRetraining completed.\n")


if __name__ == "__main__":
    drift_detected, drift_report = detect_drift()

    print("\nDrift Detection Report:\n")

    for feature, details in drift_report.items():
        print(
            f"{feature}: "
            f"{details['status']} "
            f"(PSI={details['psi_score']})"
        )

    if drift_detected:
        print("\nSignificant drift detected.")
        retrain_model()

    else:
        print("\nNo significant drift detected.")
        print("Retraining not required.")