from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os 
import json
from typing import Optional

app = FastAPI()

TASK_FILE = "tasks.json"

class TaskBody(BaseModel):
    task: str
    priority: str = "medium"

def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

@app.get("/tasks")
async def get_tasks(done: Optional[bool] = None):
    tasks = load_tasks()
    if done is not None:
        tasks = [t for t in tasks if t["done"] == done]
    return tasks

@app.get("/tasks/search")
async def search_task(q: str):
    tasks = load_tasks()
    results = [t for t in tasks if q.lower() in t["task"].lower()]
    if not results:
        raise HTTPException(status_code=404, detail="No tasks found")
    return results

@app.post("/tasks")
async def add_task(body: TaskBody):
    tasks = load_tasks()
    if len(tasks) == 0:
        new_id = 1
    else:
        new_id = tasks[-1]["id"] + 1
    new_task = {"id": new_id, "task": body.task, "done": False, "priority": body.priority}
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task