"""TMI dinámico: catálogos (DIM y tablas de apoyo), validación, cálculo y resultados
(procedimientos y tablas de src/resources/sql/tmi)."""

import logging
from typing import Optional, Tuple

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core.tmiConfig import TMI_DIM, TMI_TOTALIZADO3
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


def _fuente_final(origen: Optional[str]) -> Tuple[str, str, dict]:
    """Tabla del resultado final y filtro: el del origen pedido (ACTUAL = TOTALIZADO3, BACKUP = copia del cierre) o,
    sin origen, el oficial (BACKUP si existe, si no ACTUAL)."""
    if origen is None:
        return f"{name_server}.vw_tmi_resultado_indicador", "", {}
    return f"{name_server}.tmi_resultado_indicador", "AND origen_datos = :origen", {"origen": _origen(origen)}


def queryResultadoIndicadorTMI(db: Session, periodo: int, id_indicador: int, origen: Optional[str] = None):
    """Resultado final del indicador guardado en el periodo (tmi_resultado_indicador), como la hoja del Excel."""
    tabla, filtro, params = _fuente_final(origen)
    return _consulta(db, f"""
        SELECT {_COLS_RESULTADO}, origen_datos
        FROM {tabla}
        WHERE periodo = :periodo AND id_indicador = :id {filtro}
        ORDER BY orden_red, orden, codcentro""", {"periodo": periodo, "id": id_indicador, **params})


def queryResultadoFinalTMI(db: Session, periodo: int, origen: Optional[str] = None):
    """Resultado final de todos los indicadores del periodo (para armar el Excel sin recalcular)."""
    tabla, filtro, params = _fuente_final(origen)
    return _consulta(db, f"""
        SELECT {_COLS_RESULTADO}, origen_datos
        FROM {tabla}
        WHERE periodo = :periodo {filtro}
        ORDER BY orden_red, orden, codcentro""", {"periodo": periodo, **params})


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


def queryPeriodosResultadoTMI(db: Session):
    """Periodos que tienen resultado final guardado, del más reciente al más antiguo. Los datos son los del oficial
    (origen_datos: BACKUP si existe, si no ACTUAL); origenes: cada resultado guardado con su fecha y conteos."""
    filas = _consulta(db, f"""
        SELECT periodo, origen_datos, COUNT(DISTINCT id_indicador) AS indicadores, COUNT(DISTINCT codcentro) AS centros,
               MAX(fecha_calculo) AS fecha_calculo
        FROM {name_server}.tmi_resultado_indicador
        GROUP BY periodo, origen_datos""")
    periodos: dict = {}
    for f in filas:
        periodos.setdefault(f["periodo"], {})[f["origen_datos"]] = f
    salida = []
    for periodo in sorted(periodos, reverse=True):
        o = periodos[periodo]
        oficial = o.get("BACKUP") or o.get("ACTUAL") or next(iter(o.values()))
        salida.append({"periodo": periodo, "indicadores": oficial["indicadores"], "centros": oficial["centros"],
                       "fecha_calculo": oficial["fecha_calculo"], "origen_datos": oficial["origen_datos"],
                       "origenes": {k: {"fecha_calculo": v["fecha_calculo"], "indicadores": v["indicadores"],
                                        "centros": v["centros"]} for k, v in o.items()}})
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


def queryCalcularTMI(db: Session, periodo: int, origen: str = "ACTUAL", usuario: Optional[str] = None):
    """Calcula los indicadores del periodo (AAAAMM) en tmi_resultado: la fórmula de cada indicador sobre TOTALIZADO3
    de hoy (ACTUAL) o sobre la copia del cierre del periodo (BACKUP, TOTALIZADO3_BACKUP). Sin datos del periodo no se
    calcula (400) y el resultado guardado no se toca. Los dos cálculos se guardan aparte; el oficial (Excel y
    dashboard) es el BACKUP si existe."""
    origen = _origen(origen)
    anio, mes = divmod(int(periodo), 100)
    if origen == "BACKUP" and not queryHayBackupTMI(db, periodo):
        raise HTTPException(status_code=400,
                            detail=f"No se puede calcular {periodo} con los datos del cierre: los datos de "
                                   f"{_MESES[mes - 1]} {anio} se guardan cuando se cierra el periodo.")
    if origen == "ACTUAL" and not queryHayDatosTotalizadoTMI(db, periodo):
        raise HTTPException(status_code=400,
                            detail=f"No se puede calcular {periodo}: todavía no llegan los datos de "
                                   f"{_MESES[mes - 1]} {anio}.")
    try:
        db.execute(text(f"EXEC {name_server}.usp_tmi_calcular @PERIODO = :periodo, @ORIGEN = :origen, @USUARIO = :u"),
                   {"periodo": periodo, "origen": origen, "u": usuario})
        db.commit()
        result = db.execute(text(f"""
            SELECT puntaje, COUNT(*) AS cantidad
            FROM {name_server}.tmi_resultado
            WHERE periodo_corte = :periodo AND origen_datos = :origen
            GROUP BY puntaje
        """), {"periodo": periodo, "origen": origen})
        return {row["puntaje"]: row["cantidad"] for row in result.mappings()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def queryResultadoTMI(db: Session, periodo: int, origen: Optional[str] = None):
    """Valor y puntaje de cada mes por indicador y centro, una fila por mes hasta el corte. Cada mes sale de la fila
    que se guardó al calcular ese mes como periodo de corte (tmi_resultado guarda una fila por periodo). Solo se
    listan los centros e indicadores del periodo pedido; un mes que no se calculó queda sin valor y sin puntaje (NA)."""
    try:
        anio, mes = divmod(periodo, 100)
        result = db.execute(text(f"""
            SELECT h.id_indicador, h.codcentro, h.periodo_corte % 100 AS mes, h.valor, h.puntaje
            FROM {name_server}.fn_tmi_resultado(:origen) h
            JOIN {name_server}.fn_tmi_resultado(:origen) r ON r.periodo_corte = :periodo
                 AND r.id_indicador = h.id_indicador AND r.codcentro = h.codcentro
            WHERE h.periodo_corte BETWEEN :desde AND :periodo
        """), {"periodo": periodo, "desde": anio * 100 + 1, "origen": None if origen is None else _origen(origen)})
        filas = [dict(r) for r in result.mappings()]
        return filas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- justificación del cálculo: como fue (copia del cierre) y con los datos actuales ----------
_COLS_JUST = """origen_datos, periodo_backup, valor, estandar, acept, aceptmenos, puntaje, motivo_na, tipo_calculo,
                formula_alias, formula, formula_desarrollo, usuario_calculo, fecha_calculo"""


def queryJustificacionTMI(db: Session, periodo: int, id_indicador: int):
    """Resultado del indicador en el periodo por centro, con cada cálculo guardado (BACKUP: como fue al cierre;
    ACTUAL: con los datos de hoy), su fórmula y su desarrollo. cambio = el valor o el puntaje no coinciden."""
    filas = _consulta(db, f"""
        SELECT r.codcentro, ri.centro, ri.red, ri.orden_red, ri.orden, {', '.join('r.' + c.strip() for c in _COLS_JUST.split(','))}
        FROM {name_server}.tmi_resultado r
        LEFT JOIN {name_server}.tmi_resultado_indicador ri ON ri.periodo = r.periodo_corte AND ri.origen_datos = r.origen_datos
             AND ri.id_indicador = r.id_indicador AND ri.codcentro = r.codcentro
        WHERE r.periodo_corte = :p AND r.id_indicador = :i""", {"p": int(periodo), "i": int(id_indicador)})
    centros: dict = {}
    for f in filas:
        c = centros.setdefault(f["codcentro"], {"codcentro": f["codcentro"], "centro": f["centro"], "red": f["red"],
                                                "orden": (f["orden_red"] or 0, f["orden"] or 0), "BACKUP": None,
                                                "ACTUAL": None})
        c[f["origen_datos"]] = {k: f[k] for k in (x.strip() for x in _COLS_JUST.split(","))}
    salida = []
    for c in sorted(centros.values(), key=lambda x: (x["orden"], x["codcentro"])):
        b, a = c["BACKUP"], c["ACTUAL"]
        c["cambio"] = bool(b and a and (b["puntaje"] != a["puntaje"] or
                                        round(b["valor"] or 0, 6) != round(a["valor"] or 0, 6) or
                                        (b["valor"] is None) != (a["valor"] is None)))
        del c["orden"]
        salida.append(c)
    return {"periodo": int(periodo), "id_indicador": int(id_indicador),
            "con_backup": queryHayBackupTMI(db, periodo),
            "origenes": sorted({f["origen_datos"] for f in filas}), "centros": salida}


def queryTerminosResultadoTMI(db: Session, periodo: int, id_indicador: int, codcentro: int):
    """Valor de cada término de la fórmula (grupo, actividad y servicio) en cada cálculo guardado del periodo."""
    return _consulta(db, f"""
        SELECT origen_datos, codigo, tipgrupo, actividad, servicio, mediana, texto, valor_mes, valor, filas_mes, filas
        FROM {name_server}.tmi_resultado_termino
        WHERE periodo_corte = :p AND id_indicador = :i AND codcentro = :c
        ORDER BY LEN(codigo), codigo, tipgrupo, actividad, servicio, origen_datos""",
                     {"p": int(periodo), "i": int(id_indicador), "c": int(codcentro)})


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
