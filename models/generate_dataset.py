import pandas as pd

from streaming.simulator import stream_transactions
from streaming.schemas import TransactionEvent

from features.online_features import (
    update_customer_history,
    calculate_transaction_velocity,
    calculate_average_transaction_amount,
    calculate_merchant_diversity,
)

from models.feature_pipeline import (
    build_feature_vector,
)


def generate_dataset(num_samples=5000):

    transaction_stream = stream_transactions()

    records = []

    for _ in range(num_samples):

        event_data = next(transaction_stream)

        event = TransactionEvent(**event_data)

        update_customer_history(event)

        velocity_1m = calculate_transaction_velocity(
            event.customer_id
        )

        avg_amount_1m = (
            calculate_average_transaction_amount(
                event.customer_id
            )
        )

        merchant_diversity_1m = (
            calculate_merchant_diversity(
                event.customer_id
            )
        )

        feature_vector = build_feature_vector(
            event,
            velocity_1m,
            avg_amount_1m,
            merchant_diversity_1m,
        )

        record = {
            **feature_vector,
            "is_fraud": event.is_fraud,
        }

        records.append(record)

    df = pd.DataFrame(records)

    return df


if __name__ == "__main__":

    dataset = generate_dataset()

    dataset.to_csv(
        "dataset/processed/transactions_dataset.csv",
        index=False,
    )

    print(
        f"Dataset generated with "
        f"{len(dataset)} records"
    )