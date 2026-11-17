"""Historial de cambios de la configuración del TMI (tabla de historial)."""

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user
from src.main.db.databaseConexion import get_db
from src.main.service.historialServ import historialServ

router = APIRouter(
    prefix="/historial",
    tags=["TMI Historial"],
    dependencies=[Depends(get_current_user)],
)


@router.get("")
def historialConfigTMI(id_indicador: Optional[int] = None, tabla: Optional[str] = None, limite: int = 200,
                       db: Session = Depends(get_db)):
    """Últimos cambios de la configuración (quién, cuándo, qué campo y su valor antes y después). Filtros opcionales:
    un indicador (id_indicador) o una tabla."""
    return historialServ(db, id_indicador, tabla, limite)
