"""Catálogos del TMI (grupos, actividades, servicios y tipos de cálculo de las dimensiones del data warehouse)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user
from src.main.db.databaseConexion import get_db
from src.main.service import catalogoServ

router = APIRouter(
    prefix="/catalogo",
    tags=["TMI Catálogos"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/grupos-reporte")
async def catalogoGruposReporte(db: Session = Depends(get_db)):
    return catalogoServ.catalogoGruposReporteServ(db)


@router.get("/grupo-actividad-servicio")
async def catalogoGrupoActividadServicio(db: Session = Depends(get_db)):
    """Relación grupo -> actividad -> servicio para elegir la lógica de las variables en cascada."""
    return catalogoServ.grupoActividadServicioServ(db)


@router.get("/tipos-calculo")
async def catalogoTiposCalculo(db: Session = Depends(get_db)):
    return catalogoServ.catalogoTiposCalculoServ(db)
