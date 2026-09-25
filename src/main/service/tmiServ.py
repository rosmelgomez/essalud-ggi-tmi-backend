from src.main.dtos.tmiDto import (
    centroTmiDto,
    tmiEstandarTipoDto,
    tmiEstandarNivelDto,
    tmiEstandarCategoriaDto,
)

from sqlalchemy.orm import Session
from fastapi import HTTPException

from typing import Optional


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


# procesos internos 
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

