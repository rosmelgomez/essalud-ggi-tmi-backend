"""Cálculo del TMI: qué periodo se puede calcular (lo usan también las copias de TOTALIZADO3 y el Excel) y el
cálculo de los puntajes en tiempo real."""

import logging
from datetime import date
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.main.core.tmiConfig import TMI_CALCULO_SOLO_PERIODO_ANTERIOR
from src.main.repositories import backupRep, calculoRep, configuracionRep, resultadoRep
from src.main.service.cierreServ import periodo_a_generar

logger = logging.getLogger(__name__)


def periodo_valido(periodo: str) -> int:
    """Periodo AAAAMM como número; 400 si no es válido."""
    from src.main.service.excelDinamicoServ import _validar_periodo
    try:
        return _validar_periodo(periodo)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def periodo_calculable() -> str:
    """Periodo que se puede calcular hoy: el mes anterior (el cierre de M genera M-1)."""
    return periodo_a_generar(date.today())


def se_puede_calcular(periodo: str) -> bool:
    """Se calcula cualquier periodo hasta el mes anterior (nunca uno futuro). Con TMI_CALCULO_SOLO_PERIODO_ANTERIOR=true,
    solo el mes anterior."""
    if TMI_CALCULO_SOLO_PERIODO_ANTERIOR:
        return periodo == periodo_calculable()
    return periodo <= periodo_calculable()


def periodoCalculoServ(db: Session) -> dict:
    """Periodo que se puede calcular, último periodo con datos en TOTALIZADO3 (periodo_datos: si el mes anterior
    todavía no se cargó, la pantalla muestra y calcula hasta este) y periodos que se pueden calcular (para el Excel)."""
    calculable = periodo_calculable()
    return {"periodo_calculo": calculable,
            "periodo_datos": calculoRep.queryUltimoPeriodoDatosTMI(db, int(calculable)),
            "solo_periodo_anterior": TMI_CALCULO_SOLO_PERIODO_ANTERIOR,
            "periodos": resultadoRep.queryPeriodosResultadoTMI(db),
            # copias de TOTALIZADO3 guardadas al cierre: con ellas se calcula el periodo "como fue"
            "backups": backupRep.queryBackupsTMI(db)}


def calcularServ(db: Session, periodo: str, origen: str = "ACTUAL", usuario: Optional[str] = None) -> dict:
    """origen: ACTUAL = TOTALIZADO3 de hoy (enero..periodo); BACKUP = la copia del cierre del periodo (como fue,
    periodo_backup = periodo). Los dos en tiempo real: el resultado no se guarda."""
    p = periodo_valido(periodo)
    if not se_puede_calcular(periodo):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No se puede calcular {periodo}: el último periodo que se puede calcular es "
                                   f"{periodo_calculable()}.")
    errores = configuracionRep.queryValidarConfigTMI(db)
    if errores:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errores)
    origen = (origen or "ACTUAL").upper()
    logger.info("Usuario '%s' calculando %s con datos %s", usuario, periodo, origen)
    return {"periodo": periodo, "origen": origen, "puntajes": calculoRep.queryCalcularTMI(db, p, origen, usuario)}
