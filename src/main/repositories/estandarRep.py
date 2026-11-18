"""Estándares del TMI: indicadores del mantenimiento (tmi_estandar), estándares por tipo, nivel y categoría,
tablas maestras de estándares, estándares por indicador y % Acept (acept, aceptmenos)."""

from datetime import date

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core.tmiConfig import TMI_DIM

from src.main.repositories.tmiBaseRep import (
    name_server,
    _acept_del_anio,
    _consulta,
)


def queryEstandar(db: Session ):
    try:
        query = f"""
        SELECT i.id, ISNULL(LTRIM(RTRIM(g.desctipgrupo)), '') AS tipo, i.indicador, i.fecha_creacion, i.fecha_modificacion
        FROM {name_server}.tmi_indicador i
        LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = i.grupo
        ORDER BY i.orden, i.id
        """
        result = db.execute(text(query))
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


# fuente -> tabla de valores y columna de la clave
FUENTES_ESTANDAR = {
    "NIVEL": ("tmi_estandar_nivel", "nivel_centro"),
    "TIPO": ("tmi_estandar_tipo", "tipo_centro"),
    "CATEGORIA": ("tmi_estandar_categoria", "categoria_centro"),
}


def _asegurar_fijo_anio(db: Session, anio: int):
    """Garantiza que cada indicador tenga su fila del año en tmi_indicador_acept con el % Acept fijo (acept_fijo /
    aceptmenos_fijo), copiando el fijo del año más cercano (antes el anterior) o, si el indicador no tiene ninguno,
    REL 10 %. Los meses quedan vacíos. En banda, aceptmenos_fijo se guarda siempre (vacío = el mismo que hacia arriba)."""
    db.execute(text(f"""
        INSERT INTO {name_server}.tmi_indicador_acept
            (id_indicador, anio, tipo_acept, acept_fijo, aceptmenos_fijo)
        SELECT i.id, :anio, ISNULL(a.tipo_acept, 'REL'), ISNULL(a.acept_fijo, 0.1),
               CASE WHEN i.sentido = 'BANDA' THEN COALESCE(a.aceptmenos_fijo, a.acept_fijo, 0.1) END
        FROM {name_server}.tmi_indicador i
        {_acept_del_anio(":anio")}
        WHERE NOT EXISTS (SELECT 1 FROM {name_server}.tmi_indicador_acept f
                          WHERE f.id_indicador = i.id AND f.anio = :anio)"""), {"anio": anio})
    db.commit()


def crearAceptIndicadorTMI(db: Session, id_indicador: int, sentido: str, tipo_acept: str, acept: float,
                           aceptmenos: float | None = None):
    """% Acept inicial de un indicador nuevo: su fila del año actual en tmi_indicador_acept (los años siguientes
    copian este fijo)."""
    banda = str(sentido or "").upper() == "BANDA"
    db.execute(text(f"""
        IF NOT EXISTS (SELECT 1 FROM {name_server}.tmi_indicador_acept WHERE id_indicador = :id AND anio = :anio)
        INSERT INTO {name_server}.tmi_indicador_acept (id_indicador, anio, tipo_acept, acept_fijo, aceptmenos_fijo)
        VALUES (:id, :anio, :tipo, :acept, :aceptmenos)"""),
        {"id": id_indicador, "anio": date.today().year, "tipo": tipo_acept or "REL", "acept": acept,
         "aceptmenos": (acept if aceptmenos is None else aceptmenos) if banda else None})
    db.commit()


def aplicarCierrePeriodoTMI(db: Session, periodo: str) -> int:
    """Al cumplirse la fecha de cierre de un periodo (AAAAMM):
    1) En las tablas de estándares (tipo, nivel, categoría y el propio de cada centro), el mes del periodo toma su
       est_fijo si aún no tiene valor.
    2) En tmi_indicador_acept, el mes del periodo (acept_MM / aceptmenos_MM) toma el % Acept fijo del año si aún no
       tiene valor."""
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
        # Si es un año nuevo sin filas aún, copia las filas base (con su est_fijo) del año anterior
        db.execute(text(f"""
            IF NOT EXISTS (SELECT 1 FROM {name_server}.{tabla} WHERE anio = :anio)
            INSERT INTO {name_server}.{tabla} (id_indicador, {clave}, anio, est_fijo)
            SELECT id_indicador, {clave}, :anio, est_fijo
            FROM {name_server}.{tabla}
            WHERE anio = :anio - 1"""), {"anio": anio})
        r_est = db.execute(text(f"""
            UPDATE {name_server}.{tabla}
               SET {col_mes} = est_fijo
             WHERE anio = :anio
               AND est_fijo IS NOT NULL
               AND {col_mes} IS NULL"""), {"anio": anio})
        afectadas += r_est.rowcount or 0
    afectadas += _cierre_estandar_centro(db, anio, col_mes)

    r_tol = db.execute(text(f"""
        UPDATE {name_server}.tmi_indicador_acept
           SET acept_{mes:02d} = acept_fijo, aceptmenos_{mes:02d} = aceptmenos_fijo
         WHERE anio = :anio
           AND acept_fijo IS NOT NULL
           AND acept_{mes:02d} IS NULL"""), {"anio": anio})
    afectadas += r_tol.rowcount or 0
    db.commit()
    return afectadas


def _cierre_estandar_centro(db: Session, anio: int, col_mes: str) -> int:
    """Cierre del estándar propio de cada centro (tmi_estandar_centro), como las tablas de estándares: en un año nuevo
    copia los registros del año anterior (fijo, NA y sustento) y el mes toma el fijo donde aún no tiene valor.
    Los centros que no aplican (aplica = 0) quedan NA y no toman valor."""
    tabla = f"{name_server}.tmi_estandar_centro"
    db.execute(text(f"""
        IF NOT EXISTS (SELECT 1 FROM {tabla} WHERE anio = :anio)
        INSERT INTO {tabla} (id_centro, codcentro, id_indicador, anio, aplica, est_fijo, sustento)
        SELECT id_centro, codcentro, id_indicador, :anio, aplica, est_fijo, sustento
        FROM {tabla}
        WHERE anio = :anio - 1"""), {"anio": anio})
    r = db.execute(text(f"""
        UPDATE {tabla}
           SET {col_mes} = est_fijo
         WHERE anio = :anio AND aplica = 1
           AND est_fijo IS NOT NULL
           AND ({col_mes} IS NULL OR {col_mes} = 0)"""), {"anio": anio})
    return r.rowcount or 0


def contarFilasCierrePeriodoTMI(db: Session, periodo: str) -> int:
    """Filas que deja listas el cierre de un periodo: estándares (tipo, nivel, categoría y de centro) con valor en el mes
    y % Acept con valor en el mes (acept_MM) en tmi_indicador_acept."""
    p = str(periodo).strip()
    if len(p) != 6 or not p.isdigit() or not 1 <= int(p[4:]) <= 12:
        return 0
    anio, mes = int(p[:4]), int(p[4:])
    col_mes = f"est_{mes:02d}"
    total = 0
    for tabla in ("tmi_estandar_tipo", "tmi_estandar_nivel", "tmi_estandar_categoria", "tmi_estandar_centro"):
        total += db.execute(text(f"""
            SELECT COUNT(1) FROM {name_server}.{tabla}
            WHERE anio = :anio AND {col_mes} IS NOT NULL"""), {"anio": anio}).scalar() or 0
    total += db.execute(text(f"""
        SELECT COUNT(1) FROM {name_server}.tmi_indicador_acept
        WHERE anio = :anio AND acept_{mes:02d} IS NOT NULL"""), {"anio": anio}).scalar() or 0
    return total


def _periodo_alcanzo_cierre(db: Session, anio: int, mes: int) -> bool:
    """True si el periodo AAAAMM ya alcanzó su fecha de cierre (en la tabla tmi_cierre o por ser <= mes anterior al actual)."""
    from src.main.repositories.cierreRep import CIERRE_TABLA
    periodo = f"{anio}{mes:02d}"
    fila = _consulta(db, f"""
        SELECT fecha_cierre, estado FROM {CIERRE_TABLA} WHERE periodo = :periodo""",
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
    - Si el periodo ya alcanzó su fecha de cierre, el mes (acept_MM) toma el fijo del año si aún no tiene valor.
    - Devuelve tanto el % Acept fijo del año como el % Acept del mes seleccionado (el del mes o, si está vacío, el fijo)."""
    if not 1 <= int(mes) <= 12:
        raise HTTPException(status_code=400, detail="Mes inválido")
    mes = int(mes)
    _asegurar_fijo_anio(db, anio)
    # Meses que aún no llegan a su fecha de cierre no tienen valor propio: usan el fijo. Lo que quedó guardado en esos
    # meses se vacía para que tomen el fijo en su cierre.
    abiertos = [m for m in range(1, 13) if not _periodo_alcanzo_cierre(db, anio, m)]
    if abiertos:
        vaciar = ", ".join(f"acept_{m:02d} = NULL, aceptmenos_{m:02d} = NULL" for m in abiertos)
        hay_valor = " OR ".join(f"acept_{m:02d} IS NOT NULL OR aceptmenos_{m:02d} IS NOT NULL" for m in abiertos)
        db.execute(text(f"""
            UPDATE {name_server}.tmi_indicador_acept SET {vaciar}
            WHERE anio = :anio AND ({hay_valor})"""), {"anio": anio})
        db.commit()
    cerrado = mes not in abiertos
    if cerrado:
        aplicarCierrePeriodoTMI(db, f"{anio}{mes:02d}")
    am, amm = f"a.acept_{mes:02d}", f"a.aceptmenos_{mes:02d}"
    indicadores = _consulta(db, f"""
        SELECT i.id, i.orden, i.codigo, i.indicador, i.base_estandar, i.sentido, i.formato,
               ISNULL(a.tipo_acept, 'REL') AS tipo_acept,
               a.acept_fijo, a.aceptmenos_fijo,
               COALESCE({am}, a.acept_fijo) AS acept,
               CASE WHEN {am} IS NOT NULL THEN {amm} ELSE a.aceptmenos_fijo END AS aceptmenos,
               LTRIM(RTRIM(g.desctipgrupo)) AS grupo
        FROM {name_server}.tmi_indicador i
        LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = i.grupo
        LEFT JOIN {name_server}.tmi_indicador_acept a ON a.id_indicador = i.id AND a.anio = :anio
        WHERE i.activo = 1
        ORDER BY i.orden, i.id""", {"anio": anio})
    # CASE en lugar de CHOOSE: el servidor no lo reconoce (nivel de compatibilidad anterior a SQL Server 2012)
    mes_valor = " ".join(f"WHEN {m} THEN s.m{m:02d}" for m in range(1, 13))
    claves = _consulta(db, f"""
        SELECT i.id AS id_indicador, e.orden, e.fuente, e.clave, e.descripcion,
               CASE :mes {mes_valor} END AS estandar
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
    - acept_fijo / aceptmenos_fijo: el fijo del año, que cada mes toma en su fecha de cierre.
    - acept / aceptmenos: el valor del mes (acept_MM / aceptmenos_MM), solo si el mes ya alcanzó su fecha de cierre
      (antes usa el fijo).
    El tipo (REL / ABS) es uno por año. Sin año, guarda el fijo del año actual.
    En banda, el % hacia abajo se guarda siempre: si no viene, es el mismo que hacia arriba. En los demás sentidos no
    se usa y queda vacío."""
    existe = _consulta(db, f"SELECT id, sentido FROM {name_server}.tmi_indicador WHERE id = :id", {"id": id_indicador})
    if not existe:
        raise HTTPException(status_code=404, detail="Indicador no encontrado")
    banda = str(existe[0].get("sentido") or "").upper() == "BANDA"
    abajo = lambda menos, mas: (mas if menos is None else menos) if banda else None
    anio = datos.get("anio")
    mes = datos.get("mes")
    if anio is None:   # sin año: el fijo del año actual
        anio, mes = date.today().year, None
        datos = {**datos, "acept_fijo": datos["acept"], "aceptmenos_fijo": datos.get("aceptmenos")}
    params = {
        "id": id_indicador,
        "tipo_acept": datos["tipo_acept"],
        "acept": datos["acept"],
        "aceptmenos": abajo(datos.get("aceptmenos"), datos["acept"]),
        "acept_fijo": datos.get("acept_fijo"),
        "aceptmenos_fijo": abajo(datos.get("aceptmenos_fijo"), datos.get("acept_fijo")),
        "usuario": usuario,
        "anio": anio,
    }
    try:
        _asegurar_fijo_anio(db, anio)   # la fila del año, con su fijo
        cambios = ["tipo_acept = :tipo_acept"]
        if datos.get("acept_fijo") is not None:
            cambios.append("acept_fijo = :acept_fijo, aceptmenos_fijo = :aceptmenos_fijo")
        if mes and 1 <= int(mes) <= 12 and _periodo_alcanzo_cierre(db, anio, int(mes)):
            cambios.append(f"acept_{int(mes):02d} = :acept, aceptmenos_{int(mes):02d} = :aceptmenos")
        r = db.execute(text(f"""
            UPDATE {name_server}.tmi_indicador_acept
               SET {", ".join(cambios)}
             WHERE id_indicador = :id AND anio = :anio"""), params)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "% Acept guardado", "rows_updated": r.rowcount}


### Estándar por periodo: un solo lugar por indicador (solo las claves de su base_estandar)

def _tablas_estandar() -> dict:
    """fuente -> (tabla, columna de la clave, columna del indicador) de las tablas por columnas (est_fijo + est_MM)."""
    return {fuente: (tabla, clave, "id_indicador") for fuente, (tabla, clave) in FUENTES_ESTANDAR.items()}


def _union_estandar(tablas: dict, mes: int) -> str:
    """Las tres tablas como una sola (fuente, indicador, clave, est_fijo, est_mes) para el año :anio."""
    partes = [f"""SELECT '{fuente}' AS fuente, {col_ind} AS id_indicador, LTRIM(RTRIM({clave})) AS clave,
                         CAST(est_fijo AS FLOAT) AS est_fijo, CAST(est_{mes:02d} AS FLOAT) AS est_mes
                  FROM {name_server}.{tabla} WHERE anio = :anio"""
              for fuente, (tabla, clave, col_ind) in tablas.items()]
    return " UNION ALL ".join(partes) or ("SELECT CAST(NULL AS VARCHAR(10)) AS fuente, CAST(NULL AS INT) AS id_indicador, "
                                          "CAST(NULL AS VARCHAR(50)) AS clave, CAST(NULL AS FLOAT) AS est_fijo, "
                                          "CAST(NULL AS FLOAT) AS est_mes WHERE 1 = 0")


def queryEstandaresPeriodoTMI(db: Session, anio: int, mes: int):
    """Indicadores activos con el estándar de cada clave de su base_estandar (lo único que usa el cálculo):
    fijo del año y valor del mes. Si el mes ya alcanzó su fecha de cierre, el mes toma el fijo donde no tenga valor."""
    cerrado = _periodo_alcanzo_cierre(db, anio, mes)
    if cerrado:
        aplicarCierrePeriodoTMI(db, f"{anio}{mes:02d}")
    indicadores = _consulta(db, f"""
        SELECT i.id, i.orden, i.codigo, i.indicador, i.base_estandar, t.descripcion AS base_descripcion, i.formato,
               LTRIM(RTRIM(g.desctipgrupo)) AS grupo
        FROM {name_server}.tmi_indicador i
        LEFT JOIN {TMI_DIM}.DIM_GRUPO g ON g.tipgrupo = i.grupo
        LEFT JOIN {name_server}.tmi_tipo_estandar t ON t.codigo = i.base_estandar
        WHERE i.activo = 1
        ORDER BY i.orden, i.id""")
    claves = _consulta(db, f"""
        SELECT i.id AS id_indicador, e.orden, e.fuente, LTRIM(RTRIM(e.clave)) AS clave, e.descripcion, e.prioridad,
               v.est_fijo AS fijo, v.est_mes AS mes,
               /* centros que usan la clave, con la misma exclusión del cálculo (usp_tmi_calcular): en una base
                  combinada el centro cuenta solo en su clave más específica (tipo > categoría > nivel). Así un CNSR
                  de nivel II cuenta en "Tipo CNSR" y no en "Nivel II". */
               (SELECT COUNT(DISTINCT c.codcentro) FROM {name_server}.vw_tmi_centro_base c
                WHERE CASE e.fuente WHEN 'NIVEL' THEN c.nivel WHEN 'TIPO' THEN c.nivel_estandar ELSE c.categoria END = e.clave
                  AND NOT EXISTS (SELECT 1 FROM {name_server}.tmi_estandar e2
                                  WHERE e2.tipo_estandar = e.tipo_estandar AND e2.activo = 1
                                    AND CASE e2.fuente WHEN 'TIPO' THEN 1 WHEN 'CATEGORIA' THEN 2 ELSE 3 END
                                      < CASE e.fuente WHEN 'TIPO' THEN 1 WHEN 'CATEGORIA' THEN 2 ELSE 3 END
                                    AND CASE e2.fuente WHEN 'NIVEL' THEN c.nivel WHEN 'TIPO' THEN c.nivel_estandar ELSE c.categoria END
                                      = e2.clave)) AS centros
        FROM {name_server}.tmi_indicador i
        JOIN {name_server}.tmi_estandar e ON e.tipo_estandar = i.base_estandar AND e.activo = 1
        OUTER APPLY (SELECT TOP 1 u.est_fijo, u.est_mes FROM ({_union_estandar(_tablas_estandar(), mes)}) u
                     WHERE u.fuente = e.fuente AND u.id_indicador = i.id AND u.clave = LTRIM(RTRIM(e.clave))) v
        WHERE i.activo = 1
        ORDER BY i.id, ISNULL(e.orden, 999), e.clave""", {"anio": anio})
    por_indicador: dict = {}
    for c in claves:
        por_indicador.setdefault(c.pop("id_indicador"), []).append(c)
    for i in indicadores:
        i["claves"] = por_indicador.get(i["id"], [])
        i["mes_cerrado"] = cerrado
    return indicadores


def queryGuardarEstandarPeriodoTMI(db: Session, id_indicador: int, datos: dict):
    """Guarda el estándar de un indicador para un periodo, solo en claves de su base_estandar:
    - fijo: est_fijo del año (los meses sin valor propio lo toman en su cierre).
    - mes: est_MM del periodo. Si el mes ya cerró, un valor vacío no lo cambia. Si aún no cierra, se puede fijar antes:
      el cálculo lo usa desde ya (valor del mes o, vacío, el fijo) y el cierre lo conserva; vacío lo deja con el fijo.
    Si la clave no tiene fila en el año, la crea."""
    anio, mes = int(datos["anio"]), int(datos["mes"])
    validas = {(r["fuente"], r["clave"]) for r in _consulta(db, f"""
        SELECT e.fuente, LTRIM(RTRIM(e.clave)) AS clave
        FROM {name_server}.tmi_indicador i
        JOIN {name_server}.tmi_estandar e ON e.tipo_estandar = i.base_estandar AND e.activo = 1
        WHERE i.id = :id""", {"id": id_indicador})}
    if not validas:
        raise HTTPException(status_code=400, detail="El indicador no existe o su base de estándar no tiene claves activas.")
    tablas = _tablas_estandar()
    cerrado = _periodo_alcanzo_cierre(db, anio, mes)
    col_mes = f"est_{mes:02d}"
    filas = 0
    try:
        for v in datos["valores"]:
            fuente, clave = v["fuente"], str(v["clave"]).strip()
            if (fuente, clave) not in validas:
                raise HTTPException(status_code=400, detail=f"{clave} ({fuente}) no es una clave de la base de este indicador.")
            if fuente not in tablas:
                raise HTTPException(status_code=400, detail=f"La tabla de estándares por {fuente.lower()} no admite este guardado.")
            tabla, col_clave, col_ind = tablas[fuente]
            # 0 es un estándar válido; vacío (None) = sin estándar
            fijo = v.get("fijo")
            valor_mes = v.get("mes")
            # mes cerrado: vacío = no cambia; mes abierto: el valor enviado (vacío = vuelve a usar el fijo)
            poner_mes = valor_mes is not None if cerrado else "mes" in v
            sets = (["est_fijo = :fijo"] if "fijo" in v else []) + ([f"{col_mes} = :mes"] if poner_mes else [])
            if not sets:
                continue
            cols = [col_ind, col_clave, "anio", "est_fijo"] + ([col_mes] if valor_mes is not None else [])
            vals = [":id", ":clave", ":anio", ":fijo"] + ([":mes"] if valor_mes is not None else [])
            r = db.execute(text(f"""
                UPDATE {name_server}.{tabla} SET {', '.join(sets)}
                WHERE {col_ind} = :id AND LTRIM(RTRIM({col_clave})) = :clave AND anio = :anio;
                IF @@ROWCOUNT = 0
                    INSERT INTO {name_server}.{tabla} ({', '.join(cols)}) VALUES ({', '.join(vals)});"""),
                {"id": id_indicador, "clave": clave, "anio": anio, "fijo": fijo, "mes": valor_mes})
            filas += r.rowcount or 0
        db.commit()
        return {"message": "Estándar guardado", "rows_affected": filas, "mes_cerrado": cerrado}
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
