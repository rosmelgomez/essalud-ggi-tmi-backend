from fastapi import HTTPException
from sqlalchemy.orm import Session

def obtenerResumenEjecutivoServ(db: Session):
    try:
        from src.main.repositories.establecimiento.establecimientoRep import obtenerResumenEjecutivo
        result = obtenerResumenEjecutivo(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def obtenerDistribucionServ(db: Session, campo: str, top: int):
    try:
        from src.main.repositories.establecimiento.establecimientoRep import obtener_distribucion
        result = obtener_distribucion(db, campo, top)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))