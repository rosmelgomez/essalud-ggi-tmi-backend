"""Endpoints de centros del TMI: tmi_centro, exclusión de centro por indicador y estándares propios de centro."""

import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user
from src.main.db.databaseConexion import get_db
from src.main.dtos.tmiDinamicoDto import tmiCentroEstandarDto
from src.main.dtos.tmiDto import tmiCentroDto, tmiExclusionCentroEstandarDto
from src.main.repositories import centroRep, tmiBaseRep

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/centro",
    tags=["TMI Centros"],
    dependencies=[Depends(get_current_user)],
)


# Catálogos de nivel, tipo y categoría del centro (tmi_nivel_centro, tmi_nivel_estandar_centro, tmi_tipo_centro)
@router.get("/catalogos-centro")
async def listaCatalogosCentro(
    db: Session = Depends(get_db)
):
    return centroRep.queryCatalogosCentroTMI(db)


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

@router.put("/update-exclusion-centro-estandar")
async def queryUpdateExclusionCentroEstandar(
    dto: tmiExclusionCentroEstandarDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' actualizando exclusión de centro estándar en año %s", current_user.get("username"), dto.anio)
        from src.main.service.centroServ import queryUpdateExclusionCentroEstandarServ
        return queryUpdateExclusionCentroEstandarServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al actualizar la exclusión de centro estándar: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al actualizar la exclusión de centro estándar.",
        )



@router.delete("/delete-exclusion-centro-estandar/{id}")
async def queryDeleteExclusionCentroEstandar(
    id: int,
    mes: int | None = Query(default=None, ge=1, le=12, description="Solo quita ese mes; sin mes, todo el año"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' eliminando exclusión de centro estándar %s (mes %s)", current_user.get("username"), id, mes)
        from src.main.service.centroServ import queryDeleteExclusionCentroEstandarServ
        return queryDeleteExclusionCentroEstandarServ(db, id, mes)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al eliminar la exclusión de centro estándar: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al eliminar la exclusión de centro estándar.",
        )


@router.get("/catalogo/centros")
async def catalogoCentros(db: Session = Depends(get_db)):
    return centroRep.queryCatalogoCentrosTMI(db)

@router.get("/centro-estandar/{anio}")
async def listaCentroEstandar(anio: int, mes: int | None = Query(None, ge=1, le=12), db: Session = Depends(get_db)):
    return centroRep.queryCentroEstandarTMI(db, anio, mes)


@router.post("/centro-estandar")
async def crearCentroEstandar(dto: tmiCentroEstandarDto, db: Session = Depends(get_db)):
    # si el centro ya tiene registro del indicador en el año, solo cambia el periodo (no se duplica)
    return centroRep.queryCrearCentroEstandar(db, dto.model_dump())


@router.put("/centro-estandar/{id}")
async def actualizarCentroEstandar(id: int, dto: tmiCentroEstandarDto, db: Session = Depends(get_db)):
    return tmiBaseRep.queryActualizarFila(db, "tmi_estandar_centro", id, dto.model_dump())


@router.delete("/centro-estandar/{id}")
async def eliminarCentroEstandar(id: int, db: Session = Depends(get_db)):
    return tmiBaseRep.queryEliminarFila(db, "tmi_estandar_centro", id)
