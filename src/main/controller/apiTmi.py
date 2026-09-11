
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core.security import get_current_user
from src.main.db.databaseConexion import SessionLocal, get_db
from src.main.dtos.tmiDto import centroTmiDto, estandarTmiDto

logger = logging.getLogger(__name__)

# Todo el router de TMI requiere que el usuario esté autenticado
router = APIRouter(
    prefix="/tmi",
    tags=["TMI"],
    dependencies=[Depends(get_current_user)],
)

@router.get("/conexion")
async def conexion(current_user: dict = Depends(get_current_user)):
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

@router.post("/insert-estandar-centros/{periodo}/{periodoAnterior}")
async def queryInsertEstandaresPeriodo(
    periodo:str,
    periodoAnterior:str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryInsertEstandaresPeriodoServ
        from src.main.service.tmiServ import queryInsertCentrosTMIServ
        queryInsertCentrosTMIServ(db, periodo,periodoAnterior)
        queryInsertEstandaresPeriodoServ(db, periodo,periodoAnterior)
        return {"message": "Estandar insertado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al insertar estandar periodo: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al insertar los estándares.",
        )

@router.get("/lista-estandar/{periodo}")
async def queryEstandares(
    periodo:str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryEstandaresServ
        return queryEstandaresServ(db, periodo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar estándares: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de estándares.",
        )

@router.get("/lista-estandar-by-centro/{codcentro}/{periodo}")
async def queryEstandaresByCentro(
    codcentro: str,
    periodo:str,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.tmiServ import queryEstandaresByCentroServ
        return queryEstandaresByCentroServ(db, codcentro, periodo)
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
    dto: estandarTmiDto,
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

@router.get("/dia-ejecucion/{anio}")
async def queryDiaEjecucion(
    anio:int,
    db: Session = Depends(get_db),
):  
    try:
        from src.main.service.tmiServ import queryDiaEjecucionServ
        return queryDiaEjecucionServ(db,anio)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar dia de ejecucion: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar el dia de ejecucion.",
        )








