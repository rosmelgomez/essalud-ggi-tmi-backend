from src.main.dtos.tmiDto import (
    centroTmiDto,
    tmiEstandarTipoDto,
    tmiEstandarNivelDto,
    tmiEstandarCategoriaDto,
)

from sqlalchemy.orm import Session
from fastapi import HTTPException

from typing import Optional
from datetime import date


#tmi_centro
def queryCentrosTMIServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryCentrosTMI
        result = queryCentrosTMI(db, periodo)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertCentrosTMIServ(db: Session, periodo_actual: str, periodo_anterior:str):
    try:
        from src.main.repositories.tmiRep import queryInsertCentrosTMI
        ##if not periodo_anterior:
            ##periodo_anterior = calcular_periodo_anterior(periodo_actual)
        result = queryInsertCentrosTMI(db, periodo_actual, periodo_anterior)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateCentrosTMIServ(db: Session, dto:centroTmiDto):
    validarFilaEditable(db, "tmi_centro", dto)
    try:
        from src.main.repositories.tmiRep import queryUpdateCentrosTMI
        result = queryUpdateCentrosTMI(db, dto)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# tmi_estandar_tipo
def queryEstandarTipoServ(db: Session, periodo: str):
    try:
        from src.main.repositories.tmiRep import queryEstandarTipo
        return queryEstandarTipo(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertEstandarTipoServ(db: Session, periodo_actual: str, periodo_anterior: Optional[str] = None):
    try:
        from src.main.repositories.tmiRep import queryInsertEstandarTipo
        ##if not periodoAnterior:
        ##    periodoAnterior = calcular_periodo_anterior(periodo_actual)
        return queryInsertEstandarTipo(db, periodo_actual, periodo_anterior)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateEstandarTipoServ(db: Session, dto: tmiEstandarTipoDto):
    validarFilaEditable(db, "tmi_estandar_tipo", dto)
    try:
        from src.main.repositories.tmiRep import queryUpdateEstandarTipo
        return queryUpdateEstandarTipo(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# tmi_estandar_nivel
def queryEstandarNivelServ(db: Session, periodo: str):
    try:
        from src.main.repositories.tmiRep import queryEstandarNivel
        return queryEstandarNivel(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertEstandarNivelServ(db: Session, periodo_actual: str, periodo_anterior: Optional[str] = None):
    try:
        from src.main.repositories.tmiRep import queryInsertEstandarNivel
        ##if not periodoAnterior:
        ##    periodoAnterior = calcular_periodo_anterior(periodo)
        return queryInsertEstandarNivel(db, periodo_actual, periodo_anterior)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateEstandarNivelServ(db: Session, dto: tmiEstandarNivelDto):
    validarFilaEditable(db, "tmi_estandar_nivel", dto)
    try:
        from src.main.repositories.tmiRep import queryUpdateEstandarNivel
        return queryUpdateEstandarNivel(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# tmi_estandar_categoria
def queryEstandarCategoriaServ(db: Session, periodo: str):
    try:
        from src.main.repositories.tmiRep import queryEstandarCategoria
        return queryEstandarCategoria(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertEstandarCategoriaServ(db: Session, periodo: str, periodoAnterior: Optional[str] = None):
    try:
        from src.main.repositories.tmiRep import queryInsertEstandarCategoria
        if not periodoAnterior:
            periodoAnterior = calcular_periodo_anterior(periodo)
        return queryInsertEstandarCategoria(db, periodo, periodoAnterior)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateEstandarCategoriaServ(db: Session, dto: tmiEstandarCategoriaDto):
    validarFilaEditable(db, "tmi_estandar_categoria", dto)
    try:
        from src.main.repositories.tmiRep import queryUpdateEstandarCategoria
        return queryUpdateEstandarCategoria(db, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


### consultar estandares tipo por centro
def queryEstandaresTipoCentroServ(db: Session, codcas:str, periodo: str):
    try:
        from src.main.repositories.tmiRep import queryEstandaresTipoCentro
        return queryEstandaresTipoCentro(db, codcas, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

### consultar estandares nivel por centro
def queryEstandaresNivelCentroServ(db: Session, codcas:str, periodo: str):
    try:
        from src.main.repositories.tmiRep import queryEstandarNivelCentro
        return queryEstandarNivelCentro(db, codcas, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


### alta de filas (centros y estándares)
def queryCreateCentroTMIServ(db: Session, dto: centroTmiDto):
    return _crearFila(db, "tmi_centro", dto)

def queryCreateEstandarTipoServ(db: Session, dto: tmiEstandarTipoDto):
    return _crearFila(db, "tmi_estandar_tipo", dto)

def queryCreateEstandarNivelServ(db: Session, dto: tmiEstandarNivelDto):
    return _crearFila(db, "tmi_estandar_nivel", dto)

def queryCreateEstandarCategoriaServ(db: Session, dto: tmiEstandarCategoriaDto):
    return _crearFila(db, "tmi_estandar_categoria", dto)


def _crearFila(db: Session, tabla: str, dto):
    from src.main.repositories.tmiRep import queryCreateFila
    validarFilaEditable(db, tabla, dto)
    params = dto.model_dump() if hasattr(dto, "model_dump") else dto.dict()
    result = queryCreateFila(db, tabla, params)
    _actualizarFilasCierres(db)
    return result


### eliminación de filas (centros y estándares)
TABLAS_FILAS = ("tmi_centro", "tmi_estandar_tipo", "tmi_estandar_nivel", "tmi_estandar_categoria")


def queryDeleteFilaServ(db: Session, tabla: str, id: int):
    from src.main.repositories.tmiRep import queryContarFilasPeriodo, queryDeleteFila, queryPeriodoDeFila
    if tabla not in TABLAS_FILAS:
        raise HTTPException(status_code=400, detail=f"Tabla no permitida: {tabla}.")
    periodo = queryPeriodoDeFila(db, tabla, id)
    if periodo is None:
        raise HTTPException(status_code=404, detail=f"No existe la fila con id {id}.")
    minimo = periodo_minimo_editable()
    if periodo < minimo:
        raise HTTPException(status_code=400, detail=f"La fila es del periodo {periodo}, que ya no se puede modificar; el mínimo permitido es {minimo}.")
    # si el periodo queda vacío, el cierre lo volvería a generar copiando el periodo anterior
    if queryContarFilasPeriodo(db, tabla, periodo) <= 1:
        raise HTTPException(status_code=400, detail=f"No se puede eliminar la última fila del periodo {periodo}.")
    result = queryDeleteFila(db, tabla, id)
    _actualizarFilasCierres(db)
    return result


def _actualizarFilasCierres(db: Session):
    """Mantiene filas_insertadas de los cierres al día después de agregar filas."""
    try:
        from src.main.service.cierreServ import _actualizarFilasCierres as actualizar
        actualizar(db)
    except Exception:
        db.rollback()


# procesos internos 
def periodo_minimo_editable(hoy: Optional[date] = None) -> str:
    """Solo se agregan o modifican filas desde el mes anterior al actual
    (ej. en 2026-10 el mínimo es 202609; 202608 ya no se toca). En enero es diciembre del año anterior."""
    hoy = hoy or date.today()
    return calcular_periodo_anterior(f"{hoy.year}{hoy.month:02d}")


def validarFilaEditable(db: Session, tabla: str, dto):
    """Valida el periodo de una fila nueva o modificada; lanza 400 si no se permite."""
    from src.main.repositories.tmiRep import CLAVES_TABLA, queryContarFilasPeriodo, queryExisteFilaPeriodo, queryPeriodoDeFila

    periodo = str(dto.periodo or "").strip()
    if len(periodo) != 6 or not periodo.isdigit() or not 1 <= int(periodo[4:]) <= 12:
        raise HTTPException(status_code=400, detail=f"Periodo inválido: '{periodo}'.")
    minimo = periodo_minimo_editable()
    if periodo < minimo:
        raise HTTPException(status_code=400, detail=f"El periodo {periodo} ya no se puede modificar; el mínimo permitido es {minimo}.")
    if dto.id is not None:
        periodo_actual = queryPeriodoDeFila(db, tabla, dto.id)
        if periodo_actual is None:
            raise HTTPException(status_code=404, detail=f"No existe la fila con id {dto.id}.")
        if periodo_actual < minimo:
            raise HTTPException(status_code=400, detail=f"La fila es del periodo {periodo_actual}, que ya no se puede modificar; el mínimo permitido es {minimo}.")
    else:
        # un periodo sin filas se genera en su cierre copiando el anterior; si se agrega una fila antes, el cierre lo omitiría
        if queryContarFilasPeriodo(db, tabla, periodo) == 0:
            raise HTTPException(status_code=400, detail=f"El periodo {periodo} aún no tiene filas; se genera en su fecha de cierre copiando el periodo anterior.")
    # anio y mes siempre según el periodo
    dto.anio, dto.mes = int(periodo[:4]), int(periodo[4:])
    dto.periodo = periodo
    params = dto.model_dump() if hasattr(dto, "model_dump") else dto.dict()
    if queryExisteFilaPeriodo(db, tabla, params, dto.id):
        claves = ", ".join(f"{c}={params.get(c)}" for c in CLAVES_TABLA[tabla])
        raise HTTPException(status_code=400, detail=f"Ya existe una fila con {claves} en el periodo {periodo}.")


def calcular_periodo_anterior(periodo: str) -> str:
    try:
        if not periodo or len(periodo) != 6:
            return periodo
        anio = int(periodo[:4])
        mes = int(periodo[4:])
        if mes == 1:
            anio -= 1
            mes = 12
        else:
            mes -= 1
        return f"{anio}{mes:02d}"
    except Exception:
        return periodo

##consultas
##CE_Concent
def queryCE_ConcentServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryCE_ConcentRep
        return queryCE_ConcentRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

##CE_GCHProg
def queryCE_GCHProgServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryCE_GCHProgRep
        return queryCE_GCHProgRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

##CE_Recetas
def queryCE_RecetasServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryCE_RecetasRep
        return queryCE_RecetasRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## CE_RHrMedico
def queryCE_RHrMedicoServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryCE_RHrMedicoRep
        return queryCE_RHrMedicoRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Em_PrioI_II
def queryEm_PrioI_IIServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryEm_PrioI_IIRep
        return queryEm_PrioI_IIRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Em_PrioIV_V
def queryEm_PrioIV_VServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryEm_PrioIV_VRep
        return queryEm_PrioIV_VRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## H_Estancias
def queryH_EstanciasServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryH_EstanciasRep
        return queryH_EstanciasRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## H_ISust
def queryH_ISustServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryH_ISustRep
        return queryH_ISustRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## H_OCamas
def queryH_OCamasServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryH_OCamasRep
        return queryH_OCamasRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## H_RCama
def queryH_RCamaServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryH_RCamaRep
        return queryH_RCamaRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## H_TBMHosp
def queryH_TBMHospServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryH_TBMHospRep
        return queryH_TBMHospRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## O_Concent
def queryO_ConcentServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryO_ConcentRep
        return queryO_ConcentRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## O_GCHOdon
def queryO_GCHOdonServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryO_GCHOdonRep
        return queryO_GCHOdonRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## O_HrOdont
def queryO_HrOdontServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryO_HrOdontRep
        return queryO_HrOdontRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## O_NTOdontS
def queryO_NTOdontSServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryO_NTOdontSRep
        return queryO_NTOdontSRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_GCHProg
def queryQx_GCHProgServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryQx_GCHProgRep
        return queryQx_GCHProgRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_HTCesareas
def queryQx_HTCesareasServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryQx_HTCesareasRep
        return queryQx_HTCesareasRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_IAlta
def queryQx_IAltaServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryQx_IAltaRep
        return queryQx_IAltaRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_IMenor
def queryQx_IMenorServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryQx_IMenorRep
        return queryQx_IMenorRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_IntSusp
def queryQx_IntSuspServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryQx_IntSuspRep
        return queryQx_IntSuspRep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_RendSO
def queryQx_RendSOServ(db: Session, periodo:str):
    try:
        from src.main.repositories.tmiRep import queryQx_RendSORep
        return queryQx_RendSORep(db, periodo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

