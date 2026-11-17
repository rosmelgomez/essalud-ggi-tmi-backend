"""Cálculo del TMI: periodo que se puede calcular y cálculo de los puntajes en tiempo real."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user
from src.main.db.databaseConexion import get_db
from src.main.service import calculoServ

router = APIRouter(
    prefix="/calculo",
    tags=["TMI Cálculo"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/periodo-calculo")
async def periodoCalculoTMI(db: Session = Depends(get_db)):
    """Periodo que se puede calcular, último periodo con datos en TOTALIZADO3 y periodos que se pueden calcular."""
    return calculoServ.periodoCalculoServ(db)


@router.post("/calcular/{periodo}")
def calcularTMI(periodo: str, origen: str = "ACTUAL", db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    """origen: ACTUAL = TOTALIZADO3 de hoy (enero..periodo); BACKUP = la copia del cierre del periodo (como fue).
    Los dos en tiempo real: el resultado no se guarda."""
    # def (no async): FastAPI lo corre en un hilo aparte; el cálculo es largo y no debe bloquear el resto de la API
    return calculoServ.calcularServ(db, periodo, origen, (current_user or {}).get("username"))
