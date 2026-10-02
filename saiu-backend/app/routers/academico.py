from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.usuario import Usuario
from app.models.academico import Carrera, Curso, Ciclo, Pensum
from app.schemas.academico import (
    CarreraCreate, CarreraResponse,
    CursoCreate, CursoResponse,
    CicloCreate, CicloResponse,
    PensumCreate, PensumResponse
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

# --- PENSUM (ASOCIAR CURSOS A CARRERAS) ---
@router.post("/pensum", response_model=PensumResponse, status_code=status.HTTP_201_CREATED)
def agregar_curso_a_pensum(
    pensum: PensumCreate, 
    db: Session = Depends(get_db), 
    admin_user: Usuario = Depends(requiere_admin)
):
    # Validar que la carrera y el curso existan
    carrera = db.query(Carrera).filter(Carrera.id == pensum.carrera_id).first()
    curso = db.query(Curso).filter(Curso.id == pensum.curso_id).first()
    
    if not carrera or not curso:
        raise HTTPException(status_code=404, detail="La carrera o el curso especificado no existen.")

    db_pensum = Pensum(**pensum.dict())
    db.add(db_pensum)
    db.commit()
    db.refresh(db_pensum)
    return db_pensum

@router.get("/carreras/{carrera_id}/pensum", response_model=List[PensumResponse])
def ver_pensum_carrera(
    carrera_id: int, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    return db.query(Pensum).filter(Pensum.carrera_id == carrera_id).all()