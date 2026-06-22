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

