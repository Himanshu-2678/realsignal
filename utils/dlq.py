from datetime import datetime
from utils.logger import logger

def send_to_dlq(
    producer,
    topic,
    failed_event,
    error,
    stage,
):

    dlq_payload = {
        "failed_event": failed_event,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "consumer_stage": stage,
        "retry_count": 0,
        "failed_at": datetime.utcnow().isoformat(),
    }

    try:
        producer.send(
            topic,
            value=dlq_payload,
        )

        logger.warning(
            f"Event routed to DLQ from {stage}"
        )

    except Exception as dlq_error:

        logger.critical(
            f"DLQ publish failed: "
            f"{str(dlq_error)}"
        )