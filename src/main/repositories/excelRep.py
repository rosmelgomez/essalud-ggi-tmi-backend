"""Consultas propias del Excel del TMI."""

from sqlalchemy.orm import Session

from src.main.repositories.tmiBaseRep import name_server, _acept_del_anio, _consulta


def queryEstandaresExcelTMI(db: Session, anio: int, mes: int):
    """Estándar y % Acept de cada indicador activo en el mes, con la misma regla que usp_tmi_calcular:
    estándar = valor del mes o, si está vacío, el fijo del año (m00); 0 = sin estándar. Tolerancia = la del mes,
    si no la fija del año (tmi_indicador_acept). Solo lee (no aplica el cierre)."""
    col = f"m{mes:02d}"
    am = f"CASE WHEN a.anio = :anio THEN a.acept_{int(mes):02d} END"
    amm = f"CASE WHEN a.anio = :anio THEN a.aceptmenos_{int(mes):02d} END"
    indicadores = _consulta(db, f"""
        SELECT i.id, i.orden, i.titulo_hoja, i.indicador, i.sentido,
               ISNULL(a.tipo_acept, 'REL') AS tipo_acept,
               COALESCE({am}, a.acept_fijo) AS acept,
               CASE WHEN {am} IS NOT NULL THEN ISNULL({amm}, {am})
                    ELSE ISNULL(a.aceptmenos_fijo, a.acept_fijo) END AS aceptmenos
        FROM {name_server}.tmi_indicador i
        {_acept_del_anio(":anio")}
        WHERE i.activo = 1
        ORDER BY i.orden, i.id""", {"anio": anio})
    claves = _consulta(db, f"""
        SELECT i.id AS id_indicador, LTRIM(RTRIM(e.clave)) AS clave,
               NULLIF(COALESCE(s.{col}, s.m00), 0) AS estandar
        FROM {name_server}.tmi_indicador i
        JOIN {name_server}.tmi_estandar e ON e.tipo_estandar = i.base_estandar AND e.activo = 1
        OUTER APPLY (SELECT TOP 1 x.{col}, x.m00 FROM {name_server}.vw_tmi_std x
                     WHERE x.id_estandar = i.id AND x.anio = :anio AND x.fuente = e.fuente AND x.clave = e.clave) s
        WHERE i.activo = 1""", {"anio": anio})
    por_indicador: dict = {}
    for c in claves:
        por_indicador.setdefault(c["id_indicador"], {})[c["clave"]] = c["estandar"]
    for i in indicadores:
        i["estandares"] = por_indicador.get(i["id"], {})
    return indicadores
