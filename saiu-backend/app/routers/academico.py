from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.academico import Carrera, Curso, Ciclo
from app.models.usuario import Usuario
from app.schemas.academico import (
    CarreraCreate, CarreraResponse,
    CursoCreate, CursoResponse,
    CicloCreate, CicloResponse
)
from app.utils.security import get_current_user, requiere_admin

router = APIRouter(prefix="/academico", tags=["Académico"])

# --- CARRERAS ---
@router.post("/carreras", response_model=CarreraResponse, status_code=status.HTTP_201_CREATED)
def crear_carrera(
    carrera: CarreraCreate, 
    db: Session = Depends(get_db), 
    admin_user: Usuario = Depends(requiere_admin)
):
    db_carrera = Carrera(**carrera.dict())
    db.add(db_carrera)
    db.commit()
    db.refresh(db_carrera)
    return db_carrera

@router.get("/carreras", response_model=List[CarreraResponse])
def listar_carreras(
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    return db.query(Carrera).all()

# --- CURSOS ---
@router.post("/cursos", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
def crear_curso(
    curso: CursoCreate, 
    db: Session = Depends(get_db), 
    admin_user: Usuario = Depends(requiere_admin)
):
    db_curso = Curso(**curso.dict())
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

@router.get("/cursos", response_model=List[CursoResponse])
def listar_cursos(
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    return db.query(Curso).all()

# --- CICLOS ---
@router.post("/ciclos", response_model=CicloResponse, status_code=status.HTTP_201_CREATED)
def crear_ciclo(
    ciclo: CicloCreate, 
    db: Session = Depends(get_db), 
    admin_user: Usuario = Depends(requiere_admin)
):
    db_ciclo = Ciclo(**ciclo.dict())
    db.add(db_ciclo)
    db.commit()
    db.refresh(db_ciclo)
    return db_ciclo

@router.get("/ciclos", response_model=List[CicloResponse])
def listar_ciclos(
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    return db.query(Ciclo).all()