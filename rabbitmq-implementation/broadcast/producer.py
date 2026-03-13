import json
import uuid

import pika


QUEUE_NAME = "broadcast_queue"


def publish_broadcast_event(action, message="", message_id=None):
    resolved_message_id = message_id or uuid.uuid4().hex[:8]
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME)

    event = {
        "event_type": f"broadcast.{action}",
        "action": action,
        "message_id": resolved_message_id,
        "message": message,
    }

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(event),
    )

    connection.close()

    return event
