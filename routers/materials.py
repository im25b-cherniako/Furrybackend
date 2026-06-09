from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from typing import Annotated, List

import models
import pydantic_models
from database import get_db
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter(
    prefix="/materials",
    tags=["materials"]
)
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_material(material: pydantic_models.Material, db: db_dependency):
    db_material = models.Material(**material.model_dump())
    db.add(db_material)
    db.commit()

@router.put("/{material_id}", response_model=pydantic_models.Material)
async def update_material(material_id: int, material_data: pydantic_models.Material, db: db_dependency):
    material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if material is None:
        raise HTTPException(status_code=404, detail='Material not found')

    material.material = material_data.material
    material.is_active = material_data.is_actie
    db.commit()
    db.refresh(material)
    return material

@router.delete("/{material_id}")
async def delete_material(material_id: int, db: db_dependency):
    material = models.Material
    db_material = db.query(material).filter(material.id == material_id).first()
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    db.delete(db_material)
    db.commit()

@router.get("/{material_id}", response_model=pydantic_models.Material)
async def get_one_material(material_id: int, db: db_dependency):
    material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if material is None:
        raise HTTPException(status_code=404, detail='Material not found')
    return material

@router.get("/", response_model=List[pydantic_models.Material])
async def get_all_materials(db: db_dependency):
    return db.query(models.Material).all()

