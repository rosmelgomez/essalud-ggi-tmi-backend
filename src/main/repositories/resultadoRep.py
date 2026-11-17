"""Resultados del TMI calculados en tiempo real: resultado final por indicador y centro, valores de cada mes y
periodos que se pueden calcular."""

from typing import Optional

from sqlalchemy.orm import Session

from src.main.core.tmiConfig import TMI_TOTALIZADO3
from src.main.repositories.calculoRep import _fuente, calcularVivoTMI
from src.main.repositories.tmiBaseRep import name_server, _consulta


def _ordenFinal(filas):
    return sorted(filas, key=lambda r: (r.get("orden") is None, r.get("orden") or 0, r["codcentro"]))


def queryResultadoIndicadorTMI(db: Session, periodo: int, id_indicador: int, origen: Optional[str] = None):
    """Resultado final del indicador en el periodo, como la hoja del Excel, calculado en tiempo real (ver _fuente)."""
    final = calcularVivoTMI(db, periodo, _fuente(origen))["final"]
    return _ordenFinal([r for r in final if r["id_indicador"] == int(id_indicador)])


def queryResultadoFinalTMI(db: Session, periodo: int, origen: Optional[str] = None):
    """Resultado final de todos los indicadores del periodo (Excel y dashboard), en tiempo real (ver _fuente)."""
    return _ordenFinal(calcularVivoTMI(db, periodo, _fuente(origen))["final"])


def queryPeriodosResultadoTMI(db: Session, hasta: Optional[int] = None):
    """Periodos que se pueden calcular, del más reciente al más antiguo. origenes: con qué datos se puede calcular
    cada periodo (siempre en tiempo real):
    - BACKUP: el periodo tiene la copia del cierre (TOTALIZADO3_BACKUP).
    - ACTUAL: el periodo tiene datos en TOTALIZADO3 (hasta el último periodo que se puede calcular).
    origen_datos es ACTUAL si el periodo lo tiene; si no, BACKUP."""
    if hasta is None:
        from datetime import date
        from src.main.service.cierreServ import periodo_a_generar
        hasta = int(periodo_a_generar(date.today()))
    copias = {r["periodo_backup"] for r in _consulta(db, f"SELECT DISTINCT periodo_backup FROM {name_server}.TOTALIZADO3_BACKUP")}
    con_datos = {r["periodo"] for r in _consulta(db, f"SELECT DISTINCT periodo FROM {TMI_TOTALIZADO3} "
                                                     f"WHERE periodo <= :h", {"h": int(hasta)})}
    vivo = {"fecha_calculo": None, "indicadores": None, "centros": None, "en_vivo": True}
    salida = []
    for periodo in sorted(copias | con_datos, reverse=True):
        origenes: dict = {}
        if periodo in copias:
            origenes["BACKUP"] = dict(vivo)
        if periodo in con_datos:
            origenes["ACTUAL"] = dict(vivo)
        oficial = "ACTUAL" if "ACTUAL" in origenes else "BACKUP"
        datos = origenes[oficial]
        salida.append({"periodo": periodo, "indicadores": datos["indicadores"], "centros": datos["centros"],
                       "fecha_calculo": datos["fecha_calculo"], "origen_datos": oficial, "origenes": origenes})
    return salida


def queryResultadoTMI(db: Session, periodo: int, origen: Optional[str] = None):
    """Valor y puntaje de cada mes por indicador y centro, una fila por mes hasta el corte, solo de los centros e
    indicadores del periodo pedido: cada mes calculado ahora con la regla de ese mes (ver _fuente)."""
    vivo = calcularVivoTMI(db, periodo, _fuente(origen))
    claves = {(r["id_indicador"], r["codcentro"]) for r in vivo["resultado"]}
    return [{"id_indicador": m["id_indicador"], "codcentro": m["codcentro"], "mes": m["mes"],
             "valor": m["valor"], "puntaje": m["puntaje"]}
            for m in vivo["meses"] if (m["id_indicador"], m["codcentro"]) in claves]
