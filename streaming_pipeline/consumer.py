import json

from kafka import KafkaConsumer, KafkaProducer

from utils.logger import logger
from utils.dlq import send_to_dlq

from settings import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
    DLQ_TOPIC,
)

from streaming.schemas import TransactionEvent

from services.inference_service import (
    run_inference_pipeline,
)

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda value: json.loads(
        value.decode("utf-8")
    ),
    auto_offset_reset="earliest",
    group_id="realsignal-consumer-group",
)

dlq_producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda value: json.dumps(
        value
    ).encode("utf-8"),
)
schema_failure_count = 0
inference_failure_count = 0

for message in consumer:

    transaction_data = message.value

    # -----------------------------------
    # Schema Validation Stage
    # -----------------------------------

    try:
        event = TransactionEvent(
            **transaction_data
        )

    except Exception as e:

        logger.error(
            f"Schema validation failed: {str(e)}"
        )
        schema_failure_count += 1
        send_to_dlq(
            producer=dlq_producer,
            topic=DLQ_TOPIC,
            failed_event=transaction_data,
            error=e,
            stage="schema_validation",
        )

        continue

    # -----------------------------------
    # Inference Pipeline Stage
    # -----------------------------------

    try:
        (feature_vector, prediction_result) = run_inference_pipeline(event)

    except Exception as e:

        logger.error(
            f"Inference pipeline failed: {str(e)}"
        )
        inference_failure_count += 1
        send_to_dlq(
            producer=dlq_producer,
            topic=DLQ_TOPIC,
            failed_event=transaction_data,
            error=e,
            stage="inference_pipeline",
        )

        continue

    # -----------------------------------
    # Output Construction
    # -----------------------------------

    output = event.model_dump()
    output.update(feature_vector)
    output.update(prediction_result)

    # -----------------------------------
    # Logging
    # -----------------------------------

    if output["prediction"] == "anomaly":

        logger.warning(
            f"ANOMALY DETECTED: {output}"
        )
    else:
        logger.info(
            f"Normal transaction: "
            f"{output['transaction_id']}"
        )