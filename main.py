from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def root():
    return "Hello World"

todos = {
    1: {
    "title": "Todo 1",
    "description": "Todo 1 Description",
    "completed": False
    },
    2: {
    "title": "Todo 2",
    "description": "Todo 2 Description",
    "completed": True
    }
}

class Todo(BaseModel):
    title: str
    description: str
    completed: bool

@app.get('/todos', status_code=status.HTTP_200_OK)
def get_todos(title: str = ""):
    results = {}
    if title != "" or title !=None:
        for id, todo in todos.items():
            if title in todo['title']:
                results[id] = todo
        return results
    return todos

@app.get('/todos/{id}')
def get_todo(id: int):
    if id not in todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todos[id]

@app.post('/todos')
def create_todos(todo_item: Todo):
    id = max(todos) + 1
    todos[id] = todo_item.dict()
    return todos[id]

@app.put('/todos/{id}')
def update_todo(id: int, todo_item: Todo):
    if id not in todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    todos[id] = todo_item.dict()
    return todos[id]

@app.delete('/todos/{id}')
def delete_todo(id: int):
    if id not in todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    del todos[id]
    return "Todo deleted"
