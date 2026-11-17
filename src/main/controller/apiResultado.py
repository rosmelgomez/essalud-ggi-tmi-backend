"""Resultado de un indicador por centro en un periodo."""

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user
from src.main.db.databaseConexion import get_db
from src.main.service.resultadoServ import resultadoIndicadorServ

router = APIRouter(
    prefix="/resultado",
    tags=["TMI Resultados"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/{periodo}/{id_indicador}")
def resultadoIndicador(periodo: str, id_indicador: int, origen: Optional[str] = None, db: Session = Depends(get_db)):
    """origen: ACTUAL = calculado con TOTALIZADO3; BACKUP = con la copia del cierre (TOTALIZADO3_BACKUP); sin él, el oficial."""
    return resultadoIndicadorServ(db, periodo, id_indicador, origen)
