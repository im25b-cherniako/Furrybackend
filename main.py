from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated
import models
import pydantic_models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: pydantic_models.User, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()


@app.get("/users/{user_id}", status_code=status.HTTP_201_CREATED)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(user_id == models.User.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return