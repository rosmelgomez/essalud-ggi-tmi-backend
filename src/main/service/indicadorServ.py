"""Servicios de indicadores del TMI: mantenimiento, fórmula con letras, ámbito y consulta directa."""

from typing import Optional

from sqlalchemy.orm import Session

from src.main.dtos.tmiDinamicoDto import tmiFormulaDto, tmiIndicadorDto
from src.main.repositories import estandarRep, indicadorRep, tmiBaseRep

# el % Acept vive en tmi_indicador_acept: al crear el indicador se guarda el inicial; después solo se cambia con
# PUT /estandar/indicadores/{id}/acept (pestaña % Acept)
_SIN_ACEPT = {"tipo_acept", "acept", "aceptmenos"}


# indicadores
def listaIndicadoresServ(db: Session):
    return indicadorRep.queryIndicadoresTMI(db)


def crearIndicadorServ(db: Session, dto: tmiIndicadorDto, usuario: Optional[str]):
    respuesta = tmiBaseRep.queryInsertarFila(db, "tmi_indicador", dto.model_dump(exclude=_SIN_ACEPT), usuario)
    estandarRep.crearAceptIndicadorTMI(db, respuesta["id"], dto.sentido, dto.tipo_acept, dto.acept, dto.aceptmenos)
    return respuesta


def actualizarIndicadorServ(db: Session, id: int, dto: tmiIndicadorDto, usuario: Optional[str]):
    respuesta = tmiBaseRep.queryActualizarFila(db, "tmi_indicador", id, dto.model_dump(exclude=_SIN_ACEPT), usuario)
    # la regla de nulos (si_variable_nula / si_division_cero) cambia la expresión SQL: se devuelve con la regla nueva
    respuesta["formula_sql"] = indicadorRep.queryFormulaSqlTMI(db, id)
    return respuesta


def eliminarIndicadorServ(db: Session, id: int):
    return indicadorRep.queryEliminarIndicador(db, id)


# fórmula
def guardarFormulaServ(db: Session, id: int, dto: tmiFormulaDto, usuario: Optional[str]):
    """Guarda la fórmula con letras ((A - B) / C), la variable de cada letra y la fórmula interna que genera."""
    return indicadorRep.queryGuardarFormulaTMI(db, id, dto.formula_alias, dto.variables, usuario)


def analizarFormulaServ(db: Session, dto: tmiFormulaDto):
    """Valida la fórmula con letras y devuelve la fórmula interna y sus términos con la descripción de la DIM."""
    return indicadorRep.queryAnalizarFormulaTMI(db, dto.formula_alias, dto.variables,
                                                {"si_variable_nula": dto.si_variable_nula,
                                                 "si_division_cero": dto.si_division_cero})


# consulta directa a TOTALIZADO3
def consultaIndicadorServ(db: Session, id: int, periodo: int, con_estandares: bool = False):
    """Query que calcula el indicador directo de TOTALIZADO3 para el periodo (AAAAMM)."""
    return indicadorRep.queryConsultaIndicadorTMI(db, id, periodo, con_estandares)


# letras de la fórmula (formula_alias + formula_variable)
def listaLetrasServ(db: Session, id: int):
    return indicadorRep.queryIndicadorLetrasTMI(db, id)


