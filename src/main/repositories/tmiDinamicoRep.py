"""Consultas del TMI dinámico (procedimientos y tablas de src/resources/sql/tmi)."""

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core.tmiConfig import TMI_DB, TMI_DIM, TMI_TOTALIZADO3

name_server = f"{TMI_DB}.dbo"


### Mantenimiento (frontend). Tablas y columnas fijas: nunca vienen del usuario.
TABLAS = {
    "tmi_variable": ["nombre", "descripcion", "total_anual", "activo"],
    "tmi_variable_logica": ["id_variable", "tipgrupo", "actividad", "servicio", "condicion_hoja", "agregacion",
                            "periodo_desde", "periodo_hasta", "activo"],
    "tmi_indicador": ["grupo", "indicador", "codigo", "nombre_hoja", "titulo_hoja", "orden", "expr_numerador",
                      "expr_denominador", "tipo_calculo", "factor", "den_cero", "num_cero_na", "cero_si_letra_mes_0",
                      "sin_datos_anio", "base_estandar", "sentido", "tipo_tolerancia", "tolerancia", "decimales",
                      "cero_es_logro", "mostrar_no_aplica", "activo", "formato"],
    "tmi_indicador_variable": ["id_indicador", "letra", "id_variable"],
    "tmi_indicador_ambito": ["id_indicador", "red", "nivel", "categoria", "tipo", "codcentro", "incluir",
                             "periodo_desde", "periodo_hasta"],
    "tmi_indicador_estandar": ["id_indicador", "nivel", "categoria", "tipo", "periodo_desde", "periodo_hasta",
                               "estandar", "acept", "acept_mas", "activo"],
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
               i.sin_datos_anio, i.base_estandar, i.sentido, i.tipo_tolerancia, i.tolerancia, i.decimales,
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


def queryIndicadorAmbitoTMI(db: Session, id_indicador: int):
    return _consulta(db, f"""
        SELECT id, id_indicador, red, nivel, categoria, tipo, codcentro, incluir, periodo_desde, periodo_hasta
        FROM {name_server}.tmi_indicador_ambito WHERE id_indicador = :id
        ORDER BY incluir DESC, red, nivel, categoria, tipo, codcentro""", {"id": id_indicador})


def queryIndicadorEstandaresTMI(db: Session, id_indicador: int):
    return _consulta(db, f"""
        SELECT id, id_indicador, nivel, categoria, tipo, periodo_desde, periodo_hasta,
               estandar, acept, acept_mas, activo
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

#Grupo, actividad y servicio con sus descripciones (para la lógica de variables)
def queryGrupoActividadServicioTMI(db: Session):
    """Devuelve el grupo, actividad y servicio con sus descripciones (para la lógica de variables)."""
    return _consulta(db, f"""
       SELECT 
gas.tipgrupo,
gr.desctipgrupo,
gas.actividad,
act.desclarga,
gas.servicio,
serv.desclarga
FROM pentahodevDW.dbo.DIM_GRUPOACTIVIDADSERVICIO gas
JOIN pentahodevDW.dbo.DIM_GRUPO gr ON gas.tipgrupo = gr.tipgrupo
JOIN pentahodevDW.dbo.DIM_ACTIVIDAD act on gas.actividad = act.actividad
JOIN pentahodevDW.dbo.DIM_SERVICIO serv ON gas.servicio = serv.servicio""")

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
                   "estandar, acept, acept_mas, total, "
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
            SELECT id_indicador, codcentro, mes, valor, estandar, verde, rojo, rojo_mas, puntaje, motivo_na, visible
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
