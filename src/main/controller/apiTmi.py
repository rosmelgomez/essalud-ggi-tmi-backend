
from typing import Optional
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core.security import get_current_user
from src.main.db.databaseConexion import SessionLocal, get_db
from src.main.dtos.tmiDto import (
    centroTmiDto,
    tmiEstandarTipoDto,
    tmiEstandarNivelDto,
    tmiEstandarCategoriaDto,
)

logger = logging.getLogger(__name__)

# Todo el router de TMI requiere que el usuario esté autenticado
router = APIRouter(
    prefix="/tmi",
    tags=["TMI"],
    dependencies=[Depends(get_current_user)],
)

## insertar en bloque por periodo anterior periodoactual


# Endpoints tmi_centro
@router.get("/lista-centros/{periodo}")
async def queryCentrosTMI(
    periodo:str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryCentrosTMIServ
        return queryCentrosTMIServ(db,periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar centros TMI: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar los centros TMI.",
        )

@router.put("/update-centro")
async def queryUpdateCentrosTMI(
    dto: centroTmiDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' actualizando centro: %s", current_user.get("username"), getattr(dto, "codcentro", None))
        from src.main.service.tmiServ import queryUpdateCentrosTMIServ
        return queryUpdateCentrosTMIServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al actualizar centro TMI: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al actualizar el centro TMI.",
        )

@router.post("/create-centro")
async def queryCreateCentroTMI(
    dto: centroTmiDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' agregando fila en periodo %s", current_user.get("username"), dto.periodo)
        from src.main.service.tmiServ import queryCreateCentroTMIServ
        return queryCreateCentroTMIServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al agregar el centro TMI: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al agregar el centro TMI.",
        )

@router.delete("/delete-centro/{id}")
async def queryDeleteCentroTMI(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' eliminando fila %s de tmi_centro", current_user.get("username"), id)
        from src.main.service.tmiServ import queryDeleteFilaServ
        return queryDeleteFilaServ(db, "tmi_centro", id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al eliminar el centro TMI: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al eliminar el centro TMI.",
        )

@router.get("/queryInsertCentrosTMIServ/{periodoActual}/{periodoAnterior}")
async def queryInsertCentrosTMI(
    periodoActual:str,
    periodoAnterior:str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryInsertCentrosTMIServ
        return queryInsertCentrosTMIServ(db,periodoActual,periodoAnterior)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar centros TMI: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar los centros TMI.",
        )


# Endpoints tmi_estandar_tipo
@router.get("/lista-estandar-tipo/{periodo}")
async def queryEstandarTipo(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryEstandarTipoServ
        return queryEstandarTipoServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar estandar tipo: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de estándares por tipo.",
        )

@router.put("/update-estandar-tipo")
async def queryUpdateEstandarTipo(
    dto: tmiEstandarTipoDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        from src.main.service.tmiServ import queryUpdateEstandarTipoServ
        return queryUpdateEstandarTipoServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al actualizar estandar tipo: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al actualizar el estándar tipo.",
        )

@router.post("/create-estandar-tipo")
async def queryCreateEstandarTipo(
    dto: tmiEstandarTipoDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' agregando fila en periodo %s", current_user.get("username"), dto.periodo)
        from src.main.service.tmiServ import queryCreateEstandarTipoServ
        return queryCreateEstandarTipoServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al agregar el estándar tipo: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al agregar el estándar tipo.",
        )

@router.delete("/delete-estandar-tipo/{id}")
async def queryDeleteEstandarTipo(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' eliminando fila %s de tmi_estandar_tipo", current_user.get("username"), id)
        from src.main.service.tmiServ import queryDeleteFilaServ
        return queryDeleteFilaServ(db, "tmi_estandar_tipo", id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al eliminar el estándar tipo: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al eliminar el estándar tipo.",
        )

@router.get("/queryInsertEstandarTipoServ/{periodoActual}/{periodoAnterior}")
async def queryInsertEstandarTipo(
    periodoActual:str,
    periodoAnterior:str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryInsertEstandarTipoServ
        return queryInsertEstandarTipoServ(db,periodoActual,periodoAnterior)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar estandar tipo: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de estándares por tipo.",
        )



# Endpoints tmi_estandar_nivel
@router.get("/lista-estandar-nivel/{periodo}")
async def queryEstandarNivel(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryEstandarNivelServ
        return queryEstandarNivelServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar estandar nivel: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de estándares por nivel.",
        )

@router.put("/update-estandar-nivel")
async def queryUpdateEstandarNivel(
    dto: tmiEstandarNivelDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        from src.main.service.tmiServ import queryUpdateEstandarNivelServ
        return queryUpdateEstandarNivelServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al actualizar estandar nivel: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al actualizar el estándar nivel.",
        )

@router.post("/create-estandar-nivel")
async def queryCreateEstandarNivel(
    dto: tmiEstandarNivelDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' agregando fila en periodo %s", current_user.get("username"), dto.periodo)
        from src.main.service.tmiServ import queryCreateEstandarNivelServ
        return queryCreateEstandarNivelServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al agregar el estándar nivel: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al agregar el estándar nivel.",
        )

@router.delete("/delete-estandar-nivel/{id}")
async def queryDeleteEstandarNivel(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' eliminando fila %s de tmi_estandar_nivel", current_user.get("username"), id)
        from src.main.service.tmiServ import queryDeleteFilaServ
        return queryDeleteFilaServ(db, "tmi_estandar_nivel", id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al eliminar el estándar nivel: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al eliminar el estándar nivel.",
        )

@router.get("/queryInsertEstandarNivelServ/{periodoActual}/{periodoAnterior}")
async def queryInsertEstandarNivel(
    periodoActual:str,
    periodoAnterior:str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryInsertEstandarNivelServ
        return queryInsertEstandarNivelServ(db,periodoActual,periodoAnterior)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar estandar nivel: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de estándares por nivel.",
        )



# Endpoints tmi_estandar_categoria
@router.get("/lista-estandar-categoria/{periodo}")
async def queryEstandarCategoria(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryEstandarCategoriaServ
        return queryEstandarCategoriaServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar estandar categoria: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de estándares por categoría.",
        )

@router.put("/update-estandar-categoria")
async def queryUpdateEstandarCategoria(
    dto: tmiEstandarCategoriaDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        from src.main.service.tmiServ import queryUpdateEstandarCategoriaServ
        return queryUpdateEstandarCategoriaServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al actualizar estandar categoria: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al actualizar el estándar categoría.",
        )

@router.post("/create-estandar-categoria")
async def queryCreateEstandarCategoria(
    dto: tmiEstandarCategoriaDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' agregando fila en periodo %s", current_user.get("username"), dto.periodo)
        from src.main.service.tmiServ import queryCreateEstandarCategoriaServ
        return queryCreateEstandarCategoriaServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al agregar el estándar categoría: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al agregar el estándar categoría.",
        )

@router.delete("/delete-estandar-categoria/{id}")
async def queryDeleteEstandarCategoria(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' eliminando fila %s de tmi_estandar_categoria", current_user.get("username"), id)
        from src.main.service.tmiServ import queryDeleteFilaServ
        return queryDeleteFilaServ(db, "tmi_estandar_categoria", id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al eliminar el estándar categoría: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al eliminar el estándar categoría.",
        )

### consultar estandares tipo por centro
@router.get("/lista-estandar-tipo-centro/{codcas}/{periodo}")
async def queryEstandarCentro(
    codcas:str,
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryEstandaresTipoCentroServ
        return queryEstandaresTipoCentroServ(db, codcas, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar estandar centro: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de estándares por centro.",
        )

### consultar estandares nivel por centro
@router.get("/lista-estandar-nivel-centro/{codcas}/{periodo}")
async def queryEstandarNivelCentro(
    codcas:str,
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryEstandaresNivelCentroServ
        return queryEstandaresNivelCentroServ(db, codcas, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar estandar nivel centro: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de estándares por nivel por centro.",
        )


## consultas
## CE_Concent
@router.get("/lista-ce-concent/{periodo}")
async def queryCeConcent(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryCE_ConcentServ
        return queryCE_ConcentServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar ce concent: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de ce concent.",
        )

## CE_GCHProg
@router.get("/lista-ce-gchprog/{periodo}")
async def queryCeGCHProg(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryCE_GCHProgServ
        return queryCE_GCHProgServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar ce gchprog: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de ce gchprog.",
        )

## CE_Recetas
@router.get("/lista-ce-recetas/{periodo}")
async def queryCERecetas(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryCE_RecetasServ
        return queryCE_RecetasServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar ce recetas: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de ce recetas.",
        )

## CE_RHrMedico
@router.get("/lista-ce-rhrmedico/{periodo}")
async def queryRHrMedico(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryCE_RHrMedicoServ
        return queryCE_RHrMedicoServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar ce rhrmedico: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de ce rhrmedico.",
        )

## Em_PrioI_II
@router.get("/lista-em-prio-i-ii/{periodo}")
async def queryEmPrioI_II(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryEm_PrioI_IIServ
        return queryEm_PrioI_IIServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar em prio i ii: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de em prio i ii.",
        )

## Em_PrioIV_V
@router.get("/lista-em-prio-iv-v/{periodo}")
async def queryEmPrioIV_V(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryEm_PrioIV_VServ
        return queryEm_PrioIV_VServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar em prio iv v: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de em prio iv v.",
        )

## H_Estancias
@router.get("/lista-h-estancias/{periodo}")
async def queryHEstancias(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryH_EstanciasServ
        return queryH_EstanciasServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar h estancias: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de h estancias.",
        )

## H_ISust
@router.get("/lista-h-isust/{periodo}")
async def queryHISust(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryH_ISustServ
        return queryH_ISustServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar h isust: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de h isust.",
        )

## H_OCamas
@router.get("/lista-h-ocamas/{periodo}")
async def queryHOCamas(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryH_OCamasServ
        return queryH_OCamasServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar h ocamass: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de h ocamass.",
        )

## H_RCama
@router.get("/lista-h-rcama/{periodo}")
async def queryHRcama(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryH_RCamaServ
        return queryH_RCamaServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar h rcama: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de h rcama.",
        )

## H_TBMHosp
@router.get("/lista-h-tbmhosp/{periodo}")
async def queryHTBMHosp(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryH_TBMHospServ
        return queryH_TBMHospServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar h tbmhosp: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de h tbmhosp.",
        )   

## O_Concent
@router.get("/lista-o-concent/{periodo}")
async def queryOConcent(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryO_ConcentServ
        return queryO_ConcentServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar o concent: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de o concent.",
        )

## O_GCHOdon
@router.get("/lista-o-gchodon/{periodo}")
async def queryOGCHodon(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryO_GCHOdonServ
        return queryO_GCHOdonServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar o gchodon: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de o gchodon.",
        )   

## O_HrOdont
@router.get("/lista-o-hrodont/{periodo}")
async def queryOHrOdont(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryO_HrOdontServ
        return queryO_HrOdontServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar o hrodont: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de o hrodont.",
        )

## O_NTOdontS
@router.get("/lista-o-ntodonts/{periodo}")
async def queryONTodontS(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryO_NTOdontSServ
        return queryO_NTOdontSServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar o ntodonts: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de o ntodonts.",
        )

## Qx_GCHProg
@router.get("/lista-qx-gchprog/{periodo}")
async def queryQxGCHProg(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryQx_GCHProgServ
        return queryQx_GCHProgServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar qx gchprog: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de qx gchprog.",
        )

## Qx_HTCesareas
@router.get("/lista-qx-htcesareas/{periodo}")
async def queryQxHTCesareas(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryQx_HTCesareasServ
        return queryQx_HTCesareasServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar qx htcesareas: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de qx htcesareas.",
        )

## Qx_IAlta
@router.get("/lista-qx-ialta/{periodo}")
async def queryQxIAlta(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryQx_IAltaServ
        return queryQx_IAltaServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar qx ialta: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de qx ialta.",
        )

## Qx_IMenor
@router.get("/lista-qx-imenor/{periodo}")
async def queryQxIMenor(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryQx_IMenorServ
        return queryQx_IMenorServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar qx imenor: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de qx imenor.",
        )

## Qx_IntSusp
@router.get("/lista-qx-intsusp/{periodo}")
async def queryQxIntSusp(
    periodo: str,
    db: Session = Depends(get_db),  
):
    try:
        from src.main.service.tmiServ import queryQx_IntSuspServ
        return queryQx_IntSuspServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar qx intsusp: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de qx intsusp.",
        )

## Qx_RendSO
@router.get("/lista-qx-rendso/{periodo}")
async def queryQxRendSO(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryQx_RendSOServ
        return queryQx_RendSOServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar qx rendso: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de qx rendso.",
        )


## Generar Excel TMI (todas las vistas CE_Concent hacia abajo, por periodo)
@router.get("/generar-excel/{periodo}")
async def generarExcelTMI(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.excelServ import MESES_NOMBRE, generar_excel_tmi
        buffer = generar_excel_tmi(db, periodo)
        filename = f"TMI_Prelim_Salud_{MESES_NOMBRE[int(periodo[4:]) - 1].capitalize()}_{periodo[:4]}.xlsx"
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Error al generar excel TMI: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al generar el Excel del TMI.",
        )

