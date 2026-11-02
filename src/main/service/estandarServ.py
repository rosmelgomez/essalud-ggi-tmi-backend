"""Servicios de estándares del TMI (tmi_estandar y estándares por tipo, nivel y categoría)."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.main.dtos.tmiDto import (
    tmiEstandarDto,
    tmiEstandarTipoDto,
    tmiEstandarNivelDto,
    tmiEstandarCategoriaDto,
)


# tmi_estandar
def queryEstandarServ(db: Session):
    try:
        from src.main.repositories.estandarRep import queryEstandar
        return queryEstandar(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryInsertEstandarServ(db: Session, dto: tmiEstandarDto):
    try:
        from src.main.repositories.estandarRep import queryInsertEstandar
        return queryInsertEstandar(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryUpdateEstandarServ(db: Session, dto: tmiEstandarDto):
    try:
        from src.main.repositories.estandarRep import queryUpdateEstandar
        return queryUpdateEstandar(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryDeleteEstandarServ(db: Session, id: int):
    try:
        from src.main.repositories.estandarRep import queryDeleteEstandar
        return queryDeleteEstandar(db, id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# tmi_estandar_tipo
def queryEstandarTipoServ(db: Session, anio: int):
    try:
        from src.main.repositories.estandarRep import queryEstandarTipo
        return queryEstandarTipo(db, anio)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryInsertEstandarTipoServ(db: Session, dto:tmiEstandarTipoDto):
    try:
        from src.main.repositories.estandarRep import queryInsertEstandarTipo
        return queryInsertEstandarTipo(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryUpdateEstandarTipoServ(db: Session, dto: tmiEstandarTipoDto):
    try:
        from src.main.repositories.estandarRep import queryUpdateEstandarTipo
        return queryUpdateEstandarTipo(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryDeleteEstandarTipoServ(db: Session, id: int):
    try:
        from src.main.repositories.estandarRep import queryDeleteEstandarTipo
        return queryDeleteEstandarTipo(db, id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# tmi_estandar_nivel
def queryEstandarNivelServ(db: Session, anio: int):
    try:
        from src.main.repositories.estandarRep import queryEstandarNivel
        return queryEstandarNivel(db, anio)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryInsertEstandarNivelServ(db: Session, dto: tmiEstandarNivelDto):
    try:
        from src.main.repositories.estandarRep import queryInsertEstandarNivel
        return queryInsertEstandarNivel(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryUpdateEstandarNivelServ(db: Session, dto: tmiEstandarNivelDto):
    try:
        from src.main.repositories.estandarRep import queryUpdateEstandarNivel
        return queryUpdateEstandarNivel(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryDeleteEstandarNivelServ(db: Session, id: int):
    try:
        from src.main.repositories.estandarRep import queryDeleteEstandarNivel
        return queryDeleteEstandarNivel(db, id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# tmi_estandar_categoria
def queryEstandarCategoriaServ(db: Session, anio: int):
    try:
        from src.main.repositories.estandarRep import queryEstandarCategoria
        return queryEstandarCategoria(db, anio)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryInsertEstandarCategoriaServ(db: Session, dto: tmiEstandarCategoriaDto):
    try:
        from src.main.repositories.estandarRep import queryInsertEstandarCategoria
        return queryInsertEstandarCategoria(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryUpdateEstandarCategoriaServ(db: Session, dto: tmiEstandarCategoriaDto):
    try:
        from src.main.repositories.estandarRep import queryUpdateEstandarCategoria
        return queryUpdateEstandarCategoria(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryDeleteEstandarCategoriaServ(db: Session, id: int):
    try:
        from src.main.repositories.estandarRep import queryDeleteEstandarCategoria
        return queryDeleteEstandarCategoria(db, id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
