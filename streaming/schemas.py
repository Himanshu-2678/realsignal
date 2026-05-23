from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from typing import Optional
import uuid 


from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from typing import Optional
import uuid


class TransactionEvent(BaseModel):
    transaction_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    amount: float
    merchant_category: str
    payment_method: str

    device_id: str
    geolocation: str
    ip_address: str

    account_age_days: int

    is_fraud: Optional[bool] = False

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount must be positive")
        return value

    @field_validator("account_age_days")
    @classmethod
    def validate_account_age(cls, value):
        if value < 0:
            raise ValueError("Account age cannot be negative")
        return value