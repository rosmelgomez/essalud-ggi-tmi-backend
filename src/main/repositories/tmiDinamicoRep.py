"""Consultas del TMI dinámico (procedimientos y tablas de src/resources/sql/tmi)."""

import logging
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core.tmiConfig import TMI_DB, TMI_DIM, TMI_TOTALIZADO3

logger = logging.getLogger(__name__)

name_server = f"{TMI_DB}.dbo"


### Mantenimiento (frontend). Tablas y columnas fijas: nunca vienen del usuario.
TABLAS = {
    "tmi_variable": ["nombre", "descripcion", "total_anual", "activo"],
    "tmi_variable_logica": ["id_variable", "tipgrupo", "actividad", "servicio", "condicion_hoja", "agregacion",
                            "periodo_desde", "periodo_hasta", "activo"],
    "tmi_indicador": ["grupo", "indicador", "codigo", "nombre_hoja", "titulo_hoja", "orden", "expr_numerador",
                      "expr_denominador", "tipo_calculo", "factor", "den_cero", "num_cero_na", "cero_si_letra_mes_0",
                      "sin_datos_anio", "base_estandar", "sentido", "tipo_tolerancia", "tolerancia", "tolerancia_menos", "decimales",
                      "cero_es_logro", "mostrar_no_aplica", "activo", "formato"],
    "tmi_indicador_variable": ["id_indicador", "letra", "id_variable"],
    "tmi_indicador_ambito": ["id_indicador", "red", "nivel", "categoria", "tipo", "codcentro", "incluir",
                             "periodo_desde", "periodo_hasta"],
    "tmi_indicador_estandar": ["id_indicador", "nivel", "categoria", "tipo", "periodo_desde", "periodo_hasta",
                               "estandar", "acept", "aceptmenos", "activo"],
    "tmi_tipo_estandar": ["codigo", "descripcion", "orden", "activo"],
    "tmi_estandar": ["tipo_estandar", "orden", "fuente", "clave", "descripcion", "prioridad", "activo"],
    "tmi_centro_estandar": ["codcentro", "id_indicador", "anio", "aplica", "est_01", "est_02", "est_03", "est_04",
                            "est_05", "est_06", "est_07", "est_08", "est_09", "est_10", "est_11", "est_12",
                            "acept", "sustento"],
}
# Tablas con columnas de auditoría (usuario y fecha)
CON_AUDITORIA = {"tmi_variable", "tmi_indicador"}
# Tablas anteriores a centros_tmi.sql nombran id_estandar a la columna del indicador
_COLUMNA_INDICADOR: dict = {}


def _columna_indicador(db: Session, tabla: str) -> str:
    """id_indicador (DDL actual) o id_estandar (tablas antiguas), según exista en la tabla."""
    if tabla not in _COLUMNA_INDICADOR:
        existe = db.execute(text("SELECT COL_LENGTH(:t, 'id_indicador')"), {"t": f"{name_server}.{tabla}"}).scalar()
        _COLUMNA_INDICADOR[tabla] = "id_indicador" if existe is not None else "id_estandar"
    return _COLUMNA_INDICADOR[tabla]


def _columna(db: Session, tabla: str, columna: str) -> str:
    if columna == "id_indicador" and tabla == "tmi_centro_estandar":
        return _columna_indicador(db, tabla)
    return columna


def _consulta(db: Session, query: str, params: dict = None):
    try:
        result = db.execute(text(query), params or {})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryInsertarFila(db: Session, tabla: str, datos: dict, usuario: str = None):
    columnas = [c for c in TABLAS[tabla] if c in datos]
    params = {c: datos[c] for c in columnas}
    extra_cols, extra_vals = "", ""
    if tabla in CON_AUDITORIA:
        extra_cols, extra_vals = ", usuario_creacion, fecha_creacion", ", :usuario, GETDATE()"
        params["usuario"] = usuario
    try:
        result = db.execute(text(f"""
            INSERT INTO {name_server}.{tabla} ({', '.join(_columna(db, tabla, c) for c in columnas)}{extra_cols})
            OUTPUT INSERTED.id
            VALUES ({', '.join(':' + c for c in columnas)}{extra_vals})
        """), params)
        nuevo_id = result.scalar()
        db.commit()
        return {"message": "Registro creado", "id": nuevo_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def queryActualizarFila(db: Session, tabla: str, id: int, datos: dict, usuario: str = None):
    columnas = [c for c in TABLAS[tabla] if c in datos]
    params = {c: datos[c] for c in columnas}
    params["id"] = id
    sets = ", ".join(f"{_columna(db, tabla, c)} = :{c}" for c in columnas)
    if tabla in CON_AUDITORIA:
        sets += ", usuario_modificacion = :usuario, fecha_modificacion = GETDATE()"
        params["usuario"] = usuario
    try:
        result = db.execute(text(f"UPDATE {name_server}.{tabla} SET {sets} WHERE id = :id"), params)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"message": "Registro actualizado", "rows_updated": result.rowcount}


def queryEliminarFila(db: Session, tabla: str, id: int):
    try:
        result = db.execute(text(f"DELETE FROM {name_server}.{tabla} WHERE id = :id"), {"id": id})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"message": "Registro eliminado", "rows_deleted": result.rowcount}


def queryEliminarVariable(db: Session, id: int):
    usada = _consulta(db, f"""
        SELECT DISTINCT i.codigo FROM {name_server}.tmi_indicador_variable iv
        JOIN {name_server}.tmi_indicador i ON i.id = iv.id_indicador WHERE iv.id_variable = :id""", {"id": id})
    if usada:
        raise HTTPException(status_code=400, detail="La variable se usa en los indicadores: "
                            + ", ".join(sorted(u["codigo"] or "" for u in usada)))
    try:
        db.execute(text(f"DELETE FROM {name_server}.tmi_variable_logica WHERE id_variable = :id"), {"id": id})
        db.execute(text(f"DELETE FROM {name_server}.tmi_variable_pivot WHERE id_variable = :id"), {"id": id})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return queryEliminarFila(db, "tmi_variable", id)


def queryEliminarIndicador(db: Session, id: int):
    try:
        for tabla in ("tmi_indicador_variable", "tmi_indicador_ambito", "tmi_indicador_estandar", "tmi_resultado"):
            db.execute(text(f"DELETE FROM {name_server}.{tabla} WHERE id_indicador = :id"), {"id": id})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return queryEliminarFila(db, "tmi_indicador", id)


def queryVariablesTMI(db: Session):
    return _consulta(db, f"""
        SELECT v.id, v.nombre, v.descripcion, v.total_anual, v.activo,
               (SELECT COUNT(*) FROM {name_server}.tmi_variable_logica l WHERE l.id_variable = v.id) AS filas_logica,
               STUFF((SELECT ', ' + x.codigo FROM (SELECT DISTINCT i.codigo FROM {name_server}.tmi_indicador_variable iv
                    JOIN {name_server}.tmi_indicador i ON i.id = iv.id_indicador
                    WHERE iv.id_variable = v.id AND i.codigo IS NOT NULL) x
                    ORDER BY x.codigo FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, '') AS indicadores
        FROM {name_server}.tmi_variable v
        ORDER BY v.nombre""")


def queryVariableLogicaTMI(db: Session, id_variable: int):
    return _consulta(db, f"""
        SELECT l.id, l.id_variable, l.tipgrupo, l.actividad, l.servicio, l.condicion_hoja, l.agregacion,
               l.periodo_desde, l.periodo_hasta, l.activo, g.desctipgrupo,
               a.descactividad AS descactividad_corta, a.desclarga, a.Recurso, a.Proceso,
               COALESCE(NULLIF(LTRIM(RTRIM(a.desclarga)), ''), a.descactividad) AS descactividad
        FROM {name_server}.tmi_variable_logica l
        LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = l.tipgrupo
        LEFT JOIN {TMI_DIM}.DIM_ACTIVIDAD a ON a.actividad = l.actividad
        WHERE l.id_variable = :id
        ORDER BY l.tipgrupo, l.actividad, l.servicio""", {"id": id_variable})


def queryIndicadoresTMI(db: Session):
    return _consulta(db, f"""
        SELECT i.id, i.grupo, i.indicador, i.codigo, i.nombre_hoja, i.titulo_hoja, i.orden, i.expr_numerador,
               i.expr_denominador, i.tipo_calculo, i.factor, i.den_cero, i.num_cero_na, i.cero_si_letra_mes_0,
               i.sin_datos_anio, i.base_estandar, i.sentido, i.tipo_tolerancia, i.tolerancia, i.tolerancia_menos, i.decimales,
               i.cero_es_logro, i.mostrar_no_aplica, i.activo, i.formato, g.descripcion AS grupo_descripcion,
               STUFF((SELECT ' | ' + x.txt FROM (
                    SELECT iv.letra,
                           iv.letra + ' = ' + ISNULL(STUFF((
                               SELECT ' + ' + v.nombre
                               FROM {name_server}.tmi_indicador_variable iv2
                               JOIN {name_server}.tmi_variable v ON v.id = iv2.id_variable
                               WHERE iv2.id_indicador = i.id AND iv2.letra = iv.letra
                               ORDER BY v.nombre
                               FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 3, ''), '') AS txt
                    FROM {name_server}.tmi_indicador_variable iv
                    WHERE iv.id_indicador = i.id GROUP BY iv.letra) x
                    ORDER BY x.letra FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 3, '') AS letras
        FROM {name_server}.tmi_indicador i
        LEFT JOIN {name_server}.tmi_grupo g ON g.id = i.grupo
        ORDER BY i.orden, i.id""")


def queryIndicadorLetrasTMI(db: Session, id_indicador: int):
    return _consulta(db, f"""
        SELECT iv.id, iv.id_indicador, iv.letra, iv.id_variable, v.nombre AS variable, v.total_anual,
               (SELECT COUNT(*) FROM {name_server}.tmi_variable_logica l WHERE l.id_variable = v.id) AS filas_logica,
               STUFF((SELECT ' | ' + (
                    CAST(l.tipgrupo AS VARCHAR) + '·' + ISNULL(LTRIM(RTRIM(g.desctipgrupo)), '')
                    + ' / ' + CAST(l.actividad AS VARCHAR) + '·' + ISNULL(COALESCE(NULLIF(LTRIM(RTRIM(a.desclarga)), ''), LTRIM(RTRIM(a.descactividad))), '')
                    + ' (Serv: ' + ISNULL(CAST(l.servicio AS VARCHAR), 'Todos') + ', ' + l.agregacion + ')')
                FROM {name_server}.tmi_variable_logica l
                LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = l.tipgrupo
                LEFT JOIN {TMI_DIM}.DIM_ACTIVIDAD a ON a.actividad = l.actividad
                WHERE l.id_variable = v.id AND l.activo = 1
                ORDER BY l.tipgrupo, l.actividad, l.servicio
                FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 3, '') AS detalle_logica
        FROM {name_server}.tmi_indicador_variable iv
        JOIN {name_server}.tmi_variable v ON v.id = iv.id_variable
        WHERE iv.id_indicador = :id ORDER BY iv.letra, v.nombre""", {"id": id_indicador})


### Tablas maestras de estándares
def queryTiposEstandarTMI(db: Session):
    """Tipos de estándar con cuántas claves tienen y qué indicadores los usan."""
    return _consulta(db, f"""
        SELECT t.id, t.codigo, t.descripcion, t.orden, t.activo,
               (SELECT COUNT(*) FROM {name_server}.tmi_estandar e WHERE e.tipo_estandar = t.codigo) AS claves,
               STUFF((SELECT ', ' + i.codigo FROM {name_server}.tmi_indicador i WHERE i.base_estandar = t.codigo
                      ORDER BY i.orden FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, '') AS indicadores
        FROM {name_server}.tmi_tipo_estandar t
        ORDER BY ISNULL(t.orden, 999), t.codigo""")


def queryEstandarClavesTMI(db: Session):
    """Claves de todos los tipos de estándar, con cuántos centros tienen ese valor hoy."""
    return _consulta(db, f"""
        SELECT e.id, e.tipo_estandar, e.orden, e.fuente, e.clave, e.descripcion, e.prioridad, e.activo,
               (SELECT COUNT(DISTINCT c.codcentro) FROM {name_server}.vw_tmi_centro_base c
                WHERE CASE e.fuente WHEN 'NIVEL' THEN c.nivel WHEN 'TIPO' THEN c.tipo ELSE c.categoria END = e.clave) AS centros
        FROM {name_server}.tmi_estandar e
        ORDER BY e.tipo_estandar, ISNULL(e.orden, 999), e.prioridad DESC, e.clave""")


def queryValoresEstandarIndicadorTMI(db: Session, id_indicador: int, anio: int):
    """Claves del tipo de estándar del indicador con su valor por mes (de la tabla de su fuente)."""
    meses = ", ".join(f"s.m{m:02d} AS est_{m:02d}" for m in range(1, 13))
    return _consulta(db, f"""
        SELECT e.id AS id_clave, e.orden, e.fuente, e.clave, e.descripcion, e.prioridad, e.activo, {meses},
               (SELECT COUNT(DISTINCT c.codcentro) FROM {name_server}.vw_tmi_centro_base c
                WHERE CASE e.fuente WHEN 'NIVEL' THEN c.nivel WHEN 'TIPO' THEN c.tipo ELSE c.categoria END = e.clave) AS centros
        FROM {name_server}.tmi_indicador i
        JOIN {name_server}.tmi_estandar e ON e.tipo_estandar = i.base_estandar
        OUTER APPLY (SELECT TOP 1 * FROM {name_server}.vw_tmi_std x
                     WHERE x.id_estandar = i.id AND x.anio = :anio AND x.fuente = e.fuente AND x.clave = e.clave) s
        WHERE i.id = :id
        ORDER BY ISNULL(e.orden, 999), e.prioridad DESC, e.clave""", {"id": id_indicador, "anio": anio})


def queryAceptacionTMI(db: Session, anio: int, mes: int):
    """% Acept de los indicadores activos: su porcentaje y, por cada clave de su tipo de estándar, el estándar del mes
    (el % Acept se calcula en pantalla igual que en usp_tmi_calcular)."""
    indicadores = _consulta(db, f"""
        SELECT i.id, i.orden, i.codigo, i.indicador, i.base_estandar, i.sentido, i.formato,
               i.tipo_tolerancia, i.tolerancia, i.tolerancia_menos, g.descripcion AS grupo
        FROM {name_server}.tmi_indicador i
        LEFT JOIN {name_server}.tmi_grupo g ON g.id = i.grupo
        WHERE i.activo = 1
        ORDER BY i.orden, i.id""")
    # CASE en lugar de CHOOSE: el servidor no lo reconoce (nivel de compatibilidad anterior a SQL Server 2012)
    mes_valor = " ".join(f"WHEN {m} THEN s.m{m:02d}" for m in range(1, 13))
    claves = _consulta(db, f"""
        SELECT i.id AS id_indicador, e.orden, e.fuente, e.clave, e.descripcion,
               NULLIF(CASE :mes {mes_valor} END, 0) AS estandar
        FROM {name_server}.tmi_indicador i
        JOIN {name_server}.tmi_estandar e ON e.tipo_estandar = i.base_estandar AND e.activo = 1
        OUTER APPLY (SELECT TOP 1 * FROM {name_server}.vw_tmi_std x
                     WHERE x.id_estandar = i.id AND x.anio = :anio AND x.fuente = e.fuente AND x.clave = e.clave) s
        WHERE i.activo = 1
        ORDER BY i.id, ISNULL(e.orden, 999), e.clave""", {"anio": anio, "mes": mes})
    por_indicador: dict = {}
    for c in claves:
        por_indicador.setdefault(c.pop("id_indicador"), []).append(c)
    for i in indicadores:
        i["claves"] = por_indicador.get(i["id"], [])
    return indicadores


def queryGuardarToleranciaTMI(db: Session, id_indicador: int, datos: dict, usuario: str = None):
    """Guarda el porcentaje del % Acept del indicador (tipo, hacia arriba y, en banda, hacia abajo)."""
    try:
        r = db.execute(text(f"""
            UPDATE {name_server}.tmi_indicador
               SET tipo_tolerancia = :tipo_tolerancia, tolerancia = :tolerancia, tolerancia_menos = :tolerancia_menos,
                   usuario_modificacion = :usuario, fecha_modificacion = GETDATE()
             WHERE id = :id"""), {**datos, "id": id_indicador, "usuario": usuario})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    if r.rowcount == 0:
        raise HTTPException(status_code=404, detail="Indicador no encontrado")
    return {"message": "% Acept guardado", "rows_updated": r.rowcount}


# fuente -> tabla de valores, columna de la clave y DTO de tmiRep (que ya sabe guardar en las dos estructuras)
FUENTES_ESTANDAR = {
    "NIVEL": ("tmi_estandar_nivel", "nivel_centro", "tmiEstandarNivelDto"),
    "TIPO": ("tmi_estandar_tipo", "tipo_centro", "tmiEstandarTipoDto"),
    "CATEGORIA": ("tmi_estandar_categoria", "categoria_centro", "tmiEstandarCategoriaDto"),
}


def queryGuardarValorEstandarTMI(db: Session, id_indicador: int, datos: dict):
    """Guarda (alta o edición) el estándar del indicador para una clave y año en la tabla de su fuente."""
    from src.main.dtos import tmiDto
    from src.main.repositories import tmiRep
    tabla, columna, nombre_dto = FUENTES_ESTANDAR[datos["fuente"]]
    meses = {f"est_{m:02d}": datos.get(f"est_{m:02d}") for m in range(1, 13)}
    valores = [v for v in meses.values() if v is not None]
    dto = getattr(tmiDto, nombre_dto)(id_indicador=id_indicador, anio=datos["anio"], **{columna: datos["clave"]},
                                      est_fijo=valores[0] if valores and len(set(valores)) == 1 else None, **meses)
    return tmiRep._guardar(db, tabla, columna, dto, "Estándar guardado")


OPERADORES = {"+": "+", "-": "-", "*": "*", "/": "/"}


def queryGuardarFormulaTMI(db: Session, id_indicador: int, formula: dict, usuario: str = None):
    """Fórmula en bloques -> letras automáticas (A, B, C... por orden de aparición; la misma variable usa la misma
    letra en numerador y denominador), expr_numerador / expr_denominador y tmi_indicador_variable, en una transacción."""
    letra_de: dict = {}

    def expresion(bloques: list) -> str:
        partes = []
        for k, b in enumerate(bloques):
            v = int(b["id_variable"])
            if v not in letra_de:
                if len(letra_de) == 26:
                    raise HTTPException(status_code=400, detail="La fórmula admite como máximo 26 variables (A-Z).")
                letra_de[v] = chr(ord("A") + len(letra_de))
            if k:
                partes.append(OPERADORES[b["op"]])
            partes.append(letra_de[v])
        return " ".join(partes)

    num = expresion(formula["numerador"])
    den = expresion(formula["denominador"]) if formula["denominador"] else "1"
    existentes = {r[0] for r in db.execute(text(
        f"SELECT id FROM {name_server}.tmi_variable WHERE id IN ({', '.join(str(v) for v in letra_de)})"))}
    faltan = sorted(set(letra_de) - existentes)
    if faltan:
        raise HTTPException(status_code=400, detail=f"Variables que no existen: {faltan}")
    try:
        r = db.execute(text(f"""
            UPDATE {name_server}.tmi_indicador
               SET expr_numerador = :num, expr_denominador = :den,
                   usuario_modificacion = :usuario, fecha_modificacion = GETDATE()
             WHERE id = :id"""), {"num": num, "den": den, "usuario": usuario, "id": id_indicador})
        if r.rowcount == 0:
            raise HTTPException(status_code=404, detail="Indicador no encontrado")
        db.execute(text(f"DELETE FROM {name_server}.tmi_indicador_variable WHERE id_indicador = :id"), {"id": id_indicador})
        for v, letra in letra_de.items():
            db.execute(text(f"""INSERT INTO {name_server}.tmi_indicador_variable (id_indicador, letra, id_variable)
                                VALUES (:id, :letra, :v)"""), {"id": id_indicador, "letra": letra, "v": v})
        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return {"expr_numerador": num, "expr_denominador": den,
            "letras": [{"letra": l, "id_variable": v} for v, l in letra_de.items()]}


def queryIndicadorAmbitoTMI(db: Session, id_indicador: int):
    return _consulta(db, f"""
        SELECT id, id_indicador, red, nivel, categoria, tipo, codcentro, incluir, periodo_desde, periodo_hasta
        FROM {name_server}.tmi_indicador_ambito WHERE id_indicador = :id
        ORDER BY incluir DESC, red, nivel, categoria, tipo, codcentro""", {"id": id_indicador})


def queryIndicadorEstandaresTMI(db: Session, id_indicador: int):
    return _consulta(db, f"""
        SELECT id, id_indicador, nivel, categoria, tipo, periodo_desde, periodo_hasta,
               estandar, acept, aceptmenos, activo
        FROM {name_server}.tmi_indicador_estandar
        WHERE id_indicador = :id
        ORDER BY periodo_desde DESC, tipo, categoria, nivel""", {"id": id_indicador})


def queryCentroEstandarTMI(db: Session, anio: int):
    col = _columna_indicador(db, "tmi_centro_estandar")
    return _consulta(db, f"""
        SELECT ce.id, ce.codcentro, ce.{col} AS id_indicador, ce.anio, ce.aplica,
               ce.est_01, ce.est_02, ce.est_03, ce.est_04, ce.est_05, ce.est_06,
               ce.est_07, ce.est_08, ce.est_09, ce.est_10, ce.est_11, ce.est_12, ce.acept, ce.sustento,
               i.indicador, c.centro, c.red
        FROM {name_server}.tmi_centro_estandar ce
        LEFT JOIN {name_server}.tmi_indicador i ON i.id = ce.{col}
        OUTER APPLY (SELECT TOP 1 b.centro, b.red FROM {name_server}.vw_tmi_centro_base b
                     WHERE CAST(b.codcentro AS VARCHAR(50)) = LTRIM(RTRIM(ce.codcentro))) c
        WHERE ce.anio = :anio
        ORDER BY ce.{col}, ce.codcentro""", {"anio": anio})

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
    """Secciones del reporte (tmi_grupo) para el indicador."""
    return _consulta(db, f"""
        SELECT id, descripcion, visible, orden FROM {name_server}.tmi_grupo
        ORDER BY ISNULL(orden, 999), descripcion""")


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


def queryCatalogoCentrosTMI(db: Session):
    return _consulta(db, f"""
        SELECT codcentro, MAX(centro) AS centro, MAX(red) AS red, MAX(tipo) AS tipo,
               MAX(nivel) AS nivel, MAX(categoria) AS categoria
        FROM {name_server}.vw_tmi_centro_base GROUP BY codcentro ORDER BY MAX(red), MAX(centro)""")


_COLS_RESULTADO = ("periodo, anio, id_indicador, orden, orden_red, red, codcentro, centro, nivel, tipo, categoria, "
                   "estandar, acept, aceptmenos, total, "
                   + ", ".join(f"periodo_{m:02d}" for m in range(1, 13)) + ", puntaje, motivo_na, visible, fecha_calculo")


def queryResultadoIndicadorTMI(db: Session, periodo: int, id_indicador: int):
    """Resultado final del indicador guardado en el periodo (tmi_resultado_indicador), como la hoja del Excel."""
    return _consulta(db, f"""
        SELECT {_COLS_RESULTADO}
        FROM {name_server}.tmi_resultado_indicador
        WHERE periodo = :periodo AND id_indicador = :id
        ORDER BY orden_red, orden, codcentro""", {"periodo": periodo, "id": id_indicador})


def queryResultadoFinalTMI(db: Session, periodo: int):
    """Resultado final de todos los indicadores del periodo (para armar el Excel sin recalcular)."""
    return _consulta(db, f"""
        SELECT {_COLS_RESULTADO}
        FROM {name_server}.tmi_resultado_indicador
        WHERE periodo = :periodo
        ORDER BY orden_red, orden, codcentro""", {"periodo": periodo})


def queryPeriodosResultadoTMI(db: Session):
    """Periodos que tienen resultado final guardado, del más reciente al más antiguo."""
    return _consulta(db, f"""
        SELECT periodo, COUNT(DISTINCT id_indicador) AS indicadores, COUNT(DISTINCT codcentro) AS centros,
               MAX(fecha_calculo) AS fecha_calculo
        FROM {name_server}.tmi_resultado_indicador
        GROUP BY periodo
        ORDER BY periodo DESC""")


def queryValidarConfigTMI(db: Session):
    try:
        result = db.execute(text(f"EXEC {name_server}.usp_tmi_validar_config"))
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryCalcularTMI(db: Session, periodo: int):
    """Genera el pivot de variables y calcula los indicadores del periodo (AAAAMM) en tmi_resultado."""
    try:
        db.execute(text(f"EXEC {name_server}.usp_tmi_generar_pivot :periodo"), {"periodo": periodo})
        db.execute(text(f"EXEC {name_server}.usp_tmi_calcular :periodo"), {"periodo": periodo})
        db.commit()
        result = db.execute(text(f"""
            SELECT puntaje, COUNT(*) AS cantidad
            FROM {name_server}.tmi_resultado
            WHERE periodo_corte = :periodo AND mes = :mes
            GROUP BY puntaje
        """), {"periodo": periodo, "mes": periodo % 100})
        return {row["puntaje"]: row["cantidad"] for row in result.mappings()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def queryIndicadoresActivosTMI(db: Session):
    try:
        result = db.execute(text(f"""
            SELECT i.id, i.codigo, i.indicador, i.nombre_hoja, i.titulo_hoja, i.orden, i.sentido, i.formato,
                   g.descripcion AS grupo, g.orden AS orden_grupo
            FROM {name_server}.tmi_indicador i
            LEFT JOIN {name_server}.tmi_grupo g ON g.id = i.grupo
            WHERE i.activo = 1
            ORDER BY i.orden, i.id
        """))
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryResultadoTMI(db: Session, periodo: int):
    try:
        result = db.execute(text(f"""
            SELECT id_indicador, codcentro, mes, valor, estandar, verde, acept, aceptmenos, puntaje, motivo_na, visible
            FROM {name_server}.tmi_resultado
            WHERE periodo_corte = :periodo
        """), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryCentrosReporteTMI(db: Session, periodo: int):
    """Centros del reporte: los de tmi_centro del año (o sin año) visibles en el mes de corte."""
    try:
        result = db.execute(text(f"""
            DECLARE @anio INT = :periodo / 100, @mes INT = :periodo % 100;
            SELECT c.codcentro, MAX(c.centro) AS centro, MAX(c.red) AS red, MIN(c.orden) AS orden,
                   MIN(c.orden_tipo) AS orden_tipo, MIN(c.id_centro) AS id_centro,
                   MAX(c.nivel) AS nivel, MAX(c.categoria) AS categoria, MAX(c.tipo) AS tipo
            FROM {name_server}.vw_tmi_centro_base c
            WHERE (c.anio = @anio
                   OR (c.anio IS NULL AND NOT EXISTS (SELECT 1 FROM {name_server}.vw_tmi_centro_base x WHERE x.anio = @anio)))
              AND (CASE @mes WHEN 1 THEN c.f01 WHEN 2 THEN c.f02 WHEN 3 THEN c.f03 WHEN 4 THEN c.f04 WHEN 5 THEN c.f05 WHEN 6 THEN c.f06
                             WHEN 7 THEN c.f07 WHEN 8 THEN c.f08 WHEN 9 THEN c.f09 WHEN 10 THEN c.f10 WHEN 11 THEN c.f11 WHEN 12 THEN c.f12 END) = 1
            GROUP BY c.codcentro
            ORDER BY MIN(c.orden), MIN(c.id_centro)
        """), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
