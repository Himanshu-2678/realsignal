# inspect failed events from dead_letter_queue
import json
from kafka import KafkaConsumer
from settings import (
    KAFKA_BOOTSTRAP_SERVERS,
    DLQ_TOPIC,
)

from utils.logger import logger

consumer = KafkaConsumer(

    DLQ_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda value: json.loads(
        value.decode("utf-8")
    ),
    auto_offset_reset="earliest",
    group_id="realsignal-dlq-group",
)

logger.warning(
    "DLQ consumer started..."
)

for message in consumer:

    failed_event = message.value

    logger.error(
        f"DLQ EVENT: {failed_event}"
    )