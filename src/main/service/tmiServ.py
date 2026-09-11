from src.main.dtos.tmiDto import estandarTmiDto
from src.main.dtos.tmiDto import centroTmiDto

from sqlalchemy.orm import Session
from fastapi import HTTPException

def queryEstandaresServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryEstandares
        result = queryEstandares(db, periodo)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertEstandaresPeriodoServ(db: Session, periodo:str,periodoAnterior:str):
    try:
        from src.main.repositories.tmiRep import queryInsertEstandaresPeriodo
        result = queryInsertEstandaresPeriodo(db, periodo,periodoAnterior)
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

def queryInsertCentrosTMIServ(db: Session, periodo:str,periodoAnterior:str):
    try:
        from src.main.repositories.tmiRep import queryInsertCentrosTMI
        result = queryInsertCentrosTMI(db, periodo,periodoAnterior)
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






