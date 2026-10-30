from datetime import datetime
from sqlalchemy.orm import Session
from src.main.core.tmiConfig import TMI_DB
from src.main.dtos.tmiDto import (
    tmiCentroDto,
    tmiEstandarDto,
    tmiEstandarTipoDto,
    tmiEstandarNivelDto,
    tmiEstandarCategoriaDto,
    tmiExclusionCentroEstandarDto,
)
from fastapi import HTTPException
from sqlalchemy import text

###
name_server = f"{TMI_DB}.dbo"

### tmi_centro 
def queryCentrosTMI(db: Session):
    try:
        query = f"""
        IF OBJECT_ID('{name_server}.vw_tmi_centro_base') IS NOT NULL
            SELECT id_centro AS id, red, CAST(orden AS VARCHAR(20)) AS orden, CAST(orden_tipo AS VARCHAR(20)) AS orden_tipo,
                   CAST(codcentro AS VARCHAR(50)) AS codcentro, centro, categoria, nivel, tipo,
                   f01 AS flag, ISNULL(anio, YEAR(GETDATE())) AS anio,
                   f01 AS flag_01, f02 AS flag_02, f03 AS flag_03, f04 AS flag_04, f05 AS flag_05, f06 AS flag_06,
                   f07 AS flag_07, f08 AS flag_08, f09 AS flag_09, f10 AS flag_10, f11 AS flag_11, f12 AS flag_12
            FROM {name_server}.vw_tmi_centro_base b
            ORDER BY b.orden, b.orden_tipo, b.codcentro
        ELSE
            SELECT * FROM {name_server}.tmi_centro
        """
        result = db.execute(text(query))
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertCentrosTMI(db: Session, centro:tmiCentroDto):
    try:
        query = f"""
        IF COL_LENGTH('{name_server}.tmi_centro', 'flag_01') IS NOT NULL
            INSERT INTO {name_server}.tmi_centro
            (red,orden,orden_tipo,codcentro,centro,categoria,nivel,tipo,anio, flag_01, flag_02, flag_03, flag_04, flag_05, flag_06, flag_07, flag_08, flag_09, flag_10, flag_11, flag_12)
            VALUES 
            (:red,:orden,:orden_tipo,:codcentro,:centro,:categoria,:nivel,:tipo,ISNULL(:anio, YEAR(GETDATE())), ISNULL(:flag_01, :flag), ISNULL(:flag_02, :flag), ISNULL(:flag_03, :flag), ISNULL(:flag_04, :flag), ISNULL(:flag_05, :flag), ISNULL(:flag_06, :flag), ISNULL(:flag_07, :flag), ISNULL(:flag_08, :flag), ISNULL(:flag_09, :flag), ISNULL(:flag_10, :flag), ISNULL(:flag_11, :flag), ISNULL(:flag_12, :flag))
        ELSE
            INSERT INTO {name_server}.tmi_centro
            (red,orden,orden_tipo,codcentro,centro,categoria,nivel,tipo,flag)
            VALUES (:red,:orden,:orden_tipo,:codcentro,:centro,:categoria,:nivel,:tipo,ISNULL(:flag, 1))
        """
        params = centro.model_dump() if hasattr(centro, "model_dump") else centro.dict()
        for k in ("anio", "flag", "flag_01", "flag_02", "flag_03", "flag_04", "flag_05", "flag_06", "flag_07", "flag_08", "flag_09", "flag_10", "flag_11", "flag_12"):
            params.setdefault(k, None)
        result = db.execute(text(query), params)
        db.commit()
        return {"message": "Centros TMI insertados correctamente", "rows_inserted": result.rowcount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateCentrosTMI(db: Session, dto:tmiCentroDto):
    try:
        query = f"""
        IF COL_LENGTH('{name_server}.tmi_centro', 'flag_01') IS NOT NULL
            UPDATE {name_server}.tmi_centro
                SET red = :red
                ,orden = :orden
                ,orden_tipo = :orden_tipo
                ,codcentro = :codcentro
                ,centro = :centro
                ,categoria = :categoria
                ,nivel = :nivel
                ,tipo = :tipo
                ,anio = ISNULL(:anio, anio)
                ,flag_01 = COALESCE(:flag_01, :flag, flag_01)
                ,flag_02 = COALESCE(:flag_02, :flag, flag_02)
                ,flag_03 = COALESCE(:flag_03, :flag, flag_03)
                ,flag_04 = COALESCE(:flag_04, :flag, flag_04)
                ,flag_05 = COALESCE(:flag_05, :flag, flag_05)
                ,flag_06 = COALESCE(:flag_06, :flag, flag_06)
                ,flag_07 = COALESCE(:flag_07, :flag, flag_07)
                ,flag_08 = COALESCE(:flag_08, :flag, flag_08)
                ,flag_09 = COALESCE(:flag_09, :flag, flag_09)
                ,flag_10 = COALESCE(:flag_10, :flag, flag_10)
                ,flag_11 = COALESCE(:flag_11, :flag, flag_11)
                ,flag_12 = COALESCE(:flag_12, :flag, flag_12)
            WHERE (:id IS NOT NULL AND id = :id) OR (:id IS NULL AND codcentro = :codcentro)
        ELSE
            UPDATE {name_server}.tmi_centro
                SET red = :red
                ,orden = :orden
                ,orden_tipo = :orden_tipo
                ,codcentro = :codcentro
                ,centro = :centro
                ,categoria = :categoria
                ,nivel = :nivel
                ,tipo = :tipo
                ,flag = COALESCE(:flag, :flag_01, flag)
            WHERE (:id IS NOT NULL AND id = :id) OR (:id IS NULL AND codcentro = :codcentro)
        """
        params = dto.model_dump() if hasattr(dto, "model_dump") else dto.dict()
        for k in ("anio", "flag", "flag_01", "flag_02", "flag_03", "flag_04", "flag_05", "flag_06", "flag_07", "flag_08", "flag_09", "flag_10", "flag_11", "flag_12"):
            params.setdefault(k, None)
        result = db.execute(text(query), params)
        db.commit()
        return {"message": "Centro TMI actualizado correctamente", "rows_affected": result.rowcount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryDeleteCentrosTMI(db: Session, id:int):
    try:
        query = f"""
        DELETE FROM {name_server}.tmi_centro
        WHERE id = :id
        """
        result = db.execute(text(query), {"id": id})
        db.commit()
        return {"message": "Centro TMI eliminado correctamente", "rows_deleted": result.rowcount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
                f"LEFT JOIN {name_server}.tmi_grupo g ON g.id = i.grupo",
                "ISNULL(g.descripcion, '')", "i.orden, i.id")
    return f"JOIN {name_server}.tmi_estandar i ON i.id = {alias_col}", "ISNULL(i.tipo, '')", "i.id"


def _params(dto) -> dict:
    return dto.model_dump() if hasattr(dto, "model_dump") else dto.dict()


def _id_indicador(params: dict) -> int:
    valor = params.get("id_indicador") if params.get("id_indicador") is not None else params.get("id_estandar")
    if valor is None:
        raise HTTPException(status_code=400, detail="Falta el indicador (id_indicador).")
    return valor


def queryEstandar(db: Session ):
    try:
        query = f"""
        IF OBJECT_ID('{name_server}.tmi_indicador') IS NOT NULL
            SELECT i.id, ISNULL(g.descripcion, '') AS tipo, i.indicador, i.fecha_creacion, i.fecha_modificacion
            FROM {name_server}.tmi_indicador i
            LEFT JOIN {name_server}.tmi_grupo g ON g.id = i.grupo
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
            # 'tipo' es la sección del reporte (tmi_grupo.descripcion)
            query = f"""
            INSERT INTO {name_server}.tmi_indicador (grupo, indicador, fecha_creacion, fecha_modificacion)
            VALUES ((SELECT TOP 1 id FROM {name_server}.tmi_grupo WHERE LTRIM(RTRIM(descripcion)) = LTRIM(RTRIM(:tipo))),
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
                SET grupo = COALESCE((SELECT TOP 1 id FROM {name_server}.tmi_grupo
                                      WHERE LTRIM(RTRIM(descripcion)) = LTRIM(RTRIM(:tipo))), grupo)
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
               ISNULL(g.descripcion, '') AS tipo,
               i.indicador,
               s.clave AS {clave},
               s.anio,
               s.m01 AS est_fijo,
               s.m01 AS est_01, s.m02 AS est_02, s.m03 AS est_03, s.m04 AS est_04, s.m05 AS est_05, s.m06 AS est_06,
               s.m07 AS est_07, s.m08 AS est_08, s.m09 AS est_09, s.m10 AS est_10, s.m11 AS est_11, s.m12 AS est_12
        FROM {name_server}.vw_tmi_std s
        JOIN {name_server}.tmi_indicador i ON i.id = s.id_estandar
        LEFT JOIN {name_server}.tmi_grupo g ON g.id = i.grupo
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
    SELECT @tipo = ISNULL(g.descripcion, ''), @ind = i.indicador
    FROM {name_server}.tmi_indicador i
    LEFT JOIN {name_server}.tmi_grupo g ON g.id = i.grupo
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


### tmi_exclusion_centro_indicador (exclusión de centro por indicador; id_indicador NULL = todos los indicadores del centro)
def queryExclusionCentroEstandar(db: Session, anio: int):
    try:
        tabla = "tmi_exclusion_centro_indicador"
        col = _col_indicador(db, tabla)
        pre = "excl_" if _tiene_columna(db, tabla, "excl_01") else "estandar_"
        cod = "COALESCE(CAST(cen.codcentro AS VARCHAR(50)), exc.codcentro)" if _tiene_columna(db, tabla, "codcentro") else "cen.codcentro"
        motivo = "exc.motivo" if _tiene_columna(db, tabla, "motivo") else "CAST(NULL AS VARCHAR(300))"
        resultado = "ISNULL(exc.resultado, 'NA')" if _tiene_columna(db, tabla, "resultado") else "'NA'"
        join, tipo, orden = _indicador_join(db, f"exc.{col}")
        join = join.replace("JOIN ", "LEFT JOIN ", 1) if join.startswith("JOIN ") else join
        meses = ", ".join(f"exc.{pre}{m} AS excl_{m}" for m in MESES)
        query = f"""
        SELECT exc.id, exc.id_centro, {cod} AS codcentro, cen.centro,
               {tipo} AS tipo, ISNULL(i.indicador, 'Todos los indicadores') AS indicador,
               exc.{col} AS id_indicador, exc.{col} AS id_estandar, exc.anio, {meses}, {motivo} AS motivo, {resultado} AS resultado
        FROM {name_server}.tmi_exclusion_centro_indicador exc
        {join}
        LEFT JOIN {name_server}.vw_tmi_centro_base cen ON cen.id_centro = exc.id_centro
        WHERE exc.anio = :anio
        ORDER BY {cod}, {orden}
        """
        result = db.execute(text(query), {"anio": anio})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _params_exclusion(db: Session, dto) -> tuple:
    tabla = "tmi_exclusion_centro_indicador"
    params = _params(dto)
    params["id_indicador"] = params.get("id_indicador") if params.get("id_indicador") is not None else params.get("id_estandar")
    if params.get("id_centro") is None and not params.get("codcentro"):
        raise HTTPException(status_code=400, detail="Indique el centro (id_centro o codcentro).")
    if params.get("id_centro") is None:
        params["id_centro"] = db.execute(text(f"""
            SELECT MIN(id) FROM {name_server}.tmi_centro WHERE LTRIM(RTRIM(codcentro)) = LTRIM(RTRIM(:codcentro))"""),
            {"codcentro": params["codcentro"]}).scalar()
    col = _col_indicador(db, tabla)
    pre = "excl_" if _tiene_columna(db, tabla, "excl_01") else "estandar_"
    cols = {"id_centro": ":id_centro", col: ":id_indicador", "anio": ":anio"}
    cols.update({f"{pre}{m}": f"ISNULL(:excl_{m}, 0)" for m in MESES})
    if _tiene_columna(db, tabla, "codcentro"):
        cols["codcentro"] = f"COALESCE(:codcentro, (SELECT codcentro FROM {name_server}.tmi_centro WHERE id = :id_centro))"
    if _tiene_columna(db, tabla, "motivo"):
        cols["motivo"] = ":motivo"
    if _tiene_columna(db, tabla, "resultado"):
        cols["resultado"] = "ISNULL(:resultado, 'NA')"
    for k in ("codcentro", "motivo", "id", "resultado"):
        params.setdefault(k, None)
    return params, cols, col


def queryInsertExclusionCentroEstandar(db: Session, dto:tmiExclusionCentroEstandarDto):
    try:
        params, cols, _ = _params_exclusion(db, dto)
        query = f"""
        INSERT INTO {name_server}.tmi_exclusion_centro_indicador ({', '.join(cols)})
        VALUES ({', '.join(cols.values())})
        """
        result = db.execute(text(query), params)
        db.commit()
        return {"message": "Exclusión de centro por indicador guardada correctamente", "rows_inserted": result.rowcount}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateExclusionCentroEstandar(db: Session, dto: tmiExclusionCentroEstandarDto):
    try:
        params, cols, col = _params_exclusion(db, dto)
        sets = ", ".join(f"{c} = {v}" for c, v in cols.items())
        query = f"""
        UPDATE {name_server}.tmi_exclusion_centro_indicador SET {sets}
        WHERE (:id IS NOT NULL AND id = :id)
           OR (:id IS NULL AND id_centro = :id_centro AND anio = :anio
               AND ({col} = :id_indicador OR ({col} IS NULL AND :id_indicador IS NULL)))
        """
        result = db.execute(text(query), params)
        db.commit()
        return {"message": "Exclusión de centro por indicador actualizada correctamente", "rows_affected": result.rowcount}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


#### insertar centros y estándares
def queryCreateFila(db: Session, tabla: str, params: dict):
    try:
        columnas = COLUMNAS_TABLA[tabla]
        query = f"""
        INSERT INTO {name_server}.{tabla} ({", ".join(columnas)})
        OUTPUT INSERTED.id
        VALUES ({", ".join(":" + c for c in columnas)})
        """
        nuevo_id = db.execute(text(query), {c: params.get(c) for c in columnas}).scalar()
        db.commit()
        return {"message": "Fila agregada correctamente", "id": nuevo_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def queryDeleteFila(db: Session, tabla: str, id: int):
    try:
        query = f"DELETE FROM {name_server}.{tabla} WHERE id = :id"
        result = db.execute(text(query), {"id": id})
        db.commit()
        return {"message": "Fila eliminada correctamente", "rows_affected": result.rowcount}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



### consulta de vistas
##CE_Concent - Concentracion de Consultas -
def queryCE_ConcentRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Consulta Externa - Consultas'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Consulta Externa - Consultantes al Establecimiento'
),
CEN AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable IN ('Consulta Externa - Consultas', 'Consulta Externa - Consultantes al Establecimiento')
)
SELECT DISTINCT 
    D.id AS ORDEN, D.red AS Red, D.codcentro, D.centro AS Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar* 1.1  AS [% Acept],

    CASE 
        WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
        ) > 0
        THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
        ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
        )
        ELSE 0 
    END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN A.[202601] = 0 OR B.[202601] = 0 THEN 0 ELSE (A.[202601] * 1.00) / B.[202601] END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN A.[202602] = 0 OR B.[202602] = 0 THEN 0 ELSE ((A.[202601] + A.[202602]) * 1.00) / (B.[202601] + B.[202602]) END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN A.[202603] = 0 OR B.[202603] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603]) * 1.00) / (B.[202601] + B.[202602] + B.[202603]) END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN A.[202604] = 0 OR B.[202604] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604]) END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN A.[202605] = 0 OR B.[202605] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605]) END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN A.[202606] = 0 OR B.[202606] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606]) END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN A.[202607] = 0 OR B.[202607] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607]) END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN A.[202608] = 0 OR B.[202608] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608]) END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN A.[202609] = 0 OR B.[202609] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609]) END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN A.[202610] = 0 OR B.[202610] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610]) END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN A.[202611] = 0 OR B.[202611] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611]) END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN A.[202612] = 0 OR B.[202612] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611] + A.[202612]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611] + B.[202612]) END ELSE 0 END AS [202612]
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (        
        SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_nivel.est_01
            WHEN 2  THEN est_nivel.est_02
            WHEN 3  THEN est_nivel.est_03
            WHEN 4  THEN est_nivel.est_04
            WHEN 5  THEN est_nivel.est_05
            WHEN 6  THEN est_nivel.est_06
            WHEN 7  THEN est_nivel.est_07
            WHEN 8  THEN est_nivel.est_08
            WHEN 9  THEN est_nivel.est_09
            WHEN 10 THEN est_nivel.est_10
            WHEN 11 THEN est_nivel.est_11
            WHEN 12 THEN est_nivel.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_nivel est_nivel
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_nivel.id_estandar 
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_nivel.nivel_centro = cen.nivel
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Concentracion de Consultas' AND est_nivel.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
ORDER BY ORDEN asc;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

##CE_GCHProg - Grado de Cumplimiento de Horas Programadas
def queryCE_GCHProgRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;      
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Consulta Externa - Horas Médicas Efectivas'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Consulta Externa - Horas Médicas Programadas'
),
CEN AS (
     SELECT DISTINCT Red, codcentro, Centro
     FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
     WHERE     variable IN ('Consulta Externa - Horas Médicas Efectivas')
     UNION
     SELECT DISTINCT Red, codcentro, Centro
     FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
     WHERE     variable IN ('Consulta Externa - Horas Médicas Programadas')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.95 AS [% Acept],
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
        SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar 
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Grado de Cumplimiento de Horas Programadas' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## CE_Recetas - Promedio de Recetas por Consultas
def queryCE_RecetasRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;          
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Actividades Intermedias - Recetas Despachadas de C. E'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Consulta Externa - Consultas'
),
CEN AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     variable IN ('Actividades Intermedias - Recetas Despachadas de C. E')
    UNION
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     variable IN ('Consulta Externa - Consultas')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 1.1 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL((ISNULL(A.[202601],0) * 1.00) / NULLIF(ISNULL(B.[202601],0),0),0) ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL((ISNULL(A.[202602],0) * 1.00) / NULLIF(ISNULL(B.[202602],0),0),0) ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL((ISNULL(A.[202603],0) * 1.00) / NULLIF(ISNULL(B.[202603],0),0),0) ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL((ISNULL(A.[202604],0) * 1.00) / NULLIF(ISNULL(B.[202604],0),0),0) ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL((ISNULL(A.[202605],0) * 1.00) / NULLIF(ISNULL(B.[202605],0),0),0) ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL((ISNULL(A.[202606],0) * 1.00) / NULLIF(ISNULL(B.[202606],0),0),0) ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL((ISNULL(A.[202607],0) * 1.00) / NULLIF(ISNULL(B.[202607],0),0),0) ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL((ISNULL(A.[202608],0) * 1.00) / NULLIF(ISNULL(B.[202608],0),0),0) ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL((ISNULL(A.[202609],0) * 1.00) / NULLIF(ISNULL(B.[202609],0),0),0) ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL((ISNULL(A.[202610],0) * 1.00) / NULLIF(ISNULL(B.[202610],0),0),0) ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL((ISNULL(A.[202611],0) * 1.00) / NULLIF(ISNULL(B.[202611],0),0),0) ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL((ISNULL(A.[202612],0) * 1.00) / NULLIF(ISNULL(B.[202612],0),0),0) ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar 
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Promedio de Recetas por Consultas' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## CE_RHrMedico - Rendimiento Hora Medico
def queryCE_RHrMedicoRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;          
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Consulta Externa - Consultas'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Consulta Externa - Horas Médicas Efectivas'
),
CEN_NIVEL AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE variable IN ('Consulta Externa - Consultas', 'Consulta Externa - Horas Médicas Efectivas')
),
CEN_TIPO AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.9  AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN_NIVEL AS CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_nivel.est_01
            WHEN 2  THEN est_nivel.est_02
            WHEN 3  THEN est_nivel.est_03
            WHEN 4  THEN est_nivel.est_04
            WHEN 5  THEN est_nivel.est_05
            WHEN 6  THEN est_nivel.est_06
            WHEN 7  THEN est_nivel.est_07
            WHEN 8  THEN est_nivel.est_08
            WHEN 9  THEN est_nivel.est_09
            WHEN 10 THEN est_nivel.est_10
            WHEN 11 THEN est_nivel.est_11
            WHEN 12 THEN est_nivel.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_nivel est_nivel
    JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_nivel.id_estandar
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_nivel.nivel_centro = cen.nivel
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Rendimiento Hora Medico' AND est_nivel.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo NOT IN ('CNSR','IPO','INCOR')

UNION ALL

SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar *0.9 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / 
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
        
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

    FROM CEN_TIPO AS CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Rendimiento Hora Medico' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo IN ('CNSR','IPO','INCOR')
ORDER BY ORDEN;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Em_PrioI_II - % Prioridad I y II con respecto al Total de Emergencias
def queryEm_PrioI_IIRep(db: Session, periodo:str): 
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
               SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
               SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
               FROM        pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
               WHERE      (Variable IN ('Emergencia - Prioridad I', 'Emergencia - Prioridad II'))
               GROUP BY Red, Centro, nivel, codcentro, Año
),
X AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Emergencia - Total de Atenciones'
),
CEN AS (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Emergencia - Prioridad I', 'Emergencia - Prioridad II', 'Emergencia - Total de Atenciones'))
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.9 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(X.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(X.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN X.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / X.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN X.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / X.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN X.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / X.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN X.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / X.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN X.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / X.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN X.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / X.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN X.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / X.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN X.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / X.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN X.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / X.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN X.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / X.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN X.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / X.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN X.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / X.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN X ON CEN.codcentro = X.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = '% Prioridad I y II con respecto al Total de Emergencias' AND est_tipo.anio = @Anio
 ) AS D ON CEN.codcentro = D.codcentro;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Em_PrioIV_V - % Prioridad IV y V con respecto al Total de Emergencias
def queryEm_PrioIV_VRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;           
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
            SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
            SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
            SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
            FROM       pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
            WHERE      (Variable IN ('Emergencia - Prioridad IV', 'Emergencia - Prioridad V'))
            GROUP BY Red, Centro, nivel, codcentro, Año),
X AS (
       SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
       [202601],[202602],[202603],[202604],[202605],[202606],
       [202607],[202608],[202609],[202610],[202611],[202612], Variable
       FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
       WHERE Variable = 'Emergencia - Total de Atenciones'
),
CEN AS (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Emergencia - Prioridad IV', 'Emergencia - Prioridad V', 'Emergencia - Total de Atenciones'))
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar* 1.2 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(X.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(X.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN X.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / X.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN X.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / X.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN X.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / X.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN X.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / X.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN X.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / X.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN X.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / X.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN X.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / X.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN X.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / X.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN X.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / X.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN X.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / X.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN X.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / X.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN X.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / X.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN X ON CEN.codcentro = X.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = '% Prioridad IV y V con respecto al Total de Emergencias' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo IN ('H.N.', 'H.IV', 'H.III', 'H.II', 'H.I');
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## H_Estancias - Promedio Dia Estancia
def queryH_EstanciasRep(db: Session, periodo:str):
    try:    
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;          
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion - Estancias'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion - Egresos'
),
CEN AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     variable IN ('Hospitalizacion - Estancias')
    UNION
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     variable IN ('Hospitalizacion - Egresos')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 1.2 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Promedio Dia Estancia' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## H_ISust - Intervalo de Sustitución
def queryH_ISustRep(db: Session, periodo:str):
    try:    
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion - Días Cama Disponible'
),
B AS (
     SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
            [202601],[202602],[202603],[202604],[202605],[202606],
            [202607],[202608],[202609],[202610],[202611],[202612], Variable
     FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
     WHERE Variable = 'Hospitalizacion - Pacientes Días'
),
x AS (
     SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
     [202609], [202610], [202611], [202612], Variable
     FROM   pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
     WHERE  Variable IN ('Hospitalizacion - Egresos')
),
CEN AS (
     SELECT DISTINCT Red, codcentro, Centro
     FROM   pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
     WHERE  variable IN ('Hospitalizacion - Días Cama Disponible', 'Hospitalizacion - Pacientes Días', 'Hospitalizacion - Egresos')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 1.2 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 1 OR D.excl_01 IS NULL) THEN ISNULL(x.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 1 OR D.excl_02 IS NULL) THEN ISNULL(x.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 1 OR D.excl_03 IS NULL) THEN ISNULL(x.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 1 OR D.excl_04 IS NULL) THEN ISNULL(x.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 1 OR D.excl_05 IS NULL) THEN ISNULL(x.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 1 OR D.excl_06 IS NULL) THEN ISNULL(x.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 1 OR D.excl_07 IS NULL) THEN ISNULL(x.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 1 OR D.excl_08 IS NULL) THEN ISNULL(x.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 1 OR D.excl_09 IS NULL) THEN ISNULL(x.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 1 OR D.excl_10 IS NULL) THEN ISNULL(x.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 1 OR D.excl_11 IS NULL) THEN ISNULL(x.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 1 OR D.excl_12 IS NULL) THEN ISNULL(x.[202612],0) ELSE 0 END
         ) <> 0
    THEN ((
            CASE WHEN @Mes>=1  AND (D.excl_01 = 1 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 1 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 1 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 1 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 1 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 1 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 1 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 1 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 1 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 1 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 1 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 1 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) - (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 1 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 1 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 1 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 1 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 1 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 1 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 1 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 1 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 1 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 1 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 1 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 1 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 1 OR D.excl_01 IS NULL) THEN ISNULL(x.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 1 OR D.excl_02 IS NULL) THEN ISNULL(x.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 1 OR D.excl_03 IS NULL) THEN ISNULL(x.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 1 OR D.excl_04 IS NULL) THEN ISNULL(x.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 1 OR D.excl_05 IS NULL) THEN ISNULL(x.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 1 OR D.excl_06 IS NULL) THEN ISNULL(x.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 1 OR D.excl_07 IS NULL) THEN ISNULL(x.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 1 OR D.excl_08 IS NULL) THEN ISNULL(x.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 1 OR D.excl_09 IS NULL) THEN ISNULL(x.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 1 OR D.excl_10 IS NULL) THEN ISNULL(x.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 1 OR D.excl_11 IS NULL) THEN ISNULL(x.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 1 OR D.excl_12 IS NULL) THEN ISNULL(x.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 1 OR D.excl_01 IS NULL) THEN CASE WHEN x.[202601] <> 0 THEN ((isnull(A.[202601], 0) - isnull(B.[202601], 0)) * 1.00) / x.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 1 OR D.excl_02 IS NULL) THEN CASE WHEN x.[202602] <> 0 THEN ((isnull(A.[202602], 0) - isnull(B.[202602], 0)) * 1.00) / x.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 1 OR D.excl_03 IS NULL) THEN CASE WHEN x.[202603] <> 0 THEN ((isnull(A.[202603], 0) - isnull(B.[202603], 0)) * 1.00) / x.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 1 OR D.excl_04 IS NULL) THEN CASE WHEN x.[202604] <> 0 THEN ((isnull(A.[202604], 0) - isnull(B.[202604], 0)) * 1.00) / x.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 1 OR D.excl_05 IS NULL) THEN CASE WHEN x.[202605] <> 0 THEN ((isnull(A.[202605], 0) - isnull(B.[202605], 0)) * 1.00) / x.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 1 OR D.excl_06 IS NULL) THEN CASE WHEN x.[202606] <> 0 THEN ((isnull(A.[202606], 0) - isnull(B.[202606], 0)) * 1.00) / x.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 1 OR D.excl_07 IS NULL) THEN CASE WHEN x.[202607] <> 0 THEN ((isnull(A.[202607], 0) - isnull(B.[202607], 0)) * 1.00) / x.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 1 OR D.excl_08 IS NULL) THEN CASE WHEN x.[202608] <> 0 THEN ((isnull(A.[202608], 0) - isnull(B.[202608], 0)) * 1.00) / x.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 1 OR D.excl_09 IS NULL) THEN CASE WHEN x.[202609] <> 0 THEN ((isnull(A.[202609], 0) - isnull(B.[202609], 0)) * 1.00) / x.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 1 OR D.excl_10 IS NULL) THEN CASE WHEN x.[202610] <> 0 THEN ((isnull(A.[202610], 0) - isnull(B.[202610], 0)) * 1.00) / x.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 1 OR D.excl_11 IS NULL) THEN CASE WHEN x.[202611] <> 0 THEN ((isnull(A.[202611], 0) - isnull(B.[202611], 0)) * 1.00) / x.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 1 OR D.excl_12 IS NULL) THEN CASE WHEN x.[202612] <> 0 THEN ((isnull(A.[202612], 0) - isnull(B.[202612], 0)) * 1.00) / x.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN x ON CEN.codcentro = x.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Intervalo de Sustitución' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

##H_OCamas - Porcentaje de Ocupación de Cama
def queryH_OCamasRep(db: Session, periodo:str):
    try:    
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;           
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion - Pacientes Días'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion - Días Cama Disponible'
),
CEN AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     variable IN ('Hospitalizacion - Pacientes Días')
    UNION
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     variable IN ('Hospitalizacion - Días Cama Disponible')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.tipo AS TIPO, D.estandar AS Estandar,  D.estandar + 0.05 AS [% Acept], D.estandar - 0.05 AS [% Aceptmenos],
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Porcentaje de Ocupación de Cama' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## H_RCama -  Rendimiento Cama
def queryH_RCamaRep(db: Session, periodo:str):
    try:    
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;          
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion - Egresos'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion -  Camas Hospitalarias'
),
CEN AS (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Hospitalizacion - Egresos', 'Hospitalizacion -  Camas Hospitalarias')))
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.tipo AS TIPO, D.estandar AS Estandar, D.estandar * 0.8 AS [% Acept],
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00  / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Rendimiento Cama' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## H_TBMHosp - Tasa Neta de Mortalidad Hospitalaria
def queryH_TBMHospRep(db: Session, periodo:str):
    try:    
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); ;

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion - Defunciones después de 48 horas'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion - Egresos'
),
x AS (
      SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, 
             [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
             [202609], [202610], [202611], [202612], Variable
      FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
      WHERE Variable IN ('Hospitalizacion - Defunciones antes de 48 horas')),
CEN AS (
      SELECT DISTINCT Red, codcentro, Centro
      FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE variable IN ('Hospitalizacion - Defunciones después de 48 horas')
      UNION
      SELECT DISTINCT Red, codcentro, Centro
      FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE variable IN ('Hospitalizacion - Egresos')
      UNION
      SELECT DISTINCT Red, codcentro, Centro
      FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE variable IN ('Hospitalizacion - Defunciones antes de 48 horas')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.tipo AS TIPO, D.estandar AS Estandar, D.estandar * 1.1 AS [% Acept], 
    CASE WHEN  (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) - (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(x.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(x.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(x.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(x.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(x.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(x.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(x.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(x.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(x.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(x.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(x.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(x.[202612],0) ELSE 0 END
         )
         <> 0
    THEN ((
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN (ISNULL(A.[202601],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN (ISNULL(A.[202602],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN (ISNULL(A.[202603],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN (ISNULL(A.[202604],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN (ISNULL(A.[202605],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN (ISNULL(A.[202606],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN (ISNULL(A.[202607],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN (ISNULL(A.[202608],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN (ISNULL(A.[202609],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN (ISNULL(A.[202610],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN (ISNULL(A.[202611],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN (ISNULL(A.[202612],0))* 1.00 ELSE 0 END
         ) / ((
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) - (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(x.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(x.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(x.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(x.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(x.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(x.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(x.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(x.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(x.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(x.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(x.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(x.[202612],0) ELSE 0 END
         )))
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL)THEN CASE WHEN (isnull(B.[202601], 0) - isnull(x.[202601], 0)) <> 0 THEN ((isnull(A.[202601], 0)) * 1.00) / (isnull(B.[202601], 0) - isnull(x.[202601], 0)) ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL)THEN CASE WHEN (isnull(B.[202602], 0) - isnull(x.[202602], 0)) <> 0 THEN ((isnull(A.[202602], 0)) * 1.00) / (isnull(B.[202602], 0) - isnull(x.[202602], 0)) ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL)THEN CASE WHEN (isnull(B.[202603], 0) - isnull(x.[202603], 0)) <> 0 THEN ((isnull(A.[202603], 0)) * 1.00) / (isnull(B.[202603], 0) - isnull(x.[202603], 0)) ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL)THEN CASE WHEN (isnull(B.[202604], 0) - isnull(x.[202604], 0)) <> 0 THEN ((isnull(A.[202604], 0)) * 1.00) / (isnull(B.[202604], 0) - isnull(x.[202604], 0)) ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL)THEN CASE WHEN (isnull(B.[202605], 0) - isnull(x.[202605], 0)) <> 0 THEN ((isnull(A.[202605], 0)) * 1.00) / (isnull(B.[202605], 0) - isnull(x.[202605], 0)) ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL)THEN CASE WHEN (isnull(B.[202606], 0) - isnull(x.[202606], 0)) <> 0 THEN ((isnull(A.[202606], 0)) * 1.00) / (isnull(B.[202606], 0) - isnull(x.[202606], 0)) ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL)THEN CASE WHEN (isnull(B.[202607], 0) - isnull(x.[202607], 0)) <> 0 THEN ((isnull(A.[202607], 0)) * 1.00) / (isnull(B.[202607], 0) - isnull(x.[202607], 0)) ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL)THEN CASE WHEN (isnull(B.[202608], 0) - isnull(x.[202608], 0)) <> 0 THEN ((isnull(A.[202608], 0)) * 1.00) / (isnull(B.[202608], 0) - isnull(x.[202608], 0)) ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL)THEN CASE WHEN (isnull(B.[202609], 0) - isnull(x.[202609], 0)) <> 0 THEN ((isnull(A.[202609], 0)) * 1.00) / (isnull(B.[202609], 0) - isnull(x.[202609], 0)) ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL)THEN CASE WHEN (isnull(B.[202610], 0) - isnull(x.[202610], 0)) <> 0 THEN ((isnull(A.[202610], 0)) * 1.00) / (isnull(B.[202610], 0) - isnull(x.[202610], 0)) ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL)THEN CASE WHEN (isnull(B.[202611], 0) - isnull(x.[202611], 0)) <> 0 THEN ((isnull(A.[202611], 0)) * 1.00) / (isnull(B.[202611], 0) - isnull(x.[202611], 0)) ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL)THEN CASE WHEN (isnull(B.[202612], 0) - isnull(x.[202612], 0)) <> 0 THEN ((isnull(A.[202612], 0)) * 1.00) / (isnull(B.[202612], 0) - isnull(x.[202612], 0)) ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN x ON CEN.codcentro = x.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo 
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Tasa Neta de Mortalidad Hospitalaria' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## O_Concent - Concentración de Sesiones Odontológicas
def queryO_ConcentRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;          
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); ;

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Odontología - Sesiones Odontológicas'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Odontología - Consultantes de Odontología'
),
CEN AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     Variable IN ('Odontología - Sesiones Odontológicas', 'Odontología - Consultantes de Odontología')
)
SELECT DISTINCT 
    D.id AS ORDEN, D.red AS Red, D.codcentro, D.centro AS Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 1.1 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN A.[202601] <> 0 OR B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN A.[202602] <> 0 OR B.[202602] <> 0 THEN ((A.[202601] + A.[202602]) * 1.00) / (B.[202601] + B.[202602]) ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN A.[202603] <> 0 OR B.[202603] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603]) * 1.00) / (B.[202601] + B.[202602] + B.[202603]) ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN A.[202604] <> 0 OR B.[202604] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604]) ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN A.[202605] <> 0 OR B.[202605] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605]) ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN A.[202606] <> 0 OR B.[202606] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606]) ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN A.[202607] <> 0 OR B.[202607] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607]) ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN A.[202608] <> 0 OR B.[202608] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608]) ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN A.[202609] <> 0 OR B.[202609] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609]) ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN A.[202610] <> 0 OR B.[202610] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610]) ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN A.[202611] <> 0 OR B.[202611] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611]) ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN A.[202612] <> 0 OR B.[202612] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611] + A.[202612]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611] + B.[202612]) ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_nivel.est_01
            WHEN 2  THEN est_nivel.est_02
            WHEN 3  THEN est_nivel.est_03
            WHEN 4  THEN est_nivel.est_04
            WHEN 5  THEN est_nivel.est_05
            WHEN 6  THEN est_nivel.est_06
            WHEN 7  THEN est_nivel.est_07
            WHEN 8  THEN est_nivel.est_08
            WHEN 9  THEN est_nivel.est_09
            WHEN 10 THEN est_nivel.est_10
            WHEN 11 THEN est_nivel.est_11
            WHEN 12 THEN est_nivel.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_nivel est_nivel
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_nivel.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_nivel.nivel_centro = cen.nivel
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Concentración de Sesiones Odontológicas' AND est_nivel.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## O_GCHOdon - Grado de Cumplimiento de Hora Odontólogo
def queryO_GCHOdonRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Odontología - Horas Odontológicas Efectivas'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Odontología - Horas Odontológicas Programadas'
),
CEN AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     Variable IN ('Odontología - Sesiones Odontológicas', 'Odontología - Horas Odontológicas Efectivas')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.95 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
            CASE WHEN ( CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END) ELSE 0 END AS [202601],
            CASE WHEN ( CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END) ELSE 0 END AS [202602],
            CASE WHEN ( CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END) ELSE 0 END AS [202603],
            CASE WHEN ( CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END) ELSE 0 END AS [202604],
            CASE WHEN ( CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END) ELSE 0 END AS [202605],
            CASE WHEN ( CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END) ELSE 0 END AS [202606],
            CASE WHEN ( CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END) ELSE 0 END AS [202607],
            CASE WHEN ( CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END) ELSE 0 END AS [202608],
            CASE WHEN ( CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END) ELSE 0 END AS [202609],
            CASE WHEN ( CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL)  THEN ISNULL(B.[202610],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=10  THEN ISNULL(A.[202610],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=10  THEN ISNULL(B.[202610],0) ELSE 0 END) ELSE 0 END AS [202610],
            CASE WHEN ( CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL)  THEN ISNULL(B.[202611],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=11  THEN ISNULL(A.[202611],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=11  THEN ISNULL(B.[202611],0) ELSE 0 END) ELSE 0 END AS [202611],
            CASE WHEN ( CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL)  THEN ISNULL(B.[202612],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=12  THEN ISNULL(A.[202612],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=12  THEN ISNULL(B.[202612],0) ELSE 0 END) ELSE 0 END AS [202612]
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Grado de Cumplimiento de Hora Odontólogo' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## O_HrOdont - Rendimiento de Hora Odontológica
def queryO_HrOdontRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (
        SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608],
           [202609], [202610], [202611], [202612], Variable
         FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
         WHERE      Variable IN ('Odontología - Sesiones Odontológicas')
),
B AS (
        SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608],
            [202609], [202610], [202611], [202612], Variable
         FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
         WHERE     Variable IN ('Odontología - Horas Odontológicas Efectivas')
),
CEN_NIVEL AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE variable IN ('Odontología - Sesiones Odontológicas', 'Odontología - Horas Odontológicas Efectivas')
),
CEN_TIPO AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
)
SELECT DISTINCT
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.9 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]
FROM CEN_NIVEL AS CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_nivel.est_01
            WHEN 2  THEN est_nivel.est_02
            WHEN 3  THEN est_nivel.est_03
            WHEN 4  THEN est_nivel.est_04
            WHEN 5  THEN est_nivel.est_05
            WHEN 6  THEN est_nivel.est_06
            WHEN 7  THEN est_nivel.est_07
            WHEN 8  THEN est_nivel.est_08
            WHEN 9  THEN est_nivel.est_09
            WHEN 10 THEN est_nivel.est_10
            WHEN 11 THEN est_nivel.est_11
            WHEN 12 THEN est_nivel.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_nivel est_nivel
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_nivel.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_nivel.nivel_centro = cen.nivel
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Rendimiento Hora Odontológica' AND est_nivel.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo NOT IN ('CNSR','IPO','INCOR')

UNION ALL

SELECT DISTINCT
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.9 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]
FROM CEN_TIPO AS CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Rendimiento Hora Odontológica' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo IN ('CNSR','IPO','INCOR')
ORDER BY ORDEN;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## O_NTOdontS - Número de trabajos Odontológicos por Sesión
def queryO_NTOdontSRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (
           SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
           SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
           SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
           FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
           WHERE  Variable IN ('Odontología - Trabajos Odontológicos', 'Odontología - Diagnóstico por imágenes', 'Odontología - Procedimientos Especiales')
           GROUP BY Red, Centro, nivel, codcentro, Año),
B AS (
           SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
           [202609], [202610], [202611], [202612], Variable
           FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
           WHERE  Variable IN ('Odontología - Sesiones Odontológicas')
),
CEN AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     variable IN ('Odontología - Trabajos Odontológicos', 'Odontología - Diagnóstico por imágenes', 'Odontología - Procedimientos Especiales')
    UNION
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.9 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
            CASE WHEN ( CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END) ELSE 0 END AS [202601],
            CASE WHEN ( CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END) ELSE 0 END AS [202602],
            CASE WHEN ( CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END) ELSE 0 END AS [202603],
            CASE WHEN ( CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END) ELSE 0 END AS [202604],
            CASE WHEN ( CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END) ELSE 0 END AS [202605],
            CASE WHEN ( CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END) ELSE 0 END AS [202606],
            CASE WHEN ( CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END) ELSE 0 END AS [202607],
            CASE WHEN ( CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END) ELSE 0 END AS [202608],
            CASE WHEN ( CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END) ELSE 0 END AS [202609],
            CASE WHEN ( CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL)  THEN ISNULL(B.[202610],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=10  THEN ISNULL(A.[202610],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=10  THEN ISNULL(B.[202610],0) ELSE 0 END) ELSE 0 END AS [202610],
            CASE WHEN ( CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL)  THEN ISNULL(B.[202611],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=11  THEN ISNULL(A.[202611],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=11  THEN ISNULL(B.[202611],0) ELSE 0 END) ELSE 0 END AS [202611],
            CASE WHEN ( CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL)  THEN ISNULL(B.[202612],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=12  THEN ISNULL(A.[202612],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=12  THEN ISNULL(B.[202612],0) ELSE 0 END) ELSE 0 END AS [202612]
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar =  est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Número de trabajos Odontológicos por Sesión' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE     (A.Total * 1.00 / B.Total IS NOT NULL);
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_GCHProg - Porcentaje de Horas Quirúrgicas Efectivas
def queryQx_GCHProgRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (
      SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                             [202609], [202610], [202611], [202612], Variable
      FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE     Variable IN ('Centro Quirúrgico - Horas Uso de Sala')
),
B AS (
      SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
      [202609], [202610], [202611], [202612], Variable
      FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
      WHERE      Variable IN ('Centro Quirúrgico - Horas Programadas Intervenc.Quirurgicas')
),
CEN AS (
      SELECT DISTINCT Red, codcentro, Centro
      FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE     Variable IN ('Centro Quirúrgico - Horas Uso de Sala', 'Centro Quirúrgico - Horas Programadas Intervenc.Quirurgicas')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar - 0.1 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (ISNULL(A.[202601], 0) * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (ISNULL(A.[202602], 0) * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (ISNULL(A.[202603], 0) * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (ISNULL(A.[202604], 0) * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (ISNULL(A.[202605], 0) * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (ISNULL(A.[202606], 0) * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (ISNULL(A.[202607], 0) * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (ISNULL(A.[202608], 0) * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (ISNULL(A.[202609], 0) * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (ISNULL(A.[202610], 0) * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (ISNULL(A.[202611], 0) * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (ISNULL(A.[202612], 0) * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Porcentaje de Horas Quirúrgicas Efectivas' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_HTCesareas - Tasa de Cesáreas
def queryQx_HTCesareasRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (   
           SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
           [202609], [202610], [202611], [202612], Variable
           FROM  pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
           WHERE    Variable IN ('Centro Obstétrico - Cesáreas')
),
B AS (
     SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
     [202609], [202610], [202611], [202612], Variable
     FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
     WHERE      Variable IN ('Centro Obstétrico - Total de Partos')
),
CEN AS (
        SELECT DISTINCT Red, codcentro, Centro
        FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
        WHERE     variable IN ('Centro Obstétrico - Cesáreas')
        UNION
        SELECT DISTINCT Red, codcentro, Centro
        FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
        WHERE     variable IN ('Centro Obstétrico - Total de Partos')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 1.1 AS [% Acept],
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE NULL END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 AND A.[202601] <> 0 THEN (ISNULL(A.[202601], 0) * 1.00) / B.[202601] ELSE NULL END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 AND A.[202602] <> 0 THEN (ISNULL(A.[202602], 0) * 1.00) / B.[202602] ELSE NULL END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 AND A.[202603] <> 0 THEN (ISNULL(A.[202603], 0) * 1.00) / B.[202603] ELSE NULL END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 AND A.[202604] <> 0 THEN (ISNULL(A.[202604], 0) * 1.00) / B.[202604] ELSE NULL END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 AND A.[202605] <> 0 THEN (ISNULL(A.[202605], 0) * 1.00) / B.[202605] ELSE NULL END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 AND A.[202606] <> 0 THEN (ISNULL(A.[202606], 0) * 1.00) / B.[202606] ELSE NULL END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 AND A.[202607] <> 0 THEN (ISNULL(A.[202607], 0) * 1.00) / B.[202607] ELSE NULL END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 AND A.[202608] <> 0 THEN (ISNULL(A.[202608], 0) * 1.00) / B.[202608] ELSE NULL END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 AND A.[202609] <> 0 THEN (ISNULL(A.[202609], 0) * 1.00) / B.[202609] ELSE NULL END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 AND A.[202610] <> 0 THEN (ISNULL(A.[202610], 0) * 1.00) / B.[202610] ELSE NULL END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 AND A.[202611] <> 0 THEN (ISNULL(A.[202611], 0) * 1.00) / B.[202611] ELSE NULL END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 AND A.[202612] <> 0 THEN (ISNULL(A.[202612], 0) * 1.00) / B.[202612] ELSE NULL END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Tasa de Cesáreas' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_IAlta - Porcentaje de Intervenciones de Alta Complejidad
def queryQx_IAltaRep(db:Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;          
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (   
           SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
           [202609], [202610], [202611], [202612], Variable
           FROM  pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
           WHERE    Variable IN ('Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad')
),
B AS (
      SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
      SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
      SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
      FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
      WHERE      Variable IN ('Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                             'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                             'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento')
      GROUP BY Red, Centro, nivel, codcentro, Año
),
CEN AS (
SELECT DISTINCT Red, codcentro, Centro
FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     Variable IN ('Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 'Centro Quirúrgico - Cirugías sin clasificación de complejidad', 
                      'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 
                      'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 
                      'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.8 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
            CASE WHEN ( CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END) ELSE 0 END AS [202601],
            CASE WHEN ( CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END) ELSE 0 END AS [202602],
            CASE WHEN ( CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END) ELSE 0 END AS [202603],
            CASE WHEN ( CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END) ELSE 0 END AS [202604],
            CASE WHEN ( CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END) ELSE 0 END AS [202605],
            CASE WHEN ( CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END) ELSE 0 END AS [202606],
            CASE WHEN ( CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END) ELSE 0 END AS [202607],
            CASE WHEN ( CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END) ELSE 0 END AS [202608],
            CASE WHEN ( CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END) ELSE 0 END AS [202609],
            CASE WHEN ( CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL)  THEN ISNULL(B.[202610],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=10  THEN ISNULL(A.[202610],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=10  THEN ISNULL(B.[202610],0) ELSE 0 END) ELSE 0 END AS [202610],
            CASE WHEN ( CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL)  THEN ISNULL(B.[202611],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=11  THEN ISNULL(A.[202611],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=11  THEN ISNULL(B.[202611],0) ELSE 0 END) ELSE 0 END AS [202611],
            CASE WHEN ( CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL)  THEN ISNULL(B.[202612],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=12  THEN ISNULL(A.[202612],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=12  THEN ISNULL(B.[202612],0) ELSE 0 END) ELSE 0 END AS [202612]
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Porcentaje de Intervenciones de Alta Complejidad' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE     (A.Red IN ('ANCASH', 'APURIMAC', 'AREQUIPA', 'AYACUCHO', 'CAJAMARCA', 'CUSCO', 'HUANCAVELICA', 'HUANUCO', 'HUARAZ', 'ICA', 'RED JAEN', 'INCOR', 'JULIACA', 
                      'JUNIN', 'LA LIBERTAD', 'LAMBAYEQUE', 'LORETO', 'MADRE DE DIOS', 'MOQUEGUA', 'MOYOBAMBA', 'PASCO', 'PIURA', 'PUNO', 'REBAGLIATI', 'SABOGAL', 'TACNA', 
                      'TARAPOTO', 'TUMBES', 'RED PRESTACIONAL ALMENARA', 'RED PRESTACIONAL REBAGLIATI', 'RED PRESTACIONAL SABOGAL'));
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_IMenor - Porcentaje de Intervenciones Menores
def queryQx_IMenorRep(db:Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (
          SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
                   SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
                   SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
           FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
           WHERE      (Variable IN ('Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'))
           GROUP BY Red, Centro, nivel, codcentro, Año
),
X AS (SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
                   SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
                   SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
           FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
           WHERE      (Variable IN ('Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                                  'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                                  'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'))
           GROUP BY Red, Centro, nivel, codcentro, Año
),
CEN AS (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     Variable IN ('Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento', 
                      'Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                      'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                      'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'))
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 1.2 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(X.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(X.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN X.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / X.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN X.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / X.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN X.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / X.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN X.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / X.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN X.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / X.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN X.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / X.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN X.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / X.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN X.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / X.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN X.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / X.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN X.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / X.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN X.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / X.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN X.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / X.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN X ON CEN.codcentro = X.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Porcentaje de Intervenciones Menores' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_IntSusp - Porcentaje de Operaciones Suspendidas
def queryQx_IntSuspRep(db:Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;          
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (
      SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
      [202609], [202610], [202611], [202612], Variable
      FROM  pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE Variable IN ('Centro Quirúrgico - Operaciones Suspendidas')
),
B AS (
      SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
      [202609], [202610], [202611], [202612], Variable
      FROM  pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
      WHERE Variable IN ('Centro Quirúrgico - Intervenc.Quirurgicas Programadas')
),
CEN AS (
      SELECT DISTINCT Red, codcentro, Centro
      FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE     variable IN ('Centro Quirúrgico - Operaciones Suspendidas')
      UNION
      SELECT DISTINCT Red, codcentro, Centro
      FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE     variable IN ('Centro Quirúrgico - Intervenc.Quirurgicas Programadas')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 1.1 AS [% Acept],
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE NULL END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (ISNULL(A.[202601], 0) * 1.00) / B.[202601] ELSE NULL END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (ISNULL(A.[202602], 0) * 1.00) / B.[202602] ELSE NULL END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (ISNULL(A.[202603], 0) * 1.00) / B.[202603] ELSE NULL END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (ISNULL(A.[202604], 0) * 1.00) / B.[202604] ELSE NULL END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (ISNULL(A.[202605], 0) * 1.00) / B.[202605] ELSE NULL END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (ISNULL(A.[202606], 0) * 1.00) / B.[202606] ELSE NULL END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (ISNULL(A.[202607], 0) * 1.00) / B.[202607] ELSE NULL END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (ISNULL(A.[202608], 0) * 1.00) / B.[202608] ELSE NULL END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (ISNULL(A.[202609], 0) * 1.00) / B.[202609] ELSE NULL END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (ISNULL(A.[202610], 0) * 1.00) / B.[202610] ELSE NULL END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (ISNULL(A.[202611], 0) * 1.00) / B.[202611] ELSE NULL END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (ISNULL(A.[202612], 0) * 1.00) / B.[202612] ELSE NULL END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Porcentaje de Operaciones Suspendidas' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_RendSO - Rendimiento de Sala de Operaciones
def queryQx_RendSORep(db:Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (
        SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
                       SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
                       SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
        FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
        WHERE      (Variable IN ('Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                       'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                       'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'))
        GROUP BY Red, Centro, nivel, codcentro, Año
),
B AS (
        SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                     [202609], [202610], [202611], [202612], Variable
        FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
        WHERE      Variable IN ('Centro Quirúrgico -  Salas Quirúrgicas Funcionales')
),
CEN AS (
        SELECT DISTINCT Red, codcentro, Centro
        FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
        WHERE     Variable IN ('Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                              'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                              'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento', 
                              'Centro Quirúrgico -  Salas Quirúrgicas Funcionales')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.9 AS [% Acept],
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00  / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN ( CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END) ELSE 0 END AS [202601],
    CASE WHEN ( CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END) ELSE 0 END AS [202602],
    CASE WHEN ( CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END) ELSE 0 END AS [202603],
    CASE WHEN ( CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END) ELSE 0 END AS [202604],
    CASE WHEN ( CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END) ELSE 0 END AS [202605],
    CASE WHEN ( CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END) ELSE 0 END AS [202606],
    CASE WHEN ( CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END) ELSE 0 END AS [202607],
    CASE WHEN ( CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END) ELSE 0 END AS [202608],
    CASE WHEN ( CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END) ELSE 0 END AS [202609],
    CASE WHEN ( CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=10  THEN ISNULL(A.[202610],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=10  THEN ISNULL(B.[202610],0) ELSE 0 END) ELSE 0 END AS [202610],
    CASE WHEN ( CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=11  THEN ISNULL(A.[202611],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=11  THEN ISNULL(B.[202611],0) ELSE 0 END) ELSE 0 END AS [202611],
    CASE WHEN ( CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=12  THEN ISNULL(A.[202612],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=12  THEN ISNULL(B.[202612],0) ELSE 0 END) ELSE 0 END AS [202612]
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Rendimiento de Sala de Operaciones' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





