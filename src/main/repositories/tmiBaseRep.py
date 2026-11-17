"""Utilidades comunes de los repositorios del TMI: nombre de la base, columnas que cambian según la versión
de las tablas y alta, edición y baja genéricas de las tablas de mantenimiento."""

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core import tmiFormula
from src.main.core.tmiConfig import TMI_DB, TMI_DIM

name_server = f"{TMI_DB}.dbo"


MESES = [f"{m:02d}" for m in range(1, 13)]


def _acept_del_anio(anio: str, ind: str = "i") -> str:
    """OUTER APPLY ... a: fila de tmi_indicador_acept del indicador para el año (anio = expresión SQL). Si ese año no
    tiene fila, la del año más cercano (antes el anterior) para tomar su fijo; los meses (acept_MM) solo valen si
    a.anio = anio. Sin ninguna fila, a queda vacío (sin % Acept)."""
    return f"""OUTER APPLY (SELECT TOP 1 x.* FROM {name_server}.tmi_indicador_acept x
                     WHERE x.id_indicador = {ind}.id
                     ORDER BY CASE WHEN x.anio = {anio} THEN 0 WHEN x.anio < {anio} THEN 1 ELSE 2 END,
                              ABS(x.anio - {anio})) a"""


_QUITAR_TABLAS_FORMULA = """IF OBJECT_ID('tempdb..#termino') IS NOT NULL DROP TABLE #termino;
IF OBJECT_ID('tempdb..#formula') IS NOT NULL DROP TABLE #formula;"""


def crear_tablas_formula(db: Session) -> None:
    """Lee la fórmula de cada indicador activo ([tipgrupo;actividad#servicio], src/main/core/tmiFormula.py) y deja en la
    conexión de db las tablas temporales que usan usp_tmi_calcular y usp_tmi_validar_config:
      #formula (id_indicador, formula_sql, formula_plantilla): la expresión SQL sobre los términos (T1 / T2) y la
               plantilla del desarrollo ([T1] / [T2]).
      #termino (id_indicador, codigo, tipgrupo, actividad, servicio, mediana, periodo_mediana, condicion, texto): una fila
               por término y servicio (servicio NULL = todos; mediana = mediana en el mes; periodo_mediana = mediana del
               periodo en el acumulado; condicion = DIM_HOJA.condicion de la tipohoja, NULL = todas).
    Un indicador cuya fórmula no se puede leer no entra (la validación lo informa). Se quitan con quitar_tablas_formula."""
    cur = db.connection().connection.cursor()
    try:
        cur.execute(_QUITAR_TABLAS_FORMULA + """
            CREATE TABLE #formula (id_indicador INT PRIMARY KEY, formula_sql NVARCHAR(MAX) NOT NULL,
                                   formula_plantilla NVARCHAR(4000) NOT NULL);
            CREATE TABLE #termino (id_indicador INT NOT NULL, codigo VARCHAR(5) NOT NULL, tipgrupo INT NOT NULL,
                                   actividad INT NOT NULL, servicio INT NULL, mediana BIT NOT NULL,
                                   periodo_mediana BIT NOT NULL, condicion VARCHAR(20) NULL,
                                   texto VARCHAR(400) NOT NULL);""")
        indicadores = cur.execute(f"""SELECT id, formula, si_variable_nula, si_division_cero FROM {name_server}.tmi_indicador
                                      WHERE activo = 1 AND NULLIF(LTRIM(formula), '') IS NOT NULL""").fetchall()
        formulas, terminos = [], []
        for id_ind, texto, si_variable_nula, si_division_cero in indicadores:
            try:
                f = tmiFormula.analizar(texto, si_variable_nula or "CERO", si_division_cero or "NA")
            except tmiFormula.ErrorFormula:
                continue
            formulas.append((id_ind, f.sql, tmiFormula.plantilla(f)))
            terminos += [(id_ind, t["codigo"], t["tipgrupo"], t["actividad"], t["servicio"], 1 if t["mediana"] else 0,
                          1 if t["periodo_mediana"] else 0, t["condicion"], t["texto"])
                         for t in tmiFormula.filas_termino(f)]
        if formulas:
            cur.executemany("INSERT INTO #formula (id_indicador, formula_sql, formula_plantilla) VALUES (?, ?, ?)", formulas)
        if terminos:
            cur.executemany("""INSERT INTO #termino (id_indicador, codigo, tipgrupo, actividad, servicio, mediana,
                                                        periodo_mediana, condicion, texto)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", terminos)
    finally:
        cur.close()


def quitar_tablas_formula(db: Session) -> None:
    try:
        db.connection().connection.cursor().execute(_QUITAR_TABLAS_FORMULA).close()
    except Exception:
        pass


def _indicador_join(alias_col: str) -> tuple:
    """(JOIN del maestro de indicadores, expresión del 'tipo' = sección del reporte, orden)."""
    return (f"JOIN {name_server}.tmi_indicador i ON i.id = {alias_col} "
            f"LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = i.grupo",
            "ISNULL(LTRIM(RTRIM(g.desctipgrupo)), '')", "i.orden, i.id")


def _params(dto) -> dict:
    return dto.model_dump() if hasattr(dto, "model_dump") else dto.dict()


### Mantenimiento (frontend). Tablas y columnas fijas: nunca vienen del usuario.
TABLAS = {
    "tmi_variable": ["nombre", "descripcion", "agregacion", "total_anual", "activo"],
    "tmi_variable_logica": ["id_variable", "tipgrupo", "actividad", "servicio", "condicion_hoja",
                            "activo"],
    "tmi_indicador": ["grupo", "indicador", "codigo", "nombre_hoja", "titulo_hoja", "orden", "tipo_calculo",
                      "sin_datos_anio", "base_estandar", "sentido", "decimales",
                      "cero_es_logro", "mostrar_no_aplica", "activo", "formato", "si_variable_nula", "si_division_cero"],
    "tmi_variable_componente": ["id_variable", "id_variable_componente", "activo"],
    "tmi_tipo_estandar": ["codigo", "descripcion", "orden", "activo"],
    "tmi_estandar": ["tipo_estandar", "orden", "fuente", "clave", "descripcion", "prioridad", "activo"],
    "tmi_estandar_centro": ["codcentro", "id_indicador", "anio", "aplica", "est_fijo", "est_01", "est_02", "est_03", "est_04",
                            "est_05", "est_06", "est_07", "est_08", "est_09", "est_10", "est_11", "est_12",
                            "sustento"],
}


# Tablas con columnas de auditoría (usuario y fecha)
CON_AUDITORIA = {"tmi_variable", "tmi_indicador"}


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
        # Las tablas tienen triggers de historial: SQL Server exige OUTPUT ... INTO (error 334).
        # NOCOUNT evita que los conteos del INSERT/trigger tapen el resultado del SELECT final.
        result = db.execute(text(f"""
            SET NOCOUNT ON;
            DECLARE @ids TABLE (id BIGINT);
            INSERT INTO {name_server}.{tabla} ({', '.join(columnas)}{extra_cols})
            OUTPUT INSERTED.id INTO @ids
            VALUES ({', '.join(':' + c for c in columnas)}{extra_vals});
            SELECT id FROM @ids;
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
    sets = ", ".join(f"{c} = :{c}" for c in columnas)
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
