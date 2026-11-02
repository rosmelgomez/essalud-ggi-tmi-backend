"""Servicios de centros del TMI (tmi_centro y exclusión de centro por indicador)."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.main.dtos.tmiDto import (
    tmiCentroDto,
    tmiExclusionCentroEstandarDto,
)


#tmi_centro
def queryCentrosTMIServ(db: Session):
    try:
        from src.main.repositories.centroRep import queryCentrosTMI
        result = queryCentrosTMI(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryInsertCentrosTMIServ(db: Session, centro: tmiCentroDto):
    try:
        from src.main.repositories.centroRep import queryInsertCentrosTMI
        result = queryInsertCentrosTMI(db, centro)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryUpdateCentrosTMIServ(db: Session, dto:tmiCentroDto):
    try:
        from src.main.repositories.centroRep import queryUpdateCentrosTMI
        result = queryUpdateCentrosTMI(db, dto)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryDeleteCentrosTMIServ(db: Session, id:int):
    try:
        from src.main.repositories.centroRep import queryDeleteCentrosTMI
        result = queryDeleteCentrosTMI(db, id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


### tmi_exclusion_centro_indicador (exclusión de centro por indicador)
def queryExclusionCentroEstandarServ(db: Session, anio: int):
    try:
        from src.main.repositories.centroRep import queryExclusionCentroEstandar
        return queryExclusionCentroEstandar(db, anio)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryInsertExclusionCentroEstandarServ(db: Session, dto:tmiExclusionCentroEstandarDto):
    try:
        from src.main.repositories.centroRep import queryInsertExclusionCentroEstandar
        return queryInsertExclusionCentroEstandar(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryUpdateExclusionCentroEstandarServ(db: Session, dto:tmiExclusionCentroEstandarDto):
    try:
        from src.main.repositories.centroRep import queryUpdateExclusionCentroEstandar
        return queryUpdateExclusionCentroEstandar(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
