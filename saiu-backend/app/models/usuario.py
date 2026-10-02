from sqlalchemy import Column, Integer, String, Enum
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False) 
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(Enum('ESTUDIANTE', 'ADMINISTRADOR', 'DOCENTE'), default='ESTUDIANTE')
    activo = Column(Integer, default=1)  # <--: 1 activo, 0 inactivo