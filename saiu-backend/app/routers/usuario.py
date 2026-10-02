from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import datetime

from app.database import get_db
from app.models.usuario import Usuario
from app.models.estudiante import Estudiante
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.utils.security import requiere_admin, get_password_hash

router = APIRouter(prefix="/usuarios", tags=["Gestión de Usuarios"])

# 1. LISTAR TODOS LOS USUARIOS
@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db), 
    admin_user: Usuario = Depends(requiere_admin)
):
    return db.query(Usuario).all()

# 2. CREAR USUARIO (Y AUTO-REGISTRAR ESTUDIANTE)
@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    usuario: UsuarioCreate, 
    db: Session = Depends(get_db), 
    admin_user: Usuario = Depends(requiere_admin)
):
    # Verificar que username o email no existan
    if db.query(Usuario).filter((Usuario.username == usuario.username) | (Usuario.email == usuario.email)).first():
        raise HTTPException(status_code=400, detail="El username o email ya está en uso.")

    # Crear el usuario base
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        username=usuario.username,
        email=usuario.email,
        rol=usuario.rol,
        password_hash=get_password_hash(usuario.password),
        activo=1
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    # Lógica Automática: Si es estudiante, lo metemos a la tabla estudiantes
    if nuevo_usuario.rol == 'ESTUDIANTE':
        anio_actual = datetime.datetime.now().year
        # Generamos un carnet automático, ej: 2026-0005
        carnet_generado = f"{anio_actual}-{nuevo_usuario.id:04d}"
        
        nuevo_estudiante = Estudiante(
            usuario_id=nuevo_usuario.id,
            carnet=carnet_generado,
            fecha_ingreso=datetime.date.today()
        )
        db.add(nuevo_estudiante)
        db.commit()

    return nuevo_usuario

# 3. ACTUALIZAR DATOS DEL USUARIO
@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(
    usuario_id: int, 
    datos: UsuarioUpdate, 
    db: Session = Depends(get_db), 
    admin_user: Usuario = Depends(requiere_admin)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_data = datos.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)
    return usuario

# 4. SUSPENDER / ACTIVAR CUENTA (Borrado Lógico)
@router.patch("/{usuario_id}/estado", response_model=UsuarioResponse)
def cambiar_estado_usuario(
    usuario_id: int, 
    db: Session = Depends(get_db), 
    admin_user: Usuario = Depends(requiere_admin)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Prevenir que el admin se suspenda a sí mismo por error
    if usuario.id == admin_user.id:
        raise HTTPException(status_code=400, detail="No puedes suspender tu propia cuenta.")

    # Alternar el estado (de 1 a 0, o de 0 a 1)
    usuario.activo = 0 if usuario.activo == 1 else 1
    db.commit()
    db.refresh(usuario)
    return usuario