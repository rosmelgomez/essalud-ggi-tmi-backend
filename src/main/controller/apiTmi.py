
from typing import Optional
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
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


## prueba con 
##Ce_concent
@router.get("/lista-ce-concent/{periodo}")
async def queryCeConcent(
    periodo: str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryCeConcentServ
        return queryCeConcentServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar ce concent: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de ce concent.",
        )

##CE_GCHProg
@router.get("/lista-ce-gchprog/{periodo}")
async def queryCE_GCHProg(
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





