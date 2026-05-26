# Pydantic Tabellen
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class User(BaseModel):
    id: int
    name: str
    pwd: str

    class Config:
        orm_mode = True

class Material(BaseModel):
    id: int
    material: str
    is_active: bool

    class Config:
        orm_mode = True

class Category(BaseModel):
    id: int
    category: str
    is_active: bool

    class Config:
        orm_mode = True

class Priority(BaseModel):
    id: int
    priority: str

    class Config:
        orm_mode = True

class Progress(BaseModel):
    id: int
    progress: str

    class Config:
        orm_mode = True

class Task(BaseModel):
    id: int
    title: str
    begin: Optional[datetime] = None
    end: Optional[datetime] = None
    place: Optional[str] = None
    coordinates: Optional[str] = None
    notice: Optional[str] = None
    category_id: int
    priority_id: int
    progress_id: int
    user_id: int

    class Config:
        orm_mode = True

class File(BaseModel):
    id: int
    task_id: int
    file_path: str
    file_BLOB: bytes

    class Config:
        orm_mode = True

class TaskMaterial(BaseModel):
    task_id: int
    material_id: int
    amount: int

    class Config:
        orm_mode = True