from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

class UsuarioBase(BaseModel):
    nombre: str 
    apellido: str
    username: str
    email: EmailStr
    rol: Optional[Literal['ESTUDIANTE', 'ADMINISTRADOR', 'DOCENTE']] = 'ESTUDIANTE'

class UsuarioCreate(UsuarioBase):
    password: str

# <-- Schema para editar (sin pedir password, todo opcional)
class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    rol: Optional[Literal['ESTUDIANTE', 'ADMINISTRADOR', 'DOCENTE']] = None

class UsuarioResponse(UsuarioBase):
    id: int
    activo: int  # <-- Para que el frontend sepa si está suspendido

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"