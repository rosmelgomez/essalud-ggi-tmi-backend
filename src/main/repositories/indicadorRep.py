"""Indicadores del TMI dinámico: tmi_indicador, su fórmula (letras, variables y términos), ámbito y consulta
directa a TOTALIZADO3."""

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core import tmiFormula
from src.main.core.tmiConfig import TMI_DIM, TMI_TOTALIZADO3
from src.main.repositories import catalogoRep
from src.main.repositories.tmiBaseRep import (
    name_server,
    _acept_del_anio,
    _consulta,
    queryEliminarFila,
)


def queryIndicadoresTMI(db: Session):
    return _consulta(db, f"""
        SELECT i.id, i.grupo, i.indicador, i.codigo, i.nombre_hoja, i.titulo_hoja, i.orden, i.formula_alias, i.formula,
               i.tipo_calculo,
               i.sin_datos_anio, i.base_estandar, i.sentido,
               -- % Acept fijo del año actual (tmi_indicador_acept)
               ISNULL(a.tipo_acept, 'REL') AS tipo_acept, a.acept_fijo AS acept, a.aceptmenos_fijo AS aceptmenos, i.decimales,
               i.cero_es_logro, i.mostrar_no_aplica, i.activo, i.formato, i.si_variable_nula, i.si_division_cero,
               LTRIM(RTRIM(g.desctipgrupo)) AS grupo_descripcion
        FROM {name_server}.tmi_indicador i
        LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = i.grupo
        {_acept_del_anio("YEAR(GETDATE())")}
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
        db.execute(text(f"DELETE FROM {name_server}.tmi_indicador_acept WHERE id_indicador = :id"), {"id": id})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return queryEliminarFila(db, "tmi_indicador", id)


def queryLetrasIndicador(db: Session, id_indicador: int) -> dict:
    """Variable de cada letra del indicador ({"A": 1, "B": 2}), leída de formula_alias y formula_variable."""
    fila = db.execute(text(f"SELECT formula_alias, formula_variable FROM {name_server}.tmi_indicador WHERE id = :id"),
                      {"id": id_indicador}).first()
    if not fila or not (fila[0] or "").strip():
        return {}
    try:
        return tmiFormula.letras_de_formula(fila[0], fila[1])
    except tmiFormula.ErrorFormula as e:
        raise HTTPException(status_code=400, detail=str(e))


def queryIndicadorLetrasTMI(db: Session, id_indicador: int):
    letras = queryLetrasIndicador(db, id_indicador)
    if not letras:
        return []
    variables = {r["id_variable"]: r for r in _consulta(db, f"""
        SELECT v.id AS id_variable, v.nombre AS variable, v.agregacion, v.total_anual,
               (SELECT COUNT(*) FROM {name_server}.tmi_variable_logica l WHERE l.id_variable = v.id) AS filas_logica,
               STUFF((SELECT ' | ' + (
                    CAST(l.tipgrupo AS VARCHAR) + '·' + ISNULL(LTRIM(RTRIM(g.desctipgrupo)), '')
                    + ' / ' + CAST(l.actividad AS VARCHAR) + '·' + ISNULL(COALESCE(NULLIF(LTRIM(RTRIM(a.desclarga)), ''), LTRIM(RTRIM(a.descactividad))), '')
                    + ' (Serv: ' + ISNULL(CAST(l.servicio AS VARCHAR), 'Todos') + ')'
                    -- condición de hoja: solo las hojas de DIM_HOJA con esa condición ([g;a@CONDICION])
                    + ISNULL(' @' + REPLACE(UPPER(LTRIM(RTRIM(NULLIF(l.condicion_hoja, '')))), ' ', '_'), ''))
                FROM {name_server}.tmi_variable_logica l
                LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = l.tipgrupo
                LEFT JOIN {TMI_DIM}.DIM_ACTIVIDAD a ON a.actividad = l.actividad
                WHERE l.id_variable = v.id AND l.activo = 1
                ORDER BY l.tipgrupo, l.actividad, l.servicio
                FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 3, '') AS detalle_logica
        FROM {name_server}.tmi_variable v
        WHERE v.id IN ({", ".join(str(int(x)) for x in set(letras.values()))})""")}
    return [{"id_indicador": id_indicador, "letra": letra, **variables.get(id_var, {"id_variable": id_var})}
            for letra, id_var in sorted(letras.items())]


def _analizar(texto: str, regla: dict = None) -> tmiFormula.Formula:
    """regla: si_variable_nula / si_division_cero del indicador (sin regla = CERO / NA, el comportamiento anterior)."""
    regla = regla or {}
    try:
        return tmiFormula.analizar(texto, regla.get("si_variable_nula") or "CERO", regla.get("si_division_cero") or "NA")
    except tmiFormula.ErrorFormula as e:
        raise HTTPException(status_code=400, detail=str(e))


def _regla_nulos(db: Session, id_indicador: int) -> dict:
    fila = db.execute(text(f"""SELECT si_variable_nula, si_division_cero FROM {name_server}.tmi_indicador
                               WHERE id = :id"""), {"id": id_indicador}).mappings().first()
    if not fila:
        raise HTTPException(status_code=404, detail="Indicador no encontrado")
    return dict(fila)


def queryFormulaSqlTMI(db: Session, id_indicador: int):
    """Expresión SQL de la fórmula guardada con la regla de nulos actual del indicador (solo se muestra: el cálculo
    la arma de nuevo cada vez desde la fórmula)."""
    fila = db.execute(text(f"""SELECT formula, si_variable_nula, si_division_cero FROM {name_server}.tmi_indicador
                               WHERE id = :id"""), {"id": id_indicador}).mappings().first()
    if not fila or not fila["formula"]:
        return None
    return _analizar(fila["formula"], dict(fila)).sql


def _analizarTokens(db: Session, texto: str, regla: dict = None):
    """Términos de la fórmula interna (T1, T2...) con la descripción del grupo, la actividad y los servicios (DIM)."""
    f = _analizar(texto, regla)
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
    if servicios and catalogoRep._CON_DIM_SERVICIO is not False:
        try:
            desc_s = {r["servicio"]: r["d"] for r in db.execute(text(f"""
                SELECT servicio, LTRIM(RTRIM(desclarga)) AS d FROM {TMI_DIM}.DIM_SERVICIO
                WHERE servicio IN ({", ".join(map(str, servicios))})""")).mappings()}
        except Exception:
            db.rollback()
    terminos = []
    for t in f.terminos:
        problemas = [x for x, ok in (("el grupo no existe en los datos", t.tipgrupo in desc_g),
                                     ("la actividad no existe en los datos", t.actividad in desc_a)) if not ok]
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
        SELECT id, nombre, agregacion, total_anual FROM {name_server}.tmi_variable
        WHERE id IN ({", ".join(str(int(v)) for v in variables.values()) or "NULL"})""")}
    mapa, detalle = {}, []
    for letra, id_var in sorted(variables.items()):
        v = filas.get(id_var)
        if not v:
            raise HTTPException(status_code=400, detail=f"La variable de la letra {letra} no existe.")
        conjuntos = db.execute(text(tmiFormula.SQL_CONJUNTOS.format(esq=name_server, p=":id")), {"id": id_var}).all()
        try:
            expr, aviso = tmiFormula.expresion_variable(v["nombre"], v["agregacion"], conjuntos, v["total_anual"])
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


def queryAnalizarFormulaTMI(db: Session, formula_alias: str, variables: dict, regla: dict = None):
    """Fórmula con letras ((A - B) / C): fórmula interna, variables de cada letra y términos de TOTALIZADO3."""
    formula, detalle = _expandir(db, formula_alias, variables)
    analisis = _analizarTokens(db, formula, regla)
    return {"formula_alias": formula_alias.strip(), "variables": detalle, **analisis}


def queryGuardarFormulaTMI(db: Session, id_indicador: int, formula_alias: str, variables: dict, usuario: str = None):
    """Guarda la fórmula con letras, la misma con el id de la variable de cada letra (formula_variable: {1} / {2}) y
    la fórmula interna
    generada ([3;50#0] - [3;49#0]) / [3;47#0], en una transacción. Los términos no se guardan: el cálculo los lee de
    la fórmula."""
    regla = _regla_nulos(db, id_indicador)
    analisis = queryAnalizarFormulaTMI(db, formula_alias, variables, regla)
    malos = [f"{t['texto']}: {t['problema']}" for t in analisis["terminos"] if t["problema"]]
    if malos:
        raise HTTPException(status_code=400, detail="; ".join(malos))
    f = _analizar(analisis["formula"], regla)
    usadas = [v for v in analisis["variables"] if v["usada"]]
    try:
        formula_variable = tmiFormula.formula_con_ids(analisis["formula_alias"], {v["letra"]: v["id_variable"] for v in usadas})
    except tmiFormula.ErrorFormula as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        r = db.execute(text(f"""
            UPDATE {name_server}.tmi_indicador
               SET formula_alias = :alias, formula_variable = :fv, formula = :formula,
                   usuario_modificacion = :usuario, fecha_modificacion = GETDATE()
             WHERE id = :id"""), {"alias": analisis["formula_alias"], "fv": formula_variable, "formula": f.texto,
                                   "usuario": usuario, "id": id_indicador})
        if r.rowcount == 0:
            raise HTTPException(status_code=404, detail="Indicador no encontrado")
        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    analisis["variables"] = usadas
    return analisis


def _consulta_indicador(db: Session, id_indicador: int, periodo: int, con_estandares: bool = False) -> str:
    """con_estandares: agrega el estándar del mes de corte (también el específico del centro) y las exclusiones."""
    if periodo % 100 not in range(1, 13):
        raise HTTPException(status_code=400, detail="El periodo debe tener formato AAAAMM.")
    fila = db.execute(text(f"""SELECT id, codigo, indicador, formula, tipo_calculo, base_estandar, sentido,
                                      si_variable_nula, si_division_cero
                               FROM {name_server}.tmi_indicador
                               WHERE id = :id"""), {"id": id_indicador}).mappings().first()
    if not fila:
        raise HTTPException(status_code=404, detail="Indicador no encontrado")
    if not fila["formula"]:
        raise HTTPException(status_code=400, detail="El indicador no tiene fórmula.")
    try:
        return tmiFormula.consulta_sql(_analizar(fila["formula"], dict(fila)), TMI_TOTALIZADO3,
                                       fila["tipo_calculo"] or "MENSUAL", periodo, f"{fila['codigo']} - {fila['indicador']}",
                                       centros=f"{name_server}.vw_tmi_centro_base",
                                       dim=TMI_DIM,
                                       indicador=dict(fila) if con_estandares else None,
                                       esquema=name_server)
    except tmiFormula.ErrorFormula as e:
        raise HTTPException(status_code=400, detail=str(e))


def queryConsultaIndicadorTMI(db: Session, id_indicador: int, periodo: int, con_estandares: bool = False):
    """Texto del query que calcula el indicador directo de TOTALIZADO3 (para verlo o copiarlo)."""
    return {"sql": _consulta_indicador(db, id_indicador, periodo, con_estandares)}
