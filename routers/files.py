from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from typing import Annotated, List

import models
import pydantic_models
from database import get_db
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter(
    prefix="/files",
    tags=["files"]
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_file(file: pydantic_models.File, db: db_dependency):
    db_file = models.File(**file.model_dump())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

@router.delete("/{file_id}", response_model=pydantic_models.File)
async def delete_file(file_id: int, db: db_dependency):
    db_file = db.query(models.File).filter(models.File.id == file_id).first()
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    db.delete(db_file)
    db.commit()
    return db_file

@router.put("/{file_id}", response_model=pydantic_models.File)
async def update_file(file_id: int, file_data: pydantic_models.File, db: db_dependency):
    file = db.query(models.File).filter(models.File.id == file_id).first()
    if file is None:
        raise HTTPException(status_code=404, detail='File not found')

    file.task_id = file_data.task_id
    file.file_path = file_data.file_path
    file.file_BLOB = file_data.file_BLOB

    db.commit()
    db.refresh(file)
    return file

@router.get("/{file_id}", response_model=pydantic_models.File)
def get_one_file(file_id: int, db: db_dependency):
    file = db.query(models.File).filter(models.File.id == file_id).first()
    if file is None:
        raise HTTPException(status_code=404, detail='File not found')
    return file

@router.get("", response_model=List[pydantic_models.File])
def get_all_files(db: db_dependency):
    return db.query(models.File).all()

