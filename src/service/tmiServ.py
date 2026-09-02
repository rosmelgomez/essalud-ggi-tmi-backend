


from src.repositories.tmiRep import queryEstandares
from src.db.databaseConexion import SessionLocal
from fastapi import HTTPException
from sqlalchemy import text

def queryEstandaresServ(db: SessionLocal):
    try:
        result = queryEstandares(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))