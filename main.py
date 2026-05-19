from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated, List
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

"""
Insert-Routes
"""
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: pydantic_models.User, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()

@app.post("/material/", status_code=status.HTTP_201_CREATED)
async def create_material(material: pydantic_models.Material, db: db_dependency):
    db_material = models.Material(**material.model_dump())
    db.add(db_material)
    db.commit()

@app.post("/category/", status_code=status.HTTP_201_CREATED)
async def create_category(category: pydantic_models.Category, db: db_dependency):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

@app.post("/priority/", status_code=status.HTTP_201_CREATED)
async def create_priority(priority: pydantic_models.Priority, db: db_dependency):
    db_priority = models.Priority(**priority.model_dump())
    db.add(db_priority)
    db.commit()
    db.refresh(db_priority)

@app.post("/progress/", status_code=status.HTTP_201_CREATED)
async def create_progress(progress: pydantic_models.Progress, db: db_dependency):
    db_progress = models.Progress(**progress.model_dump())
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)

@app.post("/task/", status_code=status.HTTP_201_CREATED)
async def create_task(task: pydantic_models.Task, db: db_dependency):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

@app.post("/file/", status_code=status.HTTP_201_CREATED)
async def create_file(file: pydantic_models.File, db: db_dependency):
    db_file = models.File(**file.model_dump())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

@app.post("/taskmaterial/", status_code=status.HTTP_201_CREATED)
async def create_taskmaterial(taskmaterial: pydantic_models.TaskMaterial, db: db_dependency):
    db_taskmaterial = models.TaskMaterial(**taskmaterial.model_dump())
    db.add(db_taskmaterial)
    db.commit()
    db.refresh(db_taskmaterial)



"""
Selects
"""
@app.get("/users/{user_id}", status_code=status.HTTP_201_CREATED)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@app.get("/users/{user_id}", response_model=pydantic_models.User)
def get_one_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.id == user_id).first()

@app.get("/users", response_model=List[pydantic_models.User])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.get("/materials/{material_id}", response_model=pydantic_models.Material)
def get_one_material(material_id: int, db: Session = Depends(get_db)):
    return db.query(models.Material).filter(models.Material.id == material_id).first()

@app.get("/materials", response_model=List[pydantic_models.Material])
def get_all_materials(db: Session = Depends(get_db)):
    return db.query(models.Material).all()

@app.get("/categories/{category_id}", response_model=pydantic_models.Category)
def get_one_category(category_id: int, db: Session = Depends(get_db)):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

@app.get("/categories", response_model=List[pydantic_models.Category])
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

@app.get("/priorities/{priority_id}", response_model=pydantic_models.Priority)
def get_one_priority(priority_id: int, db: Session = Depends(get_db)):
    return db.query(models.Priority).filter(models.Priority.id == priority_id).first()

@app.get("/priorities", response_model=List[pydantic_models.Priority])
def get_all_priorities(db: Session = Depends(get_db)):
    return db.query(models.Priority).all()

@app.get("/progresses/{progress_id}", response_model=pydantic_models.Progress)
def get_one_progress(progress_id: int, db: Session = Depends(get_db)):
    return db.query(models.Progress).filter(models.Progress.id == progress_id).first()

@app.get("/progresses", response_model=List[pydantic_models.Progress])
def get_all_progresses(db: Session = Depends(get_db)):
    return db.query(models.Progress).all()

@app.get("/tasks/{task_id}", response_model=pydantic_models.Task)
def get_one_task(task_id: int, db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

@app.get("/tasks", response_model=List[pydantic_models.Task])
def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@app.get("/files/{file_id}", response_model=pydantic_models.File)
def get_one_file(file_id: int, db: Session = Depends(get_db)):
    return db.query(models.File).filter(models.File.id == file_id).first()

@app.get("/files", response_model=List[pydantic_models.File])
def get_all_files(db: Session = Depends(get_db)):
    return db.query(models.File).all()

@app.get("/task-materials/{material_id}/{task_id}", response_model=pydantic_models.TaskMaterial)
def get_one_task_material(material_id: int, task_id: int, db: Session = Depends(get_db)):
    return db.query(models.TaskMaterial).filter(
        models.TaskMaterial.material_id == material_id, models.TaskMaterial.task_id == task_id
        ).first()

@app.get("/task-materials", response_model=List[pydantic_models.TaskMaterial])
def get_all_task_materials(db: Session = Depends(get_db)):
    return db.query(models.TaskMaterial).all()


