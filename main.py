from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import fetch_one_todo, fetch_all_todos, create_todo, update_todo, remove_todo
from models import Todo

app = FastAPI()
origins = ["http://localhost:3000/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def index():
    return {"_id": 1}


@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    if response:
        return response
    raise HTTPException(404, "No documents found.")


@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_title(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, "The document {} was not found on this server.".format(str(title)))


@app.post("/api/todo", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Bad Request")


@app.put("/api/todo/{title}", response_model=Todo)
async def update_todo(title: str, description: str):
    response = await update_todo(title, description)
    if response:
        return response
    raise HTTPException(404, "Document not found.") 


@app.delete("api/todo/{title}", response_model=Todo)
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return response
    raise HTTPException(404, "Document not found.")

