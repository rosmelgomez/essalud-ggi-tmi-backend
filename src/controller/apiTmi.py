
from src.db.databaseConexion import SessionLocal
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import text

router = APIRouter()


@router.get("/conexion")
def conexion():
    try:
        from src.db.databaseConexion import SessionLocal
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"message": "conexion exitosa"}
    except Exception as e:
        return {"message": "conexion fallida", "error": str(e)}

@router.get("/lista-estandar")
async def queryEstandares(db: SessionLocal):
    try:
        from src.service.tmiServ import queryEstandaresServ
        result = queryEstandaresServ(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))