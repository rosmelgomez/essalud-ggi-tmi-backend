"""Catálogos del TMI: grupos, actividades y servicios (DIM_* y TOTALIZADO3) y tipos de cálculo."""

import logging
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core.tmiConfig import TMI_DIM
from src.main.repositories.tmiBaseRep import name_server, _consulta

logger = logging.getLogger(__name__)


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


def queryCatalogoGruposReporteTMI(db: Session):
    """Secciones del reporte para el indicador: los grupos visibles de DIM_GRUPO y los que ya usa algún indicador."""
    return _consulta(db, f"""
        SELECT g.tipgrupo AS id, LTRIM(RTRIM(g.desctipgrupo)) AS descripcion, g.Visible AS visible,
               (SELECT MIN(i.orden) FROM {name_server}.tmi_indicador i WHERE i.grupo = g.tipgrupo) AS orden
        FROM {TMI_DIM}.DIM_GRUPO g
        WHERE g.Visible = 1 OR EXISTS (SELECT 1 FROM {name_server}.tmi_indicador i WHERE i.grupo = g.tipgrupo)
        ORDER BY CASE WHEN EXISTS (SELECT 1 FROM {name_server}.tmi_indicador i WHERE i.grupo = g.tipgrupo) THEN 0 ELSE 1 END,
                 orden, descripcion""")


def queryCatalogoTiposCalculoTMI(db: Session):
    return _consulta(db, f"SELECT codigo, descripcion FROM {name_server}.tmi_tipo_calculo ORDER BY codigo")
