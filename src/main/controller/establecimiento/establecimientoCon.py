import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user
from src.main.db.databaseConexion import get_db

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/establecimiento",
    tags=["establecimientos"],
    dependencies=[Depends(get_current_user)],
)

@router.get("/resumen-ejecutivo")
async def obtenerResumenEjecutivo(
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.establecimiento.establecimientoServ import obtenerResumenEjecutivoServ
        return obtenerResumenEjecutivoServ(db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al obtener resumen ejecutivo de establecimientos: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al obtener el resumen ejecutivo de establecimientos.",
        )
## campo= 
@router.get("/distribucion/{campo}/{top}")
async def obtenerDistribucion(
    campo: str,
    top: int,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.establecimiento.establecimientoServ import obtenerDistribucionServ
        return obtenerDistribucionServ(db, campo, top)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al obtener distribución de establecimientos: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al obtener la distribución de establecimientos.",
        )