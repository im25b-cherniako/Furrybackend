from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from typing import Annotated, List

import models
import pydantic_models
from database import get_db
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter(
    prefix="/priorities",
    tags=["priorities"]
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_priority(priority: pydantic_models.Priority, db: db_dependency):
    db_priority = models.Priority(**priority.model_dump())
    db.add(db_priority)
    db.commit()
    db.refresh(db_priority)
    return db_priority

@router.delete("/{priority_id}", response_model=pydantic_models.Priority)
async def delete_priority(priority_id: int, db: db_dependency):
    db_priority = db.query(models.Priority).filter(models.Priority.id == priority_id).first()
    if db_priority is None:
        raise HTTPException(status_code=404, detail="Priority not found")
    db.delete(db_priority)
    db.commit()
    return db_priority

@router.put("/{priority_id}", response_model=pydantic_models.Priority)
async def update_priority(priority_id: int, priority_data: pydantic_models.Priority, db: db_dependency):
    priority = db.query(models.Priority).filter(models.Priority.id == priority_id).first()
    if priority is None:
        raise HTTPException(status_code=404, detail='Priority not found')

    priority.priority = priority_data.priority

    db.commit()
    db.refresh(priority)
    return priority

@router.get("/{priority_id}", response_model=pydantic_models.Priority)
def get_one_priority(priority_id: int, db: db_dependency):
    priority = db.query(models.Priority).filter(models.Priority.id == priority_id).first()
    if priority is None:
        raise HTTPException(status_code=404, detail='Priority not found')
    return priority

@router.get("", response_model=List[pydantic_models.Priority])
def get_all_priorities(db: db_dependency):
    return db.query(models.Priority).all()

