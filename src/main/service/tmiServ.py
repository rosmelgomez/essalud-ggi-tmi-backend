from src.main.dtos.tmiDto import (
    estandarTmiDto,
    centroTmiDto,
    tmiEstandarTipoDto,
    tmiEstandarNivelDto,
    tmiEstandarCategoriaDto,
)

from sqlalchemy.orm import Session
from fastapi import HTTPException

from typing import Optional

def calcular_periodo_anterior(periodo: str) -> str:
    try:
        if not periodo or len(periodo) != 6:
            return periodo
        anio = int(periodo[:4])
        mes = int(periodo[4:])
        if mes == 1:
            anio -= 1
            mes = 12
        else:
            mes -= 1
        return f"{anio}{mes:02d}"
    except Exception:
        return periodo

def queryEstandaresServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryEstandares
        result = queryEstandares(db, periodo)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertEstandaresPeriodoServ(db: Session, periodo: str, periodoAnterior: Optional[str] = None):
    try:
        from src.main.repositories.tmiRep import queryInsertEstandaresPeriodo
        if not periodoAnterior:
            periodoAnterior = calcular_periodo_anterior(periodo)
        result = queryInsertEstandaresPeriodo(db, periodo, periodoAnterior)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryEstandaresByCentroServ(db: Session, codcentro:str, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryEstandaresByCentro
        result = queryEstandaresByCentro(db, codcentro, periodo)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertCentrosTMIServ(db: Session, periodo: str, periodoAnterior: Optional[str] = None):
    try:
        from src.main.repositories.tmiRep import queryInsertCentrosTMI
        if not periodoAnterior:
            periodoAnterior = calcular_periodo_anterior(periodo)
        result = queryInsertCentrosTMI(db, periodo, periodoAnterior)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
def queryUpdateEstandaresServ(db: Session, dto:estandarTmiDto):
    try:
        from src.main.repositories.tmiRep import queryUpdateEstandares
        result = queryUpdateEstandares(db, dto)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryCentrosTMIServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryCentrosTMI
        result = queryCentrosTMI(db, periodo)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateCentrosTMIServ(db: Session, dto:centroTmiDto):
    try:
        from src.main.repositories.tmiRep import queryUpdateCentrosTMI
        result = queryUpdateCentrosTMI(db, dto)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryDiaEjecucionServ(db: Session, anio:int):
    try:
        from src.main.repositories.tmiRep import queryDiaEjecucion
        result = queryDiaEjecucion(db, anio)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# tmi_estandar_tipo
def queryEstandarTipoServ(db: Session, periodo: str):
    try:
        from src.main.repositories.tmiRep import queryEstandarTipo
        return queryEstandarTipo(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertEstandarTipoServ(db: Session, periodo: str, periodoAnterior: Optional[str] = None):
    try:
        from src.main.repositories.tmiRep import queryInsertEstandarTipo
        if not periodoAnterior:
            periodoAnterior = calcular_periodo_anterior(periodo)
        return queryInsertEstandarTipo(db, periodo, periodoAnterior)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateEstandarTipoServ(db: Session, dto: tmiEstandarTipoDto):
    try:
        from src.main.repositories.tmiRep import queryUpdateEstandarTipo
        return queryUpdateEstandarTipo(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# tmi_estandar_nivel
def queryEstandarNivelServ(db: Session, periodo: str):
    try:
        from src.main.repositories.tmiRep import queryEstandarNivel
        return queryEstandarNivel(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertEstandarNivelServ(db: Session, periodo: str, periodoAnterior: Optional[str] = None):
    try:
        from src.main.repositories.tmiRep import queryInsertEstandarNivel
        if not periodoAnterior:
            periodoAnterior = calcular_periodo_anterior(periodo)
        return queryInsertEstandarNivel(db, periodo, periodoAnterior)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateEstandarNivelServ(db: Session, dto: tmiEstandarNivelDto):
    try:
        from src.main.repositories.tmiRep import queryUpdateEstandarNivel
        return queryUpdateEstandarNivel(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# tmi_estandar_categoria
def queryEstandarCategoriaServ(db: Session, periodo: str):
    try:
        from src.main.repositories.tmiRep import queryEstandarCategoria
        return queryEstandarCategoria(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertEstandarCategoriaServ(db: Session, periodo: str, periodoAnterior: Optional[str] = None):
    try:
        from src.main.repositories.tmiRep import queryInsertEstandarCategoria
        if not periodoAnterior:
            periodoAnterior = calcular_periodo_anterior(periodo)
        return queryInsertEstandarCategoria(db, periodo, periodoAnterior)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateEstandarCategoriaServ(db: Session, dto: tmiEstandarCategoriaDto):
    try:
        from src.main.repositories.tmiRep import queryUpdateEstandarCategoria
        return queryUpdateEstandarCategoria(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateEstandarCategoriaServ(db: Session, dto: tmiEstandarCategoriaDto):
    try:
        from src.main.repositories.tmiRep import queryUpdateEstandarCategoria
        return queryUpdateEstandarCategoria(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







