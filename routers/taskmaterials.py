from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from typing import Annotated, List

import models
import pydantic_models
from database import get_db
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter(
    prefix="/taskmaterials",
    tags=["taskmaterials"]
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_taskmaterial(taskmaterial: pydantic_models.TaskMaterial, db: db_dependency):
    db_taskmaterial = models.TaskMaterial(**taskmaterial.model_dump())
    db.add(db_taskmaterial)
    db.commit()
    db.refresh(db_taskmaterial)
    return db_taskmaterial

@router.delete("/{task_id}/{material_id}", response_model=pydantic_models.TaskMaterial)
async def delete_taskmaterial(task_id: int, material_id: int, db: db_dependency):
    db_taskmaterial = db.query(models.TaskMaterial).filter(
        models.TaskMaterial.task_id == task_id, models.TaskMaterial.material_id == material_id).first()
    if db_taskmaterial is None:
        raise HTTPException(status_code=404, detail="Connection not found")
    db.delete(db_taskmaterial)
    db.commit()
    return db_taskmaterial

@router.put("/{task_id}/{material_id}", response_model=pydantic_models.TaskMaterial)
async def update_task_material(task_id: int, material_id: int, task_material_data: pydantic_models.TaskMaterial, db: db_dependency):
    task_material = db.query(models.TaskMaterial).filter(
        models.TaskMaterial.task_id == task_id, models.TaskMaterial.material_id == material_id
        ).first()
    if task_material is None:
        raise HTTPException(status_code=404, detail='Connection not found')

    task_material.material_id = task_material_data.material_id
    task_material.task_id = task_material_data.task_id
    task_material.amount = task_material_data.amount

    db.commit()
    db.refresh(task_material)
    return task_material

@router.get("/{material_id}/{task_id}", response_model=pydantic_models.TaskMaterial)
def get_one_task_material(material_id: int, task_id: int, db: db_dependency):
    task_material = db.query(models.TaskMaterial).filter(
        models.TaskMaterial.material_id == material_id, models.TaskMaterial.task_id == task_id
        ).first()
    if task_material is None:
        raise HTTPException(status_code=404, detail='Connection not found')
    return task_material

@router.get("", response_model=List[pydantic_models.TaskMaterial])
def get_all_task_materials(db: db_dependency):
    return db.query(models.TaskMaterial).all()