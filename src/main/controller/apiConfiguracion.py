"""Configuración del TMI: ejecución de los scripts SQL y validación de lo configurado."""

import asyncio

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user
from src.main.db.databaseConexion import get_db
from src.main.service import configuracionServ

router = APIRouter(
    prefix="/configuracion",
    tags=["TMI Configuración"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/ejecutar-sql")
async def ejecutarSqlTMI():
    """Vuelve a ejecutar los scripts de src/resources/sql/tmi (también corren al iniciar la aplicación)."""
    return await asyncio.to_thread(configuracionServ.ejecutarSqlServ)


@router.get("/validar-config")
async def validarConfigTMI(db: Session = Depends(get_db)):
    return configuracionServ.validarConfigServ(db)

