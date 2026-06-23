from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from typing import Annotated, List

import models
import pydantic_models
from database import get_db
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_category(category: pydantic_models.Category, db: db_dependency):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}")
async def delete_category(category_id: int, db: db_dependency):
    category = models.Category
    db_category = db.query(category).filter(category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return db_category

@router.put("/{category_id}", response_model=pydantic_models.Category)
async def update_category(category_id: int, category_data: pydantic_models.Category, db: db_dependency):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='Category not found')

    category.category = category_data.category
    category.is_active = category_data.is_active

    db.commit()
    db.refresh(category)
    return category

@router.get("/{category_id}", response_model=pydantic_models.Category)
def get_one_category(category_id: int, db: db_dependency):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='Category not found')
    return category

@router.get("", response_model=List[pydantic_models.Category])
def get_all_categories(db: db_dependency):
    return db.query(models.Category).all()