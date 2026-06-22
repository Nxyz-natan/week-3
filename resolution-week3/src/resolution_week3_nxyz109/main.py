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

@app.patch("/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            return task 
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    save_tasks(new_tasks)
    return {"message": f"Task {task_id} deleted"}

def main():
    import uvicorn
    uvicorn.run("resolution_week3_nxyz109.main:app", host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()