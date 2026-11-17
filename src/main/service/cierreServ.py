import asyncio
import calendar
import logging
import os
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from sqlalchemy import text

from src.main.db.auditoria import USUARIO_ACTUAL
from src.main.db.databaseConexion import SessionLocal, engine
from src.main.repositories import backupRep, calculoRep, cierreRep, configuracionRep, estandarRep

logger = logging.getLogger(__name__)

# Día del mes que se usa como fecha de cierre por defecto
CIERRE_DIA_DEFAULT = int(os.getenv("CIERRE_DIA_DEFAULT", "07"))
# Cada cuántos minutos se revisa si hoy es la fecha de cierre
CIERRE_INTERVALO_MINUTOS = int(os.getenv("CIERRE_INTERVALO_MINUTOS", "60"))

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


def dia_cierre(calendario: dict | None, mes: int) -> int:
    """Día de cierre del periodo MM en el calendario de su año: el del mes o, si no tiene, el general."""
    if not calendario:
        return CIERRE_DIA_DEFAULT
    return calendario.get(f"dia_{mes:02d}") or calendario.get("dia_fijo") or CIERRE_DIA_DEFAULT


def fecha_cierre_de_periodo(periodo: str, calendario: dict | None = None) -> date:
    """El periodo M se cierra en el mes M+1, el día que dice el calendario de su año (ej. 202612, día 7 -> 2027-01-07).
    Si el mes no tiene ese día (31 en febrero), se usa su último día."""
    siguiente = periodo_siguiente(periodo)
    anio, mes = int(siguiente[:4]), int(siguiente[4:])
    ultimo_dia = calendar.monthrange(anio, mes)[1]
    return date(anio, mes, max(1, min(dia_cierre(calendario, int(periodo[4:])), ultimo_dia)))


def _calendario(db: Session, anio: int) -> dict | None:
    """Calendario de cierre del año; si no existe, lo crea con el día general del año anterior."""
    cierreRep.queryAsegurarCalendario(db, anio, CIERRE_DIA_DEFAULT)
    filas = cierreRep.queryCalendario(db, anio)
    return filas[0] if filas else None


def _fechaCierre(db: Session, periodo: str) -> date:
    return fecha_cierre_de_periodo(periodo, _calendario(db, int(periodo[:4])))


def _detalle(e: Exception) -> str:
    return str(e.detail) if isinstance(e, HTTPException) else str(e)


def inicializarCierreServ(db: Session, hoy: date | None = None):
    """Registra el cierre del periodo que se cierra este mes, con la fecha de su calendario
    (las tablas tmi_cierre y tmi_cierre_calendario las crea src/main/model)."""
    hoy = hoy or date.today()
    periodo = periodo_a_generar(hoy)
    fecha = _fechaCierre(db, periodo)
    if cierreRep.queryInsertCierreDefault(db, periodo, fecha):
        logger.warning("Cierre registrado: periodo %s, fecha %s", periodo, fecha)


def _guardarCopiaTMI(db: Session, periodo: str):
    """Guarda la copia de TOTALIZADO3 del periodo (TOTALIZADO3_BACKUP; si ya existe no se toca): son los datos "como
    fueron" al cierre. El resultado no se guarda: se calcula en tiempo real con esta copia o con los datos de hoy.
    Con la configuración con errores no se cierra."""
    errores = configuracionRep.queryValidarConfigTMI(db)
    if errores:
        primero = errores[0]
        n = len(errores)
        raise RuntimeError(f"No se cerró el TMI: hay {n} {'problema' if n == 1 else 'problemas'} en la configuración. "
                           f"Corríjalos en Variables o Indicadores. El primero: {primero.get('elemento')}: "
                           f"{primero.get('problema')}")
    copia = backupRep.queryBackupTotalizado3TMI(db, int(periodo), "CIERRE")
    logger.warning("Cierre %s: copia de TOTALIZADO3 %s (%s filas)", periodo,
                   "guardada" if copia["copiado"] else "ya existía", copia["filas"])


# Mensaje del cierre que espera datos: el cierre queda PENDIENTE y se vuelve a intentar en cada revisión
_ESPERA = "Esperando datos"


def _mensajeEspera(periodo: str) -> str:
    anio, mes = int(periodo[:4]), int(periodo[4:])
    return (f"{_ESPERA}: TOTALIZADO3 todavía no tiene datos de {_MESES[mes - 1].lower()} {anio}. "
            f"El cierre se ejecutará solo cuando lleguen.")


def _reabrirSinDatos(db: Session):
    """Los cierres que quedaron en ERROR porque TOTALIZADO3 aún no tenía datos vuelven a PENDIENTE
    (antes de este cambio un cierre así quedaba en ERROR y no se reintentaba al día siguiente)."""
    for cierre in cierreRep.queryListaCierre(db):
        if cierre["estado"] == "ERROR" and "todavía no tiene datos" in (cierre.get("mensaje") or ""):
            logger.warning("Cierre %s vuelve a PENDIENTE: esperaba datos de TOTALIZADO3", cierre["periodo"].strip())
            cierreRep.queryReabrirCierre(db, cierre["id"])


def _actualizarFilasCierres(db: Session):
    """filas_insertadas de cada cierre ejecutado = filas de su periodo (estándares y % Acept del mes)."""
    for cierre in cierreRep.queryListaCierre(db):
        if cierre["estado"] == "EJECUTADO":
            filas = estandarRep.contarFilasCierrePeriodoTMI(db, cierre["periodo"].strip())
            cierreRep.queryActualizarFilasCierre(db, cierre["id"], filas)


def ejecutarCierreServ(db: Session, hoy: date | None = None):
    """Ejecuta todos los cierres cuya fecha de cierre ya llegó o ya pasó, de cualquier periodo
    (ej. cierre programado el 07 y hoy es 11: se ejecuta igual). Van del periodo más antiguo al más reciente."""
    hoy = hoy or date.today()
    inicializarCierreServ(db, hoy)
    _reabrirSinDatos(db)
    resultados = []
    for cierre in cierreRep.queryTomarCierresPendientes(db, hoy):
        periodo = cierre["periodo"].strip()
        # sin datos del mes en TOTALIZADO3 no es un error: el cierre espera (PENDIENTE) y se reintenta en la
        # próxima revisión (cada CIERRE_INTERVALO_MINUTOS) hasta que lleguen los datos
        if not calculoRep.queryHayDatosTotalizadoTMI(db, int(periodo)):
            cierreRep.queryFinalizarCierre(db, cierre["id"], "PENDIENTE", None, _mensajeEspera(periodo))
            logger.info("Cierre %s en espera: TOTALIZADO3 todavía no tiene datos del periodo", periodo)
            continue
        try:
            # al llegar la fecha de cierre, el mes toma el estándar fijo y el % Acept fijo del año (si aún no tiene valor)
            insertadas = estandarRep.aplicarCierrePeriodoTMI(db, periodo)
            # con los estándares y % Acept del mes ya listos, el cierre guarda la copia de los datos del periodo
            _guardarCopiaTMI(db, periodo)
            filas = estandarRep.contarFilasCierrePeriodoTMI(db, periodo)
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


_MESES = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
          "Noviembre", "Diciembre")
_BLOQUEADOS = ("EJECUTADO", "EN_PROCESO")


def _mesesCalendario(calendario: dict, cierres: dict[str, dict]) -> list[dict]:
    """Los 12 periodos del año: su día propio, la fecha de cierre (la real si ya tiene cierre) y su estado."""
    anio = calendario["anio"]
    meses = []
    for mes in range(1, 13):
        periodo = f"{anio}{mes:02d}"
        cierre = cierres.get(periodo)
        meses.append({
            "mes": mes,
            "periodo": periodo,
            "dia": calendario.get(f"dia_{mes:02d}"),
            "fecha_cierre": cierre["fecha_cierre"] if cierre else fecha_cierre_de_periodo(periodo, calendario),
            "estado": cierre["estado"] if cierre else None,
            "bloqueado": bool(cierre and cierre["estado"] in _BLOQUEADOS),
        })
    return meses


def queryCalendarioServ(db: Session):
    """Calendario de cierre por año (del más reciente al más antiguo), con los 12 periodos de cada año."""
    try:
        hoy = date.today()
        _calendario(db, int(periodo_a_generar(hoy)[:4]))
        _calendario(db, hoy.year)
        cierres = {c["periodo"].strip(): c for c in cierreRep.queryListaCierre(db)}
        calendarios = cierreRep.queryCalendario(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    for cal in calendarios:
        cal["meses"] = _mesesCalendario(cal, cierres)
    return calendarios


def queryGuardarCalendarioServ(db: Session, anio: int, dia_fijo: int, dias: dict[str, int | None],
                               usuario: str | None) -> bool:
    """Guarda el día general y el de cada periodo del año, y reprograma los cierres que aún no se ejecutan.
    Devuelve True si quedó algún cierre cuya fecha ya llegó (hay que ejecutarlo ahora)."""
    hoy = date.today()
    actual = _calendario(db, anio) or {}
    nuevo = {"anio": anio, "dia_fijo": dia_fijo, **dias}
    cierres = {c["periodo"].strip(): c for c in cierreRep.queryListaCierre(db)}
    reprogramar = []
    for mes in range(1, 13):
        periodo, col = f"{anio}{mes:02d}", f"dia_{mes:02d}"
        cierre = cierres.get(periodo)
        antes = cierre["fecha_cierre"] if cierre else fecha_cierre_de_periodo(periodo, actual)
        despues = fecha_cierre_de_periodo(periodo, nuevo)
        nombre = f"{_MESES[mes - 1]} {anio}"
        if cierre and cierre["estado"] in _BLOQUEADOS:
            # un cierre ejecutado conserva su fecha: solo se rechaza si se cambió su día propio
            if dias.get(col) != actual.get(col):
                raise HTTPException(status_code=400, detail=f"El cierre de {nombre} ya se ejecutó: no se cambia su día")
            continue
        if despues == antes:
            continue
        # un periodo sin cierre cuya fecha ya pasó no está programado: el cambio no le afecta
        if despues < hoy and (cierre or antes >= hoy):
            raise HTTPException(status_code=400,
                                detail=f"El cierre de {nombre} quedaría el {despues:%d/%m/%Y}, antes de hoy")
        if cierre:
            reprogramar.append((periodo, despues))
    try:
        cierreRep.queryGuardarCalendario(db, anio, dia_fijo, dias, usuario)
        for periodo, fecha in reprogramar:
            cierreRep.queryReprogramarCierre(db, periodo, fecha, usuario)
            logger.warning("Cierre %s reprogramado al %s por %s", periodo, fecha, usuario)
        # el periodo que se cierra este mes puede no tener su fila todavía
        inicializarCierreServ(db, hoy)
        return cierreRep.queryHayCierresPorEjecutar(db, hoy)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# tarea programada
def revisarCierre():
    """Ejecuta los cierres cuya fecha ya llegó, con su propia sesión (tarea programada o al guardar el calendario).
    Con varios procesos o instancias del backend, solo uno revisa a la vez (lock TMI_CIERRE en SQL Server); los
    demás no hacen nada en esa vuelta."""
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as candado:
        tomado = candado.execute(text(
            "DECLARE @r INT; EXEC @r = sp_getapplock @Resource = N'TMI_CIERRE', @LockMode = 'Exclusive', "
            "@LockOwner = 'Session', @LockTimeout = 0; SELECT @r")).scalar()
        if tomado is None or tomado < 0:
            logger.info("Otro proceso está revisando el cierre: se omite esta vuelta")
            return []
        db = SessionLocal()
        try:
            return ejecutarCierreServ(db)
        finally:
            db.close()
            candado.execute(text("EXEC sp_releaseapplock @Resource = N'TMI_CIERRE', @LockOwner = 'Session'"))


async def tareaCierre():
    """Revisa al iniciar y luego cada CIERRE_INTERVALO_MINUTOS si hoy es la fecha de cierre."""
    USUARIO_ACTUAL.set("CIERRE AUTOMÁTICO")   # usuario de sus cambios en el historial de la configuración
    while True:
        try:
            resultados = await asyncio.to_thread(revisarCierre)
            if resultados:
                logger.warning("Resultado del cierre automático: %s", resultados)
        except Exception as e:
            logger.error("Error revisando el cierre automático: %s", e, exc_info=True)
        await asyncio.sleep(CIERRE_INTERVALO_MINUTOS * 60)
