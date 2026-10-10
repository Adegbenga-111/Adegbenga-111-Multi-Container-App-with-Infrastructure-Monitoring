
from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from pymongo import DESCENDING

from database.connection import tasks_collection
from models.task import TaskCreate


def serialize_task(task: dict) -> dict:
    """Convert a MongoDB document into JSON-friendly data."""
    return {
        "_id": str(task["_id"]),
        "title": task["title"],
        "completed": task["completed"],
        "createdAt": task["createdAt"],
    }


def get_all_tasks() -> list[dict]:
    """Return all tasks, newest first."""
    tasks = tasks_collection.find().sort(
        "createdAt",
        DESCENDING,
    )

    return [serialize_task(task) for task in tasks]


def create_task(task: TaskCreate) -> dict:
    """Create and return a new task."""
    title = task.title.strip()

    if not title:
        raise ValueError("Task title cannot be empty")

    new_task = {
        "title": title,
        "completed": False,
        "createdAt": datetime.now(timezone.utc),
    }

    result = tasks_collection.insert_one(new_task)
    new_task["_id"] = result.inserted_id

    return serialize_task(new_task)


def update_task(task_id: str, completed: bool) -> dict | None:
    """Update a task's completion status."""
    try:
        object_id = ObjectId(task_id)
    except InvalidId:
        raise ValueError("Invalid task ID")

    result = tasks_collection.update_one(
        {"_id": object_id},
        {"$set": {"completed": completed}},
    )

    if result.matched_count == 0:
        return None

    updated_task = tasks_collection.find_one(
        {"_id": object_id}
    )

    return serialize_task(updated_task)


def delete_task(task_id: str) -> bool:
    """Delete a task. Return False if it does not exist."""
    try:
        object_id = ObjectId(task_id)
    except InvalidId:
        raise ValueError("Invalid task ID")

    result = tasks_collection.delete_one(
        {"_id": object_id}
    )

    return result.deleted_count > 0
