
from src.main.db.databaseConexion import SessionLocal, get_db
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.main.dtos.tmiDto import estandaresDto
from src.main.dtos.tmiDto import centroTmiDto

router = APIRouter(prefix="/tmi", tags=["TMI"])

@router.get("/conexion")
def conexion():
    try:
        from src.main.db.databaseConexion import SessionLocal
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"message": "conexion exitosa"}
    except Exception as e:
        return {"message": "conexion fallida", "error": str(e)}

@router.get("/lista-estandar")
async def queryEstandares(db: Session = Depends(get_db)):
    try:
        from src.main.service.tmiServ import queryEstandaresServ
        result = queryEstandaresServ(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/lista-estandar-by-centro/{codcentro}")
async def queryEstandaresByCentro(codcentro: str, db: Session = Depends(get_db)):
    try:
        from src.main.service.tmiServ import queryEstandaresByCentroServ
        result = queryEstandaresByCentroServ(db, codcentro)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update-estandar")
async def queryUpdateEstandares(dto: estandaresDto, db: Session = Depends(get_db)):
    try:
        from src.main.service.tmiServ import queryUpdateEstandaresServ
        result = queryUpdateEstandaresServ(db, dto)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/lista-centros")
async def queryCentrosTMI(db: Session = Depends(get_db)):
    try:
        from src.main.service.tmiServ import queryCentrosTMIServ
        result = queryCentrosTMIServ(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update-centro")
async def queryUpdateCentrosTMI(dto: centroTmiDto, db: Session = Depends(get_db)):
    try:
        from src.main.service.tmiServ import queryUpdateCentrosTMIServ
        result = queryUpdateCentrosTMIServ(db, dto)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ce-concent")
async def queryCEConcent(db: Session = Depends(get_db)):
    try:
        from src.main.service.tmiServ import queryCEConcentServ
        result = queryCEConcentServ(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))