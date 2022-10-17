import logging
import os
import json
from aio_pika import connect_robust, abc
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def consume():
    connection = await connect_robust(
        host=os.getenv('RABBITMQ_HOST'),
        port=int(os.getenv('RABBITMQ_PORT')),
        loop=asyncio.get_running_loop()
    )
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)
    queue = await channel.declare_queue(os.getenv('PUBLISH_QUEUE'))
    await queue.consume(callback)


async def callback(message: abc.AbstractIncomingMessage):
    async with message.process():
        try:
            message = json.loads(message.body.decode())
            logger.info(f"Message received: {message}")

        except Exception as e:
            logger.error(e)
