import json
import os

import pika

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django

django.setup()

from broadcast.models import BroadcastMessage, ConsumerEventLog


QUEUE_NAME = "broadcast_queue"


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME)


def callback(ch, method, properties, body):
    event = json.loads(body)
    action = event.get("action")
    message_id = event.get("message_id")
    message = event.get("message", "")

    if action == "create":
        BroadcastMessage.objects.update_or_create(
            external_id=message_id,
            defaults={
                "message": message,
                "is_deleted": False,
                "last_action": "create",
            },
        )
    elif action == "update":
        BroadcastMessage.objects.update_or_create(
            external_id=message_id,
            defaults={
                "message": message,
                "is_deleted": False,
                "last_action": "update",
            },
        )
    elif action == "delete":
        BroadcastMessage.objects.update_or_create(
            external_id=message_id,
            defaults={
                "is_deleted": True,
                "last_action": "delete",
            },
        )

    ConsumerEventLog.objects.create(
        event_type=event.get("event_type", "broadcast.unknown"),
        message_id=message_id or "unknown",
        payload=event,
    )

    print("Received event:", event)
    print(f"Processed {action} event for message ID {message_id}")


channel.basic_consume(
    queue=QUEUE_NAME,
    on_message_callback=callback,
    auto_ack=True,
)

print("Waiting for broadcast events. To exit press CTRL+C")
channel.start_consuming()
