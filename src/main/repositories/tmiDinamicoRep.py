"""Consultas del TMI dinámico (procedimientos y tablas de src/resources/sql/tmi)."""

import logging
from datetime import date
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core import tmiFormula
from src.main.core.tmiConfig import TMI_DB, TMI_DIM, TMI_TOTALIZADO3

logger = logging.getLogger(__name__)

name_server = f"{TMI_DB}.dbo"


### Mantenimiento (frontend). Tablas y columnas fijas: nunca vienen del usuario.
TABLAS = {
    "tmi_variable": ["nombre", "descripcion", "agregacion", "total_anual", "activo"],
    "tmi_variable_logica": ["id_variable", "tipgrupo", "actividad", "servicio", "condicion_hoja",
                            "periodo_desde", "periodo_hasta", "activo"],
    "tmi_indicador": ["grupo", "indicador", "codigo", "nombre_hoja", "titulo_hoja", "orden", "tipo_calculo",
                      "sin_datos_anio", "base_estandar", "sentido", "tipo_tolerancia", "tolerancia", "tolerancia_menos", "decimales",
                      "cero_es_logro", "mostrar_no_aplica", "activo", "formato"],
    "tmi_indicador_variable": ["id_indicador", "letra", "id_variable"],
    "tmi_variable_componente": ["id_variable", "id_variable_componente", "activo"],
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
    padres = _consulta(db, f"""
        SELECT v.nombre FROM {name_server}.tmi_variable_componente c
        JOIN {name_server}.tmi_variable v ON v.id = c.id_variable WHERE c.id_variable_componente = :id""", {"id": id})
    if padres:
        raise HTTPException(status_code=400, detail="La variable es componente de: "
                            + ", ".join(sorted(p["nombre"] for p in padres)))
    try:
        db.execute(text(f"DELETE FROM {name_server}.tmi_variable_logica WHERE id_variable = :id"), {"id": id})
        db.execute(text(f"DELETE FROM {name_server}.tmi_variable_componente WHERE id_variable = :id"), {"id": id})
        db.execute(text(f"DELETE FROM {name_server}.tmi_variable_pivot WHERE id_variable = :id"), {"id": id})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return queryEliminarFila(db, "tmi_variable", id)


def queryEliminarIndicador(db: Session, id: int):
    try:
        for tabla in ("tmi_indicador_tolerancia", "tmi_indicador_termino", "tmi_indicador_variable", "tmi_indicador_ambito", "tmi_indicador_estandar", "tmi_resultado"):
            db.execute(text(f"IF OBJECT_ID('{name_server}.{tabla}') IS NOT NULL DELETE FROM {name_server}.{tabla} WHERE id_indicador = :id"), {"id": id})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return queryEliminarFila(db, "tmi_indicador", id)


def queryVariablesTMI(db: Session):
    return _consulta(db, f"""
        SELECT v.id, v.nombre, v.descripcion, v.agregacion, v.total_anual, v.activo,
               (SELECT COUNT(*) FROM {name_server}.tmi_variable_logica l WHERE l.id_variable = v.id) AS filas_logica,
               (SELECT COUNT(*) FROM {name_server}.tmi_variable_componente c WHERE c.id_variable = v.id) AS componentes,
               STUFF((SELECT ', ' + x.codigo FROM (SELECT DISTINCT i.codigo FROM {name_server}.tmi_indicador_variable iv
                    JOIN {name_server}.tmi_indicador i ON i.id = iv.id_indicador
                    WHERE iv.id_variable = v.id AND i.codigo IS NOT NULL) x
                    ORDER BY x.codigo FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, '') AS indicadores
        FROM {name_server}.tmi_variable v
        ORDER BY v.nombre""")


def queryActualizarVariableTMI(db: Session, id: int, datos: dict, usuario: str = None):
    """Actualiza la variable si su nuevo cálculo coincide con el de las variables que suma y las que la suman."""
    distintas = _consulta(db, f"""
        SELECT v.nombre FROM {name_server}.tmi_variable_componente c
        JOIN {name_server}.tmi_variable v ON v.id = CASE WHEN c.id_variable = :id THEN c.id_variable_componente ELSE c.id_variable END
        WHERE (c.id_variable = :id OR c.id_variable_componente = :id) AND v.agregacion <> :agregacion""",
        {"id": id, "agregacion": datos["agregacion"]})
    if distintas:
        raise HTTPException(status_code=400, detail=f"No se puede cambiar el cálculo a {datos['agregacion']}: la variable suma "
                            "o es sumada por variables con otro cálculo: " + ", ".join(sorted(d["nombre"] for d in distintas)))
    return queryActualizarFila(db, "tmi_variable", id, datos, usuario)


def queryVariableComponentesTMI(db: Session, id_variable: int):
    """Componentes de una variable compuesta, con lo que suma cada uno."""
    return _consulta(db, f"""
        SELECT c.id, c.id_variable, c.id_variable_componente, c.activo, v.nombre AS componente, v.activo AS componente_activo,
               v.agregacion,
               (SELECT COUNT(*) FROM {name_server}.tmi_variable_logica l WHERE l.id_variable = v.id AND l.activo = 1) AS filas_logica,
               (SELECT COUNT(*) FROM {name_server}.tmi_variable_componente c2 WHERE c2.id_variable = v.id) AS componentes
        FROM {name_server}.tmi_variable_componente c
        JOIN {name_server}.tmi_variable v ON v.id = c.id_variable_componente
        WHERE c.id_variable = :id
        ORDER BY v.nombre""", {"id": id_variable})


def queryInsertarComponenteTMI(db: Session, datos: dict):
    """Agrega un componente si no forma un ciclo (la variable no puede contenerse a sí misma)."""
    ciclo = db.execute(text(f"""
        ;WITH arbol AS (
            SELECT :comp AS id_var, 0 AS nivel
            UNION ALL
            SELECT c.id_variable_componente, a.nivel + 1
            FROM arbol a JOIN {name_server}.tmi_variable_componente c ON c.id_variable = a.id_var AND c.activo = 1
            WHERE a.nivel < 10)
        SELECT COUNT(*) FROM arbol WHERE id_var = :var OPTION (MAXRECURSION 20)"""),
        {"comp": datos["id_variable_componente"], "var": datos["id_variable"]}).scalar()
    if datos["id_variable"] == datos["id_variable_componente"] or ciclo:
        raise HTTPException(status_code=400, detail="Ese componente contiene a la variable: se formaría un ciclo.")
    calculos = db.execute(text(f"""
        SELECT COUNT(DISTINCT agregacion) FROM {name_server}.tmi_variable WHERE id IN (:var, :comp)"""),
        {"comp": datos["id_variable_componente"], "var": datos["id_variable"]}).scalar()
    if calculos > 1:
        raise HTTPException(status_code=400, detail="La variable y el componente tienen distinto cálculo (SUMA y MEDIANA): "
                                                    "no se pueden sumar.")
    return queryInsertarFila(db, "tmi_variable_componente", datos)


def queryVariableLogicaTMI(db: Session, id_variable: int):
    return _consulta(db, f"""
        SELECT l.id, l.id_variable, l.tipgrupo, l.actividad, l.servicio, l.condicion_hoja,
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
        SELECT i.id, i.grupo, i.indicador, i.codigo, i.nombre_hoja, i.titulo_hoja, i.orden, i.formula_alias, i.formula,
               i.tipo_calculo,
               i.sin_datos_anio, i.base_estandar, i.sentido, i.tipo_tolerancia, i.tolerancia, i.tolerancia_menos, i.decimales,
               i.cero_es_logro, i.mostrar_no_aplica, i.activo, i.formato, g.descripcion AS grupo_descripcion
        FROM {name_server}.tmi_indicador i
        LEFT JOIN {name_server}.tmi_grupo g ON g.id = i.grupo
        ORDER BY i.orden, i.id""")


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


def _asegurar_tabla_tolerancia(db: Session):
    """Crea tmi_indicador_tolerancia (mes = 0 fijo del año; mes = 1..12 valor de cada mes) si aún no existe."""
    db.execute(text(f"""
        IF OBJECT_ID('{name_server}.tmi_indicador_tolerancia') IS NULL
        CREATE TABLE {name_server}.tmi_indicador_tolerancia (
            id                   INT IDENTITY(1,1) PRIMARY KEY,
            id_indicador         INT NOT NULL REFERENCES {name_server}.tmi_indicador(id),
            anio                 INT NOT NULL,
            mes                  INT NOT NULL CONSTRAINT CK_tmi_indicador_tolerancia_mes CHECK (mes BETWEEN 0 AND 12),
            tipo_tolerancia      VARCHAR(3) NOT NULL DEFAULT 'REL' CHECK (tipo_tolerancia IN ('REL', 'ABS')),
            tolerancia           FLOAT NOT NULL,
            tolerancia_menos     FLOAT NULL,
            usuario_modificacion VARCHAR(200) NULL,
            fecha_modificacion   DATETIME NULL,
            CONSTRAINT UX_tmi_indicador_tolerancia UNIQUE (id_indicador, anio, mes)
        )
        ELSE IF NOT EXISTS (
            SELECT 1 FROM {TMI_DB}.sys.check_constraints
            WHERE parent_object_id = OBJECT_ID('{name_server}.tmi_indicador_tolerancia')
              AND definition LIKE '%0%'
        )
        BEGIN
            DECLARE @ck SYSNAME;
            SELECT TOP 1 @ck = name FROM {TMI_DB}.sys.check_constraints
            WHERE parent_object_id = OBJECT_ID('{name_server}.tmi_indicador_tolerancia')
              AND COL_NAME(parent_object_id, parent_column_id) = 'mes';
            IF @ck IS NOT NULL
                EXEC('ALTER TABLE {name_server}.tmi_indicador_tolerancia DROP CONSTRAINT [' + @ck + ']');
            ALTER TABLE {name_server}.tmi_indicador_tolerancia
                ADD CONSTRAINT CK_tmi_indicador_tolerancia_mes CHECK (mes BETWEEN 0 AND 12);
        END"""))
    db.commit()


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
    _asegurar_tabla_tolerancia(db)
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
    _asegurar_tabla_tolerancia(db)
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
               g.descripcion AS grupo
        FROM {name_server}.tmi_indicador i
        LEFT JOIN {name_server}.tmi_grupo g ON g.id = i.grupo
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
    _asegurar_tabla_tolerancia(db)
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
    if servicios and _CON_DIM_SERVICIO is not False:
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


def queryVariableDeFila(db: Session, tabla: str, id: int):
    """Variable dueña de una fila de lógica o de componente (para regenerar fórmulas después de borrarla)."""
    if tabla not in ("tmi_variable_logica", "tmi_variable_componente"):
        raise ValueError(tabla)
    return db.execute(text(f"SELECT id_variable FROM {name_server}.{tabla} WHERE id = :id"), {"id": id}).scalar()


def regenerarFormulasVariable(db: Session, id_variable: int) -> None:
    """Una variable cambió (conjuntos, componentes o cálculo): se vuelve a generar la fórmula interna de los indicadores
    que la usan, directo o dentro de una variable compuesta. Si no se puede (p. ej. quedó sin conjuntos), el indicador
    conserva su fórmula anterior y se avisa en el log."""
    try:
        ids = [r[0] for r in db.execute(text(f"""
            WITH arriba AS (
                SELECT CAST(:id AS INT) AS id_var, 0 AS nivel
                UNION ALL
                SELECT c.id_variable, a.nivel + 1
                FROM arriba a JOIN {name_server}.tmi_variable_componente c ON c.id_variable_componente = a.id_var
                WHERE a.nivel < 10
            )
            SELECT DISTINCT iv.id_indicador
            FROM {name_server}.tmi_indicador_variable iv
            JOIN {name_server}.tmi_indicador i ON i.id = iv.id_indicador AND i.formula_alias IS NOT NULL
            WHERE iv.id_variable IN (SELECT id_var FROM arriba)
            OPTION (MAXRECURSION 20)"""), {"id": id_variable}).all()]
    except Exception as e:
        db.rollback()
        logger.warning("No se pudo buscar los indicadores de la variable %s: %s", id_variable, e)
        return
    for id_ind in ids:
        try:
            alias = db.execute(text(f"SELECT formula_alias FROM {name_server}.tmi_indicador WHERE id = :id"),
                               {"id": id_ind}).scalar()
            letras = {r[0]: r[1] for r in db.execute(text(f"""SELECT letra, id_variable FROM {name_server}.tmi_indicador_variable
                                                             WHERE id_indicador = :id"""), {"id": id_ind}).all()}
            queryGuardarFormulaTMI(db, id_ind, alias, letras, "sistema")
        except Exception as e:
            db.rollback()
            logger.warning("No se pudo regenerar la fórmula del indicador %s: %s", id_ind, getattr(e, "detail", e))


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
    """Estándares propios de centro del año. acept_defecto = % Acept que se usa cuando el centro no tiene uno propio:
    su estándar del periodo de consulta ± el % Acept del indicador en ese periodo (como usp_tmi_calcular)."""
    col = _columna_indicador(db, "tmi_centro_estandar")
    _asegurar_tabla_tolerancia(db)
    hoy = date.today()
    anterior = (hoy.year - 1, 12) if hoy.month == 1 else (hoy.year, hoy.month - 1)
    # periodo de consulta: el último que se calcula (mes anterior) en su año; en otros años, diciembre
    mes = anterior[1] if anio == anterior[0] else 12
    return _consulta(db, f"""
        SELECT ce.id, ce.codcentro, ce.{col} AS id_indicador, ce.anio, ce.aplica,
               ce.est_01, ce.est_02, ce.est_03, ce.est_04, ce.est_05, ce.est_06,
               ce.est_07, ce.est_08, ce.est_09, ce.est_10, ce.est_11, ce.est_12, ce.acept, ce.sustento,
               i.indicador, c.centro, c.red, :mes AS mes_consulta,
               CASE WHEN i.sentido IN ('MENOR', 'BANDA')
                    THEN CASE t.tipo WHEN 'ABS' THEN e.est + t.tol ELSE e.est * (1 + t.tol) END
                    ELSE CASE t.tipo WHEN 'ABS' THEN e.est - t.tol ELSE e.est * (1 - t.tol) END END AS acept_defecto
        FROM {name_server}.tmi_centro_estandar ce
        LEFT JOIN {name_server}.tmi_indicador i ON i.id = ce.{col}
        OUTER APPLY (SELECT TOP 1 b.centro, b.red FROM {name_server}.vw_tmi_centro_base b
                     WHERE CAST(b.codcentro AS VARCHAR(50)) = LTRIM(RTRIM(ce.codcentro))) c
        CROSS APPLY (SELECT NULLIF(CASE :mes WHEN 1 THEN ce.est_01 WHEN 2 THEN ce.est_02 WHEN 3 THEN ce.est_03
                                             WHEN 4 THEN ce.est_04 WHEN 5 THEN ce.est_05 WHEN 6 THEN ce.est_06
                                             WHEN 7 THEN ce.est_07 WHEN 8 THEN ce.est_08 WHEN 9 THEN ce.est_09
                                             WHEN 10 THEN ce.est_10 WHEN 11 THEN ce.est_11 WHEN 12 THEN ce.est_12 END, 0) AS est) e
        OUTER APPLY (SELECT TOP 1 x.tipo_tolerancia AS tipo, x.tolerancia AS tol
                     FROM (SELECT tipo_tolerancia, tolerancia, 1 AS p FROM {name_server}.tmi_indicador_tolerancia
                           WHERE id_indicador = i.id AND anio = :anio AND mes = :mes
                           UNION ALL
                           SELECT tipo_tolerancia, tolerancia, 2 FROM {name_server}.tmi_indicador_tolerancia
                           WHERE id_indicador = i.id AND anio = :anio AND mes = 0
                           UNION ALL
                           SELECT i.tipo_tolerancia, i.tolerancia, 3) x
                     ORDER BY x.p) t
        WHERE ce.anio = :anio
        ORDER BY ce.{col}, ce.codcentro""", {"anio": anio, "mes": mes})

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
    """Calcula los indicadores del periodo (AAAAMM) en tmi_resultado: la fórmula de cada indicador sobre TOTALIZADO3."""
    try:
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
