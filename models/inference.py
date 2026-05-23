import joblib
import pandas as pd
from settings import MODEL_PATH
from utils.logger import logger

model = joblib.load(MODEL_PATH)
logger.info("Isolation Forest model loaded successfully.")

def predict_anomaly(feature_vector):

    try:
        input_df = pd.DataFrame([feature_vector])

        prediction = model.predict(input_df)[0]

        anomaly_score = model.decision_function(input_df)[0]

        result = {
            "prediction": (
                "anomaly"
                if prediction == -1
                else "normal"
            ),
            "anomaly_score": round(float(anomaly_score), 4),
        }

        logger.info(f"Prediction generated: {result}")

        return result

    except Exception as error:

        logger.error(f"Inference failed: {str(error)}")

        return {
            "prediction": "error",
            "anomaly_score": None,
            "message": "Inference failed",
        }

