import random
from faker import Faker
from streaming.schemas import TransactionEvent
from settings import FRAUD_PROBABILITY

fake = Faker()


def create_customer_profile(customer_id):

    locations = ["Delhi", "Mumbai", "Bangalore", "Hyderabad"]

    amount_ranges = [
        (100, 1000),
        (500, 3000),
        (1000, 8000),
    ]

    categories = ["grocery", "food", "travel", "electronics", "gaming", "fuel"]

    profile = {
        "customer_id": customer_id,
        "home_location": random.choice(locations),
        "usual_amount_range": random.choice(amount_ranges),
        "preferred_categories": random.sample(categories, k=3),
        "account_age_days": random.randint(30, 2500)}

    return profile


def generate_normal_transaction(profile):

    min_amount, max_amount = profile["usual_amount_range"]

    amount = round(
        random.uniform(min_amount, max_amount) ,2)

    merchant_category = random.choice(
        profile["preferred_categories"])

    event = TransactionEvent(
        customer_id=profile["customer_id"],
        amount=amount,
        merchant_category=merchant_category,
        payment_method=random.choice(
            ["UPI", "Credit Card", "Debit Card"]
        ),
        device_id=fake.uuid4(),
        geolocation=profile["home_location"],
        ip_address=fake.ipv4(),
        account_age_days=profile["account_age_days"],
        is_fraud=False
    )

    return event


profile = create_customer_profile("cust_101")
event = generate_normal_transaction(profile)

#print(event.model_dump())


# creating transactions that intentionally violate customer behaviour
def generate_fraud_transaction(profile):

    suspicious_locations = ["Moscow", "Dubai", "Singapore", "London"]
    suspicious_categories = ["electronics", "gaming"]

    amount = round(random.uniform(25000, 100000), 2)

    event = TransactionEvent(
        customer_id=profile["customer_id"],
        amount=amount,
        merchant_category=random.choice(suspicious_categories),
        payment_method=random.choice(["UPI", "Credit Card", "Debit Card"]),
        device_id=fake.uuid4(),
        geolocation=random.choice(suspicious_locations),
        ip_address=fake.ipv4(),
        account_age_days=profile["account_age_days"],
        is_fraud=True,
        risk_context={
            "amount_spike": True,
            "geo_anomaly": True,
            "merchant_shift": True
        }
    )

    return event


# simulate real streaming behavior
def stream_transactions():
    
    customer_profiles = [
        create_customer_profile(f"cust_{i}")
        for i in range(1, 6)
    ]

    while True:

        profile = random.choice(customer_profiles)

        fraud_probability = random.random()

        if fraud_probability < FRAUD_PROBABILITY:
            event = generate_fraud_transaction(profile)
        else:
            event = generate_normal_transaction(profile)

        event_data = event.model_dump(mode="json")
        
        yield event_data    

