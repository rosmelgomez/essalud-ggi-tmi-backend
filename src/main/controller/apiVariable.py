"""Endpoints de variables del TMI dinámico: variables, componentes (variables compuestas) y lógica."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.main.core.security import get_current_user, nombre_usuario
from src.main.db.databaseConexion import get_db
from src.main.dtos.tmiDinamicoDto import (
    tmiVariableComponenteDto,
    tmiVariableDto,
    tmiVariableLogicaDto,
)
from src.main.repositories import tmiBaseRep, variableRep

router = APIRouter(
    prefix="/tmi/dinamico",
    tags=["TMI Variables"],
    dependencies=[Depends(get_current_user)],
)


# variables
@router.get("/variables")
async def listaVariables(db: Session = Depends(get_db)):
    return variableRep.queryVariablesTMI(db)


@router.post("/variables")
async def crearVariable(dto: tmiVariableDto, db: Session = Depends(get_db),
                        current_user: dict = Depends(get_current_user)):
    return tmiBaseRep.queryInsertarFila(db, "tmi_variable", dto.model_dump(), nombre_usuario(current_user))


@router.put("/variables/{id}")
async def actualizarVariable(id: int, dto: tmiVariableDto, db: Session = Depends(get_db),
                             current_user: dict = Depends(get_current_user)):
    r = variableRep.queryActualizarVariableTMI(db, id, dto.model_dump(), nombre_usuario(current_user))
    variableRep.regenerarFormulasVariable(db, id)
    return r


@router.delete("/variables/{id}")
async def eliminarVariable(id: int, db: Session = Depends(get_db)):
    return variableRep.queryEliminarVariable(db, id)


@router.get("/variables/{id}/componentes")
async def listaComponentes(id: int, db: Session = Depends(get_db)):
    """Variables que suma una variable compuesta."""
    return variableRep.queryVariableComponentesTMI(db, id)


@router.post("/componentes")
async def crearComponente(dto: tmiVariableComponenteDto, db: Session = Depends(get_db)):
    r = variableRep.queryInsertarComponenteTMI(db, dto.model_dump())
    variableRep.regenerarFormulasVariable(db, dto.id_variable)
    return r


@router.delete("/componentes/{id}")
async def eliminarComponente(id: int, db: Session = Depends(get_db)):
    id_var = variableRep.queryVariableDeFila(db, "tmi_variable_componente", id)
    r = tmiBaseRep.queryEliminarFila(db, "tmi_variable_componente", id)
    if id_var:
        variableRep.regenerarFormulasVariable(db, id_var)
    return r


@router.get("/variables/{id}/logica")
async def listaLogica(id: int, db: Session = Depends(get_db)):
    return variableRep.queryVariableLogicaTMI(db, id)


@router.post("/logica")
async def crearLogica(dto: tmiVariableLogicaDto, db: Session = Depends(get_db)):
    r = tmiBaseRep.queryInsertarFila(db, "tmi_variable_logica", dto.model_dump())
    variableRep.regenerarFormulasVariable(db, dto.id_variable)
    return r


@router.put("/logica/{id}")
async def actualizarLogica(id: int, dto: tmiVariableLogicaDto, db: Session = Depends(get_db)):
    r = tmiBaseRep.queryActualizarFila(db, "tmi_variable_logica", id, dto.model_dump())
    variableRep.regenerarFormulasVariable(db, dto.id_variable)
    return r


@router.delete("/logica/{id}")
async def eliminarLogica(id: int, db: Session = Depends(get_db)):
    id_var = variableRep.queryVariableDeFila(db, "tmi_variable_logica", id)
    r = tmiBaseRep.queryEliminarFila(db, "tmi_variable_logica", id)
    if id_var:
        variableRep.regenerarFormulasVariable(db, id_var)
    return r
