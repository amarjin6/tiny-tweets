import json
import os
from pika import BlockingConnection, ConnectionParameters

connection = BlockingConnection(
    ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST'),
        heartbeat=600,
        blocked_connection_timeout=300
    )
)
channel = connection.channel()
channel.queue_declare(queue=os.getenv('PUBLISH_QUEUE'))


def publish(message: dict) -> None:
    channel.basic_publish(
        exchange='',
        routing_key=os.getenv('PUBLISH_QUEUE'),
        body=json.dumps(message)
    )
