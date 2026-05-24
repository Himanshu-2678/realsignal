import pandas as pd
import random
from streaming.simulator import stream_transactions
from streaming.schemas import TransactionEvent
from features.online_features import (
    update_customer_history,
    calculate_transaction_velocity,
    calculate_average_transaction_amount,
    calculate_merchant_diversity,
)
from models.feature_pipeline import build_feature_vector


def generate_current_data(num_samples=5000):
    transaction_stream = stream_transactions()
    records = []

    for _ in range(num_samples):
        event_data = next(transaction_stream)

        event_data["amount"] *= random.uniform(1.5, 3.0)

        event = TransactionEvent(**event_data)

        update_customer_history(event)

        velocity_1m = calculate_transaction_velocity(event.customer_id)
        avg_amount_1m = calculate_average_transaction_amount(event.customer_id)
        merchant_diversity_1m = calculate_merchant_diversity(event.customer_id)

        feature_vector = build_feature_vector(
            event,
            velocity_1m,
            avg_amount_1m,
            merchant_diversity_1m,
        )

        records.append({**feature_vector, "is_fraud": event.is_fraud})

    return pd.DataFrame(records)


if __name__ == "__main__":
    dataset = generate_current_data()
    dataset.to_csv("dataset/processed/current_transactions.csv", index=False)
    print(f"Current dataset generated with {len(dataset)} records")