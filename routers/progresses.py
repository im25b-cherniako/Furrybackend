from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from typing import Annotated, List

import models
import pydantic_models
from database import get_db
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter(
    prefix="/progresses",
    tags=["progresses"]
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_progress(progress: pydantic_models.Progress, db: db_dependency):
    db_progress = models.Progress(**progress.model_dump())
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

@router.delete("/{progress_id}", response_model=pydantic_models.Progress)
async def delete_progress(progress_id: int, db: db_dependency):
    db_progress = db.query(models.Progress).filter(models.Progress.id == progress_id).first()
    if db_progress is None:
        raise HTTPException(status_code=404, detail="Progress not found")
    db.delete(db_progress)
    db.commit()
    return db_progress

@router.put("/{progress_id}", response_model=pydantic_models.Progress)
async def update_progress(progress_id: int, progress_data: pydantic_models.Progress, db: db_dependency):
    progress = db.query(models.Progress).filter(models.Progress.id == progress_id).first()
    if progress is None:
        raise HTTPException(status_code=404, detail='Progress not found')

    progress.progress = progress_data.progress

    db.commit()
    db.refresh(progress)
    return progress

@router.get("/{progress_id}", response_model=pydantic_models.Progress)
def get_one_progress(progress_id: int, db: db_dependency):
    progress = db.query(models.Progress).filter(models.Progress.id == progress_id).first()
    if progress is None:
        raise HTTPException(status_code=404, detail='Progress not found')
    return progress

@router.get("", response_model=List[pydantic_models.Progress])
def get_all_progresses(db: db_dependency):
    return db.query(models.Progress).all()