import httpx
import asyncio

from auth import create_token
from models.tasks import TaskSchemaAdd


async def process_message(message_body):
    # Creating a JWT token for authentication
    jwt_token = create_token()

    url = "http://fastapi-app:8001/api/v1/tasks"

    headers = {
        "Authorization": f"Bearer {jwt_token}"
    }

    # Data for creating a new task (deserializing message_body from a JSON string into a Python dictionary)
    task_data = json.loads(message_body)

    # Trying to validate task data using Pydantic
    try:
        task = TaskSchemaAdd(**task_data)
        print("The data has been successfully validated:", task.json())
    except Exception as e:
        print("Validation error:", e)

    # Asynchronously sending a request to create a task
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=task_data, headers=headers)
        return response.json()


async def process_and_delete_message(raw_message, broker_repository):
    # Processing a message
    message_body = raw_message['Body']
    await process_message(message_body)

    # Removing a processed message from the message broker
    receipt_handle = raw_message['ReceiptHandle']
    await broker_repository.delete_message(receipt_handle)
