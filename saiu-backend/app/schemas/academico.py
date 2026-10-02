from pydantic import BaseModel
from typing import Optional

class CarreraBase(BaseModel):
    codigo_carrera: str
    nombre: str
    creditos_totales: int

class CarreraCreate(CarreraBase):
    pass

class CarreraResponse(CarreraBase):
    id: int

    class Config:
        from_attributes = True

class CursoBase(BaseModel):
    codigo_curso: str
    nombre: str
    creditos: int

class CursoCreate(CursoBase):
    pass

class CursoResponse(CursoBase):
    id: int

    class Config:
        from_attributes = True

class CicloBase(BaseModel):
    codigo: str  # Ej. '2026-1'
    nombre: str  # Ej. 'Primer Semestre 2026'
    activo: Optional[bool] = False

class CicloCreate(CicloBase):
    pass

class CicloResponse(CicloBase):
    id: int

    class Config:
        from_attributes = True

# --- PENSUM ---
class PensumCreate(BaseModel):
    carrera_id: int
    curso_id: int
    semestre: int

class PensumResponse(PensumCreate):
    id: int
    curso: Optional[CursoResponse] = None  # Para ver el detalle del curso anidado

    class Config:
        from_attributes = True