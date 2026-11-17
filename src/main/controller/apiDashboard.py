"""Dashboard del TMI (público, de solo lectura: ver RUTAS_PUBLICAS en webSecurityConfig)."""

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user
from src.main.db.databaseConexion import get_db
from src.main.controller.apiExcel import respuesta_excel
from src.main.service import dashboardServ

router = APIRouter(
    prefix="/dashboard",
    tags=["TMI Dashboard"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/periodos")
def periodosDashboardTMI(origen: Optional[str] = None, db: Session = Depends(get_db)):
    """Periodos para el dashboard. Con origen=ACTUAL solo los que tienen datos actuales."""
    return dashboardServ.periodosDashboardServ(db, origen)


@router.get("/{periodo}")
def dashboardTMI(periodo: str, origen: Optional[str] = None, db: Session = Depends(get_db)):
    """Datos del dashboard con los puntajes calculados como en el Excel, siempre en tiempo real."""
    return dashboardServ.dashboardServ(db, periodo, origen)


@router.get("/{periodo}/excel")
def excelDashboardTMI(periodo: str, origen: Optional[str] = None, db: Session = Depends(get_db)):
    """Excel del periodo para los dashboards: el mismo de Administración, con todos los indicadores, calculado en
    tiempo real con los datos de hoy."""
    return respuesta_excel(db, periodo, calcular=False, indicadores=None, origen=dashboardServ.origenDashboard(origen))
