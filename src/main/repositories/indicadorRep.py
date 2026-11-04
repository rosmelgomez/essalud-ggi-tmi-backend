"""Indicadores del TMI dinámico: tmi_indicador, su fórmula (letras, variables y términos), ámbito y consulta
directa a TOTALIZADO3."""

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core import tmiFormula
from src.main.core.tmiConfig import TMI_DIM, TMI_TOTALIZADO3
from src.main.repositories import tmiDinamicoRep
from src.main.repositories.tmiBaseRep import (
    name_server,
    _consulta,
    queryEliminarFila,
)


def queryIndicadoresTMI(db: Session):
    return _consulta(db, f"""
        SELECT i.id, i.grupo, i.indicador, i.codigo, i.nombre_hoja, i.titulo_hoja, i.orden, i.formula_alias, i.formula,
               i.tipo_calculo,
               i.sin_datos_anio, i.base_estandar, i.sentido, i.tipo_tolerancia, i.tolerancia, i.tolerancia_menos, i.decimales,
               i.cero_es_logro, i.mostrar_no_aplica, i.activo, i.formato, LTRIM(RTRIM(g.desctipgrupo)) AS grupo_descripcion
        FROM {name_server}.tmi_indicador i
        LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = i.grupo
        ORDER BY i.orden, i.id""")


def queryIndicadoresActivosTMI(db: Session):
    try:
        result = db.execute(text(f"""
            SELECT i.id, i.codigo, i.indicador, i.nombre_hoja, i.titulo_hoja, i.orden, i.sentido, i.formato, i.tipo_calculo,
                   LTRIM(RTRIM(g.desctipgrupo)) AS grupo, MIN(i.orden) OVER (PARTITION BY i.grupo) AS orden_grupo
            FROM {name_server}.tmi_indicador i
            LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = i.grupo
            WHERE i.activo = 1
            ORDER BY i.orden, i.id
        """))
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryEliminarIndicador(db: Session, id: int):
    try:
        for tabla in ("tmi_indicador_tolerancia", "tmi_indicador_termino", "tmi_indicador_variable", "tmi_indicador_ambito", "tmi_indicador_estandar", "tmi_resultado"):
            db.execute(text(f"IF OBJECT_ID('{name_server}.{tabla}') IS NOT NULL DELETE FROM {name_server}.{tabla} WHERE id_indicador = :id"), {"id": id})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return queryEliminarFila(db, "tmi_indicador", id)


def queryIndicadorLetrasTMI(db: Session, id_indicador: int):
    return _consulta(db, f"""
        SELECT iv.id, iv.id_indicador, iv.letra, iv.id_variable, v.nombre AS variable, v.agregacion, v.total_anual,
               (SELECT COUNT(*) FROM {name_server}.tmi_variable_logica l WHERE l.id_variable = v.id) AS filas_logica,
               STUFF((SELECT ' | ' + (
                    CAST(l.tipgrupo AS VARCHAR) + '·' + ISNULL(LTRIM(RTRIM(g.desctipgrupo)), '')
                    + ' / ' + CAST(l.actividad AS VARCHAR) + '·' + ISNULL(COALESCE(NULLIF(LTRIM(RTRIM(a.desclarga)), ''), LTRIM(RTRIM(a.descactividad))), '')
                    + ' (Serv: ' + ISNULL(CAST(l.servicio AS VARCHAR), 'Todos') + ')')
                FROM {name_server}.tmi_variable_logica l
                LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = l.tipgrupo
                LEFT JOIN {TMI_DIM}.DIM_ACTIVIDAD a ON a.actividad = l.actividad
                WHERE l.id_variable = v.id AND l.activo = 1
                ORDER BY l.tipgrupo, l.actividad, l.servicio
                FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 3, '') AS detalle_logica
        FROM {name_server}.tmi_indicador_variable iv
        JOIN {name_server}.tmi_variable v ON v.id = iv.id_variable
        WHERE iv.id_indicador = :id ORDER BY iv.letra, v.nombre""", {"id": id_indicador})


def queryIndicadorAmbitoTMI(db: Session, id_indicador: int):
    return _consulta(db, f"""
        SELECT id, id_indicador, red, nivel, categoria, tipo, codcentro, incluir, periodo_desde, periodo_hasta
        FROM {name_server}.tmi_indicador_ambito WHERE id_indicador = :id
        ORDER BY incluir DESC, red, nivel, categoria, tipo, codcentro""", {"id": id_indicador})


def _analizar(texto: str) -> tmiFormula.Formula:
    try:
        return tmiFormula.analizar(texto)
    except tmiFormula.ErrorFormula as e:
        raise HTTPException(status_code=400, detail=str(e))


def _analizarTokens(db: Session, texto: str):
    """Términos de la fórmula interna (T1, T2...) con la descripción del grupo, la actividad y los servicios (DIM)."""
    f = _analizar(texto)
    grupos = {t.tipgrupo for t in f.terminos}
    actividades = {t.actividad for t in f.terminos}
    servicios = {s for t in f.terminos for s in t.servicios}
    desc_g = {r["tipgrupo"]: r["d"] for r in _consulta(db, f"""
        SELECT tipgrupo, LTRIM(RTRIM(desctipgrupo)) AS d FROM {TMI_DIM}.DIM_GRUPO
        WHERE tipgrupo IN ({", ".join(map(str, grupos))})""")}
    desc_a = {r["actividad"]: r["d"] for r in _consulta(db, f"""
        SELECT actividad, COALESCE(NULLIF(LTRIM(RTRIM(desclarga)), ''), LTRIM(RTRIM(descactividad))) AS d
        FROM {TMI_DIM}.DIM_ACTIVIDAD WHERE actividad IN ({", ".join(map(str, actividades))})""")}
    desc_s = {}
    if servicios and tmiDinamicoRep._CON_DIM_SERVICIO is not False:
        try:
            desc_s = {r["servicio"]: r["d"] for r in db.execute(text(f"""
                SELECT servicio, LTRIM(RTRIM(desclarga)) AS d FROM {TMI_DIM}.DIM_SERVICIO
                WHERE servicio IN ({", ".join(map(str, servicios))})""")).mappings()}
        except Exception:
            db.rollback()
    terminos = []
    for t in f.terminos:
        problemas = [x for x, ok in (("grupo no existe en DIM_GRUPO", t.tipgrupo in desc_g),
                                     ("actividad no existe en DIM_ACTIVIDAD", t.actividad in desc_a)) if not ok]
        terminos.append({
            "codigo": f.codigo(t), "texto": t.texto, "tipgrupo": t.tipgrupo, "grupo": desc_g.get(t.tipgrupo),
            "actividad": t.actividad, "descactividad": desc_a.get(t.actividad),
            "servicios": [{"servicio": s, "descservicio": desc_s.get(s)} for s in t.servicios],
            "mediana": t.mediana, "problema": "; ".join(problemas) or None})
    return {"formula": f.texto, "formula_sql": f.sql, "terminos": terminos}


def _expandir(db: Session, formula_alias: str, variables: dict):
    """Fórmula con letras -> fórmula interna con términos de TOTALIZADO3, y el detalle de la variable de cada letra."""
    usadas = set(tmiFormula.letras_usadas(formula_alias))
    filas = {r["id"]: r for r in _consulta(db, f"""
        SELECT id, nombre, agregacion FROM {name_server}.tmi_variable
        WHERE id IN ({", ".join(str(int(v)) for v in variables.values()) or "NULL"})""")}
    mapa, detalle = {}, []
    for letra, id_var in sorted(variables.items()):
        v = filas.get(id_var)
        if not v:
            raise HTTPException(status_code=400, detail=f"La variable de la letra {letra} no existe.")
        conjuntos = db.execute(text(tmiFormula.SQL_CONJUNTOS.format(esq=name_server, p=":id")), {"id": id_var}).all()
        try:
            expr, aviso = tmiFormula.expresion_variable(v["nombre"], v["agregacion"], conjuntos)
        except tmiFormula.ErrorFormula as e:
            if letra in usadas:
                raise HTTPException(status_code=400, detail=f"{letra}: {e}")
            expr, aviso = None, str(e)
        if expr:
            mapa[letra] = expr
        detalle.append({"letra": letra, "id_variable": id_var, "nombre": v["nombre"], "agregacion": v["agregacion"],
                        "expresion": expr, "aviso": aviso, "usada": letra in usadas})
    try:
        formula = tmiFormula.expandir_alias(formula_alias, mapa)
    except tmiFormula.ErrorFormula as e:
        raise HTTPException(status_code=400, detail=str(e))
    return formula, detalle


def queryAnalizarFormulaTMI(db: Session, formula_alias: str, variables: dict):
    """Fórmula con letras ((A - B) / C): fórmula interna, variables de cada letra y términos de TOTALIZADO3."""
    formula, detalle = _expandir(db, formula_alias, variables)
    analisis = _analizarTokens(db, formula)
    return {"formula_alias": formula_alias.strip(), "variables": detalle, **analisis}


def queryGuardarFormulaTMI(db: Session, id_indicador: int, formula_alias: str, variables: dict, usuario: str = None):
    """Guarda la fórmula con letras, la variable de cada letra usada (tmi_indicador_variable) y la fórmula interna
    generada ([3;50#0] - [3;49#0]) / [3;47#0] con sus términos (tmi_indicador_termino) y formula_sql, en una transacción."""
    analisis = queryAnalizarFormulaTMI(db, formula_alias, variables)
    malos = [f"{t['texto']}: {t['problema']}" for t in analisis["terminos"] if t["problema"]]
    if malos:
        raise HTTPException(status_code=400, detail="; ".join(malos))
    f = _analizar(analisis["formula"])
    usadas = [v for v in analisis["variables"] if v["usada"]]
    try:
        r = db.execute(text(f"""
            UPDATE {name_server}.tmi_indicador
               SET formula_alias = :alias, formula = :formula, formula_sql = :sql,
                   usuario_modificacion = :usuario, fecha_modificacion = GETDATE()
             WHERE id = :id"""), {"alias": analisis["formula_alias"], "formula": f.texto, "sql": f.sql,
                                   "usuario": usuario, "id": id_indicador})
        if r.rowcount == 0:
            raise HTTPException(status_code=404, detail="Indicador no encontrado")
        db.execute(text(f"DELETE FROM {name_server}.tmi_indicador_termino WHERE id_indicador = :id"), {"id": id_indicador})
        for t in tmiFormula.filas_termino(f):
            db.execute(text(f"""INSERT INTO {name_server}.tmi_indicador_termino
                                    (id_indicador, codigo, tipgrupo, actividad, servicio, mediana, texto)
                                VALUES (:id, :codigo, :tipgrupo, :actividad, :servicio, :mediana, :texto)"""),
                       {"id": id_indicador, **t})
        db.execute(text(f"DELETE FROM {name_server}.tmi_indicador_variable WHERE id_indicador = :id"), {"id": id_indicador})
        for v in usadas:
            db.execute(text(f"""INSERT INTO {name_server}.tmi_indicador_variable (id_indicador, letra, id_variable)
                                VALUES (:id, :letra, :v)"""), {"id": id_indicador, "letra": v["letra"], "v": v["id_variable"]})
        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    analisis["variables"] = usadas
    return analisis


def _consulta_indicador(db: Session, id_indicador: int, periodo: int) -> str:
    if periodo % 100 not in range(1, 13):
        raise HTTPException(status_code=400, detail="El periodo debe tener formato AAAAMM.")
    fila = db.execute(text(f"""SELECT codigo, indicador, formula, tipo_calculo FROM {name_server}.tmi_indicador
                               WHERE id = :id"""), {"id": id_indicador}).mappings().first()
    if not fila:
        raise HTTPException(status_code=404, detail="Indicador no encontrado")
    if not fila["formula"]:
        raise HTTPException(status_code=400, detail="El indicador no tiene fórmula.")
    return tmiFormula.consulta_sql(_analizar(fila["formula"]), TMI_TOTALIZADO3, fila["tipo_calculo"] or "MENSUAL",
                                   periodo, f"{fila['codigo']} - {fila['indicador']}",
                                   centros=f"{name_server}.vw_tmi_centro_base")


def queryConsultaIndicadorTMI(db: Session, id_indicador: int, periodo: int):
    """Texto del query que calcula el indicador directo de TOTALIZADO3 (para verlo o copiarlo)."""
    return {"sql": _consulta_indicador(db, id_indicador, periodo)}


def queryResultadoDirectoTMI(db: Session, id_indicador: int, periodo: int):
    """Ejecuta ese query: valor de la fórmula por centro y mes, sin estándares ni exclusiones."""
    sql = _consulta_indicador(db, id_indicador, periodo)
    try:
        filas = [dict(r) for r in db.execute(text(sql)).mappings()]
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return {"sql": sql, "filas": filas}
