import os
import json
import aioboto3
import botocore.exceptions
from pydantic import ValidationError

from brokers_handlers.message_broker import AbstractMessageBroker
from models.sqs import TaskMessage

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME")

class SQSBroker(AbstractMessageBroker):
    def __init__(self, queue_url, message_handler=None):
        self.queue_url = queue_url
        self.message_handler = message_handler
        self.session = aioboto3.Session(aws_access_key_id=AWS_ACCESS_KEY,
                                        aws_secret_access_key=AWS_SECRET_KEY,
                                        region_name=AWS_REGION_NAME)

    def set_message_handler(self, message_handler):
        self.message_handler = message_handler

    async def listen_messages(self):
        try:
            async with self.session.client("sqs") as sqs:
                while True:
                    response = await sqs.receive_message(
                        QueueUrl=self.queue_url,
                        MaxNumberOfMessages=10,
                        WaitTimeSeconds=20
                    )
                    messages = response.get('Messages', [])
                    if messages:
                        for raw_message in messages:
                            try:
                                message_body = raw_message["Body"]
                                message_data = json.loads(message_body)
                                task_message = TaskMessage(**message_data)
                                await self.message_handler(task_message)
                            except ValidationError as e:
                                print(f"Validation error for message: {e.json()}")
                            except json.JSONDecodeError:
                                print("Error decoding message body as JSON")
                    else:
                        print("No messages received.")
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
                print(f"Queue {self.queue_url} does not exist.")
            else:
                print(f"An error occurred: {error.response['Error']['Message']}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    async def send_message(self, task_message: TaskMessage):
        try:
            async with self.session.client("sqs") as sqs:
                message_body = task_message.json()
                await sqs.send_message(
                    QueueUrl=self.queue_url,
                    MessageBody=message_body
                )
        except botocore.exceptions.ClientError as error:
            print(f"Failed to send message: {error.response['Error']['Message']}")
        except Exception as e:
            print(f"An unexpected error occurred while sending message: {str(e)}")

    async def delete_message(self, receipt_handle):
        try:
            async with self.session.client("sqs") as sqs:
                await sqs.delete_message(
                    QueueUrl=self.queue_url,
                    ReceiptHandle=receipt_handle
                )
        except botocore.exceptions.ClientError as error:
            print(f"Failed to delete message: {error.response['Error']['Message']}")
        except Exception as e:
            print(f"An unexpected error occurred while deleting message: {str(e)}")
