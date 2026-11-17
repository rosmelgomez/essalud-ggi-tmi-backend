"""Servicio del resultado de un indicador por centro en un periodo."""

from typing import Optional

from sqlalchemy.orm import Session

from src.main.repositories import resultadoRep
from src.main.service.calculoServ import periodo_valido


def resultadoIndicadorServ(db: Session, periodo: str, id_indicador: int, origen: Optional[str] = None):
    """origen: ACTUAL = calculado con TOTALIZADO3; BACKUP = con la copia del cierre (TOTALIZADO3_BACKUP); sin él, el oficial."""
    return resultadoRep.queryResultadoIndicadorTMI(db, periodo_valido(periodo), id_indicador, origen)
