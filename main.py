from fastapi import FastAPI, Request, Response
from sqlalchemy import text


app = FastAPI(
title="microservicio de gestion del tmi",
description="gestion del tmi",
)


@app.get("/conexion")
def conexion():
    try:
        from src.db.database import SessionLocal
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"message": "conexion exitosa"}
    except Exception as e:
        return {"message": "conexion fallida", "error": str(e)}