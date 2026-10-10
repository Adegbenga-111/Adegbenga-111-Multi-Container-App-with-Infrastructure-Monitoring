from fastapi import APIRouter, HTTPException, status
from pymongo.errors import PyMongoError
from models.task import TaskCreate, TaskUpdate
from services import task_service

router = APIRouter(
    prefix="/api/tasks",
    tags=["Tasks"],
)

# CHANGED: "/" replaced with ""
@router.get("")
def get_tasks():
    try:
        return task_service.get_all_tasks()
    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="Database temporarily unavailable",
        )

# CHANGED: "/" replaced with ""
@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    try:
        return task_service.create_task(task)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="Database temporarily unavailable",
        )

@router.put("/{task_id}")
def update_task(task_id: str, task: TaskUpdate):
    try:
        updated = task_service.update_task(
            task_id,
            task.completed,
        )
        if updated is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found",
            )
        return updated
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="Database temporarily unavailable",
        )

@router.delete("/{task_id}")
def delete_task(task_id: str):
    try:
        deleted = task_service.delete_task(task_id)
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Task not found",
            )
        return {"message": "Task deleted successfully"}
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="Database temporarily unavailable",
        )
