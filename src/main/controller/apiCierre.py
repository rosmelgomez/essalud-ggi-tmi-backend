import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.main.core.security import get_current_user
from src.main.db.databaseConexion import get_db
from src.main.dtos.tmiDto import cierreUpdateDto
from src.main.service.cierreServ import queryListaCierreServ, queryUpdateFechaCierreServ

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/tmi/cierre",
    tags=["TMI Cierre"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/lista")
async def queryListaCierre(db: Session = Depends(get_db)):
    try:
        return queryListaCierreServ(db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar cierres: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar los cierres.",
        )


@router.put("/{periodo}")
async def queryUpdateFechaCierre(
    periodo: str,
    dto: cierreUpdateDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' actualizando fecha de cierre %s: %s", current_user.get("username"), periodo, dto.fecha_cierre)
        return queryUpdateFechaCierreServ(db, periodo, dto.fecha_cierre, current_user.get("username"))
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al actualizar fecha de cierre: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al actualizar la fecha de cierre.",
        )
