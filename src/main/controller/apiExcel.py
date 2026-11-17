"""Excel del TMI desde la plantilla vacía (src/resources/plantillas)."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user
from src.main.db.databaseConexion import get_db
from src.main.service.excelServ import generarExcelServ

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/excel",
    tags=["TMI Excel"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/{periodo}")
def generarExcelTMIDinamico(periodo: str, calcular: bool = True, indicadores: Optional[str] = None,
                            origen: Optional[str] = None, db: Session = Depends(get_db)):
    """Excel del periodo. indicadores = ids separados por coma (1,4,7) para generar solo esas hojas; sin él, todos.
    origen: ACTUAL (TOTALIZADO3) o BACKUP (copia del cierre); sin él, el oficial."""
    return respuesta_excel(db, periodo, calcular, indicadores, origen)


def respuesta_excel(db: Session, periodo: str, calcular: bool, indicadores: Optional[str], origen: Optional[str] = None):
    """Devuelve el Excel como descarga (también lo usa el dashboard)."""
    try:
        buffer, nombre = generarExcelServ(db, periodo, calcular, indicadores, origen)
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="{nombre}"'},
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Error al generar excel TMI dinámico: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al generar el Excel del TMI.",
        )
