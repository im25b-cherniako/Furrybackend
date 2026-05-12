from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey, BLOB
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "Benutzer"
    id = Column("BenutzerID", Integer, primary_key=True)
    name = Column("BenutzerName", String(100), nullable=False)
    pwd = Column("BenutzerPWD", String(100), nullable=False)

    task_owner = relationship("Task", back_populates="users")
class Material(Base):
    __tablename__ = "Material"
    id = Column("MaterialID", Integer, primary_key=True)
    material = Column("Material", String(100), nullable=False)
    is_active = Column("IstAktiv", Boolean, nullable=False, default=True)

    task_material_owner = relationship("TaskMaterial", back_populates="materials")
class Category(Base):
    __tablename__ = "Kategorie"
    id = Column("KategorieID", Integer, primary_key=True)
    category = Column("Kategorie", String(100), nullable=False)
    is_active = Column("IstAktiv", Boolean, nullable=False, default=True)

    tasks = relationship("Task", back_populates="categories")

class Priority(Base):
    __tablename__ = "Prioritaet"
    id = Column("PrioritaetID", Integer, primary_key=True)
    priority = Column("Prioritaet", String(100), nullable=False)

    tasks = relationship("Task", back_populates="priorities")

class Progress(Base):
    __tablename__ = "Fortschritt"
    id = Column("FortschrittID", Integer, primary_key=True)
    progress = Column("Fortschritt", String(100), nullable=False)

    tasks = relationship("Task", back_populates="progresses")

class Task(Base):
    __tablename__ = "Aufgabe"
    id = Column("AufgabeID", Integer, primary_key=True)
    title = Column("Titel", String(100), nullable=False)
    begin = Column("Beginn", DateTime, nullable=True)
    end = Column("Ende", DateTime, nullable=True)
    place = Column("Ort", String(250), nullable=True)
    coordinates = Column("Koordinaten", String(250), nullable=True)
    notice = Column("Notiz", Text, nullable=True)
    category_id = Column("KategorieID", Integer, ForeignKey("Kategorie.KategorieID"))
    priority_id = Column("PrioritaetID", Integer, ForeignKey("Prioritaet.PrioritaetID"))
    progress_id = Column("FortschrittID", Integer, ForeignKey("Fortschritt.FortschrittID"))
    user_id = Column("BenutzerID", Integer, ForeignKey("Benutzer.BenutzerID"))

    categories = relationship("Category", back_populates="tasks")
    priorities = relationship("Priority", back_populates="tasks")
    progresses = relationship("Progress", back_populates="tasks")
    users = relationship("User", back_populates="tasks")
    files = relationship("File", back_populates="tasks")
    task_materials = relationship("TaskMaterial", back_populates="tasks")

class File(Base):
    __tablename__ = "Datei"
    id = Column("DateiID", Integer, primary_key=True)
    task_id = Column("AufgabeID", Integer, ForeignKey("Aufgabe.AufgabeID"))
    file_path = Column("Dateipfad", String(250))
    file_BLOB = Column("DateiBLOB", BLOB)

    tasks = relationship("Task", back_populates="files")
class TaskMaterial(Base):
    __tablename__ = "AufgabeMaterial"
    task_id = Column("AufgabeID", Integer, ForeignKey("Aufgabe.AufgabeID"), primary_key=True)
    material_id = Column("MaterialID", Integer, ForeignKey("Material.MaterialID"), primary_key=True)
    amount = Column("Anzahl", Integer, nullable=True)

    tasks = relationship("Task", back_populates="task_materials")
    materials = relationship("Material", back_populates="task_materials")