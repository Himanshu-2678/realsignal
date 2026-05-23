def build_feature_vector(
    event,
    velocity_1m,
    avg_amount_1m,
    merchant_diversity_1m,
):

    feature_vector = {
        "amount": event.amount,
        "velocity_1m": velocity_1m,
        "avg_amount_1m": avg_amount_1m,
        "merchant_diversity_1m": merchant_diversity_1m,
    }

    return feature_vector