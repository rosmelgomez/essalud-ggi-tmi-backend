"""Justificación del cálculo del TMI: como fue (copia del cierre) y con los datos actuales."""

from typing import Optional

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core import tmiFormula
from src.main.core.tmiConfig import TMI_DIM, TMI_TOTALIZADO3
from src.main.repositories.backupRep import queryHayBackupTMI
from src.main.repositories.calculoRep import _calcularEnParalelo, calcularVivoTMI, queryHayDatosTotalizadoTMI
from src.main.repositories.tmiBaseRep import name_server, _consulta


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
                      "orden": c.get("orden"),
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
                                                "orden": f["orden"] or 0, "BACKUP": None,
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


_COLS_TERMINO = ("origen_datos", "codigo", "tipgrupo", "actividad", "servicio", "mediana", "periodo_mediana",
                 "condicion", "texto", "valor_mes", "valor",
                 "filas_mes", "filas", "valor_mes_termino", "valor_termino")


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
    fila = db.execute(text(f"""SELECT tipo_calculo, formula, si_variable_nula, si_division_cero
                               FROM {name_server}.tmi_indicador WHERE id = :i"""), {"i": int(id_indicador)}).first()
    if not fila or not (fila[1] or "").strip():
        return []
    ind = fila[0]
    # términos de la fórmula del indicador, leídos de tmi_indicador.formula ([tipgrupo;actividad#servicio])
    try:
        f = tmiFormula.analizar(fila[1], fila[2] or "CERO", fila[3] or "NA")
    except tmiFormula.ErrorFormula as e:
        raise HTTPException(status_code=400, detail=f"La fórmula del indicador no se puede leer: {e}")
    defs = [t for t in tmiFormula.filas_termino(f) if codigo is None or t["codigo"] == codigo]
    if not defs:
        return []
    desde = periodo if (ind or "").upper() != "ACUMULADO" else anio * 100 + 1
    # filtro de los términos con valores enteros validados y la condición de hoja que valida tmiFormula ([A-Z0-9_])
    def parte(d):
        p = f"X.tipgrupo = {int(d['tipgrupo'])} AND X.actividad = {int(d['actividad'])}"
        if d["servicio"] is not None:
            p += f" AND X.servicio = {int(d['servicio'])}"
        if d["condicion"]:
            p += (f" AND X.tipohoja IN (SELECT h.tipohoja FROM {TMI_DIM}.DIM_HOJA h WHERE CAST(h.ANIOHOJA AS INT) = {anio}"
                  f" AND REPLACE(UPPER(LTRIM(RTRIM(h.CONDICION))), ' ', '_') = '{d['condicion']}')")
        return f"({p})"
    partes = [parte(d) for d in defs]
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
