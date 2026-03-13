import json
import uuid

import pika


QUEUE_NAME = "broadcast_queue"


def publish_broadcast_event(action, message="", message_id=None):
    resolved_message_id = message_id or uuid.uuid4().hex[:8]

    event = {
        "event_type": f"broadcast.{action}",
        "action": action,
        "message_id": resolved_message_id,
        "message": message,
    }

    print("Connecting to RabbitMQ...")
    credentials = pika.PlainCredentials("guest", "guest")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="127.0.0.1",
            port=5672,
            virtual_host="/",
            credentials=credentials,
        )
    )

    channel = connection.channel()

    print("Declaring queue...")
    channel.queue_declare(queue=QUEUE_NAME)
    print("Queue declared successfully")

    print("Publishing event to RabbitMQ:", event)
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(event),
        mandatory=True,
    )
    print("Publish success")

    connection.close()
    print("Connection closed")

    return event
