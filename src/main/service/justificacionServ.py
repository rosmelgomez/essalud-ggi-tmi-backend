"""Servicios de la justificación del cálculo: como fue (copia del cierre) y con los datos de hoy."""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.main.repositories import justificacionRep
from src.main.service.calculoServ import periodo_valido


def resumenCambiosServ(db: Session, periodo: str):
    return justificacionRep.queryResumenCambiosTMI(db, periodo_valido(periodo))


def justificacionServ(db: Session, periodo: str, id_indicador: int):
    return justificacionRep.queryJustificacionTMI(db, periodo_valido(periodo), id_indicador)


def terminosJustificacionServ(db: Session, periodo: str, id_indicador: int, codcentro: int):
    return justificacionRep.queryTerminosResultadoTMI(db, periodo_valido(periodo), id_indicador, codcentro)


def filasJustificacionServ(db: Session, periodo: str, id_indicador: int, codcentro: int, codigo: Optional[str] = None):
    """codigo: un término de la fórmula (T1, T2...); sin él, todos."""
    if codigo is not None and not (codigo.startswith("T") and codigo[1:].isdigit()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Término inválido")
    return justificacionRep.queryFilasCambiadasTMI(db, periodo_valido(periodo), id_indicador, codcentro, codigo)
