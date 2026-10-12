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
    # desactivado por ahora: tmi_estandar_categoria aún no tiene datos
    # "tmi_estandar_categoria": tmiRep.queryInsertEstandarCategoria,
}


# procesos internos
def periodo_a_generar(hoy: date) -> str:
    """El cierre del mes M genera el periodo M-1 (ej. cierre de 2026-09 -> 202608).
    En enero se genera diciembre del año anterior (ej. cierre de 2027-01 -> 202612)."""
    if hoy.month == 1:
        return f"{hoy.year - 1}12"
    return f"{hoy.year}{hoy.month - 1:02d}"


def periodo_siguiente(periodo: str) -> str:
    anio, mes = int(periodo[:4]), int(periodo[4:])
    return f"{anio + 1}01" if mes == 12 else f"{anio}{mes + 1:02d}"


def fecha_cierre_de_periodo(periodo: str) -> date:
    """El periodo M se cierra en el mes M+1, el día CIERRE_DIA_DEFAULT (ej. 202612 -> 2027-01-07)."""
    siguiente = periodo_siguiente(periodo)
    anio, mes = int(siguiente[:4]), int(siguiente[4:])
    ultimo_dia = calendar.monthrange(anio, mes)[1]
    return date(anio, mes, max(1, min(CIERRE_DIA_DEFAULT, ultimo_dia)))


def _detalle(e: Exception) -> str:
    return str(e.detail) if isinstance(e, HTTPException) else str(e)


def _conteos(db: Session, hasta: str) -> dict[str, dict[str, int]]:
    """Filas por periodo de cada tabla del cierre: {tabla: {periodo: filas}}."""
    return {tabla: cierreRep.queryConteoPorPeriodo(db, tabla, hasta) for tabla in INSERTS_CIERRE}


def inicializarCierreServ(db: Session, hoy: date | None = None):
    """Crea la tabla cierre si no existe e inserta la fecha por defecto del mes actual."""
    hoy = hoy or date.today()
    cierreRep.queryCrearTablaCierre(db)
    periodo = periodo_a_generar(hoy)
    if cierreRep.queryInsertCierreDefault(db, periodo, fecha_cierre_de_periodo(periodo)):
        logger.warning("Cierre por defecto registrado: periodo %s, fecha %s", periodo, fecha_cierre_de_periodo(periodo))


def _prepararCierres(db: Session, hoy: date) -> dict[str, str]:
    """Deja listos los cierres desde el primer periodo con datos hasta el último cierre cuya fecha ya llegó:
    crea la fila de cierre de cada periodo que falte (02 viene de 01, 03 de 02...), reabre los cierres con
    ERROR que ya se pueden generar porque se guardaron datos nuevos, y los EJECUTADO que se quedaron sin datos.
    Devuelve el primer periodo con datos de cada tabla."""
    objetivo = cierreRep.queryUltimoPeriodoCierre(db, hoy)
    if not objetivo:
        return {}
    conteos = _conteos(db, objetivo)
    origenes = {tabla: min(c) for tabla, c in conteos.items() if c}
    if not origenes:
        return {}

    periodos = []
    periodo = periodo_siguiente(min(origenes.values()))
    while periodo <= objetivo:
        periodos.append(periodo)
        if cierreRep.queryInsertCierreDefault(db, periodo, fecha_cierre_de_periodo(periodo)):
            logger.warning("Cierre registrado para completar periodos: %s", periodo)
        periodo = periodo_siguiente(periodo)

    # simula el cierre en orden para saber qué periodos se pueden generar con los datos actuales
    disponibles = {tabla: set(c) for tabla, c in conteos.items()}
    generables = set()
    for periodo in periodos:
        anterior = calcular_periodo_anterior(periodo)
        ok = True
        for tabla in INSERTS_CIERRE:
            if periodo in disponibles[tabla]:
                continue
            if anterior in disponibles[tabla]:
                disponibles[tabla].add(periodo)
            elif not (tabla in origenes and anterior < origenes[tabla]):
                ok = False
        if ok:
            generables.add(periodo)

    for cierre in cierreRep.queryListaCierre(db):
        periodo = cierre["periodo"].strip()
        if periodo not in periodos:
            continue
        sin_datos = any(
            conteos[tabla].get(periodo, 0) == 0
            for tabla in INSERTS_CIERRE
            if tabla not in origenes or periodo >= origenes[tabla]
        )
        if (cierre["estado"] == "EJECUTADO" and sin_datos) or (cierre["estado"] == "ERROR" and periodo in generables):
            logger.warning("Cierre %s reabierto (%s)", periodo, cierre["estado"])
            cierreRep.queryReabrirCierre(db, cierre["id"])
    return origenes


def _ejecutarInserts(db: Session, periodo_actual: str, origenes: dict[str, str]) -> int:
    periodo_anterior = calcular_periodo_anterior(periodo_actual)
    total = 0
    for tabla, insertar in INSERTS_CIERRE.items():
        # si el periodo ya tiene datos no se vuelve a insertar (evita duplicados)
        if cierreRep.queryContarPeriodo(db, tabla, periodo_actual) > 0:
            logger.warning("Cierre %s: %s ya tiene datos, se omite", periodo_actual, tabla)
            continue
        # la tabla empieza en un periodo posterior: todavía no hay de dónde copiar
        if tabla in origenes and periodo_anterior < origenes[tabla]:
            logger.warning("Cierre %s: %s empieza en %s, se omite", periodo_actual, tabla, origenes[tabla])
            continue
        if cierreRep.queryContarPeriodo(db, tabla, periodo_anterior) == 0:
            raise RuntimeError(f"{tabla} no tiene datos en el periodo anterior {periodo_anterior}")
        result = insertar(db, periodo_actual, periodo_anterior)
        total += result.get("rows_inserted", 0) or 0
        logger.warning("Cierre %s: %s filas insertadas en %s", periodo_actual, result.get("rows_inserted"), tabla)
    return total


def _filasPeriodo(db: Session, periodo: str) -> int:
    return sum(cierreRep.queryContarPeriodo(db, tabla, periodo) for tabla in INSERTS_CIERRE)


def _actualizarFilasCierres(db: Session):
    """filas_insertadas de cada cierre ejecutado = filas que tiene su periodo en las tablas del cierre."""
    cierres = [c for c in cierreRep.queryListaCierre(db) if c["estado"] == "EJECUTADO"]
    if not cierres:
        return
    conteos = _conteos(db, max(c["periodo"].strip() for c in cierres))
    for cierre in cierres:
        periodo = cierre["periodo"].strip()
        cierreRep.queryActualizarFilasCierre(db, cierre["id"], sum(c.get(periodo, 0) for c in conteos.values()))


def ejecutarCierreServ(db: Session, hoy: date | None = None):
    """Ejecuta todos los cierres cuya fecha de cierre ya llegó o ya pasó, de cualquier periodo
    (ej. cierre programado el 07 y hoy es 11: se ejecuta igual). Van del periodo más antiguo al más reciente,
    completando los periodos que falten desde el primero con datos."""
    hoy = hoy or date.today()
    inicializarCierreServ(db, hoy)
    origenes = _prepararCierres(db, hoy)
    resultados = []
    for cierre in cierreRep.queryTomarCierresPendientes(db, hoy):
        periodo = cierre["periodo"].strip()
        try:
            insertadas = _ejecutarInserts(db, periodo, origenes)
            filas = _filasPeriodo(db, periodo)
            cierreRep.queryFinalizarCierre(db, cierre["id"], "EJECUTADO", filas, None)
            resultados.append({"periodo": periodo, "estado": "EJECUTADO", "filas_insertadas": insertadas, "filas_periodo": filas})
        except Exception as e:
            db.rollback()
            logger.error("Error en cierre %s: %s", periodo, _detalle(e), exc_info=True)
            cierreRep.queryFinalizarCierre(db, cierre["id"], "ERROR", None, _detalle(e))
            resultados.append({"periodo": periodo, "estado": "ERROR", "mensaje": _detalle(e)})
    # cada vez que se guardan datos nuevos en las tablas, se actualizan las filas de cada periodo
    _actualizarFilasCierres(db)
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
