from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel

app = FastAPI()

class TaskBase(BaseModel):
    title: str
    description: str

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    status: bool

tasks_db = []

@app.get("/tasks", response_model=List[Task])
def read_tasks(skip: int = 0, limit: int = 10):
    return tasks_db[skip : skip + limit]

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if task:
        return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    task_id = len(tasks_db) + 1
    new_task = {"id": task_id, "status": False, **task.dict()}
    tasks_db.append(new_task)
    return new_task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate):
    existing_task = next((t for t in tasks_db if t["id"] == task_id), None)
    if existing_task:
        existing_task.update({"status": False, **task.dict()})
        return existing_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if task:
        tasks_db.remove(task)
        return task
    raise HTTPException(status_code=404, detail="Task not found")