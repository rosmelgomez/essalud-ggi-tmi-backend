"""Servicios de estándares del TMI (tmi_estandar y estándares por tipo, nivel y categoría)."""

from fastapi import HTTPException
from sqlalchemy.orm import Session



# tmi_estandar
def queryEstandarServ(db: Session):
    try:
        from src.main.repositories.estandarRep import queryEstandar
        return queryEstandar(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


