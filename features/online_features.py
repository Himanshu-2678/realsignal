from collections import defaultdict, deque
from datetime import datetime, timezone, timedelta

customer_transaction_history = defaultdict(
    lambda: deque(maxlen=100)
)

def update_customer_history(event):
    customer_id = event.customer_id
    customer_transaction_history[customer_id].append(event)


def get_recent_transactions(customer_id, window_minutes=1):

    transactions = customer_transaction_history[customer_id]
    current_time = datetime.now(timezone.utc)

    window_start_time = current_time - timedelta(
        minutes=window_minutes
    )

    recent_transactions = [
        txn for txn in transactions
        if txn.timestamp >= window_start_time
    ]

    return recent_transactions


# total transaction velocity
def calculate_transaction_velocity(customer_id):

    recent_transactions = get_recent_transactions(
        customer_id
    )

    return len(recent_transactions)


# average transaction veloctiy
def calculate_average_transaction_amount(customer_id):

    recent_transactions = get_recent_transactions(
        customer_id
    )

    if not recent_transactions:
        return 0

    total_amount = sum(
        txn.amount for txn in recent_transactions
    )

    average_amount = (
        total_amount / len(recent_transactions)
    )

    return round(average_amount, 2)


def calculate_merchant_diversity(customer_id):

    recent_transactions = get_recent_transactions(
        customer_id
    )

    unique_categories = {
        txn.merchant_category
        for txn in recent_transactions
    }

    return len(unique_categories)