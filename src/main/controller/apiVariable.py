"""Endpoints de variables del TMI dinámico: variables, componentes (variables compuestas) y lógica."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user, nombre_usuario
from src.main.db.databaseConexion import get_db
from src.main.dtos.tmiDinamicoDto import (
    tmiVariableComponenteDto,
    tmiVariableDto,
    tmiVariableLogicaDto,
)
from src.main.service import variableServ

router = APIRouter(
    prefix="/variable",
    tags=["TMI Variables"],
    dependencies=[Depends(get_current_user)],
)


# variables
@router.get("/variables")
async def listaVariables(db: Session = Depends(get_db)):
    return variableServ.listaVariablesServ(db)


@router.post("/variables")
async def crearVariable(dto: tmiVariableDto, db: Session = Depends(get_db),
                        current_user: dict = Depends(get_current_user)):
    return variableServ.crearVariableServ(db, dto, nombre_usuario(current_user))


@router.put("/variables/{id}")
async def actualizarVariable(id: int, dto: tmiVariableDto, db: Session = Depends(get_db),
                             current_user: dict = Depends(get_current_user)):
    return variableServ.actualizarVariableServ(db, id, dto, nombre_usuario(current_user))


@router.delete("/variables/{id}")
async def eliminarVariable(id: int, db: Session = Depends(get_db)):
    return variableServ.eliminarVariableServ(db, id)


# componentes
@router.get("/variables/{id}/componentes")
async def listaComponentes(id: int, db: Session = Depends(get_db)):
    """Variables que suma una variable compuesta."""
    return variableServ.listaComponentesServ(db, id)


@router.post("/componentes")
async def crearComponente(dto: tmiVariableComponenteDto, db: Session = Depends(get_db)):
    return variableServ.crearComponenteServ(db, dto)


@router.delete("/componentes/{id}")
async def eliminarComponente(id: int, db: Session = Depends(get_db)):
    return variableServ.eliminarComponenteServ(db, id)


# lógica
@router.get("/variables/{id}/consulta/{periodo}")
async def consultaVariable(id: int, periodo: int, db: Session = Depends(get_db)):
    """Query para SSMS que calcula la variable directo de TOTALIZADO3 para el periodo (AAAAMM): valor de cada mes y
    de enero al mes (total anual)."""
    return variableServ.consultaVariableServ(db, id, periodo)


@router.get("/variables/{id}/logica")
async def listaLogica(id: int, db: Session = Depends(get_db)):
    return variableServ.listaLogicaServ(db, id)


@router.post("/logica")
async def crearLogica(dto: tmiVariableLogicaDto, db: Session = Depends(get_db)):
    return variableServ.crearLogicaServ(db, dto)


@router.put("/logica/{id}")
async def actualizarLogica(id: int, dto: tmiVariableLogicaDto, db: Session = Depends(get_db)):
    return variableServ.actualizarLogicaServ(db, id, dto)


@router.delete("/logica/{id}")
async def eliminarLogica(id: int, db: Session = Depends(get_db)):
    return variableServ.eliminarLogicaServ(db, id)
