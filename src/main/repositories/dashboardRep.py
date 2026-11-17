"""Consultas propias del dashboard del TMI."""

from sqlalchemy.orm import Session

from src.main.repositories.tmiBaseRep import name_server, _consulta


def queryCentrosActivosTMI(db: Session, periodo: int):
    """Códigos de los centros activos (flag = 1 en tmi_centro), como usp_tmi_calcular. El flag vale todo el año."""
    filas = _consulta(db, f"""
        SELECT DISTINCT c.codcentro
        FROM {name_server}.vw_tmi_centro_base c
        WHERE c.codcentro IS NOT NULL AND c.flag = 1""")
    return {r["codcentro"] for r in filas}
