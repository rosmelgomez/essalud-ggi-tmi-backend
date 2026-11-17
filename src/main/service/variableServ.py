"""Servicios de variables del TMI: variables, componentes (variables compuestas) y lógica. Cada cambio que afecta
el cálculo de una variable regenera las fórmulas de los indicadores que la usan."""

from typing import Optional

from sqlalchemy.orm import Session

from src.main.dtos.tmiDinamicoDto import (
    tmiVariableComponenteDto,
    tmiVariableDto,
    tmiVariableLogicaDto,
)
from src.main.repositories import tmiBaseRep, variableRep


# variables
def listaVariablesServ(db: Session):
    return variableRep.queryVariablesTMI(db)


def crearVariableServ(db: Session, dto: tmiVariableDto, usuario: Optional[str]):
    return tmiBaseRep.queryInsertarFila(db, "tmi_variable", dto.model_dump(), usuario)


def _conAvisos(r, avisos: list):
    """Respuesta con los indicadores cuya fórmula no se pudo actualizar (avisos: [] si todo salió bien)."""
    if isinstance(r, dict):
        r["avisos"] = avisos
    return r


def actualizarVariableServ(db: Session, id: int, dto: tmiVariableDto, usuario: Optional[str]):
    r = variableRep.queryActualizarVariableTMI(db, id, dto.model_dump(), usuario)
    return _conAvisos(r, variableRep.regenerarFormulasVariable(db, id))


def eliminarVariableServ(db: Session, id: int):
    return variableRep.queryEliminarVariable(db, id)


# componentes (tmi_variable_componente)
def listaComponentesServ(db: Session, id: int):
    """Variables que suma una variable compuesta."""
    return variableRep.queryVariableComponentesTMI(db, id)


def crearComponenteServ(db: Session, dto: tmiVariableComponenteDto):
    r = variableRep.queryInsertarComponenteTMI(db, dto.model_dump())
    return _conAvisos(r, variableRep.regenerarFormulasVariable(db, dto.id_variable))


def eliminarComponenteServ(db: Session, id: int):
    return _eliminarYRegenerar(db, "tmi_variable_componente", id)


# lógica (tmi_variable_logica)
def consultaVariableServ(db: Session, id: int, periodo: int):
    return variableRep.queryConsultaVariableTMI(db, id, periodo)


def listaLogicaServ(db: Session, id: int):
    return variableRep.queryVariableLogicaTMI(db, id)


def crearLogicaServ(db: Session, dto: tmiVariableLogicaDto):
    r = tmiBaseRep.queryInsertarFila(db, "tmi_variable_logica", dto.model_dump())
    return _conAvisos(r, variableRep.regenerarFormulasVariable(db, dto.id_variable))


def actualizarLogicaServ(db: Session, id: int, dto: tmiVariableLogicaDto):
    # si la fila pasa a otra variable, también cambian las fórmulas de la variable anterior
    id_anterior = variableRep.queryVariableDeFila(db, "tmi_variable_logica", id)
    r = tmiBaseRep.queryActualizarFila(db, "tmi_variable_logica", id, dto.model_dump())
    return _conAvisos(r, variableRep.regenerarFormulasVariable(db, dto.id_variable, id_anterior))


def eliminarLogicaServ(db: Session, id: int):
    return _eliminarYRegenerar(db, "tmi_variable_logica", id)


def _eliminarYRegenerar(db: Session, tabla: str, id: int):
    """Borra la fila y regenera las fórmulas de la variable a la que pertenecía."""
    id_var = variableRep.queryVariableDeFila(db, tabla, id)
    r = tmiBaseRep.queryEliminarFila(db, tabla, id)
    return _conAvisos(r, variableRep.regenerarFormulasVariable(db, id_var))
