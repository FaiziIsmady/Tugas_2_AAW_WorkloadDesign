import json
import pika


QUEUE_NAME = "broadcast_queue"


def publish_broadcast_event(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME)

    event = {
        "event_type": "broadcast.sent",
        "message": message,
    }

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(event),
    )

    connection.close()

    return event
