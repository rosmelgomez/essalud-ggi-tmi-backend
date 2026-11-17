"""Cálculo del TMI en tiempo real (usp_tmi_calcular, que no escribe nada): datos del periodo, origen de los datos y
resultado en memoria."""

import logging
import os
import threading
import time
from typing import Dict, Optional, Tuple

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core.tmiConfig import TMI_TOTALIZADO3
from src.main.db.databaseConexion import SessionLocal
from src.main.repositories.backupRep import queryHayBackupTMI
from src.main.repositories.tmiBaseRep import crear_tablas_formula, name_server, quitar_tablas_formula

logger = logging.getLogger(__name__)


_MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'setiembre', 'octubre',
          'noviembre', 'diciembre']


def queryHayDatosTotalizadoTMI(db: Session, periodo: int) -> bool:
    """True si TOTALIZADO3 tiene algún registro del periodo (AAAAMM)."""
    try:
        return db.execute(text(f"SELECT CASE WHEN EXISTS (SELECT 1 FROM {TMI_TOTALIZADO3} WHERE periodo = {int(periodo)}) "
                               f"THEN 1 ELSE 0 END")).scalar() == 1
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryUltimoPeriodoDatosTMI(db: Session, hasta: int) -> Optional[str]:
    """Último periodo (AAAAMM) con datos en TOTALIZADO3 hasta el periodo dado (se busca en los 12 meses anteriores)."""
    try:
        desde = (int(hasta) // 100 - 1) * 100 + int(hasta) % 100
        p = db.execute(text(f"SELECT MAX(periodo) FROM {TMI_TOTALIZADO3} "
                            f"WHERE periodo BETWEEN {desde} AND {int(hasta)}")).scalar()
        return str(p) if p else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


ORIGENES = ("ACTUAL", "BACKUP")


def _origen(origen: Optional[str]) -> str:
    o = (origen or "ACTUAL").upper()
    if o not in ORIGENES:
        raise HTTPException(status_code=400, detail="El origen de los datos debe ser ACTUAL o BACKUP.")
    return o


def _fuente(origen: Optional[str]) -> str:
    """Origen de los datos del cálculo (siempre en tiempo real; el resultado no se guarda): ACTUAL con TOTALIZADO3 de
    hoy o BACKUP con la copia del cierre (TOTALIZADO3_BACKUP, periodo_backup = periodo). Sin origen, ACTUAL."""
    return _origen(origen) if origen is not None else "ACTUAL"


def _validarDatos(db: Session, periodo: int, origen: str):
    """400 si el periodo no tiene los datos que necesita el cálculo (copia del cierre o TOTALIZADO3 del mes)."""
    anio, mes = divmod(int(periodo), 100)
    if origen == "BACKUP" and not queryHayBackupTMI(db, periodo):
        raise HTTPException(status_code=400,
                            detail=f"No se puede calcular {periodo} con los datos del cierre: los datos de "
                                   f"{_MESES[mes - 1]} {anio} se guardan cuando se cierra el periodo.")
    if origen == "ACTUAL" and not queryHayDatosTotalizadoTMI(db, periodo):
        raise HTTPException(status_code=400,
                            detail=f"No se puede calcular {periodo}: todavía no llegan los datos de "
                                   f"{_MESES[mes - 1]} {anio}.")


# ---------- cálculo en tiempo real (no se guarda) ----------
# usp_tmi_calcular devuelve el resultado sin escribir nada. Una pantalla pide varias cosas
# del mismo cálculo (resultado, justificación, términos, Excel), así que se guarda en memoria y se vuelve a calcular
# cuando cambian los datos (firma de TOTALIZADO3 o de la copia), la configuración (tmi_config_historial) o pasan
# TMI_VIVO_CACHE_SEG segundos (por las tablas de configuración sin historial).
_VIVO_SEG = int(os.getenv("TMI_VIVO_CACHE_SEG", "600"))
_VIVO_MAX = 24
_vivo_cache: Dict[Tuple[int, str], Tuple[tuple, float, dict]] = {}
_vivo_locks: Dict[Tuple[int, str], threading.Lock] = {}
_vivo_lock = threading.Lock()


def _firmaVivo(db: Session, periodo: int, origen: str) -> tuple:
    """Cambia si cambian los datos que usa el cálculo o la configuración."""
    anio = int(periodo) // 100
    config = db.execute(text(f"SELECT MAX(id) FROM {name_server}.tmi_config_historial")).scalar()
    if origen == "BACKUP":
        datos = db.execute(text(f"SELECT COUNT_BIG(*), MAX(fecha_backup) FROM {name_server}.TOTALIZADO3_BACKUP "
                                f"WHERE periodo_backup = :p"), {"p": int(periodo)}).fetchone()
    else:
        datos = db.execute(text(f"SELECT COUNT_BIG(*), SUM(CAST(cantidad AS BIGINT)), MAX(fechamod), MAX(fechacrea), "
                                f"CHECKSUM_AGG(CHECKSUM(ID, cantidad)) FROM {TMI_TOTALIZADO3} "
                                f"WHERE periodo BETWEEN :d AND :p"), {"d": anio * 100 + 1, "p": int(periodo)}).fetchone()
    return (config, tuple(datos))


def _ejecutarVivo(db: Session, periodo: int, origen: str, usuario: Optional[str]) -> dict:
    """usp_tmi_calcular: 4 resultados (final, resultado del mes de corte, términos, cada mes). Antes
    Python lee la fórmula de cada indicador y deja sus términos en la conexión (#formula, #termino)."""
    crear_tablas_formula(db)
    cur = db.connection().connection.cursor()
    try:
        cur.execute(f"EXEC {name_server}.usp_tmi_calcular @PERIODO = ?, @ORIGEN = ?, @USUARIO = ?",
                    int(periodo), origen, usuario)
        conjuntos = []
        while True:
            if cur.description:
                cols = [d[0] for d in cur.description]
                conjuntos.append([dict(zip(cols, fila)) for fila in cur.fetchall()])
            if not cur.nextset():
                break
    finally:
        cur.close()
        quitar_tablas_formula(db)
    if len(conjuntos) != 4:
        raise RuntimeError(f"usp_tmi_calcular devolvió {len(conjuntos)} resultados en lugar de 4")
    final, resultado, terminos, meses = conjuntos
    for f in final + resultado:
        f["visible"] = bool(f["visible"]) if f.get("visible") is not None else None
    for t in terminos:
        t["mediana"] = bool(t["mediana"])
        t["periodo_mediana"] = bool(t.get("periodo_mediana"))
    return {"periodo": int(periodo), "origen": origen, "final": final, "resultado": resultado,
            "terminos": terminos, "meses": meses}


def calcularVivoTMI(db: Session, periodo: int, origen: str = "ACTUAL", usuario: Optional[str] = None,
                    forzar: bool = False) -> dict:
    """Resultado del periodo calculado en tiempo real, sin guardar nada: ACTUAL con TOTALIZADO3 de hoy (enero..periodo)
    o BACKUP con la copia del cierre (periodo_backup = periodo). forzar = no usar el que está en memoria."""
    origen = _origen(origen)
    periodo = int(periodo)
    _validarDatos(db, periodo, origen)
    clave = (periodo, origen)
    with _vivo_lock:
        lock = _vivo_locks.setdefault(clave, threading.Lock())
    with lock:   # dos pedidos del mismo periodo a la vez: el segundo espera y usa el del primero
        firma = _firmaVivo(db, periodo, origen)
        guardado = _vivo_cache.get(clave)
        if not forzar and guardado and guardado[0] == firma and time.time() - guardado[1] < _VIVO_SEG:
            return guardado[2]
        inicio = time.time()
        try:
            datos = _ejecutarVivo(db, periodo, origen, usuario)
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        logger.info("TMI %s %s calculado en tiempo real en %.1f s", periodo, origen, time.time() - inicio)
        with _vivo_lock:
            if len(_vivo_cache) >= _VIVO_MAX and clave not in _vivo_cache:
                _vivo_cache.pop(min(_vivo_cache, key=lambda k: _vivo_cache[k][1]))
            _vivo_cache[clave] = (firma, time.time(), datos)
        return datos


def _calcularEnParalelo(db: Session, periodo: int, origenes) -> None:
    """Deja en memoria el cálculo en tiempo real de cada origen, todos a la vez: el primero con la conexión del pedido
    y los demás en hilos con su propia conexión (una conexión no corre dos consultas a la vez). Lo que se pida
    después sale de la memoria. Un error aquí no se muestra: el pedido de cada origen lo vuelve a intentar y lo
    informa."""
    origenes = list(dict.fromkeys(origenes))
    if len(origenes) < 2:
        return

    def otro(origen: str) -> None:
        sesion = SessionLocal()
        try:
            calcularVivoTMI(sesion, periodo, origen)
        except Exception as e:
            logger.warning("TMI %s %s: no se pudo calcular en paralelo: %s", periodo, origen, e)
        finally:
            sesion.close()

    hilos = [threading.Thread(target=otro, args=(o,), daemon=True) for o in origenes[1:]]
    for h in hilos:
        h.start()
    try:
        calcularVivoTMI(db, periodo, origenes[0])
    except Exception as e:
        logger.warning("TMI %s %s: no se pudo calcular en paralelo: %s", periodo, origenes[0], e)
    finally:
        for h in hilos:
            h.join()


def _puntajes(filas) -> dict:
    conteo: dict = {}
    for r in filas:
        conteo[r["puntaje"]] = conteo.get(r["puntaje"], 0) + 1
    return conteo


def queryCalcularTMI(db: Session, periodo: int, origen: str = "ACTUAL", usuario: Optional[str] = None):
    """Calcula los indicadores del periodo (AAAAMM) en tiempo real, sin guardar nada: ACTUAL con TOTALIZADO3 de hoy o
    BACKUP con la copia del cierre del periodo. Devuelve la cantidad de centros × indicadores por puntaje. Sin datos
    del periodo no se calcula (400)."""
    return _puntajes(calcularVivoTMI(db, periodo, _origen(origen), usuario, forzar=True)["resultado"])
