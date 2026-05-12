# Tabellen
from pydantic import BaseModel
from datetime import datetime


class Material(BaseModel):
    material_id: int
    material: str
    is_active: bool

    class Config:
        from_attributes = True

class User(BaseModel):
    user_id: int
    user_name: str
    pwd: str

    class Config:
        from_attributes = True

class Category(BaseModel):
    category_id: int
    category: str
    is_active: bool

    class Config:
        from_attributes = True

class Priority(BaseModel):
    priority_id: int
    priority: str

    class Config:
        from_attributes = True

class Progress(BaseModel):
    progress_id: int
    progress: str

    class Config:
        from_attributes = True

class Task(BaseModel):
    task_id: int
    title: str
    start: datetime
    end: datetime
    place: str
    coordinates: str
    note: str
    category_id: int
    progress_id: int
    priority_id: int
    user_id: int

    class Config:
        from_attributes = True

