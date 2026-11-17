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
    _acept_del_anio,
    MESES,
    _indicador_join,
    _params,
    _consulta,
)


### tmi_centro 
def queryCentrosTMI(db: Session):
    try:
        result = db.execute(text(f"""
            SELECT id_centro AS id, codred, red, CAST(codcentro AS VARCHAR(50)) AS codcentro, centro, categoria, nivel,
                   nivel_estandar, tipo, flag
            FROM {name_server}.vw_tmi_centro_base b
            ORDER BY b.codcentro"""))
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# nivel_estandar une el centro con los estándares de fuente NIVEL; nivel (I, II, III) es informativo
_DATOS_CENTRO = ("codred", "red", "codcentro", "centro", "categoria", "nivel", "nivel_estandar", "tipo")


def _params_centro(dto) -> dict:
    params = dto.model_dump() if hasattr(dto, "model_dump") else dto.dict()
    for k in _DATOS_CENTRO + ("id", "flag"):
        params.setdefault(k, None)
    return params


def queryInsertCentrosTMI(db: Session, centro:tmiCentroDto):
    try:
        query = f"""
        INSERT INTO {name_server}.tmi_centro ({', '.join(_DATOS_CENTRO)}, flag)
        VALUES ({', '.join(':' + c for c in _DATOS_CENTRO)}, ISNULL(:flag, 1))"""
        result = db.execute(text(query), _params_centro(centro))
        db.commit()
        return {"message": "Centros TMI insertados correctamente", "rows_inserted": result.rowcount}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def queryUpdateCentrosTMI(db: Session, dto:tmiCentroDto):
    try:
        sets = [f"{c} = :{c}" for c in _DATOS_CENTRO] + ["flag = ISNULL(:flag, flag)"]
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


def queryCrearCentroEstandar(db: Session, datos: dict):
    """Alta de estándar propio de centro. Antes busca un registro del mismo año, codcentro e indicador:
    - no existe: se crea (fijo, NA y sustento del formulario).
    - existe: no se duplica; solo cambia el periodo `mes` de ese registro (como la exclusión de centro):
        * mes ya cerrado: est_MM = el valor del mes o, si viene vacío, el fijo ingresado; el fijo del año queda igual.
        * mes aún abierto: se actualiza el fijo y est_MM toma el valor del mes (vacío = usa el fijo); el cálculo lo
          usa desde ya y el cierre lo conserva. Los otros meses quedan igual.
        * NA (aplica = 0): el registro queda NA (el NA es del año en esta tabla).
      El sustento solo cambia si se envía uno."""
    from src.main.repositories.tmiBaseRep import queryInsertarFila
    from src.main.repositories.estandarRep import _periodo_alcanzo_cierre
    tabla = f"{name_server}.tmi_estandar_centro"
    existente = db.execute(text(f"""
        SELECT TOP 1 id FROM {tabla}
        WHERE anio = :anio AND LTRIM(RTRIM(codcentro)) = LTRIM(RTRIM(:codcentro)) AND id_indicador = :id_indicador
        ORDER BY id"""), datos).scalar()
    mes = datos.pop("mes", None)
    if existente is None:
        return queryInsertarFila(db, "tmi_estandar_centro", datos)
    p = {"id": existente, "fijo": datos.get("est_fijo"), "sustento": datos.get("sustento") or None}
    try:
        if not datos.get("aplica", True):
            sets = "aplica = 0, est_fijo = NULL, " + ", ".join(f"est_{m} = NULL" for m in MESES)
        elif mes and _periodo_alcanzo_cierre(db, int(datos["anio"]), int(mes)):
            c = f"est_{int(mes):02d}"
            p["valor"] = datos.get(c)
            sets = f"aplica = 1, {c} = COALESCE(:valor, :fijo, est_fijo), est_fijo = COALESCE(est_fijo, :fijo)"
        else:
            # el periodo aún no cierra: cambia el fijo y, si viene, el valor propio del mes (vacío = usa el fijo)
            sets = "aplica = 1, est_fijo = COALESCE(:fijo, est_fijo)"
            if mes:
                c = f"est_{int(mes):02d}"
                p["valor"] = datos.get(c)
                sets += f", {c} = :valor"
        db.execute(text(f"UPDATE {tabla} SET {sets}, sustento = COALESCE(:sustento, sustento) WHERE id = :id"), p)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "El centro ya tenía estándar de ese indicador en el año: se actualizó solo el periodo",
            "id": existente, "actualizado": True}


### tmi_exclusion_centro_indicador (exclusión de centro por indicador; id_indicador NULL = todos los indicadores del centro)
def queryExclusionCentroEstandar(db: Session, anio: int):
    try:
        cod = "COALESCE(CAST(cen.codcentro AS VARCHAR(50)), exc.codcentro)"
        resultado = "ISNULL(exc.resultado, 'NA')"
        join, tipo, orden = _indicador_join("exc.id_indicador")
        join = join.replace("JOIN ", "LEFT JOIN ", 1)
        # resultado de cada mes: el propio o el de la fila
        meses = ", ".join(f"exc.excl_{m}, COALESCE(exc.res_{m}, {resultado}) AS res_{m}" for m in MESES)
        query = f"""
        SELECT exc.id, exc.id_centro, {cod} AS codcentro, cen.centro,
               {tipo} AS tipo, ISNULL(i.indicador, 'Todos los indicadores') AS indicador,
               exc.id_indicador, exc.id_indicador AS id_estandar, exc.anio, {meses}, exc.motivo, {resultado} AS resultado
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
    params = _params(dto)
    params["id_indicador"] = params.get("id_indicador") if params.get("id_indicador") is not None else params.get("id_estandar")
    if params.get("id_centro") is None and not params.get("codcentro"):
        raise HTTPException(status_code=400, detail="Indique el centro (id_centro o codcentro).")
    if params.get("id_centro") is None:
        params["id_centro"] = db.execute(text(f"""
            SELECT MIN(id) FROM {name_server}.tmi_centro WHERE LTRIM(RTRIM(codcentro)) = LTRIM(RTRIM(:codcentro))"""),
            {"codcentro": params["codcentro"]}).scalar()
    cols = {"id_centro": ":id_centro", "id_indicador": ":id_indicador", "anio": ":anio"}
    cols.update({f"excl_{m}": f"ISNULL(:excl_{m}, 0)" for m in MESES})
    cols["codcentro"] = f"COALESCE(:codcentro, (SELECT codcentro FROM {name_server}.tmi_centro WHERE id = :id_centro))"
    cols["motivo"] = ":motivo"
    cols["resultado"] = "ISNULL(:resultado, 'NA')"
    # resultado de cada mes excluido: el propio o el general; un mes no excluido no guarda resultado
    cols.update({f"res_{m}": f"CASE WHEN ISNULL(:excl_{m}, 0) = 1 THEN COALESCE(:res_{m}, :resultado, 'NA') END"
                 for m in MESES})
    for k in ("codcentro", "motivo", "id", "resultado", *(f"res_{m}" for m in MESES)):
        params.setdefault(k, None)
    params.pop("ids_indicador", None)
    params.pop("mes", None)
    return params, cols


def queryInsertExclusionCentroEstandar(db: Session, dto:tmiExclusionCentroEstandarDto):
    """ids_indicador con valores: un registro por indicador; si el centro ya tiene exclusión de ese indicador en el año,
    se actualiza en lugar de duplicarla: los meses marcados se suman a los ya excluidos (un mes guardado no se pierde).
    Sin ids_indicador: un solo registro con id_indicador (NULL = todos)."""
    try:
        params, cols = _params_exclusion(db, dto)
        ids = list(dict.fromkeys(dto.ids_indicador or [])) or [params["id_indicador"]]
        meses = {f"excl_{m}": f"CASE WHEN ISNULL(:excl_{m}, 0) = 1 THEN 1 ELSE ISNULL(excl_{m}, 0) END" for m in MESES}
        # un mes que ya estaba excluido conserva su resultado (aunque cambie el general de la fila)
        meses.update({f"res_{m}": (f"CASE WHEN ISNULL(:excl_{m}, 0) = 1 THEN COALESCE(:res_{m}, :resultado, 'NA') "
                                   f"WHEN ISNULL(excl_{m}, 0) = 1 THEN COALESCE(res_{m}, resultado) END")
                      for m in MESES})
        # registro existente: solo se suman los meses; centro, indicador, año y resultado general quedan como están,
        # y el motivo solo cambia si se envía uno
        claves = {"id_centro", "id_indicador", "anio", "codcentro", "resultado"}
        sets = ", ".join(f"{c} = {meses.get(c, v)}" for c, v in cols.items() if c not in claves)
        sets = sets.replace("motivo = :motivo", "motivo = COALESCE(:motivo, motivo)")
        # el centro se busca por id_centro o por codcentro (el mismo centro con cualquiera de los dos)
        centro = (f"(id_centro = :id_centro OR LTRIM(RTRIM(codcentro)) = (SELECT LTRIM(RTRIM(codcentro)) "
                  f"FROM {name_server}.tmi_centro WHERE id = :id_centro))")
        query = f"""
        UPDATE {name_server}.tmi_exclusion_centro_indicador SET {sets}
        WHERE {centro} AND anio = :anio
          AND (id_indicador = :id_indicador OR (id_indicador IS NULL AND :id_indicador IS NULL));
        IF @@ROWCOUNT = 0
            INSERT INTO {name_server}.tmi_exclusion_centro_indicador ({', '.join(cols)})
            VALUES ({', '.join(cols.values())});
        """
        for id_indicador in ids:
            db.execute(text(query), {**params, "id_indicador": id_indicador, "id_estandar": id_indicador})
        _quitar_solapes(db, params["anio"], params["id_centro"])
        db.commit()
        return {"message": f"Exclusión de centro guardada correctamente para {len(ids)} indicador(es)", "rows_inserted": len(ids)}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def _quitar_mes_exclusion(db: Session, id: int, mes: str) -> int:
    """Quita la exclusión de un mes del registro; si el registro se queda sin meses excluidos, se borra."""
    tabla = f"{name_server}.tmi_exclusion_centro_indicador"
    sin_meses = " AND ".join(f"ISNULL(excl_{m}, 0) = 0" for m in MESES)
    r = db.execute(text(f"UPDATE {tabla} SET excl_{mes} = 0, res_{mes} = NULL WHERE id = :id"), {"id": id})
    db.execute(text(f"DELETE FROM {tabla} WHERE id = :id AND {sin_meses}"), {"id": id})
    return r.rowcount or 0


def _quitar_solapes(db: Session, anio: int, id_centro: int | None = None) -> None:
    """Un mes que la fila de «Todos los indicadores» del centro ya excluye con el mismo resultado sobra en las filas de
    cada indicador: se quita de ellas, y la fila que se queda sin meses se borra. Si el resultado es distinto, la fila
    del indicador se queda: es la que manda (fn_tmi_exclusion). id_centro None = todos los centros del año."""
    tabla = f"{name_server}.tmi_exclusion_centro_indicador"
    repetido = {m: (f"t.excl_{m} = 1 AND p.excl_{m} = 1 "
                    f"AND COALESCE(p.res_{m}, p.resultado) = COALESCE(t.res_{m}, t.resultado)") for m in MESES}
    sets = ", ".join(f"excl_{m} = CASE WHEN {c} THEN 0 ELSE p.excl_{m} END, "
                     f"res_{m} = CASE WHEN {c} THEN NULL ELSE p.res_{m} END" for m, c in repetido.items())
    filtro = "p.anio = :anio AND (:id_centro IS NULL OR p.id_centro = :id_centro) AND p.id_indicador IS NOT NULL"
    sin_meses = " AND ".join(f"ISNULL(p.excl_{m}, 0) = 0" for m in MESES)
    db.execute(text(f"""
        UPDATE p SET {sets}
        FROM {tabla} p
        JOIN {tabla} t ON t.id_centro = p.id_centro AND t.anio = p.anio AND t.id_indicador IS NULL
        WHERE {filtro};
        DELETE p FROM {tabla} p WHERE {filtro} AND {sin_meses};"""), {"anio": anio, "id_centro": id_centro})


def _mes_exclusion(db: Session, dto: tmiExclusionCentroEstandarDto) -> dict:
    """Edición por periodo: solo cambia el mes dto.mes del registro dto.id.
    - excl_MM = 0: el mes deja de estar excluido (si el registro se queda sin meses, se borra).
    - mismo centro e indicador: el mes queda excluido con su resultado ('0' o 'NA').
    - otro centro o indicador: el mes pasa a la exclusión de ese centro e indicador en el año (se crea si no existe) y
      sale del registro original; los otros meses del registro original no cambian."""
    tabla = f"{name_server}.tmi_exclusion_centro_indicador"
    params, _ = _params_exclusion(db, dto)
    m = f"{dto.mes:02d}"
    actual = db.execute(text(f"SELECT id_centro, id_indicador, anio FROM {tabla} WHERE id = :id"),
                        {"id": dto.id}).mappings().first()
    if actual is None:
        raise HTTPException(status_code=404, detail="La exclusión no existe o ya fue eliminada.")
    if not params.get(f"excl_{m}"):
        _quitar_mes_exclusion(db, dto.id, m)
        return {"message": "El mes dejó de estar excluido", "rows_affected": 1}
    res = params.get(f"res_{m}") or params.get("resultado") or "NA"
    p = {"id": dto.id, "res": res, "motivo": params.get("motivo"), "id_centro": params["id_centro"],
         "codcentro": params.get("codcentro"), "id_indicador": params["id_indicador"], "anio": actual["anio"]}
    mismo = (int(actual["id_centro"] or 0) == int(p["id_centro"] or 0)
             and (actual["id_indicador"] if actual["id_indicador"] is None else int(actual["id_indicador"]))
             == (p["id_indicador"] if p["id_indicador"] is None else int(p["id_indicador"])))
    if mismo:
        db.execute(text(f"""UPDATE {tabla} SET excl_{m} = 1, res_{m} = :res, motivo = COALESCE(:motivo, motivo)
                            WHERE id = :id"""), p)
        return {"message": "Exclusión del mes actualizada correctamente", "rows_affected": 1}
    _quitar_mes_exclusion(db, dto.id, m)
    db.execute(text(f"""
        UPDATE {tabla} SET excl_{m} = 1, res_{m} = :res
        WHERE id_centro = :id_centro AND anio = :anio
          AND (id_indicador = :id_indicador OR (id_indicador IS NULL AND :id_indicador IS NULL));
        IF @@ROWCOUNT = 0
            INSERT INTO {tabla} (id_centro, codcentro, id_indicador, anio, {", ".join(f"excl_{x}" for x in MESES)},
                                 resultado, res_{m}, motivo)
            VALUES (:id_centro,
                    COALESCE(:codcentro, (SELECT codcentro FROM {name_server}.tmi_centro WHERE id = :id_centro)),
                    :id_indicador, :anio, {", ".join("1" if x == m else "0" for x in MESES)}, :res, :res, :motivo);"""), p)
    return {"message": "El mes pasó a la exclusión del centro e indicador elegidos", "rows_affected": 1}


def queryUpdateExclusionCentroEstandar(db: Session, dto: tmiExclusionCentroEstandarDto):
    try:
        if dto.mes is not None and dto.id is not None:
            r = _mes_exclusion(db, dto)
            _quitar_solapes(db, dto.anio, dto.id_centro)
            db.commit()
            return r
        params, cols = _params_exclusion(db, dto)
        if params.get("id") is not None:
            # al editar no se puede dejar dos registros del mismo centro, indicador y año
            otro = db.execute(text(f"""
                SELECT TOP 1 id FROM {name_server}.tmi_exclusion_centro_indicador
                WHERE id <> :id AND id_centro = :id_centro AND anio = :anio
                  AND (id_indicador = :id_indicador OR (id_indicador IS NULL AND :id_indicador IS NULL))"""), params).scalar()
            if otro is not None:
                raise HTTPException(status_code=400, detail=(
                    "Ya existe otra exclusión de este centro para ese indicador y año. Edite ese registro."))
        sets = ", ".join(f"{c} = {v}" for c, v in cols.items())
        query = f"""
        UPDATE {name_server}.tmi_exclusion_centro_indicador SET {sets}
        WHERE (:id IS NOT NULL AND id = :id)
           OR (:id IS NULL AND id_centro = :id_centro AND anio = :anio
               AND (id_indicador = :id_indicador OR (id_indicador IS NULL AND :id_indicador IS NULL)))
        """
        result = db.execute(text(query), params)
        _quitar_solapes(db, params["anio"], params["id_centro"])
        db.commit()
        return {"message": "Exclusión de centro por indicador actualizada correctamente", "rows_affected": result.rowcount}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def queryDeleteExclusionCentroEstandar(db: Session, id: int, mes: int | None = None):
    """Con mes: solo quita la exclusión de ese mes (si el registro se queda sin meses, se borra). Sin mes: todo el año."""
    try:
        if mes is not None:
            n = _quitar_mes_exclusion(db, id, f"{mes:02d}")
            db.commit()
            if n == 0:
                raise HTTPException(status_code=404, detail="La exclusión no existe o ya fue eliminada.")
            return {"message": "Exclusión del mes quitada correctamente", "rows_deleted": n}
        result = db.execute(text(f"DELETE FROM {name_server}.tmi_exclusion_centro_indicador WHERE id = :id"), {"id": id})
        db.commit()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="La exclusión no existe o ya fue eliminada.")
    return {"message": "Exclusión de centro por indicador eliminada correctamente", "rows_deleted": result.rowcount}


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


def queryCentroEstandarTMI(db: Session, anio: int, mes: int | None = None):
    """Estándares propios de centro del año, como las tablas de estándares: est_fijo (el que toma cada mes en su fecha
    de cierre) y est_MM. Si el mes ya alcanzó su fecha de cierre, primero aplica el cierre (el mes toma el fijo).
    estandar = el que usa el mes de consulta (el del mes o, vacío, el fijo); acept = ese estándar ± el
    % Acept del indicador en el periodo (como usp_tmi_calcular; el centro no tiene % Acept propio).
    mes = periodo de consulta (1..12); sin mes, el último que se calcula (mes anterior) en su año; en otros años, diciembre.
    Devuelve {anio, mes, mes_cerrado, filas}: mes_cerrado dice si el mes ya se puede cambiar solo (aun sin filas)."""
    if mes is None:
        hoy = date.today()
        anterior = (hoy.year - 1, 12) if hoy.month == 1 else (hoy.year, hoy.month - 1)
        mes = anterior[1] if anio == anterior[0] else 12
    from src.main.repositories.estandarRep import _periodo_alcanzo_cierre, aplicarCierrePeriodoTMI
    cerrado = _periodo_alcanzo_cierre(db, anio, mes)
    if cerrado:
        aplicarCierrePeriodoTMI(db, f"{anio}{mes:02d}")
    filas = _consulta(db, f"""
        SELECT ce.id, ce.codcentro, ce.id_indicador, ce.anio, ce.aplica, ce.est_fijo,
               ce.est_01, ce.est_02, ce.est_03, ce.est_04, ce.est_05, ce.est_06,
               ce.est_07, ce.est_08, ce.est_09, ce.est_10, ce.est_11, ce.est_12, ce.sustento,
               i.indicador, c.centro, c.red, e.est AS estandar,
               CASE WHEN i.sentido IN ('MENOR', 'BANDA')
                    THEN CASE t.tipo WHEN 'ABS' THEN e.est + t.tol ELSE e.est * (1 + t.tol) END
                    ELSE CASE t.tipo WHEN 'ABS' THEN e.est - t.tol ELSE e.est * (1 - t.tol) END END AS acept
        FROM {name_server}.tmi_estandar_centro ce
        LEFT JOIN {name_server}.tmi_indicador i ON i.id = ce.id_indicador
        OUTER APPLY (SELECT TOP 1 b.centro, b.red FROM {name_server}.vw_tmi_centro_base b
                     WHERE CAST(b.codcentro AS VARCHAR(50)) = LTRIM(RTRIM(ce.codcentro))) c
        /* como el cálculo (fn_tmi_estandar): el valor del mes o, vacío, el fijo; 0 = sin estándar */
        CROSS APPLY (SELECT NULLIF(COALESCE(CASE :mes WHEN 1 THEN ce.est_01 WHEN 2 THEN ce.est_02 WHEN 3 THEN ce.est_03
                                             WHEN 4 THEN ce.est_04 WHEN 5 THEN ce.est_05 WHEN 6 THEN ce.est_06
                                             WHEN 7 THEN ce.est_07 WHEN 8 THEN ce.est_08 WHEN 9 THEN ce.est_09
                                             WHEN 10 THEN ce.est_10 WHEN 11 THEN ce.est_11 WHEN 12 THEN ce.est_12 END,
                                    ce.est_fijo), 0) AS est) e
        {_acept_del_anio(":anio")}
        CROSS APPLY (SELECT ISNULL(a.tipo_acept, 'REL') AS tipo,
                            COALESCE(CASE WHEN a.anio = :anio THEN a.acept_{int(mes):02d} END, a.acept_fijo) AS tol) t
        WHERE ce.anio = :anio
        ORDER BY ce.id_indicador, ce.codcentro""", {"anio": anio, "mes": mes})
    return {"anio": anio, "mes": mes, "mes_cerrado": cerrado, "filas": filas}
