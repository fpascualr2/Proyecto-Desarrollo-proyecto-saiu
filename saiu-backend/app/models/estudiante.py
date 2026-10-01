from sqlalchemy import Column, Integer, String, Date, DECIMAL, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False)
    carnet = Column(String(20), unique=True, nullable=False)
    carrera_id = Column(Integer, ForeignKey("carreras.id"), nullable=False)
    fecha_ingreso = Column(Date, nullable=False)

    # Relaciones
    usuario = relationship("Usuario")
    carrera = relationship("Carrera", back_populates="estudiantes")
    historial = relationship("HistorialAcademico", back_populates="estudiante", cascade="all, delete")
    tramites_graduacion = relationship("EstudianteOpcionGraduacion", back_populates="estudiante", cascade="all, delete")

class HistorialAcademico(Base):
    __tablename__ = "historial_academico"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id", ondelete="CASCADE"), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)
    ciclo_id = Column(Integer, ForeignKey("ciclos.id"), nullable=False)
    nota = Column(DECIMAL(5, 2), nullable=True)
    estado = Column(Enum('CURSANDO', 'APROBADO', 'REPROBADO'), default='CURSANDO')

    # Relaciones
    estudiante = relationship("Estudiante", back_populates="historial")
    curso = relationship("Curso")
    ciclo = relationship("Ciclo")

class CursoRequisito(Base):
    __tablename__ = "curso_requisitos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    curso_id = Column(Integer, ForeignKey("cursos.id", ondelete="CASCADE"), nullable=False)
    requisito_curso_id = Column(Integer, ForeignKey("cursos.id", ondelete="CASCADE"), nullable=False)

class OpcionGraduacion(Base):
    __tablename__ = "opciones_graduacion"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    porcentaje_minimo_avance = Column(DECIMAL(5, 2), nullable=False)

    tramites = relationship("EstudianteOpcionGraduacion", back_populates="opcion")

class EstudianteOpcionGraduacion(Base):
    __tablename__ = "estudiante_opciones_graduacion"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id", ondelete="CASCADE"), nullable=False)
    opcion_id = Column(Integer, ForeignKey("opciones_graduacion.id"), nullable=False)
    estado_tramite = Column(Enum('PENDIENTE', 'EN_REVISION', 'APROBADO', 'FINALIZADO'), default='PENDIENTE')
    observaciones = Column(Text, nullable=True)

    # Relaciones
    estudiante = relationship("Estudiante", back_populates="tramites_graduacion")
    opcion = relationship("OpcionGraduacion", back_populates="tramites")