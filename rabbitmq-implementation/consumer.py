import json
import pika


QUEUE_NAME = "broadcast_queue"


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME)


def callback(ch, method, properties, body):
    event = json.loads(body)
    print("Received event:", event)
    print(f"Processing broadcast message: {event['message']}")


channel.basic_consume(
    queue=QUEUE_NAME,
    on_message_callback=callback,
    auto_ack=True,
)

print("Waiting for broadcast events. To exit press CTRL+C")
channel.start_consuming()
