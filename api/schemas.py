from pydantic import BaseModel  

class PredictionRequest(BaseModel):

    amount: float
    velocity_1m: int
    avg_amount_1m: float
    merchant_diversity_1m: int