"""Centros del TMI: tmi_centro, exclusión de centro por indicador y estándares propios de centro."""

from datetime import date

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.dtos.tmiDto import (
    tmiCentroDto,
    tmiExclusionCentroEstandarDto,
)
from src.main.repositories.tmiBaseRep import (
    name_server,
    MESES,
    _tiene_columna,
    _col_indicador,
    _indicador_join,
    _params,
    _columna_indicador,
    _consulta,
)


### tmi_centro 
def queryCentrosTMI(db: Session):
    try:
        query = f"""
        IF OBJECT_ID('{name_server}.vw_tmi_centro_base') IS NOT NULL
            SELECT id_centro AS id, codred, red, CAST(orden AS VARCHAR(20)) AS orden, CAST(orden_tipo AS VARCHAR(20)) AS orden_tipo,
                   CAST(codcentro AS VARCHAR(50)) AS codcentro, centro, categoria, nivel, nivel_estandar, tipo,
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


# Datos del centro que se guardan si la tabla los tiene (tmi_centro cambió: nivel_estandar reemplaza a nivel, que queda solo informativo, en la
# unión con los estándares; orden, orden_tipo y codred pueden no existir según la versión de la tabla)
_DATOS_CENTRO = ("codred", "red", "orden", "orden_tipo", "codcentro", "centro", "categoria", "nivel", "nivel_estandar", "tipo")
_FLAGS_MES = tuple(f"flag_{m}" for m in MESES)


def _columnas_centro(db: Session) -> set:
    filas = db.execute(text("SELECT name FROM sys.columns WHERE object_id = OBJECT_ID(:t)"),
                       {"t": f"{name_server}.tmi_centro"}).scalars()
    return {f.lower() for f in filas}


def _params_centro(dto) -> dict:
    params = dto.model_dump() if hasattr(dto, "model_dump") else dto.dict()
    for k in _DATOS_CENTRO + ("id", "anio", "flag") + _FLAGS_MES:
        params.setdefault(k, None)
    return params


def queryInsertCentrosTMI(db: Session, centro:tmiCentroDto):
    try:
        # Las columnas se eligen aquí: SQL Server compila el lote entero y falla con columnas que la tabla no tiene.
        existentes = _columnas_centro(db)
        cols = {c: f":{c}" for c in _DATOS_CENTRO if c in existentes}
        if "flag_01" in existentes:
            if "anio" in existentes:
                cols["anio"] = "ISNULL(:anio, YEAR(GETDATE()))"
            cols.update({f: f"ISNULL(:{f}, ISNULL(:flag, 1))" for f in _FLAGS_MES})
        elif "flag" in existentes:
            cols["flag"] = "ISNULL(:flag, 1)"
        query = f"""
        INSERT INTO {name_server}.tmi_centro ({', '.join(cols)})
        VALUES ({', '.join(cols.values())})"""
        result = db.execute(text(query), _params_centro(centro))
        db.commit()
        return {"message": "Centros TMI insertados correctamente", "rows_inserted": result.rowcount}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def queryUpdateCentrosTMI(db: Session, dto:tmiCentroDto):
    try:
        # columnas elegidas aquí (ver queryInsertCentrosTMI)
        existentes = _columnas_centro(db)
        # orden y orden_tipo ya no se editan en la pantalla: si no vienen se conserva lo guardado
        sets = [f"{c} = COALESCE(:{c}, {c})" if c in ("orden", "orden_tipo") else f"{c} = :{c}"
                for c in _DATOS_CENTRO if c in existentes]
        if "flag_01" in existentes:
            if "anio" in existentes:
                sets.append("anio = ISNULL(:anio, anio)")
            sets += [f"{f} = COALESCE(:{f}, :flag, {f})" for f in _FLAGS_MES]
        elif "flag" in existentes:
            sets.append("flag = COALESCE(:flag, :flag_01, flag)")
        query = f"""
        UPDATE {name_server}.tmi_centro
            SET {', '.join(sets)}
        WHERE (:id IS NOT NULL AND id = :id) OR (:id IS NULL AND codcentro = :codcentro)"""
        result = db.execute(text(query), _params_centro(dto))
        db.commit()
        return {"message": "Centro TMI actualizado correctamente", "rows_affected": result.rowcount}
    except Exception as e:
        db.rollback()
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


### tmi_exclusion_centro_indicador (exclusión de centro por indicador; id_indicador NULL = todos los indicadores del centro)
def queryExclusionCentroEstandar(db: Session, anio: int):
    try:
        tabla = "tmi_exclusion_centro_indicador"
        col = _col_indicador(db, tabla)
        pre = "excl_" if _tiene_columna(db, tabla, "excl_01") else "estandar_"
        cod = "COALESCE(CAST(cen.codcentro AS VARCHAR(50)), exc.codcentro)" if _tiene_columna(db, tabla, "codcentro") else "cen.codcentro"
        motivo = "exc.motivo" if _tiene_columna(db, tabla, "motivo") else "CAST(NULL AS VARCHAR(300))"
        resultado = "ISNULL(exc.resultado, '0')" if _tiene_columna(db, tabla, "resultado") else "'0'"
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
        cols["resultado"] = "ISNULL(:resultado, '0')"
    for k in ("codcentro", "motivo", "id", "resultado"):
        params.setdefault(k, None)
    params.pop("ids_indicador", None)
    return params, cols, col


def queryInsertExclusionCentroEstandar(db: Session, dto:tmiExclusionCentroEstandarDto):
    """ids_indicador con valores: un registro por indicador; si el centro ya tiene exclusión de ese indicador en el año,
    se actualiza en lugar de duplicarla: los meses marcados se suman a los ya excluidos (un mes guardado no se pierde).
    Sin ids_indicador: un solo registro con id_indicador (NULL = todos)."""
    try:
        params, cols, col = _params_exclusion(db, dto)
        ids = list(dict.fromkeys(dto.ids_indicador or [])) or [params["id_indicador"]]
        pre = "excl_" if "excl_01" in cols else "estandar_"
        meses = {f"{pre}{m}": f"CASE WHEN ISNULL(:excl_{m}, 0) = 1 THEN 1 ELSE ISNULL({pre}{m}, 0) END" for m in MESES}
        sets = ", ".join(f"{c} = {meses.get(c, v)}" for c, v in cols.items())
        query = f"""
        UPDATE {name_server}.tmi_exclusion_centro_indicador SET {sets}
        WHERE id_centro = :id_centro AND anio = :anio
          AND ({col} = :id_indicador OR ({col} IS NULL AND :id_indicador IS NULL));
        IF @@ROWCOUNT = 0
            INSERT INTO {name_server}.tmi_exclusion_centro_indicador ({', '.join(cols)})
            VALUES ({', '.join(cols.values())});
        """
        for id_indicador in ids:
            db.execute(text(query), {**params, "id_indicador": id_indicador, "id_estandar": id_indicador})
        db.commit()
        return {"message": f"Exclusión de centro guardada correctamente para {len(ids)} indicador(es)", "rows_inserted": len(ids)}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def queryUpdateExclusionCentroEstandar(db: Session, dto: tmiExclusionCentroEstandarDto):
    try:
        params, cols, col = _params_exclusion(db, dto)
        if params.get("id") is not None:
            # al editar no se puede dejar dos registros del mismo centro, indicador y año
            otro = db.execute(text(f"""
                SELECT TOP 1 id FROM {name_server}.tmi_exclusion_centro_indicador
                WHERE id <> :id AND id_centro = :id_centro AND anio = :anio
                  AND ({col} = :id_indicador OR ({col} IS NULL AND :id_indicador IS NULL))"""), params).scalar()
            if otro is not None:
                raise HTTPException(status_code=400, detail=(
                    "Ya existe otra exclusión de este centro para ese indicador y año. Edite ese registro."))
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


def queryCatalogosCentroTMI(db: Session) -> dict:
    """Catálogos activos del centro, en su orden (para filtros y para el formulario de centros):
    niveles = nivel de atención (I, II, III); niveles_estandar y tipos = los que unen el centro con los estándares."""
    def lista(tabla: str):
        try:
            return _consulta(db, f"""
                SELECT codigo, descripcion, orden FROM {name_server}.{tabla}
                WHERE activo = 1 ORDER BY ISNULL(orden, 999), codigo""")
        except HTTPException:
            return []   # la tabla todavía no existe (se crea al reiniciar el backend)
    return {"niveles": lista("tmi_nivel_centro"), "niveles_estandar": lista("tmi_nivel_estandar_centro"),
            "tipos": lista("tmi_tipo_centro")}


def queryCatalogoCentrosTMI(db: Session):
    return _consulta(db, f"""
        SELECT codcentro, MAX(centro) AS centro, MAX(red) AS red, MAX(tipo) AS tipo,
               MAX(nivel) AS nivel, MAX(nivel_estandar) AS nivel_estandar, MAX(categoria) AS categoria
        FROM {name_server}.vw_tmi_centro_base GROUP BY codcentro ORDER BY MAX(red), MAX(centro)""")


def queryCentroEstandarTMI(db: Session, anio: int):
    """Estándares propios de centro del año. acept_defecto = % Acept que se usa cuando el centro no tiene uno propio:
    su estándar del periodo de consulta ± el % Acept del indicador en ese periodo (como usp_tmi_calcular)."""
    col = _columna_indicador(db, "tmi_centro_estandar")
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
