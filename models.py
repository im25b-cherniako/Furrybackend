from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "Benutzer"
    id = Column("BenutzerID", Integer, primary_key=True)
    name = Column("BenutzerName", String(100), nullable=False)
    pwd = Column("BenutzerPWD", String(100), nullable=False)

class Material(Base):
    __tablename__ = "Material"
    id = Column("MaterialID", Integer, primary_key=True)
    material = Column("Material", String(100), nullable=False)
    active = Column("IstAktiv", Boolean, nullable=False, default=True)