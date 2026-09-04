from src.main.repositories.tmiRep import queryCEConcent
from src.main.repositories.tmiRep import queryCentrosTMI
from src.main.repositories.tmiRep import queryUpdateEstandares
from src.main.repositories.tmiRep import queryEstandaresByCentro
from src.main.repositories.tmiRep import queryEstandares
from src.main.repositories.tmiRep import queryUpdateCentrosTMI

from src.main.dtos.tmiDto import estandaresDto
from src.main.dtos.tmiDto import centroTmiDto

from sqlalchemy.orm import Session
from fastapi import HTTPException

def queryEstandaresServ(db: Session):
    try:
        result = queryEstandares(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryEstandaresByCentroServ(db: Session, codcentro:str):
    try:
        result = queryEstandaresByCentro(db, codcentro)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateEstandaresServ(db: Session, dto:estandaresDto):
    try:
        result = queryUpdateEstandares(db, dto)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryCentrosTMIServ(db: Session):
    try:
        result = queryCentrosTMI(db)
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