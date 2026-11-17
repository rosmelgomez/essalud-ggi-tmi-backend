"""Servicio del historial de cambios de la configuración del TMI."""

from typing import Optional

from sqlalchemy.orm import Session

from src.main.repositories import historialRep


def historialServ(db: Session, id_indicador: Optional[int] = None, tabla: Optional[str] = None, limite: int = 200):
    return historialRep.queryHistorialTMI(db, id_indicador, tabla, limite)
