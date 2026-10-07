import asyncio
import calendar
import logging
import os
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.main.db.databaseConexion import SessionLocal
from src.main.repositories import cierreRep, tmiRep
from src.main.service.tmiServ import calcular_periodo_anterior

logger = logging.getLogger(__name__)

# Día del mes que se usa como fecha de cierre por defecto
CIERRE_DIA_DEFAULT = int(os.getenv("CIERRE_DIA_DEFAULT", "07"))
# Cada cuántos minutos se revisa si hoy es la fecha de cierre
CIERRE_INTERVALO_MINUTOS = int(os.getenv("CIERRE_INTERVALO_MINUTOS", "60"))

# Inserción del periodo nuevo copiando el periodo anterior (funciones existentes)
INSERTS_CIERRE = {
    "tmi_centro": tmiRep.queryInsertCentrosTMI,
    "tmi_estandar_tipo": tmiRep.queryInsertEstandarTipo,
    "tmi_estandar_nivel": tmiRep.queryInsertEstandarNivel,
    "tmi_estandar_categoria": tmiRep.queryInsertEstandarCategoria,
}


# procesos internos
def periodo_a_generar(hoy: date) -> str:
    """El cierre del mes M genera el periodo M-1 (ej. cierre de 2026-09 -> 202608)."""
    return calcular_periodo_anterior(f"{hoy.year}{hoy.month:02d}")


def fecha_cierre_default(hoy: date) -> date:
    ultimo_dia = calendar.monthrange(hoy.year, hoy.month)[1]
    return date(hoy.year, hoy.month, max(1, min(CIERRE_DIA_DEFAULT, ultimo_dia)))


def _detalle(e: Exception) -> str:
    return str(e.detail) if isinstance(e, HTTPException) else str(e)


def inicializarCierreServ(db: Session, hoy: date | None = None):
    """Crea la tabla cierre si no existe e inserta la fecha por defecto del mes actual."""
    hoy = hoy or date.today()
    cierreRep.queryCrearTablaCierre(db)
    periodo = periodo_a_generar(hoy)
    if cierreRep.queryInsertCierreDefault(db, periodo, fecha_cierre_default(hoy)):
        logger.warning("Cierre por defecto registrado: periodo %s, fecha %s", periodo, fecha_cierre_default(hoy))


def _ejecutarInserts(db: Session, periodo_actual: str) -> int:
    periodo_anterior = calcular_periodo_anterior(periodo_actual)
    total = 0
    for tabla, insertar in INSERTS_CIERRE.items():
        # si el periodo ya tiene datos no se vuelve a insertar (evita duplicados)
        if cierreRep.queryContarPeriodo(db, tabla, periodo_actual) > 0:
            logger.warning("Cierre %s: %s ya tiene datos, se omite", periodo_actual, tabla)
            continue
        if cierreRep.queryContarPeriodo(db, tabla, periodo_anterior) == 0:
            raise RuntimeError(f"{tabla} no tiene datos en el periodo anterior {periodo_anterior}")
        result = insertar(db, periodo_actual, periodo_anterior)
        total += result.get("rows_inserted", 0) or 0
        logger.warning("Cierre %s: %s filas insertadas en %s", periodo_actual, result.get("rows_inserted"), tabla)
    return total


def ejecutarCierreServ(db: Session, hoy: date | None = None):
    """Ejecuta los inserts si la fecha de cierre es igual a la fecha actual."""
    hoy = hoy or date.today()
    inicializarCierreServ(db, hoy)
    resultados = []
    for cierre in cierreRep.queryTomarCierreHoy(db, hoy):
        periodo = cierre["periodo"].strip()
        try:
            filas = _ejecutarInserts(db, periodo)
            cierreRep.queryFinalizarCierre(db, cierre["id"], "EJECUTADO", filas, None)
            resultados.append({"periodo": periodo, "estado": "EJECUTADO", "filas_insertadas": filas})
        except Exception as e:
            db.rollback()
            logger.error("Error en cierre %s: %s", periodo, _detalle(e), exc_info=True)
            cierreRep.queryFinalizarCierre(db, cierre["id"], "ERROR", None, _detalle(e))
            resultados.append({"periodo": periodo, "estado": "ERROR", "mensaje": _detalle(e)})
    return resultados


# endpoints
def queryListaCierreServ(db: Session):
    try:
        return cierreRep.queryListaCierre(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryUpdateFechaCierreServ(db: Session, periodo: str, fecha_cierre: date, usuario: str | None):
    # el cierre solo se ejecuta cuando la fecha de cierre es igual a hoy
    if fecha_cierre < date.today():
        raise HTTPException(status_code=400, detail="La fecha de cierre no puede ser anterior a hoy")
    try:
        filas = cierreRep.queryUpdateFechaCierre(db, periodo, fecha_cierre, usuario)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if filas == 0:
        raise HTTPException(status_code=404, detail="El periodo no existe o el cierre ya fue ejecutado")
    return {"message": "Fecha de cierre actualizada correctamente", "periodo": periodo, "fecha_cierre": fecha_cierre}


# tarea programada
def _revisarCierre():
    db = SessionLocal()
    try:
        return ejecutarCierreServ(db)
    finally:
        db.close()


async def tareaCierre():
    """Revisa al iniciar y luego cada CIERRE_INTERVALO_MINUTOS si hoy es la fecha de cierre."""
    while True:
        try:
            resultados = await asyncio.to_thread(_revisarCierre)
            if resultados:
                logger.warning("Resultado del cierre automático: %s", resultados)
        except Exception as e:
            logger.error("Error revisando el cierre automático: %s", e, exc_info=True)
        await asyncio.sleep(CIERRE_INTERVALO_MINUTOS * 60)
