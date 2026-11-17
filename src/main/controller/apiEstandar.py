"""Endpoints de estándares del TMI: tmi_estandar, estándares por tipo, nivel y categoría, tablas maestras,
estándares por indicador y % Acept."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user, nombre_usuario
from src.main.db.databaseConexion import get_db
from src.main.dtos.tmiDinamicoDto import tmiEstandarPeriodoDto, tmiToleranciaDto
from src.main.repositories import estandarRep

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/estandar",
    tags=["TMI Estándares"],
    dependencies=[Depends(get_current_user)],
)


# Endpoints tmi_estandar
@router.get("/lista-estandar")
async def queryEstandar(
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.estandarServ import queryEstandarServ
        return queryEstandarServ(db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar estandar: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de estándares.",
        )


# estándares específicos de centro
# tablas maestras de estándares: tipos (NIVEL, NIVEL_TIPO, TIPO, CATEGORIA...) y sus claves
@router.get("/tipos-estandar")
async def listaTiposEstandar(db: Session = Depends(get_db)):
    return estandarRep.queryTiposEstandarTMI(db)


@router.get("/estandares-periodo/{anio}/{mes}")
async def estandaresPeriodoTMI(anio: int, mes: int, db: Session = Depends(get_db)):
    """Estándar de cada indicador activo solo en las claves de su base_estandar: fijo del año y valor del mes."""
    if not 1 <= mes <= 12:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El mes debe estar entre 1 y 12.")
    return estandarRep.queryEstandaresPeriodoTMI(db, anio, mes)


@router.put("/indicadores/{id}/estandar-periodo")
async def guardarEstandarPeriodo(id: int, dto: tmiEstandarPeriodoDto, db: Session = Depends(get_db)):
    return estandarRep.queryGuardarEstandarPeriodoTMI(db, id, dto.model_dump())


@router.get("/aceptacion/{anio}/{mes}")
async def aceptacionTMI(anio: int, mes: int, db: Session = Depends(get_db)):
    """% Acept de los indicadores activos: porcentaje y estándar del mes por clave (el % Acept se calcula)."""
    if not 1 <= mes <= 12:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El mes debe estar entre 1 y 12.")
    return estandarRep.queryAceptacionTMI(db, anio, mes)


@router.put("/indicadores/{id}/acept")
async def guardarToleranciaIndicador(id: int, dto: tmiToleranciaDto, db: Session = Depends(get_db),
                                     current_user: dict = Depends(get_current_user)):
    return estandarRep.queryGuardarToleranciaTMI(db, id, dto.model_dump(), nombre_usuario(current_user))
