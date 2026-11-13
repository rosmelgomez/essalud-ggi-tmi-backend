"""TMI dinámico: catálogos (DIM y tablas de apoyo), validación, cálculo y resultados
(procedimientos y tablas de src/resources/sql/tmi)."""

import logging
import os
import threading
import time
from typing import Dict, Optional, Tuple

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core.tmiConfig import TMI_DIM, TMI_TOTALIZADO3
from src.main.db.databaseConexion import SessionLocal
from src.main.repositories.tmiBaseRep import (
    name_server,
    _consulta,
)

logger = logging.getLogger(__name__)


_CON_DIM_SERVICIO: Optional[bool] = None   # None = todavía no se comprobó si se puede leer DIM_SERVICIO


def queryGrupoActividadServicioTMI(db: Session):
    """Relación grupo -> actividad -> servicio (DIM_GRUPOACTIVIDADSERVICIO, sin las desactivadas) con sus
    descripciones, para elegir la lógica de las variables en cascada. Si DIM_SERVICIO no se puede leer (no existe en
    esa base), el servicio sale sin descripción."""
    global _CON_DIM_SERVICIO

    def consulta(con_servicio: bool) -> str:
     
        return f"""
        SELECT gas.tipgrupo, LTRIM(RTRIM(gr.desctipgrupo)) AS desctipgrupo,
               gas.actividad, COALESCE(NULLIF(LTRIM(RTRIM(act.desclarga)), ''), LTRIM(RTRIM(act.descactividad))) AS descactividad,
               act.Proceso AS proceso, act.Recurso AS recurso,
               gas.servicio, LTRIM(RTRIM(serv.desclarga)) AS descservicio
        FROM {TMI_DIM}.DIM_GRUPOACTIVIDADSERVICIO gas
        JOIN {TMI_DIM}.DIM_GRUPO gr ON gr.tipgrupo = gas.tipgrupo
        JOIN {TMI_DIM}.DIM_ACTIVIDAD act ON act.actividad = gas.actividad
        JOIN {TMI_DIM}.DIM_SERVICIO serv ON serv.servicio = gas.servicio
        WHERE ISNULL(gas.desactivado, 0) = 0
        ORDER BY gas.tipgrupo, gas.actividad, gas.servicio"""

    if _CON_DIM_SERVICIO is not False:
        try:
            filas = [dict(r) for r in db.execute(text(consulta(True))).mappings()]
            _CON_DIM_SERVICIO = True
            return filas
        except Exception as e:
            db.rollback()
            if "DIM_SERVICIO" not in str(e):
                raise HTTPException(status_code=500, detail=str(e))
            logger.warning("No se puede leer %s.DIM_SERVICIO: los servicios se listan sin descripción", TMI_DIM)
            _CON_DIM_SERVICIO = False
    return _consulta(db, consulta(False))


def queryCatalogoGruposTMI(db: Session):
    """Grupos de DIM_GRUPO (para la lógica de variables)."""
    return _consulta(db, f"""
        SELECT g.tipgrupo AS id, g.tipgrupo, g.desctipgrupo, g.desctipgrupo AS descripcion, g.Visible
        FROM {TMI_DIM}.DIM_GRUPO g WHERE g.Visible = 1 ORDER BY g.tipgrupo""")


def queryCatalogoGruposReporteTMI(db: Session):
    """Secciones del reporte para el indicador: los grupos visibles de DIM_GRUPO y los que ya usa algún indicador."""
    return _consulta(db, f"""
        SELECT g.tipgrupo AS id, LTRIM(RTRIM(g.desctipgrupo)) AS descripcion, g.Visible AS visible,
               (SELECT MIN(i.orden) FROM {name_server}.tmi_indicador i WHERE i.grupo = g.tipgrupo) AS orden
        FROM {TMI_DIM}.DIM_GRUPO g
        WHERE g.Visible = 1 OR EXISTS (SELECT 1 FROM {name_server}.tmi_indicador i WHERE i.grupo = g.tipgrupo)
        ORDER BY CASE WHEN EXISTS (SELECT 1 FROM {name_server}.tmi_indicador i WHERE i.grupo = g.tipgrupo) THEN 0 ELSE 1 END,
                 orden, descripcion""")


def queryCatalogoActividadesTMI(db: Session):
    return _consulta(db, f"""
        SELECT a.actividad AS id, a.actividad, a.descactividad, a.Recurso, a.Recurso AS recurso,
               a.desclarga, a.Visible, a.Proceso,
               COALESCE(NULLIF(LTRIM(RTRIM(a.desclarga)), ''), a.descactividad) AS descripcion
        FROM {TMI_DIM}.DIM_ACTIVIDAD a WHERE a.Visible = 1 AND a.actividad > 0
        ORDER BY a.actividad""")


def queryCatalogoServiciosTMI(db: Session, tipgrupo: int, actividad: int):
    """Servicios con datos en TOTALIZADO3 para un grupo y actividad (no existe DIM de servicios)."""
    return _consulta(db, f"""
        SELECT servicio AS id, MAX(descservicio) AS descripcion, MIN(periodo) AS periodo_desde, MAX(periodo) AS periodo_hasta
        FROM {TMI_TOTALIZADO3} WHERE tipgrupo = :tipgrupo AND actividad = :actividad
        GROUP BY servicio ORDER BY servicio""", {"tipgrupo": tipgrupo, "actividad": actividad})


def queryCatalogoTiposCalculoTMI(db: Session):
    return _consulta(db, f"SELECT codigo, descripcion FROM {name_server}.tmi_tipo_calculo ORDER BY codigo")


_COLS_RESULTADO = ("periodo, anio, id_indicador, orden, orden_red, red, codcentro, centro, nivel, nivel_estandar, tipo, categoria, "
                   "estandar, acept, aceptmenos, total, "
                   + ", ".join(f"periodo_{m:02d}" for m in range(1, 13)) + ", puntaje, motivo_na, visible, fecha_calculo")


def _fuente(origen: Optional[str]) -> str:
    """Origen de los datos del cálculo (siempre en tiempo real; el resultado no se guarda): ACTUAL con TOTALIZADO3 de
    hoy o BACKUP con la copia del cierre (TOTALIZADO3_BACKUP, periodo_backup = periodo). Sin origen, ACTUAL."""
    return _origen(origen) if origen is not None else "ACTUAL"


def _ordenFinal(filas):
    return sorted(filas, key=lambda r: (r.get("orden_red") is None, r.get("orden_red") or 0,
                                        r.get("orden") is None, r.get("orden") or 0, r["codcentro"]))


def queryResultadoIndicadorTMI(db: Session, periodo: int, id_indicador: int, origen: Optional[str] = None):
    """Resultado final del indicador en el periodo, como la hoja del Excel, calculado en tiempo real (ver _fuente)."""
    final = calcularVivoTMI(db, periodo, _fuente(origen))["final"]
    return _ordenFinal([r for r in final if r["id_indicador"] == int(id_indicador)])


def queryResultadoFinalTMI(db: Session, periodo: int, origen: Optional[str] = None):
    """Resultado final de todos los indicadores del periodo (Excel y dashboard), en tiempo real (ver _fuente)."""
    return _ordenFinal(calcularVivoTMI(db, periodo, _fuente(origen))["final"])


def queryCentrosActivosTMI(db: Session, periodo: int):
    """Códigos de los centros activos en el mes del periodo (flag del mes = 1 en tmi_centro), con la misma regla de
    año que usp_tmi_calcular: los del año o, si el año no tiene centros, los sin año."""
    anio, mes = periodo // 100, periodo % 100
    filas = _consulta(db, f"""
        SELECT DISTINCT c.codcentro
        FROM {name_server}.vw_tmi_centro_base c
        WHERE (c.anio = :anio OR (c.anio IS NULL AND NOT EXISTS (
                   SELECT 1 FROM {name_server}.vw_tmi_centro_base x WHERE x.anio = :anio)))
          AND c.codcentro IS NOT NULL AND c.f{mes:02d} = 1""", {"anio": anio})
    return {r["codcentro"] for r in filas}


def queryPeriodosResultadoTMI(db: Session, hasta: Optional[int] = None):
    """Periodos que se pueden calcular, del más reciente al más antiguo. origenes: con qué datos se puede calcular
    cada periodo (siempre en tiempo real):
    - BACKUP: el periodo tiene la copia del cierre (TOTALIZADO3_BACKUP).
    - ACTUAL: el periodo tiene datos en TOTALIZADO3 (hasta el último periodo que se puede calcular).
    origen_datos es ACTUAL si el periodo lo tiene; si no, BACKUP."""
    if hasta is None:
        from datetime import date
        from src.main.service.cierreServ import periodo_a_generar
        hasta = int(periodo_a_generar(date.today()))
    copias = {r["periodo_backup"] for r in _consulta(db, f"SELECT DISTINCT periodo_backup FROM {name_server}.TOTALIZADO3_BACKUP")}
    con_datos = {r["periodo"] for r in _consulta(db, f"SELECT DISTINCT periodo FROM {TMI_TOTALIZADO3} "
                                                     f"WHERE periodo <= :h", {"h": int(hasta)})}
    vivo = {"fecha_calculo": None, "indicadores": None, "centros": None, "en_vivo": True}
    salida = []
    for periodo in sorted(copias | con_datos, reverse=True):
        origenes: dict = {}
        if periodo in copias:
            origenes["BACKUP"] = dict(vivo)
        if periodo in con_datos:
            origenes["ACTUAL"] = dict(vivo)
        oficial = "ACTUAL" if "ACTUAL" in origenes else "BACKUP"
        datos = origenes[oficial]
        salida.append({"periodo": periodo, "indicadores": datos["indicadores"], "centros": datos["centros"],
                       "fecha_calculo": datos["fecha_calculo"], "origen_datos": oficial, "origenes": origenes})
    return salida


def queryValidarConfigTMI(db: Session):
    try:
        result = db.execute(text(f"EXEC {name_server}.usp_tmi_validar_config"))
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryAvisosConfigTMI(db: Session, periodo: int):
    """Avisos que no bloquean el cálculo: centros que quedarían NA por falta de estándar o de % Acept en el periodo."""
    try:
        result = db.execute(text(f"EXEC {name_server}.usp_tmi_avisos_config @PERIODO = :p"), {"p": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


def queryHayBackupTMI(db: Session, periodo: int) -> bool:
    """True si TOTALIZADO3_BACKUP tiene la copia del periodo (AAAAMM)."""
    return db.execute(text(f"SELECT CASE WHEN EXISTS (SELECT 1 FROM {name_server}.TOTALIZADO3_BACKUP "
                           f"WHERE periodo_backup = :p) THEN 1 ELSE 0 END"), {"p": int(periodo)}).scalar() == 1


def queryBackupsTMI(db: Session):
    """Copias de TOTALIZADO3 guardadas: periodo, filas, fecha y usuario de la copia (de la más reciente a la más antigua)."""
    return _consulta(db, f"""
        SELECT periodo_backup, COUNT(*) AS filas, MAX(fecha_backup) AS fecha_backup, MAX(usuario_backup) AS usuario_backup
        FROM {name_server}.TOTALIZADO3_BACKUP
        GROUP BY periodo_backup
        ORDER BY periodo_backup DESC""")


def queryBackupTotalizado3TMI(db: Session, periodo: int, usuario: Optional[str] = None, reemplazar: bool = False):
    """Copia TOTALIZADO3 (enero..periodo) en TOTALIZADO3_BACKUP con periodo_backup = periodo. TOTALIZADO3 solo se
    lee. Si la copia ya existe no se toca, salvo reemplazar. Devuelve {copiado, filas}."""
    try:
        fila = db.execute(text(f"EXEC {name_server}.usp_tmi_backup_totalizado3 @PERIODO = :p, @USUARIO = :u, "
                               f"@REEMPLAZAR = :r"), {"p": int(periodo), "u": usuario, "r": 1 if reemplazar else 0}
                          ).mappings().first()
        db.commit()
        return {"periodo": int(periodo), "copiado": bool(fila["copiado"]), "filas": fila["filas"]}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


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
# El mismo usp_tmi_calcular con @GUARDAR = 0 devuelve el resultado sin escribir nada. Una pantalla pide varias cosas
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
    """usp_tmi_calcular @GUARDAR = 0: 4 resultados (final, resultado del mes de corte, términos, cada mes)."""
    cur = db.connection().connection.cursor()
    try:
        cur.execute(f"EXEC {name_server}.usp_tmi_calcular @PERIODO = ?, @ORIGEN = ?, @USUARIO = ?, @GUARDAR = 0",
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
    if len(conjuntos) != 4:
        raise RuntimeError(f"usp_tmi_calcular devolvió {len(conjuntos)} resultados en lugar de 4")
    final, resultado, terminos, meses = conjuntos
    for f in final + resultado:
        f["visible"] = bool(f["visible"]) if f.get("visible") is not None else None
    for t in terminos:
        t["mediana"] = bool(t["mediana"])
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


def queryResultadoTMI(db: Session, periodo: int, origen: Optional[str] = None):
    """Valor y puntaje de cada mes por indicador y centro, una fila por mes hasta el corte, solo de los centros e
    indicadores del periodo pedido: cada mes calculado ahora con la regla de ese mes (ver _fuente)."""
    vivo = calcularVivoTMI(db, periodo, _fuente(origen))
    claves = {(r["id_indicador"], r["codcentro"]) for r in vivo["resultado"]}
    return [{"id_indicador": m["id_indicador"], "codcentro": m["codcentro"], "mes": m["mes"],
             "valor": m["valor"], "puntaje": m["puntaje"]}
            for m in vivo["meses"] if (m["id_indicador"], m["codcentro"]) in claves]


# ---------- justificación del cálculo: como fue (copia del cierre) y con los datos actuales ----------
_COLS_JUST = """origen_datos, periodo_backup, valor, estandar, acept, aceptmenos, puntaje, motivo_na, tipo_calculo,
                formula_alias, formula, formula_desarrollo, usuario_calculo, fecha_calculo"""


def _filasVivoJustificacion(db: Session, periodo: int, id_indicador: int, origen: str):
    """Filas de la justificación (resultado del mes con el centro) del cálculo en tiempo real."""
    vivo = calcularVivoTMI(db, periodo, origen)
    centros = {r["codcentro"]: r for r in vivo["final"] if r["id_indicador"] == int(id_indicador)}
    filas = []
    for r in vivo["resultado"]:
        if r["id_indicador"] != int(id_indicador):
            continue
        c = centros.get(r["codcentro"], {})
        filas.append({"codcentro": r["codcentro"], "centro": c.get("centro"), "red": c.get("red"),
                      "orden_red": c.get("orden_red"), "orden": c.get("orden"),
                      **{k: r.get(k) for k in (x.strip() for x in _COLS_JUST.split(","))}})
    return filas


def _filasComoFue(db: Session, periodo: int, id_indicador: Optional[int]):
    """Filas "como fue" (BACKUP) de un indicador o de todos (id_indicador None): el cálculo en tiempo real con la copia
    del cierre."""
    if not queryHayBackupTMI(db, periodo):
        return []
    if id_indicador is not None:
        return _filasVivoJustificacion(db, periodo, id_indicador, "BACKUP")
    return [dict(r) for r in calcularVivoTMI(db, periodo, "BACKUP")["resultado"]]


def _vivoJustificacion(db: Session, periodo: int) -> list:
    """Orígenes que la justificación calcula en tiempo real: como fue (BACKUP) si hay copia del cierre, y hoy (ACTUAL)
    si hay datos. Se calculan los dos a la vez."""
    origenes = ["BACKUP"] if queryHayBackupTMI(db, periodo) else []
    if queryHayDatosTotalizadoTMI(db, periodo):
        origenes.append("ACTUAL")
    _calcularEnParalelo(db, periodo, origenes)
    return origenes


def _cambio(b: Optional[dict], a: Optional[dict]) -> bool:
    """El valor o el puntaje no coinciden entre como fue (b) y hoy (a). Solo si están los dos."""
    return bool(b and a and (b["puntaje"] != a["puntaje"] or
                             round(b["valor"] or 0, 6) != round(a["valor"] or 0, 6) or
                             (b["valor"] is None) != (a["valor"] is None)))


def queryResumenCambiosTMI(db: Session, periodo: int):
    """Cuántos centros cambiaron en cada indicador del periodo entre como fue (BACKUP, ver queryJustificacionTMI) y
    con los datos de hoy (ACTUAL, en tiempo real): cambios = valor o puntaje distinto; cambios_puntaje = puntaje
    distinto. Lista todos los indicadores activos, primero los que cambiaron."""
    vivo = _vivoJustificacion(db, periodo)
    como_fue = {(r["id_indicador"], r["codcentro"]): r for r in _filasComoFue(db, periodo, None)}
    hoy = {}
    if "ACTUAL" in vivo:
        hoy = {(r["id_indicador"], r["codcentro"]): r for r in calcularVivoTMI(db, periodo, "ACTUAL")["resultado"]}
    indicadores = _consulta(db, f"""
        SELECT id, orden, codigo, indicador FROM {name_server}.tmi_indicador WHERE activo = 1 ORDER BY orden, id""")
    salida = []
    for ind in indicadores:
        claves = {k for k in como_fue.keys() | hoy.keys() if k[0] == ind["id"]}
        cambios = [k for k in claves if _cambio(como_fue.get(k), hoy.get(k))]
        salida.append({"id_indicador": ind["id"], "orden": ind["orden"], "codigo": ind["codigo"],
                       "indicador": ind["indicador"], "centros": len(claves), "cambios": len(cambios),
                       "cambios_puntaje": sum(1 for k in cambios if como_fue[k]["puntaje"] != hoy[k]["puntaje"])})
    salida.sort(key=lambda x: (x["cambios"] == 0, x["orden"] or 0, x["id_indicador"]))
    return {"periodo": int(periodo), "con_backup": queryHayBackupTMI(db, periodo),
            "con_datos_hoy": bool(hoy), "indicadores_con_cambios": sum(1 for x in salida if x["cambios"]),
            "centros_con_cambios": sum(x["cambios"] for x in salida), "indicadores": salida}


def queryJustificacionTMI(db: Session, periodo: int, id_indicador: int):
    """Resultado del indicador en el periodo por centro, como fue y con los datos de hoy, con su fórmula y su
    desarrollo. cambio = el valor o el puntaje no coinciden.
    - como fue (BACKUP): en tiempo real con la copia del cierre (TOTALIZADO3_BACKUP) y la configuración de hoy.
    - con los datos de hoy (ACTUAL): en tiempo real con TOTALIZADO3."""
    vivo = _vivoJustificacion(db, periodo)
    filas = _filasComoFue(db, periodo, id_indicador)
    if "ACTUAL" in vivo:
        filas += _filasVivoJustificacion(db, periodo, id_indicador, "ACTUAL")
    centros: dict = {}
    for f in filas:
        c = centros.setdefault(f["codcentro"], {"codcentro": f["codcentro"], "centro": f["centro"], "red": f["red"],
                                                "orden": (f["orden_red"] or 0, f["orden"] or 0), "BACKUP": None,
                                                "ACTUAL": None})
        c[f["origen_datos"]] = {k: f[k] for k in (x.strip() for x in _COLS_JUST.split(","))}
    salida = []
    for c in sorted(centros.values(), key=lambda x: (x["orden"], x["codcentro"])):
        c["cambio"] = _cambio(c["BACKUP"], c["ACTUAL"])
        del c["orden"]
        salida.append(c)
    return {"periodo": int(periodo), "id_indicador": int(id_indicador),
            "con_backup": queryHayBackupTMI(db, periodo),
            "cambios": sum(1 for c in salida if c["cambio"]),
            "origenes": sorted({f["origen_datos"] for f in filas}), "centros": salida}


_COLS_TERMINO = ("origen_datos", "codigo", "tipgrupo", "actividad", "servicio", "mediana", "texto", "valor_mes", "valor",
                 "filas_mes", "filas")


def queryTerminosResultadoTMI(db: Session, periodo: int, id_indicador: int, codcentro: int):
    """Valor de cada término de la fórmula (grupo, actividad y servicio) como fue (BACKUP) y con los datos de hoy
    (ACTUAL), en tiempo real como queryJustificacionTMI."""
    filas = []
    for o in _vivoJustificacion(db, periodo):
        filas += [{k: t[k] for k in _COLS_TERMINO} for t in calcularVivoTMI(db, periodo, o)["terminos"]
                  if t["id_indicador"] == int(id_indicador) and t["codcentro"] == int(codcentro)]
    return sorted(filas, key=lambda t: (len(t["codigo"]), t["codigo"], t["tipgrupo"], t["actividad"],
                                        t["servicio"] is None, t["servicio"] or 0, t["origen_datos"]))


def queryFilasCambiadasTMI(db: Session, periodo: int, id_indicador: int, codcentro: int, codigo: Optional[str] = None):
    """Filas de TOTALIZADO3 que cambiaron entre la copia del cierre del periodo y hoy, para los términos del indicador
    (o solo el término codigo) en el centro: cantidad antes y ahora, quién la modificó y cuándo. Filas nuevas (solo
    hoy) y borradas (solo en la copia). Un indicador MENSUAL solo mira el mes del periodo; uno ACUMULADO, enero..periodo.
    TOTALIZADO3 solo se lee."""
    periodo, anio = int(periodo), int(periodo) // 100
    if not queryHayBackupTMI(db, periodo):
        raise HTTPException(status_code=400, detail=f"El periodo {periodo} no tiene los datos del cierre guardados.")
    ind = db.execute(text(f"SELECT tipo_calculo FROM {name_server}.tmi_indicador WHERE id = :i"),
                     {"i": int(id_indicador)}).scalar()
    defs = _consulta(db, f"""
        SELECT codigo, tipgrupo, actividad, servicio FROM {name_server}.tmi_indicador_termino
        WHERE id_indicador = :i AND (:cod IS NULL OR codigo = :cod)""", {"i": int(id_indicador), "cod": codigo})
    if not defs:
        return []
    desde = periodo if (ind or "").upper() != "ACUMULADO" else anio * 100 + 1
    # filtro de los términos con valores enteros validados (no hay texto del usuario en el SQL)
    partes = [f"(X.tipgrupo = {int(d['tipgrupo'])} AND X.actividad = {int(d['actividad'])}"
              + (f" AND X.servicio = {int(d['servicio'])})" if d["servicio"] is not None else ")") for d in defs]
    filtro = " OR ".join(partes)
    cols = ("ID, periodo, tipgrupo, desctipgrupo, actividad, descactividad, servicio, descservicio, cantidad, "
            "usuariomod, fechamod")
    sel = lambda alias: ", ".join(f"{alias}.{c}" for c in cols.split(", "))
    sql = f"""
        SELECT COALESCE(b.ID, a.ID) AS ID, COALESCE(b.periodo, a.periodo) AS periodo,
               COALESCE(b.tipgrupo, a.tipgrupo) AS tipgrupo, COALESCE(b.desctipgrupo, a.desctipgrupo) AS desctipgrupo,
               COALESCE(b.actividad, a.actividad) AS actividad, COALESCE(b.descactividad, a.descactividad) AS descactividad,
               COALESCE(b.servicio, a.servicio) AS servicio, COALESCE(b.descservicio, a.descservicio) AS descservicio,
               b.cantidad AS cantidad_backup, a.cantidad AS cantidad_actual,
               a.usuariomod, a.fechamod, b.usuariomod AS usuariomod_backup, b.fechamod AS fechamod_backup,
               CASE WHEN b.ID IS NULL THEN 'NUEVA' WHEN a.ID IS NULL THEN 'BORRADA' ELSE 'CAMBIO' END AS cambio
        FROM (SELECT {sel('X')} FROM {name_server}.TOTALIZADO3_BACKUP X
              WHERE X.periodo_backup = {periodo} AND X.codcentro_ses = {int(codcentro)}
                AND X.periodo BETWEEN {desde} AND {periodo} AND ({filtro})) b
        FULL JOIN (SELECT {sel('X')} FROM {TMI_TOTALIZADO3} X
              WHERE X.codcentro_ses = {int(codcentro)} AND X.periodo BETWEEN {desde} AND {periodo} AND ({filtro})) a
          ON a.ID = b.ID
        WHERE b.ID IS NULL OR a.ID IS NULL OR ISNULL(a.cantidad, -2147483648) <> ISNULL(b.cantidad, -2147483648)
        ORDER BY periodo, tipgrupo, actividad, servicio, ID"""
    return _consulta(db, sql)
