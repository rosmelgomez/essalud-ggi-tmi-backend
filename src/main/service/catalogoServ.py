"""Servicios de los catálogos del TMI (grupos, actividades, servicios y tipos de cálculo)."""

from sqlalchemy.orm import Session

from src.main.repositories import catalogoRep


def catalogoGruposReporteServ(db: Session):
    return catalogoRep.queryCatalogoGruposReporteTMI(db)


def grupoActividadServicioServ(db: Session):
    """Relación grupo -> actividad -> servicio para elegir la lógica de las variables en cascada."""
    return catalogoRep.queryGrupoActividadServicioTMI(db)


def catalogoTiposCalculoServ(db: Session):
    return catalogoRep.queryCatalogoTiposCalculoTMI(db)
