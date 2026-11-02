"""TMI dinámico: catálogos (DIM y tablas de apoyo), validación, cálculo y resultados
(procedimientos y tablas de src/resources/sql/tmi)."""

import logging
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.core.tmiConfig import TMI_DIM, TMI_TOTALIZADO3
from src.main.repositories.tmiBaseRep import (
    name_server,
    _consulta,
)

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


def queryCatalogoGruposTMI(db: Session):
    """Grupos de DIM_GRUPO (para la lógica de variables)."""
    return _consulta(db, f"""
        SELECT g.tipgrupo AS id, g.tipgrupo, g.desctipgrupo, g.desctipgrupo AS descripcion, g.Visible
        FROM {TMI_DIM}.DIM_GRUPO g WHERE g.Visible = 1 ORDER BY g.tipgrupo""")


def queryCatalogoGruposReporteTMI(db: Session):
    """Secciones del reporte para el indicador: los grupos visibles de DIM_GRUPO y los que ya usa algún indicador."""
    return _consulta(db, f"""
        SELECT g.tipgrupo AS id, LTRIM(RTRIM(g.desctipgrupo)) AS descripcion, g.Visible AS visible,
               (SELECT MIN(i.orden) FROM {name_server}.tmi_indicador i WHERE i.grupo = g.tipgrupo) AS orden
        FROM {TMI_DIM}.DIM_GRUPO g
        WHERE g.Visible = 1 OR EXISTS (SELECT 1 FROM {name_server}.tmi_indicador i WHERE i.grupo = g.tipgrupo)
        ORDER BY CASE WHEN EXISTS (SELECT 1 FROM {name_server}.tmi_indicador i WHERE i.grupo = g.tipgrupo) THEN 0 ELSE 1 END,
                 orden, descripcion""")


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
