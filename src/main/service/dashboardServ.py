"""Datos del dashboard del TMI: el resultado final guardado del periodo con los mismos cálculos del Excel
(excelDinamicoServ y excelPuntajesServ), en JSON para el frontend.

- Indicadores: puntaje nacional = promedio de las redes sin las redes "- APP".
- Redes: puntaje por indicador = promedio de sus centros; los institutos van como red propia.
- Centros: solo los activos en el mes del periodo (flag del mes en tmi_centro). Puntaje por indicador (NA -> null),
  puntaje sobre 20, notas mensuales y valor/estándar de cada indicador.
"""

from collections import defaultdict
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set

from sqlalchemy.orm import Session

from src.main.repositories.centroRep import queryCatalogosCentroTMI
from src.main.repositories.indicadorRep import queryIndicadoresActivosTMI
from src.main.repositories.tmiDinamicoRep import queryCentrosActivosTMI, queryResultadoFinalTMI, queryResultadoTMI
from src.main.service.excelDinamicoServ import (
    NA, _es_red, _fuera_del_excel, _sin_produccion, _orden_redes, _promedio, _puntaje, _validar_periodo,
)
from src.main.service.excelPuntajesServ import calcular_totales


def _f(valor: Any) -> Optional[float]:
    if isinstance(valor, bool) or valor is None or valor == NA:
        return None
    if isinstance(valor, (int, float, Decimal)):
        return round(float(valor), 4)
    return None


def _nota(puntajes: List[Any], mensuales: List[List[Any]], mes: int):
    """Puntaje sobre 20 y notas mensuales (Ene..mes) como en la hoja Puntajes."""
    tot = calcular_totales(puntajes, mensuales, mes)
    return round(tot[4], 4), [round(v, 4) for v in tot[5:5 + mes]]


def armar_dashboard(periodo: str, filas_final: List[Dict[str, Any]], indicadores: List[Dict[str, Any]],
                    filas_mes: List[Dict[str, Any]], activos: Optional[Set[int]] = None) -> Dict[str, Any]:
    """filas_final: tmi_resultado_indicador del periodo; indicadores: activos de tmi_indicador;
    filas_mes: tmi_resultado del periodo (puntaje de cada mes); activos: códigos de los centros activos (None = todos)."""
    p = _validar_periodo(periodo)
    anio, mes = int(periodo[:4]), p % 100
    final: Dict[int, Dict[int, Dict[str, Any]]] = defaultdict(dict)
    centros_por_cod: Dict[int, Dict[str, Any]] = {}
    if activos is not None:   # centros dados de baja después del cálculo: no se muestran ni se cuentan
        filas_final = [r for r in filas_final if r["codcentro"] in activos]
    for r in filas_final:   # vienen ordenadas por orden_red, orden
        final[r["id_indicador"]][r["codcentro"]] = r
        centros_por_cod.setdefault(r["codcentro"], {
            "codcentro": r["codcentro"], "centro": r["centro"], "red": r["red"], "orden": r["orden_red"],
            "nivel": r["nivel"], "tipo": r.get("tipo"), "categoria": r["categoria"]})
    fecha = max((r["fecha_calculo"] for r in filas_final if r.get("fecha_calculo")), default=None)
    centros = list(centros_por_cod.values())
    indicadores = [i for i in indicadores if i["id"] in final]
    res: Dict[int, Dict[int, Dict[int, Any]]] = defaultdict(lambda: defaultdict(dict))
    for r in filas_mes:
        res[r["id_indicador"]][r["codcentro"]][r["mes"]] = r.get("puntaje")

    redes_orden = _orden_redes(centros)
    # por indicador: puntaje y meses de cada centro visible, y promedio de cada red (como _llenar_indicador).
    # Como en el Excel, no entran los centros sin información o sin estándar en el indicador.
    por_ind = []
    for ind in indicadores:
        fin = final[ind["id"]]
        pc: Dict[int, Dict[str, Any]] = {}
        pr: Dict[str, Dict[str, Any]] = {}
        for red in redes_orden:
            miembros = [c for c in centros if (c["red"] or "") == red
                        and c["codcentro"] in fin and fin[c["codcentro"]].get("visible", 1)
                        and not _fuera_del_excel(fin[c["codcentro"]])]
            if not miembros:
                continue
            for c in miembros:
                corte = fin[c["codcentro"]]
                pun = _puntaje(corte.get("puntaje"))
                meses = res[ind["id"]].get(c["codcentro"], {})
                det = None
                if not _sin_produccion(corte):   # producción NA: sin detalle; con producción 0 sí se muestra
                    det = {"p": None if pun == NA else pun, "v": _f(corte.get("total")),
                           "e": _f(corte.get("estandar")), "acept": _f(corte.get("acept")),
                           "aceptmenos": _f(corte.get("aceptmenos")),
                           "m": [_f(corte.get(f"periodo_{k:02d}")) for k in range(1, mes + 1)]}
                pc[c["codcentro"]] = {"p": pun, "m": [_puntaje(meses.get(k + 1)) if k < mes else None for k in range(12)],
                                      "det": det}
            if _es_red(red):
                pr[red] = {"p": _promedio([pc[c["codcentro"]]["p"] for c in miembros]),
                           "m": [_promedio([pc[c["codcentro"]]["m"][k] for c in miembros]) if k < mes else None
                                 for k in range(12)]}
        nacional = _promedio([d["p"] for red, d in pr.items() if "APP" not in red.upper()])
        por_ind.append({"centros": pc, "redes": pr, "nacional": nacional})

    salida_ind = [{"id": i["id"], "codigo": i["codigo"], "nombre": (i["titulo_hoja"] or i["indicador"] or "").strip(),
                   "servicio": (i.get("grupo") or "").strip(), "sentido": i.get("sentido"), "formato": i.get("formato"),
                   "tipo_calculo": (i.get("tipo_calculo") or "MENSUAL").upper(),
                   "nacional": _f(d["nacional"])} for i, d in zip(indicadores, por_ind)]

    salida_centros, salida_redes = [], []
    for red in redes_orden:
        if _es_red(red) and any(red in d["redes"] for d in por_ind):
            datos = [d["redes"].get(red, {"p": NA, "m": [NA] * 12}) for d in por_ind]
            if all(x["p"] == NA for x in datos):   # red sin ningún centro con puntaje (oculta en el Excel)
                continue
            nota, mensual = _nota([x["p"] for x in datos], [x["m"] for x in datos], mes)
            salida_redes.append({"nombre": red, "instituto": False, "app": "APP" in red.upper(),
                                 "pts": [_f(x["p"]) for x in datos], "nota": nota, "mensual": mensual})
        for c in (c for c in centros if (c["red"] or "") == red):
            datos = [d["centros"].get(c["codcentro"]) for d in por_ind]
            if all(x is None or x["p"] == NA for x in datos):   # sin ningún indicador evaluado
                continue
            datos = [x or {"p": NA, "m": [NA] * 12, "det": None} for x in datos]
            nota, mensual = _nota([x["p"] for x in datos], [x["m"] for x in datos], mes)
            fila = {"cod": c["codcentro"], "nombre": (c["centro"] or "").strip(), "red": (red or "").strip(),
                    "nivel": c["nivel"], "tipo": c["tipo"], "categoria": c["categoria"], "pts": [_f(x["p"]) for x in datos],
                    "nota": nota, "mensual": mensual, "det": [x["det"] for x in datos]}
            salida_centros.append(fila)
            if not _es_red(red):   # institutos: en Puntajes_RED van como fila propia
                salida_redes.append({"nombre": fila["red"], "instituto": True, "app": False,
                                     "pts": fila["pts"], "nota": nota, "mensual": mensual})

    return {"periodo": periodo, "anio": anio, "mes": mes, "fecha_calculo": str(fecha) if fecha else None,
            "indicadores": salida_ind, "redes": salida_redes, "centros": salida_centros}


def dashboard_tmi(db: Session, periodo: str) -> Dict[str, Any]:
    p = _validar_periodo(periodo)
    filas_final = queryResultadoFinalTMI(db, p)
    if not filas_final:
        raise ValueError(f"No hay resultado guardado del periodo {periodo}: ese periodo no se calculó.")
    datos = armar_dashboard(periodo, filas_final, queryIndicadoresActivosTMI(db), queryResultadoTMI(db, p),
                            queryCentrosActivosTMI(db, p))
    # nombres y orden de nivel (de atención: I, II, III, tmi_nivel_centro) y tipo para los filtros del tablero
    datos["catalogos"] = queryCatalogosCentroTMI(db)
    return datos

