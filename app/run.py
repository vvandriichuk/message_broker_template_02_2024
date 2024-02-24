import asyncio

from brokers_handlers.sqs import SQSBroker
from repository import BrokerRepository
from utils import process_and_delete_message

broker = SQSBroker("your_sqs_queue_url")
broker_repository = BrokerRepository(broker)
broker.set_message_handler(lambda msg: asyncio.run(process_and_delete_message(msg, broker_repository)))


async def main():
    await broker_repository.listen_messages()


if __name__ == "__main__":
    asyncio.run(main())
