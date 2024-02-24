from pydantic import BaseModel


class TaskSchemaAdd(BaseModel):
    title: str
    author_id: int
    assignee_id: int