from settings import (
    VELOCITY_THRESHOLD,
    AVG_AMOUNT_THRESHOLD,
    MERCHANT_DIVERSITY_THRESHOLD,
    LARGE_TRANSACTION_THRESHOLD,
)

def generate_anomaly_reasons(feature_vector):
    reasons = []

    if feature_vector["velocity_1m"] > VELOCITY_THRESHOLD:
        reasons.append("High Transaction Velocity")

    if feature_vector["avg_amount_1m"] > AVG_AMOUNT_THRESHOLD:
        reasons.append("High Average Transaction Amount")

    if feature_vector["merchant_diversity_1m"] > MERCHANT_DIVERSITY_THRESHOLD:
        reasons.append("High Merchant Diversity")

    if feature_vector["amount"] > LARGE_TRANSACTION_THRESHOLD:
        reasons.append("Large Transaction Amount")

    return reasons