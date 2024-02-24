from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class TaskMessage(BaseModel):
    task_type: str = Field(..., description="The type of the task to be performed")
    task_data: Dict[str, Any] = Field(..., description="Data necessary to perform the task")
    task_id: Optional[str] = Field(None, description="An optional unique identifier for the task")
