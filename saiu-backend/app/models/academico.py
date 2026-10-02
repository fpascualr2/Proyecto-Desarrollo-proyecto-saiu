from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Carrera(Base):
    __tablename__ = "carreras"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo_carrera = Column(String(10), unique=True, nullable=False)
    nombre = Column(String(150), nullable=False)
    creditos_totales = Column(Integer, nullable=False)

    # Relaciones
    estudiantes = relationship("Estudiante", back_populates="carrera")
    pensum = relationship("Pensum", back_populates="carrera", cascade="all, delete")

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo_curso = Column(String(15), unique=True, nullable=False)
    nombre = Column(String(150), nullable=False)
    creditos = Column(Integer, nullable=False)

    # Relaciones
    pensum = relationship("Pensum", back_populates="curso", cascade="all, delete")

class Ciclo(Base):
    __tablename__ = "ciclos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo = Column(String(20), unique=True, nullable=False) # Ej. 2026-1
    nombre = Column(String(100), nullable=False) # Ej. Primer Semestre 2026
    activo = Column(Boolean, default=False)

class Pensum(Base):
    __tablename__ = "pensum"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    carrera_id = Column(Integer, ForeignKey("carreras.id", ondelete="CASCADE"), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id", ondelete="CASCADE"), nullable=False)
    semestre = Column(Integer, nullable=False)

    # Relaciones
    carrera = relationship("Carrera", back_populates="pensum")
    curso = relationship("Curso", back_populates="pensum")

class Seccion(Base):
    __tablename__ = "secciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    curso_id = Column(Integer, ForeignKey("cursos.id", ondelete="CASCADE"), nullable=False)
    docente_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    ciclo_id = Column(Integer, ForeignKey("ciclos.id", ondelete="CASCADE"), nullable=False)
    nombre_seccion = Column(String(10), default='A')

    # Relaciones
    curso = relationship("Curso")
    docente = relationship("Usuario")
    ciclo = relationship("Ciclo")