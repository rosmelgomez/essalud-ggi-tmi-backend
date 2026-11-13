"""Excel del TMI dinámico: se arma desde la plantilla vacía TMI_PLANTILLA_BASE.xlsx.

- Una hoja por indicador activo de tmi_indicador (copiada de _MODELO_INDICADOR), en su orden.
- Filas y valores desde el resultado final del periodo (cálculo en tiempo real): los centros, sus datos
  y los valores son los de la configuración de hoy.
  Los puntajes mensuales de las hojas Puntajes salen del mismo cálculo.
- Formato condicional calculado sobre las filas escritas; columna F (código de centro) visible;
  columna N (% Acept de arriba) solo en indicadores de BANDA.
- Puntajes y Puntajes_RED con una columna por indicador activo (excelPuntajesServ).
"""

import io
import logging
import re
import unicodedata
from collections import defaultdict
from copy import copy
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List, Optional

from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.formatting.rule import Rule
from openpyxl.utils import get_column_letter
from sqlalchemy.orm import Session

from src.main.repositories.estandarRep import queryEstandaresExcelTMI
from src.main.repositories.indicadorRep import queryIndicadoresActivosTMI
from src.main.repositories.tmiDinamicoRep import (
    queryResultadoFinalTMI,
    queryResultadoTMI,
)
from src.main.service.excelServ import MESES_NOMBRE, _restaurar_dibujos

logger = logging.getLogger(__name__)

PLANTILLA_BASE = Path(__file__).resolve().parents[2] / "resources" / "plantillas" / "TMI_PLANTILLA_BASE.xlsx"
# Los dibujos (logos y botones con hipervínculo) se restauran desde la plantilla original: en la base, creada con
# openpyxl, sus relaciones de hipervínculo se perdieron y Excel tenía que reparar el archivo.
PLANTILLA_DIBUJOS = PLANTILLA_BASE.with_name("TMI_PLANTILLA.xlsx")
# hoja modelo de la base -> hoja de la plantilla original de la que salió (crear_plantilla_base.py)
HOJA_ORIGINAL = {"_MODELO_INDICADOR": "H_% O.Cama", "_MODELO_PUNTAJES": "Puntajes", "_MODELO_PUNTAJES_RED": "Puntajes_RED"}
MODELO_INDICADOR = "_MODELO_INDICADOR"
MODELO_PUNTAJES = "_MODELO_PUNTAJES"
MODELO_PUNTAJES_RED = "_MODELO_PUNTAJES_RED"

# Columnas de la hoja de indicador
COL_PUNTAJE, COL_CODIGO, COL_MARCA, COL_COD, COL_CENTRO = 3, 4, 5, 6, 7
COL_NIVEL, COL_TIPO, COL_VALOR, COL_ESTANDAR, COL_VERDE, COL_ACEPT = 8, 9, 10, 11, 12, 13
# la plantilla trae N:R (Rojo +, auxiliares y Anual) antes de los meses; se quitan y Ene queda en N
COL_QUITAR, CANT_QUITAR = 14, 5  # N:R
COL_MES1 = 14                    # N (en la plantilla, S)
FILA_TOTAL, FILA_DATOS = 8, 10
FILA_MODELO_RED, FILA_MODELO_CENTRO = 10, 11
# Formato de los valores por indicador (tmi_indicador.formato), como en TMI_PLANTILLA.xlsx
FORMATO_NUMERO = {"NUMERO": "0.00", "PORCENTAJE": "0.00%"}
COLS_VALORES = [COL_VALOR, COL_ESTANDAR, COL_VERDE, COL_ACEPT] + [COL_MES1 + i for i in range(12)]
CODIGO_PUNTAJE = {5: 1, 3: 2, 1: 3, 0: 3}
NA = "NA"


def _sin_produccion(corte: Dict[str, Any]) -> bool:
    """Producción NA: el centro no tiene valor real en el corte (total NULL: sin datos en el año, división entre 0,
    mes excluido o fuera de ámbito). Solo estos centros se ocultan; con producción 0 o con valor se muestran aunque su
    puntaje sea NA (por ejemplo, sin estándar)."""
    return corte.get("total") is None


def _fuera_del_excel(corte: Dict[str, Any]) -> bool:
    """El centro no se lista en la hoja del indicador (ni cuenta en Puntajes): sin información en el corte
    (producción NA o sin datos en el año) o sin estándar."""
    return _sin_produccion(corte) or corte.get("motivo_na") in ("SIN_ESTANDAR", "SIN_DATOS_ANIO")


def _validar_periodo(periodo: str) -> int:
    if not periodo or len(periodo) != 6 or not periodo.isdigit() or not 1 <= int(periodo[4:]) <= 12:
        raise ValueError("El periodo debe tener formato AAAAMM.")
    return int(periodo)


def _puntaje(valor: Optional[str]) -> Any:
    return NA if valor in (None, NA) else int(valor)


def _promedio(valores: List[Any]):
    nums = [float(v) for v in valores if isinstance(v, (int, float)) and not isinstance(v, bool)]
    return round(mean(nums), 3) if nums else NA


def _copiar_fila(origen, destino, fila_origen: int, fila_destino: int, ultima_col: int) -> None:
    for c in range(1, ultima_col + 1):
        src, dst = origen.cell(fila_origen, c), destino.cell(fila_destino, c)
        dst.value = None
        if src.has_style:
            dst._style = copy(src._style)
    altura = origen.row_dimensions[fila_origen].height
    if altura:
        destino.row_dimensions[fila_destino].height = altura


def reiniciar_filas(ws, desde: int) -> None:
    """Quita alto, ocultamiento y agrupación de las filas >= desde. delete_rows/limpiar no mueven row_dimensions:
    las filas ocultas y agrupadas de la plantilla quedaban sobre otros centros (se veían menos y mal agrupados)."""
    for r in [r for r in ws.row_dimensions if r >= desde]:
        del ws.row_dimensions[r]


def _copiar_imagenes(origen, destino) -> None:
    for img in getattr(origen, "_images", []):
        # _data() cierra el flujo de la imagen: se guardan los bytes para poder copiarla a varias hojas
        datos = getattr(img, "_tmi_bytes", None)
        if datos is None:
            datos = img._data()
            img._tmi_bytes = datos
            img.ref = io.BytesIO(datos)
        nueva = Image(io.BytesIO(datos))
        nueva.anchor = copy(img.anchor)
        nueva.width, nueva.height = img.width, img.height
        destino.add_image(nueva)


def _rangos(filas: List[int], col: str) -> str:
    """Filas -> 'E11:E20 E23:E34' (bloques consecutivos)."""
    bloques, inicio, previo = [], None, None
    for f in sorted(filas):
        if inicio is None:
            inicio = previo = f
        elif f == previo + 1:
            previo = f
        else:
            bloques.append((inicio, previo))
            inicio = previo = f
    if inicio is not None:
        bloques.append((inicio, previo))
    return " ".join(f"{col}{a}:{col}{b}" for a, b in bloques)


def _formato_condicional(ws, modelo, filas_centro: List[int]) -> None:
    """Copia las reglas guardadas en E11 del modelo al rango de filas de centros escritas."""
    if not filas_centro:
        return
    primera = min(filas_centro)
    sqref = _rangos(filas_centro, "E")
    for cf in modelo.conditional_formatting:
        for regla in cf.rules:
            nueva = Rule(type=regla.type, dxf=copy(regla.dxf), stopIfTrue=regla.stopIfTrue,
                         formula=[re.sub(r"\bC11\b", f"C{primera}", f) for f in (regla.formula or [])])
            ws.conditional_formatting.add(sqref, nueva)


def _quitar_columnas_modelo(ws, desde: int, cantidad: int) -> None:
    """Elimina columnas de la hoja modelo y corre a la izquierda lo que sigue (los meses de S:AD pasan a N:Y).
    delete_cols solo mueve las celdas: las celdas combinadas y los anchos de columna se corren aquí."""
    hasta = desde + cantidad - 1
    ws.delete_cols(desde, cantidad)
    for rango in list(ws.merged_cells.ranges):
        if rango.min_col > hasta:
            ws.merged_cells.remove(rango)
            ws.merge_cells(start_row=rango.min_row, end_row=rango.max_row,
                           start_column=rango.min_col - cantidad, end_column=rango.max_col - cantidad)
    dims = []
    for dim in ws.column_dimensions.values():
        if not dim.min:
            continue
        lo, hi = dim.min, dim.max or dim.min
        if lo < desde:                       # antes de lo borrado (M venía como rango M:N)
            hi = min(hi, desde - 1)
        elif lo <= hasta:                    # dentro de lo borrado
            if hi <= hasta:
                continue
            lo = hasta + 1
        if lo > hasta:
            lo -= cantidad
            hi = hi if hi >= 16384 else hi - cantidad
        dims.append((lo, hi, dim))
    ws.column_dimensions.clear()
    for lo, hi, dim in dims:
        nueva = ws.column_dimensions[get_column_letter(lo)]
        nueva.min, nueva.max, nueva.width, nueva.hidden = lo, hi, dim.width, dim.hidden
        nueva.outlineLevel, nueva.bestFit, nueva._style = dim.outlineLevel, dim.bestFit, copy(dim._style)


def _es_red(nombre: str) -> bool:
    """Solo los grupos 'RED ...' tienen fila de red y entran al promedio nacional. Los institutos (INCOR, CNSR)
    figuran en tmi_centro con su propio nombre como red: se listan sin fila de red, como en el Excel oficial."""
    return nombre.strip().upper().startswith("RED ")


def _orden_redes(centros: List[Dict[str, Any]]) -> List[str]:
    vistos: Dict[str, tuple] = {}
    for c in centros:
        red = c["red"] or ""
        vistos.setdefault(red, (c["orden"] if c["orden"] is not None else 9999, len(vistos)))
    return [red for red, _ in sorted(vistos.items(), key=lambda x: x[1])]


def _llenar_indicador(wb, modelo, ind: Dict[str, Any], centros: List[Dict[str, Any]],
                      final: Dict[int, Dict[str, Any]], res: Dict[int, Dict[int, Dict[str, Any]]],
                      anio: str, mes: int) -> Dict[str, Any]:
    """final: {codcentro: fila del resultado final}; res: {codcentro: {mes: fila del resultado del mes}}."""
    """Crea la hoja del indicador y devuelve los puntajes por centro y por red (periodo y mensuales)."""
    ws = wb.copy_worksheet(modelo)
    ws.title = ind["nombre_hoja"]
    ws.sheet_state = "visible"
    ws.freeze_panes = modelo.freeze_panes
    # copy_worksheet no copia la vista: sin esto la hoja sale con cuadrícula (debe verse en blanco como Estandares)
    ws.sheet_view.showGridLines = False
    _copiar_imagenes(modelo, ws)
    ultima_col = modelo.max_column
    banda = (ind["sentido"] or "").upper() == "BANDA"
    formato = FORMATO_NUMERO.get((ind.get("formato") or "NUMERO").upper(), "0.00")

    ws.cell(3, COL_PUNTAJE, value=ind["titulo_hoja"] or ind["indicador"])
    ws.cell(5, COL_MES1, value=f"AÑO: {anio}")
    # en banda, M = % Aceptmenos (abajo); el % Acept de arriba ya no tiene columna (N es Ene)
    ws.cell(6, COL_ACEPT).value = "% Aceptmenos" if banda else "% Acept"
    ws.column_dimensions["F"].hidden = True   # códigos de centro: se usan internamente, no se muestran

    # filas de la plantilla copiada: se rehacen desde la fila de datos
    if ws.max_row >= FILA_DATOS:
        ws.delete_rows(FILA_DATOS, ws.max_row - FILA_DATOS + 1)
    reiniciar_filas(ws, FILA_DATOS)

    por_red: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for c in centros:
        corte = final.get(c["codcentro"])
        if corte and corte.get("visible", 1) and not _fuera_del_excel(corte):
            por_red[c["red"] or ""].append(c)

    puntajes_centro: Dict[int, Dict[str, Any]] = {}
    puntajes_red: Dict[str, Dict[str, Any]] = {}
    filas_centro: List[int] = []
    fila = FILA_DATOS
    for red in _orden_redes(centros):
        miembros = por_red.get(red)
        if not miembros:
            continue
        es_red = _es_red(red)
        fila_red = fila
        if es_red:
            _copiar_fila(modelo, ws, FILA_MODELO_RED, fila_red, ultima_col)
            ws.cell(fila_red, COL_CENTRO, value=red)
            fila += 1
        for c in miembros:
            meses = res.get(c["codcentro"], {})
            corte = final[c["codcentro"]]
            p = _puntaje(corte.get("puntaje"))
            fila_na = _sin_produccion(corte)
            _copiar_fila(modelo, ws, FILA_MODELO_CENTRO, fila, ultima_col)
            for col in COLS_VALORES:   # la fila modelo sale de H_% O.Cama (porcentaje)
                ws.cell(fila, col).number_format = formato
            ws.cell(fila, COL_PUNTAJE, value=p)
            ws.cell(fila, COL_CODIGO, value=CODIGO_PUNTAJE.get(p, NA))
            ws.cell(fila, COL_MARCA, value="=")
            ws.cell(fila, COL_COD, value=c["codcentro"])
            ws.cell(fila, COL_CENTRO, value=c["centro"])
            if es_red:   # centros agrupados bajo la fila de su red (resumen arriba)
                ws.row_dimensions[fila].outline_level = 1
            if fila_na:  # producción NA: queda en el Excel pero oculto (con producción 0 se ve)
                ws.row_dimensions[fila].hidden = True
            if fila_na:
                for col in (COL_NIVEL, COL_TIPO, COL_VALOR, COL_ESTANDAR, COL_VERDE, COL_ACEPT):
                    ws.cell(fila, col, value=NA)
                for i in range(12):
                    ws.cell(fila, COL_MES1 + i, value=NA)
            else:
                o_na = lambda v: NA if v is None else v   # sin estándar o mes excluido: NA, no 0
                ws.cell(fila, COL_NIVEL, value=c["nivel"])
                ws.cell(fila, COL_TIPO, value=c["tipo"])
                ws.cell(fila, COL_VALOR, value=corte.get("total"))
                ws.cell(fila, COL_ESTANDAR, value=o_na(corte.get("estandar")))
                ws.cell(fila, COL_VERDE, value=o_na(corte.get("estandar")))
                ws.cell(fila, COL_ACEPT, value=o_na(corte.get("aceptmenos") if banda else corte.get("acept")))
                for i in range(12):
                    v = corte.get(f"periodo_{i + 1:02d}")
                    ws.cell(fila, COL_MES1 + i, value=v if v is not None else (NA if i < mes else 0))
            mensual = [_puntaje(meses.get(i + 1, {}).get("puntaje")) if i < mes else None for i in range(12)]
            puntajes_centro[c["codcentro"]] = {"p": p, "m": mensual, "sin_prod": fila_na}
            filas_centro.append(fila)
            fila += 1
        if es_red:
            p_red = _promedio([puntajes_centro[c["codcentro"]]["p"] for c in miembros])
            m_red = [_promedio([puntajes_centro[c["codcentro"]]["m"][i] for c in miembros]) if i < mes else None
                     for i in range(12)]
            ws.cell(fila_red, COL_PUNTAJE, value=p_red)
            puntajes_red[red] = {"p": p_red, "m": m_red}
        if all(puntajes_centro[c["codcentro"]]["sin_prod"] for c in miembros):
            for f in range(fila_red, fila + 1):   # red sin ningún centro con producción: red y fila en blanco ocultas
                ws.row_dimensions[f].hidden = True
        fila += 1   # fila en blanco entre redes

    # TOTAL NACIONAL = promedio de las redes, sin las redes "- APP"
    ws.cell(FILA_TOTAL, COL_PUNTAJE,
            value=_promedio([d["p"] for red, d in puntajes_red.items() if "APP" not in red.upper()]))
    _formato_condicional(ws, modelo, filas_centro)
    return {"centros": puntajes_centro, "redes": puntajes_red}


def _actualizar_resumen(wb, anio: str, mes: int) -> None:
    ws = wb["Resumen"]
    ws["B9"] = f"CIFRAS PRELIMINARES A {MESES_NOMBRE[mes - 1]} {anio} (*)"
    # Fórmulas ='hoja'!C8 de indicadores que no se generaron (inactivos) -> NA
    for fila in ws.iter_rows():
        for celda in fila:
            v = celda.value
            if isinstance(v, str) and v.startswith("=") and "!" in v:
                m = re.match(r"^=\+?'?([^'!]+)'?!", v)
                if m and m.group(1) not in wb.sheetnames:
                    celda.value = NA


def _normalizar_titulo(texto: Any) -> str:
    texto = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode().upper()
    texto = re.sub(r"\(\*+\)", " ", texto.strip().lstrip("-"))
    return re.sub(r"[^A-Z0-9%]+", " ", texto).strip()


def _llenar_estandares(wb, db: Session, anio: str, mes: int) -> None:
    """Hoja Estandares con el estándar y el % Acept del mes de corte (cambian de un mes a otro). Cada bloque de la
    plantilla (título "- INDICADOR", fila Nivel con las claves, fila Estandar y filas de % Acept) se llena con el
    indicador del mismo título; la columna P lleva la tolerancia del mes."""
    if "Estandares" not in wb.sheetnames:
        return
    ws = wb["Estandares"]
    datos = queryEstandaresExcelTMI(db, int(anio), mes)
    por_titulo = {_normalizar_titulo(i["titulo_hoja"] or i["indicador"]): i for i in datos}
    ws["B3"] = f"ESTANDARES DE INDICADORES - {MESES_NOMBRE[mes - 1]} {anio}"
    fila, ultima = 1, ws.max_row
    while fila <= ultima:
        titulo = ws.cell(fila, 3).value
        if not (isinstance(titulo, str) and titulo.strip().startswith("-")
                and str(ws.cell(fila + 1, 3).value or "").strip().upper() == "NIVEL"):
            fila += 1
            continue
        ind = por_titulo.get(_normalizar_titulo(titulo))
        cab, f_est = fila + 1, fila + 2
        filas_acept = [f for f in range(f_est + 1, f_est + 3)
                       if "ACEPT" in str(ws.cell(f, 3).value or "").upper()]
        fila = (filas_acept[-1] if filas_acept else f_est) + 1
        if ind is None:
            logger.warning("Hoja Estandares: el bloque %r no corresponde a ningún indicador activo", titulo)
            continue
        tol, tol_menos = ind["tolerancia"] or 0, ind["tolerancia_menos"] or 0
        rel = (ind["tipo_tolerancia"] or "REL") != "ABS"
        for col in range(4, 15):   # D..N
            clave = str(ws.cell(cab, col).value or "").strip()
            if not clave:
                continue
            if clave.upper().startswith("NIVEL "):
                clave = clave[6:].strip()   # "Nivel III" -> III
            est = ind["estandares"].get(clave)
            ws.cell(f_est, col).value = est
            letra = ws.cell(f_est, col).column_letter
            for k, f in enumerate(filas_acept):
                # banda: 1.a fila = límite de arriba (% No Acept. MAS), 2.a = de abajo (MENOS)
                arriba = ind["sentido"] == "MENOR" or (ind["sentido"] == "BANDA" and k == 0)
                t = tol if arriba or ind["sentido"] != "BANDA" else tol_menos
                if est is None:
                    ws.cell(f, col).value = None
                elif rel:
                    ws.cell(f, col).value = f"=+{letra}{f_est}*{round(1 + t if arriba else 1 - t, 10)}"
                else:
                    ws.cell(f, col).value = f"=+{letra}{f_est}{'+' if arriba else '-'}{t}"
        for k, f in enumerate(filas_acept):
            ws.cell(f, 16).value = tol_menos if ind["sentido"] == "BANDA" and k == 1 else tol


def generar_excel_tmi_dinamico(db: Session, periodo: str, calcular: bool = True,
                               ids: Optional[List[int]] = None, origen: Optional[str] = None) -> io.BytesIO:
    """Genera el libro TMI del periodo AAAAMM.
    calcular: se mantiene por compatibilidad; ya no cambia nada (el resultado se calcula en tiempo real).
    ids: indicadores que lleva el Excel (sus hojas y los puntajes); None = todos los calculados.
    origen: ACTUAL = TOTALIZADO3 de hoy; BACKUP = la copia del cierre; None = ACTUAL. Siempre en tiempo real."""
    from src.main.service.excelPuntajesServ import llenar_puntajes

    p = _validar_periodo(periodo)
    anio, mes = periodo[:4], p % 100
    # el Excel sale del cálculo en tiempo real (ACTUAL con TOTALIZADO3 de hoy, o BACKUP con la copia del cierre)
    filas_final = queryResultadoFinalTMI(db, p, origen)
    if not filas_final:
        raise ValueError(f"No hay resultado del periodo {periodo}: ningún indicador activo tiene centros en ese periodo.")
    final: Dict[int, Dict[int, Dict[str, Any]]] = defaultdict(dict)
    centros_por_cod: Dict[int, Dict[str, Any]] = {}
    for r in filas_final:   # vienen ordenadas por orden_red, orden
        final[r["id_indicador"]][r["codcentro"]] = r
        centros_por_cod.setdefault(r["codcentro"], {
            "codcentro": r["codcentro"], "centro": r["centro"], "red": r["red"], "orden": r["orden_red"],
            "id_centro": r["orden"], "nivel": r["nivel"], "categoria": r["categoria"], "tipo": r["tipo"]})
    centros = list(centros_por_cod.values())
    # indicadores calculados en el periodo (en el orden actual de tmi_indicador)
    indicadores = [i for i in queryIndicadoresActivosTMI(db) if i["id"] in final]
    if not indicadores:
        raise ValueError(f"Los indicadores calculados en {periodo} ya no están activos en tmi_indicador.")
    if ids is not None:
        indicadores = [i for i in indicadores if i["id"] in set(ids)]
        if not indicadores:
            raise ValueError(f"Ninguno de los indicadores elegidos tiene resultado en {periodo}.")
    res: Dict[int, Dict[int, Dict[int, Dict[str, Any]]]] = defaultdict(lambda: defaultdict(dict))
    for r in queryResultadoTMI(db, p, origen):
        res[r["id_indicador"]][r["codcentro"]][r["mes"]] = r

    wb = load_workbook(PLANTILLA_BASE)
    modelo = wb[MODELO_INDICADOR]
    _quitar_columnas_modelo(modelo, COL_QUITAR, CANT_QUITAR)   # una vez: todas las hojas salen de este modelo
    hoja_origen: Dict[str, str] = {}
    resultados = []
    for ind in indicadores:
        resultados.append(_llenar_indicador(wb, modelo, ind, centros, final[ind["id"]], res.get(ind["id"], {}), anio, mes))
        hoja_origen[ind["nombre_hoja"]] = MODELO_INDICADOR

    # Puntajes por centro (bloques por red) y por red
    titulos = [{"codigo": i["codigo"], "titulo": (i["indicador"] or "").strip().title(), "grupo": i["grupo"] or ""}
               for i in indicadores]
    filas_centro: List[Dict[str, Any]] = []
    filas_red: List[Dict[str, Any]] = []
    for red in _orden_redes(centros):
        filas_de_red: List[Dict[str, Any]] = []
        for c in (c for c in centros if (c["red"] or "") == red):
            datos = [r["centros"].get(c["codcentro"]) for r in resultados]
            if all(d is None for d in datos):
                continue
            datos = [d or {"p": NA, "m": [NA] * 12, "sin_prod": True} for d in datos]
            filas_de_red.append({"tipo_fila": "CENTRO", "codcentro": c["codcentro"], "nombre": c["centro"],
                                 "nivel": c["nivel"], "tipo": c["tipo"], "agrupar": _es_red(red),
                                 "puntajes": [d["p"] for d in datos], "mensuales": [d["m"] for d in datos],
                                 # producción NA en todos los indicadores: fila oculta (con producción 0 se ve)
                                 "oculto": all(d["sin_prod"] for d in datos)})
        if _es_red(red):
            if all(red not in r["redes"] for r in resultados):
                continue
            datos_red = [r["redes"].get(red, {"p": NA, "m": [NA] * 12}) for r in resultados]
            fila_red = {"tipo_fila": "RED", "codcentro": None, "nombre": red, "nivel": None, "tipo": None,
                        "puntajes": [d["p"] for d in datos_red], "mensuales": [d["m"] for d in datos_red],
                        "oculto": all(f["oculto"] for f in filas_de_red)}
            filas_centro.append(fila_red)
            filas_red.append(dict(fila_red))
        for fila in filas_de_red:
            filas_centro.append(fila)
            if not _es_red(red):   # institutos: en Puntajes_RED van como fila propia
                filas_red.append(dict(fila, tipo_fila="RED"))

    pun = llenar_puntajes(wb, MODELO_PUNTAJES, "Puntajes", titulos, filas_centro, anio, mes, por_centro=True)
    pun_red = llenar_puntajes(wb, MODELO_PUNTAJES_RED, "Puntajes_RED", titulos, filas_red, anio, mes, por_centro=False)
    for hoja, nombre_modelo in ((pun, MODELO_PUNTAJES), (pun_red, MODELO_PUNTAJES_RED)):
        _copiar_imagenes(wb[nombre_modelo], hoja)
        hoja_origen[hoja.title] = nombre_modelo

    _actualizar_resumen(wb, anio, mes)
    _llenar_estandares(wb, db, anio, mes)
    for nombre in (MODELO_INDICADOR, MODELO_PUNTAJES, MODELO_PUNTAJES_RED):
        wb.remove(wb[nombre])
    wb.active = wb.sheetnames.index("Resumen")

    buffer = io.BytesIO()
    wb.save(buffer)
    hoja_origen = {hoja: HOJA_ORIGINAL.get(modelo, modelo) for hoja, modelo in hoja_origen.items()}
    return io.BytesIO(_restaurar_dibujos(buffer.getvalue(), PLANTILLA_DIBUJOS, hoja_origen))
