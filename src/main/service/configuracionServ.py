"""Servicios de la configuración del TMI: scripts SQL y validación."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.main.repositories import configuracionRep


def ejecutarSqlServ() -> dict:
    """Vuelve a ejecutar los scripts de src/resources/sql/tmi; 500 con el detalle si alguno falla."""
    from src.main.db.sqlRunner import ejecutar_scripts
    resultado = ejecutar_scripts()
    if any(estado != "OK" for estado in resultado.values()):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=resultado)
    return resultado


def validarConfigServ(db: Session):
    return configuracionRep.queryValidarConfigTMI(db)

