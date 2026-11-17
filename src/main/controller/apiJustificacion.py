"""Justificación del cálculo: diferencias entre como fue (copia del cierre) y con los datos de hoy."""

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user
from src.main.db.databaseConexion import get_db
from src.main.service import justificacionServ

router = APIRouter(
    prefix="/justificacion",
    tags=["TMI Justificación"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/{periodo}/resumen")
def resumenCambiosTMI(periodo: str, db: Session = Depends(get_db)):
    """Por indicador: cuántos centros cambiaron entre como fue (cierre) y con los datos de hoy. Va antes de
    /{periodo}/{id_indicador} para que "resumen" no se tome como id."""
    return justificacionServ.resumenCambiosServ(db, periodo)


@router.get("/{periodo}/{id_indicador}")
def justificacionTMI(periodo: str, id_indicador: int, db: Session = Depends(get_db)):
    """Resultado de cada centro como fue (copia del cierre) y con los datos actuales, con la fórmula desarrollada."""
    return justificacionServ.justificacionServ(db, periodo, id_indicador)


@router.get("/{periodo}/{id_indicador}/{codcentro}/terminos")
def terminosJustificacionTMI(periodo: str, id_indicador: int, codcentro: int, db: Session = Depends(get_db)):
    """Valor de cada término (grupo, actividad, servicio) en cada cálculo guardado."""
    return justificacionServ.terminosJustificacionServ(db, periodo, id_indicador, codcentro)


@router.get("/{periodo}/{id_indicador}/{codcentro}/filas")
def filasJustificacionTMI(periodo: str, id_indicador: int, codcentro: int, codigo: Optional[str] = None,
                          db: Session = Depends(get_db)):
    """Filas de TOTALIZADO3 que cambiaron desde la copia del cierre (cantidad antes y ahora, quién y cuándo)."""
    return justificacionServ.filasJustificacionServ(db, periodo, id_indicador, codcentro, codigo)
