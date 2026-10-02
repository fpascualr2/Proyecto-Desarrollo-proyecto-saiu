from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.models.usuario import Usuario
from app.models.academico import Seccion, Ciclo
from app.models.estudiante import Estudiante
from app.utils.security import get_current_user, requiere_docente

router = APIRouter(prefix="/docente", tags=["Módulo Docente"])

# --- ESQUEMAS PARA CALIFICACIONES Y CURSOS ---
class CalificacionUpdate(BaseModel):
    estudiante_id: int
    curso_id: int
    ciclo_id: int
    nota: float
    estado: str  # 'APROBADO' o 'REPROBADO'

# 1. VER CURSOS ASIGNADOS AL DOCENTE EN EL CICLO ACTIVO
@router.get("/mis-cursos")
def listar_cursos_docente(
    db: Session = Depends(get_db),
    docente: Usuario = Depends(requiere_docente)
):
    # Buscar el ciclo activo actual
    ciclo_activo = db.query(Ciclo).filter(Ciclo.activo == True).first()
    if not ciclo_activo:
        raise HTTPException(status_code=404, detail="No hay un ciclo académico activo en este momento.")

    # Buscar las secciones que imparte este docente en el ciclo activo
    secciones = db.query(Seccion).filter(
        Seccion.docente_id == docente.id,
        Seccion.ciclo_id == ciclo_activo.id
    ).all()

    resultado = []
    for sec in secciones:
        resultado.append({
            "seccion_id": sec.id,
            "nombre_seccion": sec.nombre_seccion,
            "curso_id": sec.curso.id,
            "codigo_curso": sec.curso.codigo_curso,
            "nombre_curso": sec.curso.nombre,
            "creditos": sec.curso.creditos,
            "ciclo": ciclo_activo.nombre
        })
    return resultado

# 2. CALIFICAR A UN ESTUDIANTE (Actualizar Historial Académico)
@router.post("/calificar")
def calificar_estudiante(
    data: CalificacionUpdate,
    db: Session = Depends(get_db),
    docente: Usuario = Depends(requiere_docente)
):
    from app.models.estudiante import HistorialAcademico
    
    # Validar que el estudiante exista
    estudiante = db.query(Estudiante).filter(Estudiante.id == data.estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado.")

    # Buscar si ya tiene registro en el historial para ese curso y ciclo
    historial = db.query(HistorialAcademico).filter(
        HistorialAcademico.estudiante_id == data.estudiante_id,
        HistorialAcademico.curso_id == data.curso_id,
        HistorialAcademico.ciclo_id == data.ciclo_id
    ).first()

    if historial:
        # Actualizar nota y estado
        historial.nota = data.nota
        historial.estado = data.estado
    else:
        # Crear nuevo registro si no existía
        nuevo_historial = HistorialAcademico(
            estudiante_id=data.estudiante_id,
            curso_id=data.curso_id,
            ciclo_id=data.ciclo_id,
            nota=data.nota,
            estado=data.estado
        )
        db.add(nuevo_historial)

    db.commit()
    return {"message": "Calificación registrada exitosamente con éxito."}