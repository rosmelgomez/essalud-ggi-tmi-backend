from src.main.repositories.tmiRep import queryInsertCentrosTMI
from src.main.repositories.tmiRep import queryInsertEstandaresPeriodo
from src.main.repositories.tmiRep import queryCEConcent
from src.main.repositories.tmiRep import queryCentrosTMI
from src.main.repositories.tmiRep import queryUpdateEstandares
from src.main.repositories.tmiRep import queryEstandaresByCentro
from src.main.repositories.tmiRep import queryEstandares
from src.main.repositories.tmiRep import queryUpdateCentrosTMI

from src.main.dtos.tmiDto import estandarTmiDto
from src.main.dtos.tmiDto import centroTmiDto

from sqlalchemy.orm import Session
from fastapi import HTTPException

def queryEstandaresServ(db: Session, periodo:str):
    try:
        result = queryEstandares(db, periodo)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertEstandaresPeriodoServ(db: Session, periodo:str,periodoAnterior:str):
    try:
        result = queryInsertEstandaresPeriodo(db, periodo,periodoAnterior)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryEstandaresByCentroServ(db: Session, codcentro:str, periodo:str):
    try:
        result = queryEstandaresByCentro(db, codcentro, periodo)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertCentrosTMIServ(db: Session, periodo:str,periodoAnterior:str):
    try:
        result = queryInsertCentrosTMI(db, periodo,periodoAnterior)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
def queryUpdateEstandaresServ(db: Session, dto:estandarTmiDto):
    try:
        result = queryUpdateEstandares(db, dto)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryCentrosTMIServ(db: Session, periodo:str):
    try:
        result = queryCentrosTMI(db, periodo)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateCentrosTMIServ(db: Session, dto:centroTmiDto):
    try:
        result = queryUpdateCentrosTMI(db, dto)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryCEConcentServ(db: Session):
    try:
        result = queryCEConcent(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))