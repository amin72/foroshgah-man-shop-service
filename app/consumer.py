import asyncio
import json
import os
import sys

import aio_pika
import structlog
from tortoise import Tortoise, run_async
from tortoise.transactions import in_transaction

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.models.shop import Shop

logger = structlog.stdlib.get_logger(__name__)


# Initialize Tortoise ORM before consuming messages
async def init_tortoise():
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["app.models"]},
    )
    await Tortoise.generate_schemas()


async def create_shop_record_for_user(user_id: str) -> None:
    """
    Function to create a shop record for a user.

    Parameters:
    user_id: ID of the user (string)
    """

    async with in_transaction():
        shop = await Shop.get_or_create(owner_id=user_id)
        await logger.info("Create shop record", user_id=user_id, shop_id=shop.id)


async def callback(message: aio_pika.IncomingMessage) -> None:
    """
    Callback function to handle the received message from the queue.

    Parameters:
    message: The message content, received as bytes.
    """
    async with message.process():
        data = json.loads(message.body.decode())
        user_id = data["user_id"]
        user_type = data["user_type"]

        print(f"Received message: user_id={user_id}, user_type={user_type}")

        if user_type == "Seller":
            await create_shop_record_for_user(user_id)


async def start_listening() -> None:
    # Connect to RabbitMQ using aio_pika
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")

    async with connection:
        channel = await connection.channel()

        # Declare the queue
        queue = await channel.declare_queue("user_type_changed", durable=True)

        # Start consuming messages asynchronously
        await queue.consume(callback)

        print("Waiting for messages...\n")

        # Keep the event loop running to process messages
        await asyncio.Future()  # This is a trick to keep the loop running


async def main():
    # Initialize the database connection
    await init_tortoise()

    # Start listening to RabbitMQ messages
    await start_listening()


if __name__ == "__main__":
    run_async(main())
