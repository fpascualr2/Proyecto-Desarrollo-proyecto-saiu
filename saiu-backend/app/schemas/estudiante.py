from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date

class EstudianteBase(BaseModel):
    carnet: str
    carrera_id: int
    fecha_ingreso: date

class EstudianteCreate(EstudianteBase):
    usuario_id: int

class EstudianteResponse(EstudianteBase):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True

class HistorialBase(BaseModel):
    curso_id: int
    ciclo_id: int
    nota: Optional[float] = None
    estado: Optional[Literal['CURSANDO', 'APROBADO', 'REPROBADO']] = 'CURSANDO'

class HistorialCreate(HistorialBase):
    estudiante_id: int

class HistorialUpdate(BaseModel):
    nota: Optional[float] = None
    estado: Optional[Literal['CURSANDO', 'APROBADO', 'REPROBADO']] = None

class HistorialResponse(HistorialBase):
    id: int
    estudiante_id: int

    class Config:
        from_attributes = True

class TramiteGraduacionCreate(BaseModel):
    opcion_id: int
    observaciones: Optional[str] = None

class TramiteGraduacionResponse(BaseModel):
    id: int
    estudiante_id: int
    opcion_id: int
    estado_tramite: str
    observaciones: Optional[str] = None

    class Config:
        from_attributes = True

class HistorialCreate(BaseModel):
    curso_id: int
    ciclo_id: int
    nota: float = Field(..., ge=0.0, le=100.0, description="La nota debe estar entre 0 y 100")
    estado: str
    estudiante_id: int

class HistorialUpdate(BaseModel):
    nota: Optional[float] = Field(None, ge=0.0, le=100.0)
    estado: Optional[str] = None