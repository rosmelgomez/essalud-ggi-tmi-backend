"""Endpoints de centros del TMI: tmi_centro, exclusión de centro por indicador y estándares propios de centro."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.main.core.security import get_current_user
from src.main.db.databaseConexion import get_db
from src.main.dtos.tmiDinamicoDto import tmiCentroEstandarDto
from src.main.dtos.tmiDto import tmiCentroDto, tmiExclusionCentroEstandarDto
from src.main.repositories import centroRep, tmiBaseRep

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/tmi",
    tags=["TMI Centros"],
    dependencies=[Depends(get_current_user)],
)

routerDinamico = APIRouter(
    prefix="/tmi/dinamico",
    tags=["TMI Centros"],
    dependencies=[Depends(get_current_user)],
)


# Endpoints tmi_centro
@router.get("/lista-centros")
async def queryCentrosTMI(
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.centroServ import queryCentrosTMIServ
        return queryCentrosTMIServ(db)
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
    dto: tmiCentroDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' actualizando centro: %s", current_user.get("username"), getattr(dto, "codcentro", None))
        from src.main.service.centroServ import queryUpdateCentrosTMIServ
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
    dto: tmiCentroDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' agregando centro en año %s", current_user.get("username"), dto.anio)
        from src.main.service.centroServ import queryInsertCentrosTMIServ
        return queryInsertCentrosTMIServ(db, dto)
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
        from src.main.service.centroServ import queryDeleteCentrosTMIServ
        return queryDeleteCentrosTMIServ(db, id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al eliminar el centro TMI: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al eliminar el centro TMI.",
        )


### tmi_exclusion_centro_indicador (exclusión de centro por indicador)
@router.get("/lista-exclusion-centro-estandar/{anio}")
async def queryExclusionCentroEstandar(
    anio: int,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.centroServ import queryExclusionCentroEstandarServ
        return queryExclusionCentroEstandarServ(db, anio)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar exclusión de centro estándar: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de exclusión de centro estándar.",
        )


@router.post("/create-exclusion-centro-estandar")
async def queryCreateExclusionCentroEstandar(
    dto: tmiExclusionCentroEstandarDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' agregando exclusión de centro estándar en año %s", current_user.get("username"), dto.anio)
        from src.main.service.centroServ import queryInsertExclusionCentroEstandarServ
        return queryInsertExclusionCentroEstandarServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al agregar la exclusión de centro estándar: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al agregar la exclusión de centro estándar.",
        )


@routerDinamico.get("/catalogo/centros")
async def catalogoCentros(db: Session = Depends(get_db)):
    return centroRep.queryCatalogoCentrosTMI(db)


@routerDinamico.get("/centro-estandar/{anio}")
async def listaCentroEstandar(anio: int, db: Session = Depends(get_db)):
    return centroRep.queryCentroEstandarTMI(db, anio)


@routerDinamico.post("/centro-estandar")
async def crearCentroEstandar(dto: tmiCentroEstandarDto, db: Session = Depends(get_db)):
    return tmiBaseRep.queryInsertarFila(db, "tmi_centro_estandar", dto.model_dump())


@routerDinamico.put("/centro-estandar/{id}")
async def actualizarCentroEstandar(id: int, dto: tmiCentroEstandarDto, db: Session = Depends(get_db)):
    return tmiBaseRep.queryActualizarFila(db, "tmi_centro_estandar", id, dto.model_dump())


@routerDinamico.delete("/centro-estandar/{id}")
async def eliminarCentroEstandar(id: int, db: Session = Depends(get_db)):
    return tmiBaseRep.queryEliminarFila(db, "tmi_centro_estandar", id)
