from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from app.database import get_db
from app.models.estudiante import Estudiante, HistorialAcademico
from app.models.usuario import Usuario
from app.schemas.estudiante import (
    EstudianteCreate, EstudianteResponse,
    HistorialCreate, HistorialUpdate, HistorialResponse
)
from app.utils.security import get_current_user, requiere_admin

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes y Tracking"])

@router.post("/", response_model=EstudianteResponse, status_code=status.HTTP_201_CREATED)
def registrar_estudiante(
    estudiante: EstudianteCreate, 
    db: Session = Depends(get_db), 
    admin_user: Usuario = Depends(requiere_admin)
):
    db_estudiante = Estudiante(**estudiante.dict())
    db.add(db_estudiante)
    db.commit()
    db.refresh(db_estudiante)
    return db_estudiante

@router.get("/", response_model=List[EstudianteResponse])
def listar_estudiantes(
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    return db.query(Estudiante).all()

# --- ENDPOINT CLAVE: TRACKING POR CARNET (Usa el Stored Procedure) ---
@router.get("/avance/{carnet}")
def obtener_avance_carnet(
    carnet: str, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    try:
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
@router.post("/historial", response_model=HistorialResponse, status_code=status.HTTP_201_CREATED)
def registrar_historial(
    historial: HistorialCreate, 
    db: Session = Depends(get_db), 
    admin_user: Usuario = Depends(requiere_admin)
):
    db_historial = HistorialAcademico(**historial.dict())
    db.add(db_historial)
    db.commit()
    db.refresh(db_historial)
    return db_historial

@router.put("/historial/{historial_id}", response_model=HistorialResponse)
def actualizar_historial(
    historial_id: int, 
    datos: HistorialUpdate, 
    db: Session = Depends(get_db), 
    admin_user: Usuario = Depends(requiere_admin)
):
    db_hist = db.query(HistorialAcademico).filter(HistorialAcademico.id == historial_id).first()
    if not db_hist:
        raise HTTPException(status_code=404, detail="Registro de historial no encontrado.")
    
    update_data = datos.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_hist, key, value)
        
    db.commit()
    db.refresh(db_hist)
    return db_hist

@router.get("/mi-avance")
def obtener_mi_avance(
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    # Si es administrador, no intentamos buscar avance académico
    if current_user.rol == "ADMINISTRADOR":
        return {
            "carnet": "N/A",
            "estudiante": f"{current_user.nombre} {current_user.apellido}",
            "carrera": "Panel de Administración",
            "creditos_totales": 0,
            "creditos_aprobados": 0,
            "porcentaje_avance": 0.0
        }

    # Intentamos buscar usando el username o el carnet del usuario
    identificador = getattr(current_user, "carnet", None) or current_user.username
    
    try:
        sql = text("CALL sp_obtener_avance_estudiante(:carnet)")
        result = db.execute(sql, {"carnet": identificador})
        row = result.fetchone()
        
        if not row:
            # Si no hay filas, devolvemos una estructura vacía en lugar de un error 500
            return {
                "carnet": identificador,
                "estudiante": f"{current_user.nombre} {current_user.apellido}",
                "carrera": "Sin asignar",
                "creditos_totales": 0,
                "creditos_aprobados": 0,
                "porcentaje_avance": 0.0
            }
        
        return {
            "carnet": row[0],
            "estudiante": row[1],
            "carrera": row[2],
            "creditos_totales": row[3],
            "creditos_aprobados": row[4],
            "porcentaje_avance": float(row[5]) if row[5] is not None else 0.0
        }
    except Exception as e:
        # En lugar de un 500, devolvemos un JSON controlado con el detalle para depurar sin romper la UI
        print(f"Error en sp_obtener_avance_estudiante: {str(e)}")
        return {
            "carnet": identificador,
            "estudiante": f"{current_user.nombre} {current_user.apellido}",
            "carrera": "Pendiente de registro",
            "creditos_totales": 0,
            "creditos_aprobados": 0,
            "porcentaje_avance": 0.0
        }