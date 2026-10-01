from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from app.database import get_db
from app.models.estudiante import Estudiante, HistorialAcademico
from app.schemas.estudiante import (
    EstudianteCreate, EstudianteResponse,
    HistorialCreate, HistorialUpdate, HistorialResponse
)

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes y Tracking"])

@router.post("/", response_model=EstudianteResponse)
def registrar_estudiante(estudiante: EstudianteCreate, db: Session = Depends(get_db)):
    db_estudiante = Estudiante(**estudiante.dict())
    db.add(db_estudiante)
    db.commit()
    db.refresh(db_estudiante)
    return db_estudiante

@router.get("/", response_model=List[EstudianteResponse])
def listar_estudiantes(db: Session = Depends(get_db)):
    return db.query(Estudiante).all()

# --- ENDPOINT CLAVE: TRACKING POR CARNET (Usa el Stored Procedure) ---
@router.get("/avance/{carnet}")
def obtener_avance_carnet(carnet: str, db: Session = Depends(get_db)):
    try:
        # Ejecutamos el Stored Procedure que definimos en MySQL
        sql = text("CALL sp_obtener_avance_estudiante(:carnet)")
        result = db.execute(sql, {"carnet": carnet})
        row = result.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado o sin registro para este carnet.")
        
        avance_data = {
            "carnet": row[0],
            "estudiante": row[1],
            "carrera": row[2],
            "creditos_totales": row[3],
            "creditos_aprobados": row[4],
            "porcentaje_avance": float(row[5]) if row[5] is not None else 0.0
        }
        return avance_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- HISTORIAL ACADÉMICO ---
@router.post("/historial", response_model=HistorialResponse)
def registrar_historial(historial: HistorialCreate, db: Session = Depends(get_db)):
    db_historial = HistorialAcademico(**historial.dict())
    db.add(db_historial)
    db.commit()
    db.refresh(db_historial)
    return db_historial

@router.put("/historial/{historial_id}", response_model=HistorialResponse)
def actualizar_historial(historial_id: int, datos: HistorialUpdate, db: Session = Depends(get_db)):
    db_hist = db.query(HistorialAcademico).filter(HistorialAcademico.id == historial_id).first()
    if not db_hist:
        raise HTTPException(status_code=404, detail="Registro de historial no encontrado.")
    
    update_data = datos.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_hist, key, value)
        
    db.commit()
    db.refresh(db_hist)
    return db_hist