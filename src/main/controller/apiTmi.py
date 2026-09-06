
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core.security import get_current_user
from src.main.db.databaseConexion import SessionLocal, get_db
from src.main.dtos.tmiDto import centroTmiDto, estandaresDto

logger = logging.getLogger(__name__)

# Todo el router de TMI requiere que el usuario esté autenticado
router = APIRouter(
    prefix="/tmi",
    tags=["TMI"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/conexion")
def conexion(current_user: dict = Depends(get_current_user)):
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"message": "conexion exitosa"}
    except Exception as e:
        logger.error("Error en prueba de conexión a BD: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al conectar con el servidor de base de datos.",
        )


@router.get("/lista-estandar")
async def queryEstandares(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        from src.main.service.tmiServ import queryEstandaresServ
        return queryEstandaresServ(db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar estándares: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de estándares.",
        )


@router.get("/lista-estandar-by-centro/{codcentro}")
async def queryEstandaresByCentro(
    codcentro: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        from src.main.service.tmiServ import queryEstandaresByCentroServ
        return queryEstandaresByCentroServ(db, codcentro)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar estándares por centro %s: %s", codcentro, e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar los estándares del centro seleccionado.",
        )


@router.put("/update-estandar")
async def queryUpdateEstandares(
    dto: estandaresDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' actualizando estándar ID: %s", current_user.get("username"), getattr(dto, "id", None))
        from src.main.service.tmiServ import queryUpdateEstandaresServ
        return queryUpdateEstandaresServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al actualizar estándar: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al actualizar el estándar.",
        )


@router.get("/lista-centros")
async def queryCentrosTMI(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        from src.main.service.tmiServ import queryCentrosTMIServ
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


@router.get("/ce-concent")
async def queryCEConcent(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        from src.main.service.tmiServ import queryCEConcentServ
        return queryCEConcentServ(db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar concentrado CE: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar los datos de concentración.",
        )