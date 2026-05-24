from settings import (
    VELOCITY_THRESHOLD,
    AVG_AMOUNT_THRESHOLD,
    MERCHANT_DIVERSITY_THRESHOLD,
    LARGE_TRANSACTION_THRESHOLD,
)

def generate_anomaly_reasons(feature_vector):
    reasons = []

    if feature_vector["velocity_1m"] > VELOCITY_THRESHOLD:
        reasons.append("high_transaction_velocity")

    if feature_vector["avg_amount_1m"] > AVG_AMOUNT_THRESHOLD:
        reasons.append("high_average_transaction_amount")

    if feature_vector["merchant_diversity_1m"] > MERCHANT_DIVERSITY_THRESHOLD:
        reasons.append("high_merchant_diversity")

    if feature_vector["amount"] > LARGE_TRANSACTION_THRESHOLD:
        reasons.append("large_transaction_amount")

    return reasons