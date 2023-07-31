from fastapi import FastAPI
from pydantic import BaseModel
from celery.result import AsyncResult
from typing import Any
from celery_worker import generate_task, get_active_tasks, get_scheduled_tasks

app = FastAPI()


class Item(BaseModel):
    value: int


@app.post("/task/")
async def add_task(item: Item) -> Any:
    task = generate_task.delay(item.value)
    return {"task_id": task.id}


@app.get("/task/{task_id}")
async def get_task(task_id: str) -> Any:
    result = AsyncResult(task_id)
    if result.ready():
        res = result.get()
        return {"result": res[0],
                "duration": res[1]}
    else:
        return {"status": "Task not completed yet"}


@app.get("/tasks/active")
async def active_tasks() -> Any:
    return get_active_tasks()


@app.get("/tasks/scheduled")
async def active_tasks() -> Any:
    return get_scheduled_tasks()
