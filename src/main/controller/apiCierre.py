import logging

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user
from src.main.db.databaseConexion import get_db
from src.main.dtos.tmiDto import cierreCalendarioDto
from src.main.service.cierreServ import (
    queryCalendarioServ,
    queryGuardarCalendarioServ,
    queryListaCierreServ,
    revisarCierre,
)

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


@router.get("/calendario")
async def queryCalendario(db: Session = Depends(get_db)):
    try:
        return queryCalendarioServ(db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar el calendario de cierre: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar el calendario de cierre.",
        )


@router.put("/calendario/{anio}")
def queryGuardarCalendario(
    anio: int,
    dto: cierreCalendarioDto,
    background: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if not 2000 <= anio <= 2100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Año inválido")
    usuario = current_user.get("username")
    logger.info("Usuario '%s' actualizando el calendario de cierre %s: %s", usuario, anio, dto.model_dump())
    dias = dto.model_dump(exclude={"dia_fijo"})
    ejecutar = queryGuardarCalendarioServ(db, anio, dto.dia_fijo, dias, usuario)
    # si algún cierre quedó con la fecha de hoy (o ya pasada), se ejecuta ahora sin esperar la revisión automática
    if ejecutar:
        background.add_task(revisarCierre)
    return {"message": "Calendario de cierre guardado", "anio": anio, "ejecutando": ejecutar}
