from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated, List
from routers import users, materials, priorities, categories, progresses, tasks, files, taskmaterials
import models
import pydantic_models
from database import get_db
from database import engine, SessionLocal
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]

app.include_router(users.router)
app.include_router(materials.router)
app.include_router(priorities.router)
app.include_router(categories.router)
app.include_router(progresses.router)
app.include_router(tasks.router)
app.include_router(files.router)
app.include_router(taskmaterials.router)

"""
Stored Procedure
"""
@app.get("/task-users/")
async def get_task_users(db: db_dependency):
    task_model = models.Task
    user_model = models.User
    result = db.execute(select(user_model.name, task_model.title, task_model.notice, task_model.place).join(user_model))

    return result.mappings().all()