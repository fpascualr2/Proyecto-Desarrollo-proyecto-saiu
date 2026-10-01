from pydantic import BaseModel
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