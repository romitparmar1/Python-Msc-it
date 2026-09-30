from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date

app = FastAPI()


class Todo(BaseModel):
    name: str
    user_id: int
    due_date: date
    status: str


@app.get("/")
def read_root():
    return {"Hello": "Python"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


@app.post("/adds/")
def create_task(task: Todo):
    return {
        "name": task.name,
        "user_id": task.user_id,
        "due_date": task.due_date,
        "status": task.status
    }


