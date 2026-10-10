from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        description="The task title",
    )

    def clean_title(self) -> str:
        return self.title.strip()


class TaskUpdate(BaseModel):
    completed: bool


class TaskResponse(BaseModel):
    id: str = Field(alias="_id")
    title: str
    completed: bool
    createdAt: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={
            datetime: lambda value: value.isoformat()
        },
    )
