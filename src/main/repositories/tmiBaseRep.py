"""Utilidades comunes de los repositorios del TMI: nombre de la base, columnas que cambian según la versión
de las tablas y alta, edición y baja genéricas de las tablas de mantenimiento."""

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core.tmiConfig import TMI_DB, TMI_DIM

name_server = f"{TMI_DB}.dbo"


MESES = [f"{m:02d}" for m in range(1, 13)]


def _tiene_columna(db: Session, tabla: str, columna: str) -> bool:
    return db.execute(text("SELECT COL_LENGTH(:t, :c)"), {"t": f"{name_server}.{tabla}", "c": columna}).scalar() is not None


def _existe_tabla(db: Session, tabla: str) -> bool:
    return db.execute(text("SELECT OBJECT_ID(:t)"), {"t": f"{name_server}.{tabla}"}).scalar() is not None


def _col_indicador(db: Session, tabla: str) -> str:
    return "id_indicador" if _tiene_columna(db, tabla, "id_indicador") else "id_estandar"


def _formato_largo(db: Session, tabla: str) -> bool:
    return _tiene_columna(db, tabla, "mes") and not _tiene_columna(db, tabla, "est_01")


def _indicador_join(db: Session, alias_col: str) -> tuple:
    """(JOIN del maestro de indicadores, expresión del 'tipo' = sección del reporte, orden)."""
    if _existe_tabla(db, "tmi_indicador"):
        return (f"JOIN {name_server}.tmi_indicador i ON i.id = {alias_col} "
                f"LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = i.grupo",
                "ISNULL(LTRIM(RTRIM(g.desctipgrupo)), '')", "i.orden, i.id")
    return f"JOIN {name_server}.tmi_estandar i ON i.id = {alias_col}", "ISNULL(i.tipo, '')", "i.id"


def _params(dto) -> dict:
    return dto.model_dump() if hasattr(dto, "model_dump") else dto.dict()


def _id_indicador(params: dict) -> int:
    valor = params.get("id_indicador") if params.get("id_indicador") is not None else params.get("id_estandar")
    if valor is None:
        raise HTTPException(status_code=400, detail="Falta el indicador (id_indicador).")
    return valor


### Mantenimiento (frontend). Tablas y columnas fijas: nunca vienen del usuario.
TABLAS = {
    "tmi_variable": ["nombre", "descripcion", "agregacion", "total_anual", "activo"],
    "tmi_variable_logica": ["id_variable", "tipgrupo", "actividad", "servicio", "condicion_hoja",
                            "periodo_desde", "periodo_hasta", "activo"],
    "tmi_indicador": ["grupo", "indicador", "codigo", "nombre_hoja", "titulo_hoja", "orden", "tipo_calculo",
                      "sin_datos_anio", "base_estandar", "sentido", "tipo_tolerancia", "tolerancia", "tolerancia_menos", "decimales",
                      "cero_es_logro", "mostrar_no_aplica", "activo", "formato", "si_variable_nula", "si_division_cero"],
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
        # Las tablas tienen triggers de historial: SQL Server exige OUTPUT ... INTO (error 334).
        # NOCOUNT evita que los conteos del INSERT/trigger tapen el resultado del SELECT final.
        result = db.execute(text(f"""
            SET NOCOUNT ON;
            DECLARE @ids TABLE (id BIGINT);
            INSERT INTO {name_server}.{tabla} ({', '.join(_columna(db, tabla, c) for c in columnas)}{extra_cols})
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
