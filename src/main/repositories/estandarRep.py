"""Estándares del TMI: indicadores del mantenimiento (tmi_estandar), estándares por tipo, nivel y categoría,
tablas maestras de estándares, estándares por indicador y % Acept (tolerancia)."""

from datetime import date

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core.tmiConfig import TMI_DIM

from src.main.dtos.tmiDto import (
    tmiEstandarDto,
    tmiEstandarTipoDto,
    tmiEstandarNivelDto,
    tmiEstandarCategoriaDto,
)
from src.main.repositories.tmiBaseRep import (
    name_server,
    MESES,
    _tiene_columna,
    _existe_tabla,
    _col_indicador,
    _formato_largo,
    _indicador_join,
    _params,
    _id_indicador,
    _consulta,
)


def queryEstandar(db: Session ):
    try:
        query = f"""
        IF OBJECT_ID('{name_server}.tmi_indicador') IS NOT NULL
            SELECT i.id, ISNULL(LTRIM(RTRIM(g.desctipgrupo)), '') AS tipo, i.indicador, i.fecha_creacion, i.fecha_modificacion
            FROM {name_server}.tmi_indicador i
            LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = i.grupo
            ORDER BY i.orden, i.id
        ELSE
            SELECT * FROM {name_server}.tmi_estandar
        """
        result = db.execute(text(query))
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryInsertEstandar(db: Session, estandar: tmiEstandarDto):
    try:
        params = _params(estandar)
        if _existe_tabla(db, "tmi_indicador"):
            # 'tipo' es la sección del reporte (DIM_GRUPO.desctipgrupo)
            query = f"""
            INSERT INTO {name_server}.tmi_indicador (grupo, indicador, fecha_creacion, fecha_modificacion)
            VALUES ((SELECT TOP 1 tipgrupo FROM {TMI_DIM}.DIM_GRUPO WHERE LTRIM(RTRIM(desctipgrupo)) = LTRIM(RTRIM(:tipo))),
                    :indicador, COALESCE(:fecha_creacion, GETDATE()), COALESCE(:fecha_modificacion, GETDATE()))
            """
        else:
            query = f"""
            INSERT INTO {name_server}.tmi_estandar
            (tipo ,indicador ,fecha_creacion ,fecha_modificacion)
            VALUES (:tipo ,:indicador ,COALESCE(:fecha_creacion, GETDATE()) ,COALESCE(:fecha_modificacion, GETDATE()))
            """
        result = db.execute(text(query), params)
        db.commit()
        return {"message": "Estándar insertado correctamente", "rows_inserted": result.rowcount}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def queryUpdateEstandar(db: Session, dto: tmiEstandarDto):
    try:
        params = _params(dto)
        if _existe_tabla(db, "tmi_indicador"):
            query = f"""
            UPDATE {name_server}.tmi_indicador
                SET grupo = COALESCE((SELECT TOP 1 tipgrupo FROM {TMI_DIM}.DIM_GRUPO
                                      WHERE LTRIM(RTRIM(desctipgrupo)) = LTRIM(RTRIM(:tipo))), grupo)
                ,indicador = :indicador
                ,fecha_modificacion = COALESCE(:fecha_modificacion, GETDATE())
            WHERE (:id IS NOT NULL AND id = :id) OR (:id IS NULL AND indicador = :indicador)
            """
        else:
            query = f"""
            UPDATE {name_server}.tmi_estandar
                SET tipo = :tipo
                ,indicador = :indicador
                ,fecha_creacion = COALESCE(:fecha_creacion, fecha_creacion)
                ,fecha_modificacion = COALESCE(:fecha_modificacion, GETDATE())
            WHERE (:id IS NOT NULL AND id = :id) OR (:id IS NULL AND indicador = :indicador)
            """
        result = db.execute(text(query), params)
        db.commit()
        return {"message": "Estándar actualizado correctamente", "rows_affected": result.rowcount}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def queryDeleteEstandar(db: Session, id: int):
    tabla = "tmi_indicador" if _existe_tabla(db, "tmi_indicador") else "tmi_estandar"
    try:
        result = db.execute(text(f"DELETE FROM {name_server}.{tabla} WHERE id = :id"), {"id": id})
        db.commit()
        return {"message": "Estándar eliminado correctamente", "rows_deleted": result.rowcount}
    except Exception as e:
        db.rollback()
        if "REFERENCE" in str(e).upper() or "FOREIGN KEY" in str(e).upper():
            raise HTTPException(status_code=400, detail="El indicador tiene estándares, letras o exclusiones: "
                                                        "elimínelos antes o márquelo como inactivo.")
        raise HTTPException(status_code=500, detail=str(e))


### tmi_estandar_tipo / _nivel / _categoria (misma estructura, cambia la clave del centro)
def _listar_estandar(db: Session, tabla: str, clave: str, fuente: str, anio: int):
    if _formato_largo(db, tabla):
        # formato largo: se lee por la vista adaptadora (no tiene un id por fila)
        query = f"""
        SELECT ROW_NUMBER() OVER (ORDER BY i.orden, s.id_estandar, s.clave) AS id,
               s.id_estandar AS id_indicador, s.id_estandar,
               ISNULL(LTRIM(RTRIM(g.desctipgrupo)), '') AS tipo,
               i.indicador,
               s.clave AS {clave},
               s.anio,
               s.m01 AS est_fijo,
               s.m01 AS est_01, s.m02 AS est_02, s.m03 AS est_03, s.m04 AS est_04, s.m05 AS est_05, s.m06 AS est_06,
               s.m07 AS est_07, s.m08 AS est_08, s.m09 AS est_09, s.m10 AS est_10, s.m11 AS est_11, s.m12 AS est_12
        FROM {name_server}.vw_tmi_std s
        JOIN {name_server}.tmi_indicador i ON i.id = s.id_estandar
        LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = i.grupo
        WHERE s.fuente = '{fuente}' AND s.anio = :anio
        ORDER BY i.orden, s.id_estandar, s.clave
        """
    else:
        col = _col_indicador(db, tabla)
        pre = "est_" if _tiene_columna(db, tabla, "est_01") else "estandar_"
        fijo = "t.est_fijo" if _tiene_columna(db, tabla, "est_fijo") else "CAST(NULL AS FLOAT)"
        join, tipo, orden = _indicador_join(db, f"t.{col}")
        meses = ", ".join(f"t.{pre}{m} AS est_{m}" for m in MESES)
        query = f"""
        SELECT t.id, t.{col} AS id_indicador, t.{col} AS id_estandar, {tipo} AS tipo, i.indicador,
               t.{clave}, t.anio, {fijo} AS est_fijo, {meses}
        FROM {name_server}.{tabla} t
        {join}
        WHERE t.anio = :anio
        ORDER BY {orden}, t.{clave}
        """
    result = db.execute(text(query), {"anio": anio})
    return [dict(row) for row in result.mappings()]


def _guardar_estandar(db: Session, tabla: str, clave: str, dto):
    """Alta o edición. Con id: actualiza esa fila. Sin id: actualiza la fila del mismo indicador, clave y año,
    o la crea (así no se duplica la combinación, que tiene UNIQUE)."""
    params = _params(dto)
    params["id_indicador"] = _id_indicador(params)
    col = _col_indicador(db, tabla)
    pre = "est_" if _tiene_columna(db, tabla, "est_01") else "estandar_"
    con_fijo = _tiene_columna(db, tabla, "est_fijo")
    sets = [f"{col} = :id_indicador", f"{clave} = LTRIM(RTRIM(:{clave}))", "anio = :anio"]
    sets += [f"{pre}{m} = :est_{m}" for m in MESES] + (["est_fijo = :est_fijo"] if con_fijo else [])
    cols = [col, clave, "anio"] + [f"{pre}{m}" for m in MESES] + (["est_fijo"] if con_fijo else [])
    vals = [":id_indicador", f"LTRIM(RTRIM(:{clave}))", ":anio"] + [f":est_{m}" for m in MESES] + ([":est_fijo"] if con_fijo else [])
    if params.get("id"):
        query = f"UPDATE {name_server}.{tabla} SET {', '.join(sets)} WHERE id = :id"
    else:
        query = f"""
        UPDATE {name_server}.{tabla} SET {', '.join(sets)}
        WHERE {col} = :id_indicador AND LTRIM(RTRIM({clave})) = LTRIM(RTRIM(:{clave})) AND anio = :anio;
        IF @@ROWCOUNT = 0
            INSERT INTO {name_server}.{tabla} ({', '.join(cols)}) VALUES ({', '.join(vals)});
        """
    result = db.execute(text(query), params)
    db.commit()
    return result.rowcount


def _guardar_estandar_largo(db: Session, tabla: str, clave: str, dto):
    """Formato largo (una fila por mes, indicador por nombre): se reemplazan los 12 meses."""
    params = _params(dto)
    params["id_indicador"] = _id_indicador(params)
    query = f"""
    DECLARE @tipo VARCHAR(200), @ind VARCHAR(200);
    SELECT @tipo = ISNULL(LTRIM(RTRIM(g.desctipgrupo)), ''), @ind = i.indicador
    FROM {name_server}.tmi_indicador i
    LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = i.grupo
    WHERE i.id = :id_indicador;

    DELETE s FROM {name_server}.{tabla} s
    WHERE REPLACE(LTRIM(RTRIM(s.indicador)), ' de ', ' ') = REPLACE(LTRIM(RTRIM(@ind)), ' de ', ' ')
      AND LTRIM(RTRIM(s.{clave})) = LTRIM(RTRIM(:{clave}))
      AND s.anio = :anio;

    INSERT INTO {name_server}.{tabla} (tipo, indicador, {clave}, anio, mes, periodo, estandar)
    SELECT @tipo, @ind, LTRIM(RTRIM(:{clave})), :anio, v.mes,
           CAST(:anio AS VARCHAR(4)) + RIGHT('0' + CAST(v.mes AS VARCHAR(2)), 2), v.est
    FROM (VALUES
        (1, :est_01), (2, :est_02), (3, :est_03), (4, :est_04), (5, :est_05), (6, :est_06),
        (7, :est_07), (8, :est_08), (9, :est_09), (10, :est_10), (11, :est_11), (12, :est_12)
    ) v(mes, est);
    """
    result = db.execute(text(query), params)
    db.commit()
    return result.rowcount


def _guardar(db: Session, tabla: str, clave: str, dto, mensaje: str):
    try:
        if _formato_largo(db, tabla):
            filas = _guardar_estandar_largo(db, tabla, clave, dto)
        else:
            filas = _guardar_estandar(db, tabla, clave, dto)
        return {"message": mensaje, "rows_affected": filas}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def _eliminar(db: Session, tabla: str, id: int, mensaje: str):
    try:
        if _formato_largo(db, tabla):
            raise HTTPException(status_code=400, detail=f"{tabla} está en formato largo: sus filas no tienen id. "
                                                        "Guarde los estándares en 0 para dejarlos sin efecto.")
        result = db.execute(text(f"DELETE FROM {name_server}.{tabla} WHERE id = :id"), {"id": id})
        db.commit()
        return {"message": mensaje, "rows_deleted": result.rowcount}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def queryEstandarTipo(db: Session, anio: int):
    try:
        return _listar_estandar(db, "tmi_estandar_tipo", "tipo_centro", "TIPO", anio)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryInsertEstandarTipo(db: Session, estandar_tipo: tmiEstandarTipoDto):
    return _guardar(db, "tmi_estandar_tipo", "tipo_centro", estandar_tipo, "Estándares por Tipo guardados correctamente")


def queryUpdateEstandarTipo(db: Session, dto: tmiEstandarTipoDto):
    return _guardar(db, "tmi_estandar_tipo", "tipo_centro", dto, "Estándar Tipo actualizado correctamente")


def queryDeleteEstandarTipo(db: Session, id: int):
    return _eliminar(db, "tmi_estandar_tipo", id, "Estándar Tipo eliminado correctamente")


def queryEstandarNivel(db: Session, anio: int):
    try:
        return _listar_estandar(db, "tmi_estandar_nivel", "nivel_centro", "NIVEL", anio)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryInsertEstandarNivel(db: Session, estardar_nivel: tmiEstandarNivelDto):
    return _guardar(db, "tmi_estandar_nivel", "nivel_centro", estardar_nivel, "Estándares por Nivel guardados correctamente")


def queryUpdateEstandarNivel(db: Session, dto: tmiEstandarNivelDto):
    return _guardar(db, "tmi_estandar_nivel", "nivel_centro", dto, "Estándar Nivel actualizado correctamente")


def queryDeleteEstandarNivel(db: Session, id: int):
    return _eliminar(db, "tmi_estandar_nivel", id, "Estándar Nivel eliminado correctamente")


def queryEstandarCategoria(db: Session, anio: int):
    try:
        return _listar_estandar(db, "tmi_estandar_categoria", "categoria_centro", "CATEGORIA", anio)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryInsertEstandarCategoria(db: Session, estandar_categoria: tmiEstandarCategoriaDto):
    return _guardar(db, "tmi_estandar_categoria", "categoria_centro", estandar_categoria,
                    "Estándares por Categoría guardados correctamente")


def queryUpdateEstandarCategoria(db: Session, dto: tmiEstandarCategoriaDto):
    return _guardar(db, "tmi_estandar_categoria", "categoria_centro", dto, "Estándar Categoría actualizado correctamente")


def queryDeleteEstandarCategoria(db: Session, id: int):
    return _eliminar(db, "tmi_estandar_categoria", id, "Estándar Categoría eliminado correctamente")


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


# fuente -> tabla de valores, columna de la clave y DTO (_guardar ya sabe guardar en las dos estructuras)
FUENTES_ESTANDAR = {
    "NIVEL": ("tmi_estandar_nivel", "nivel_centro", "tmiEstandarNivelDto"),
    "TIPO": ("tmi_estandar_tipo", "tipo_centro", "tmiEstandarTipoDto"),
    "CATEGORIA": ("tmi_estandar_categoria", "categoria_centro", "tmiEstandarCategoriaDto"),
}


def queryGuardarValorEstandarTMI(db: Session, id_indicador: int, datos: dict):
    """Guarda (alta o edición) el estándar del indicador para una clave y año en la tabla de su fuente."""
    from src.main.dtos import tmiDto
    tabla, columna, nombre_dto = FUENTES_ESTANDAR[datos["fuente"]]
    meses = {f"est_{m:02d}": datos.get(f"est_{m:02d}") for m in range(1, 13)}
    valores = [v for v in meses.values() if v is not None]
    dto = getattr(tmiDto, nombre_dto)(id_indicador=id_indicador, anio=datos["anio"], **{columna: datos["clave"]},
                                      est_fijo=valores[0] if valores and len(set(valores)) == 1 else None, **meses)
    return _guardar(db, tabla, columna, dto, "Estándar guardado")


def queryIndicadorEstandaresTMI(db: Session, id_indicador: int):
    return _consulta(db, f"""
        SELECT id, id_indicador, nivel, categoria, tipo, periodo_desde, periodo_hasta,
               estandar, acept, aceptmenos, activo
        FROM {name_server}.tmi_indicador_estandar
        WHERE id_indicador = :id
        ORDER BY periodo_desde DESC, tipo, categoria, nivel""", {"id": id_indicador})


def _asegurar_fijo_anio(db: Session, anio: int):
    """Garantiza que cada indicador tenga su % Acept fijo del año (mes = 0), copiando del año anterior o de tmi_indicador."""
    db.execute(text(f"""
        INSERT INTO {name_server}.tmi_indicador_tolerancia
            (id_indicador, anio, mes, tipo_tolerancia, tolerancia, tolerancia_menos, fecha_modificacion)
        SELECT i.id, :anio, 0,
               COALESCE(ant.tipo_tolerancia, i.tipo_tolerancia, 'REL'),
               COALESCE(ant.tolerancia, i.tolerancia, 0),
               CASE WHEN ant.id IS NOT NULL THEN ant.tolerancia_menos ELSE i.tolerancia_menos END,
               GETDATE()
        FROM {name_server}.tmi_indicador i
        LEFT JOIN {name_server}.tmi_indicador_tolerancia ant
               ON ant.id_indicador = i.id AND ant.anio = :anio - 1 AND ant.mes = 0
        WHERE NOT EXISTS (
            SELECT 1 FROM {name_server}.tmi_indicador_tolerancia f
            WHERE f.id_indicador = i.id AND f.anio = :anio AND f.mes = 0
        )"""), {"anio": anio})
    db.commit()


def aplicarCierrePeriodoTMI(db: Session, periodo: str) -> int:
    """Al cumplirse la fecha de cierre de un periodo (AAAAMM):
    1) En las tablas de estándares (tipo, nivel, categoría), el mes del periodo toma su est_fijo si aún no tiene valor.
    2) En tmi_indicador_tolerancia, el mes del periodo toma el % Acept fijo del año (mes = 0) si aún no fue definido."""
    p = str(periodo).strip()
    if len(p) != 6 or not p.isdigit():
        return 0
    anio, mes = int(p[:4]), int(p[4:])
    if not 1 <= mes <= 12:
        return 0
    _asegurar_fijo_anio(db, anio)
    afectadas = 0
    col_mes = f"est_{mes:02d}"
    for tabla, clave in (("tmi_estandar_tipo", "tipo_centro"),
                         ("tmi_estandar_nivel", "nivel_centro"),
                         ("tmi_estandar_categoria", "categoria_centro")):
        tiene_fijo = db.execute(text("SELECT COL_LENGTH(:t, 'est_fijo')"), {"t": f"{name_server}.{tabla}"}).scalar()
        tiene_mes = db.execute(text("SELECT COL_LENGTH(:t, :c)"), {"t": f"{name_server}.{tabla}", "c": col_mes}).scalar()
        if tiene_fijo is None or tiene_mes is None:
            continue
        col_ind = "id_indicador" if db.execute(
            text("SELECT COL_LENGTH(:t, 'id_indicador')"), {"t": f"{name_server}.{tabla}"}
        ).scalar() is not None else "id_estandar"
        # Si es un año nuevo sin filas aún, copia las filas base (con su est_fijo) del año anterior
        db.execute(text(f"""
            IF NOT EXISTS (SELECT 1 FROM {name_server}.{tabla} WHERE anio = :anio)
            INSERT INTO {name_server}.{tabla} ({col_ind}, {clave}, anio, est_fijo)
            SELECT {col_ind}, {clave}, :anio, est_fijo
            FROM {name_server}.{tabla}
            WHERE anio = :anio - 1"""), {"anio": anio})
        r_est = db.execute(text(f"""
            UPDATE {name_server}.{tabla}
               SET {col_mes} = est_fijo
             WHERE anio = :anio
               AND est_fijo IS NOT NULL
               AND ({col_mes} IS NULL OR {col_mes} = 0)"""), {"anio": anio})
        afectadas += r_est.rowcount or 0

    r_tol = db.execute(text(f"""
        INSERT INTO {name_server}.tmi_indicador_tolerancia
            (id_indicador, anio, mes, tipo_tolerancia, tolerancia, tolerancia_menos, fecha_modificacion)
        SELECT f.id_indicador, :anio, :mes, f.tipo_tolerancia, f.tolerancia, f.tolerancia_menos, GETDATE()
        FROM {name_server}.tmi_indicador_tolerancia f
        WHERE f.anio = :anio AND f.mes = 0
          AND NOT EXISTS (
              SELECT 1 FROM {name_server}.tmi_indicador_tolerancia m
              WHERE m.id_indicador = f.id_indicador AND m.anio = :anio AND m.mes = :mes
          )"""), {"anio": anio, "mes": mes})
    afectadas += r_tol.rowcount or 0
    db.commit()
    return afectadas


def contarFilasCierrePeriodoTMI(db: Session, periodo: str) -> int:
    """Filas que deja listas el cierre de un periodo: estándares (tipo, nivel, categoría) con valor en el mes
    y % Acept propio del mes en tmi_indicador_tolerancia."""
    p = str(periodo).strip()
    if len(p) != 6 or not p.isdigit() or not 1 <= int(p[4:]) <= 12:
        return 0
    anio, mes = int(p[:4]), int(p[4:])
    col_mes = f"est_{mes:02d}"
    total = 0
    for tabla in ("tmi_estandar_tipo", "tmi_estandar_nivel", "tmi_estandar_categoria"):
        if db.execute(text("SELECT COL_LENGTH(:t, :c)"), {"t": f"{name_server}.{tabla}", "c": col_mes}).scalar() is None:
            continue
        total += db.execute(text(f"""
            SELECT COUNT(1) FROM {name_server}.{tabla}
            WHERE anio = :anio AND {col_mes} IS NOT NULL"""), {"anio": anio}).scalar() or 0
    total += db.execute(text(f"""
        SELECT COUNT(1) FROM {name_server}.tmi_indicador_tolerancia
        WHERE anio = :anio AND mes = :mes"""), {"anio": anio, "mes": mes}).scalar() or 0
    return total


def _periodo_alcanzo_cierre(db: Session, anio: int, mes: int) -> bool:
    """True si el periodo AAAAMM ya alcanzó su fecha de cierre (en la tabla cierre o por ser <= mes anterior al actual)."""
    from src.main.repositories.cierreRep import CIERRE_TABLA
    periodo = f"{anio}{mes:02d}"
    fila = _consulta(db, f"""
        IF OBJECT_ID('{CIERRE_TABLA}', 'U') IS NOT NULL
            SELECT fecha_cierre, estado FROM {CIERRE_TABLA} WHERE periodo = :periodo
        ELSE
            SELECT CAST(NULL AS DATE) AS fecha_cierre, CAST(NULL AS VARCHAR(20)) AS estado WHERE 1 = 0""",
        {"periodo": periodo})
    hoy = date.today()
    if fila and fila[0].get("fecha_cierre"):
        fc = fila[0]["fecha_cierre"]
        if isinstance(fc, str):
            fc = date.fromisoformat(fc[:10])
        elif hasattr(fc, "date"):
            fc = fc.date()
        return fc <= hoy or fila[0].get("estado") == "EJECUTADO"
    periodo_mes_anterior = f"{hoy.year - 1}12" if hoy.month == 1 else f"{hoy.year}{hoy.month - 1:02d}"
    return periodo <= periodo_mes_anterior


def queryAceptacionTMI(db: Session, anio: int, mes: int):
    """% Acept de los indicadores activos para el año y mes seleccionados:
    - Si el periodo ya alcanzó su fecha de cierre, materializa su valor desde el fijo del año (mes = 0).
    - Devuelve tanto el % Acept fijo del año como el % Acept del mes seleccionado."""
    _asegurar_fijo_anio(db, anio)
    # Meses que aún no llegan a su fecha de cierre no tienen valor propio: usan el fijo. Las filas de esos meses que
    # creó la versión anterior al guardar "todo el año" se quitan para que tomen el fijo en su cierre.
    abiertos = [m for m in range(1, 13) if not _periodo_alcanzo_cierre(db, anio, m)]
    if abiertos:
        db.execute(text(f"""
            DELETE FROM {name_server}.tmi_indicador_tolerancia
            WHERE anio = :anio AND mes IN ({", ".join(map(str, abiertos))})"""), {"anio": anio})
        db.commit()
    cerrado = mes not in abiertos
    if cerrado:
        aplicarCierrePeriodoTMI(db, f"{anio}{mes:02d}")
    indicadores = _consulta(db, f"""
        SELECT i.id, i.orden, i.codigo, i.indicador, i.base_estandar, i.sentido, i.formato,
               COALESCE(m.tipo_tolerancia, f.tipo_tolerancia, i.tipo_tolerancia) AS tipo_tolerancia,
               COALESCE(f.tolerancia, i.tolerancia) AS tolerancia_fijo,
               CASE WHEN f.id IS NOT NULL THEN f.tolerancia_menos ELSE i.tolerancia_menos END AS tolerancia_menos_fijo,
               COALESCE(m.tolerancia, f.tolerancia, i.tolerancia) AS tolerancia,
               CASE WHEN m.id IS NOT NULL THEN m.tolerancia_menos
                    WHEN f.id IS NOT NULL THEN f.tolerancia_menos
                    ELSE i.tolerancia_menos END AS tolerancia_menos,
               CAST(CASE WHEN m.id IS NOT NULL THEN 1 ELSE 0 END AS BIT) AS mes_cerrado,
               LTRIM(RTRIM(g.desctipgrupo)) AS grupo
        FROM {name_server}.tmi_indicador i
        LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = i.grupo
        LEFT JOIN {name_server}.tmi_indicador_tolerancia f
               ON f.id_indicador = i.id AND f.anio = :anio AND f.mes = 0
        LEFT JOIN {name_server}.tmi_indicador_tolerancia m
               ON m.id_indicador = i.id AND m.anio = :anio AND m.mes = :mes
        WHERE i.activo = 1
        ORDER BY i.orden, i.id""", {"anio": anio, "mes": mes})
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
        i["mes_cerrado"] = cerrado
    return indicadores


def queryGuardarToleranciaTMI(db: Session, id_indicador: int, datos: dict, usuario: str = None):
    """Guarda el % Acept del indicador para un año:
    - tolerancia_fijo / tolerancia_menos_fijo: el fijo del año (mes = 0), que cada mes toma en su fecha de cierre.
    - tolerancia / tolerancia_menos: el valor del mes, solo si el mes ya alcanzó su fecha de cierre (antes usa el fijo).
    Sin año, guarda el valor base del indicador."""
    existe = _consulta(db, f"SELECT id FROM {name_server}.tmi_indicador WHERE id = :id", {"id": id_indicador})
    if not existe:
        raise HTTPException(status_code=404, detail="Indicador no encontrado")
    anio = datos.get("anio")
    mes = datos.get("mes")
    params = {
        "id": id_indicador,
        "tipo_tolerancia": datos["tipo_tolerancia"],
        "tolerancia": datos["tolerancia"],
        "tolerancia_menos": datos.get("tolerancia_menos"),
        "usuario": usuario,
        "anio": anio,
    }
    guardar_fila = f"""
        UPDATE {name_server}.tmi_indicador_tolerancia
           SET tipo_tolerancia = :tipo_tolerancia, tolerancia = :tolerancia, tolerancia_menos = :tolerancia_menos,
               usuario_modificacion = :usuario, fecha_modificacion = GETDATE()
         WHERE id_indicador = :id AND anio = :anio AND mes = :mes;
        IF @@ROWCOUNT = 0
            INSERT INTO {name_server}.tmi_indicador_tolerancia
                (id_indicador, anio, mes, tipo_tolerancia, tolerancia, tolerancia_menos, usuario_modificacion, fecha_modificacion)
            VALUES (:id, :anio, :mes, :tipo_tolerancia, :tolerancia, :tolerancia_menos, :usuario, GETDATE());"""
    filas = 0
    try:
        if anio is not None:
            if datos.get("tolerancia_fijo") is not None:
                db.execute(text(guardar_fila), {**params, "mes": 0, "tolerancia": datos["tolerancia_fijo"],
                                                "tolerancia_menos": datos.get("tolerancia_menos_fijo")})
                filas += 1
            if mes and _periodo_alcanzo_cierre(db, anio, mes):
                db.execute(text(guardar_fila), {**params, "mes": mes})
                filas += 1
            db.commit()
            return {"message": "% Acept guardado", "rows_updated": filas}
        else:
            r = db.execute(text(f"""
                UPDATE {name_server}.tmi_indicador
                   SET tipo_tolerancia = :tipo_tolerancia, tolerancia = :tolerancia, tolerancia_menos = :tolerancia_menos,
                       usuario_modificacion = :usuario, fecha_modificacion = GETDATE()
                 WHERE id = :id"""), params)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "% Acept guardado", "rows_updated": r.rowcount}
