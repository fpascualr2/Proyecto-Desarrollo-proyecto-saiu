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

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"