from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.utils.security import verify_password, create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    rol: str
    nombre_completo: str

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Buscar al usuario por correo o username
    usuario = db.query(Usuario).filter(Usuario.username == form_data.username).first()
    
    if not usuario or not verify_password(form_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    if not usuario.activo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="El usuario está inactivo")

    # Crear el payload del token con los datos del usuario
    token_payload = {
        "sub": usuario.username,
        "usuario_id": usuario.id,
        "rol": usuario.rol
    }
    
    token = create_access_token(data=token_payload)

    return {
        "access_token": token,
        "token_type": "bearer",
        "rol": usuario.rol,
        "nombre_completo": f"{usuario.nombre} {usuario.apellido}"
    }