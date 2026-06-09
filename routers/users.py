from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from typing import Annotated, List

import models
import pydantic_models
from database import get_db
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=pydantic_models.User)
async def create_user(user: pydantic_models.User, db: db_dependency):
    result = db.execute(select(models.User).where(models.User.namr == user.name))
    existing_name = result.scalars().first()
    if existing_name:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Name already exists",
        )
    new_user = models.User(
        id=user.id,
        name=user.name,
        pwd=user.pwd,
    )

    db.add(new_user)
    db.commit()


@router.delete("/{user_id}", status_code=status.HTTP_200_OK, response_model=pydantic_models.User)
async def delete_user(user_id: int, db: db_dependency):
    db_user = db.execute(select(models.User).where(models.User.user_id == user_id))

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="User not found")
    db.delete(db_user)
    db.commit()


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=pydantic_models.User)
def get_one_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=pydantic_models.User)
async def update_user(user_id: int, user_data: pydantic_models.User, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')

    user.name = user_data.name
    user.pwd = user_data.pwd

    db.commit()
    db.refresh(user)
    return user


@router.get("/", response_model=List[pydantic_models.User])
def get_all_users(db: db_dependency):
    return db.query(models.User).all()
