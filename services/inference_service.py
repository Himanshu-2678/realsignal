from features.online_features import (
    update_customer_history,
    calculate_transaction_velocity,
    calculate_average_transaction_amount,
    calculate_merchant_diversity,
)

from models.feature_pipeline import (
    build_feature_vector,
)

from models.inference import (
    predict_anomaly,
)


def run_inference_pipeline(event):

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

    prediction_result = predict_anomaly(
        feature_vector
    )

    return (
        feature_vector,
        prediction_result,
    )