import httpx
import asyncio

from auth import create_token
from models.tasks import TaskSchemaAdd


async def create_task():
    jwt_token = await create_token()

    url = "http://fastapi-app:8001/api/v1/tasks"

    headers = {
        "Authorization": f"Bearer {jwt_token}"
    }

    task_data = {
        "title": "Test task 2",
        "author_id": 1,
        "assignee_id": 2
    }

    try:
        task = TaskSchemaAdd(**task_data)
        print("The data has been successfully validated:", task.json())
    except Exception as e:
        print("Validation error:", e)

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=task_data, headers=headers)
        return response.json()


if __name__ == "__main__":
    asyncio.run(create_task())
