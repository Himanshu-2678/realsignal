import pandas as pd
import joblib 

from streaming.simulator import stream_transactions
from sklearn.ensemble import IsolationForest

from settings import (
    MODEL_PATH,
    N_ESTIMATORS,
    CONTAMINATION,
)

from features.online_features import (
    update_customer_history,
    calculate_transaction_velocity,
    calculate_average_transaction_amount,
    calculate_merchant_diversity,
)

from models.feature_pipeline import (
    build_feature_vector
)

dataset = []

stream = stream_transactions()

for _ in range(500):

    event = next(stream)
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

    feature_vector["is_fraud"] = event.is_fraud

    dataset.append(feature_vector)


# converting the dataset into dataframe
df = pd.DataFrame(dataset)

print(df.head())

print(df.shape)



"""
Model Building
"""

X = df.drop(columns=["is_fraud"])

model = IsolationForest(
    n_estimators=N_ESTIMATORS,
    contamination=CONTAMINATION,
    random_state=42,
)

model.fit(X)

predictions = model.predict(X)


"""
Isolation Forest outputs: 1 = Normal, -1 = Anomaly
"""


df["anomaly_prediction"] = predictions

df["anomaly_prediction"] = (
    df["anomaly_prediction"] == -1
)

fraud_detected = df[
    (df["is_fraud"] == True)
    &
    (df["anomaly_prediction"] == True)
]

print("\nFraud Transactions Detected:")
print(len(fraud_detected))

print("\nTotal Fraud Transactions:")
print(df["is_fraud"].sum())

# saving the model
joblib.dump(
    model,
    MODEL_PATH,
)