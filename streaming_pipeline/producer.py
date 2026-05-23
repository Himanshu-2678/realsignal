import json
import time

from kafka import KafkaProducer

from streaming.simulator import (
    stream_transactions,
)


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",

    value_serializer=lambda value: json.dumps(
        value
    ).encode("utf-8"),
)


for event in stream_transactions():

    producer.send(
        "transactions",
        value=event,
    )

    print(
        f"Produced transaction: "
        f"{event['transaction_id']}"
    )

    time.sleep(1)   