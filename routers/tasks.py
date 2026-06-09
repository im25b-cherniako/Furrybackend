from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from typing import Annotated, List

import models
import pydantic_models
from database import get_db
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(task: pydantic_models.Task, db: db_dependency):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

@router.delete("/{task_id}")
async def delete_task(task_id: int, db: db_dependency):
    task = models.Task
    db_task = db.query(task).filter(task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()

@router.put("/{task_id}", response_model=pydantic_models.Task)
async def update_task(task_id: int, task_data: pydantic_models.Task, db: db_dependency):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')

    task.title = task_data.title
    task.begin = task_data.begin
    task.end = task_data.end
    task.place = task_data.place
    task.coordinates = task_data.coordinates
    task.notice = task_data.notice
    task.category_id = task_data.category_id
    task.priority_id = task_data.priority_id
    task.progress_id = task_data.progress_id
    task.user_id = task_data.user_id

    db.commit()
    db.refresh(task)
    return task

@router.get("/{task_id}", response_model=pydantic_models.Task)
def get_one_task(task_id: int, db: db_dependency):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return task

@router.get("/", response_model=List[pydantic_models.Task])
def get_all_tasks(db: db_dependency):
    return db.query(models.Task).all()

