"""Hojas "Puntajes" y "Puntajes_RED" del TMI con un número variable de indicadores.

Las hojas se arman a partir de los modelos ocultos de la plantilla
(_MODELO_PUNTAJES y _MODELO_PUNTAJES_RED). Como el número de indicadores puede
cambiar, las columnas de indicadores, totales y meses se reconstruyen en tiempo de
ejecución copiando estilos y anchos de las columnas modelo.

Layout del modelo:
- Fila 3..6: encabezados. Indicador: título en fila 3 (merge filas 3-5) y grupo en
  fila 6 (merge horizontal por bloque). Totales: merge filas 3-6. Meses: "AÑO: aaaa"
  en fila 5 (merge sobre los 12 meses) y Ene..Dic en fila 6.
- Fila 10: estilo de fila RED; fila 11: estilo de fila CENTRO (solo por centro).
"""

from copy import copy
from typing import Any, Dict, List, Optional

from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

NA = "NA"
MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
TOTALES = ["Cantidad de Indicadores", "Puntaje Total", "Puntaje Máximo", "%", "Puntaje"]
FILA_TITULO, FILA_GRUPO, FILA_ANIO, FILA_MES = 3, 6, 5, 6
FILA_ENC_FIN = 9          # filas 1..9: zona de encabezado (estilos por columna)
FILA_DATOS = 10
FILA_MODELO_RED, FILA_MODELO_CENTRO = 10, 11
N_TOTALES, N_MESES = 5, 12


def _num(valor: Any) -> Optional[float]:
    if isinstance(valor, bool) or valor is None:
        return None
    if isinstance(valor, (int, float)):
        return float(valor)
    try:
        from decimal import Decimal
        if isinstance(valor, Decimal):
            return float(valor)
    except ImportError:  # pragma: no cover
        pass
    return None


def _es_num(valor: Any) -> bool:
    return _num(valor) is not None


def calcular_totales(puntajes: List[Any], mensuales: List[List[Any]], mes: int) -> List[float]:
    """[cantidad, total, máximo, %, puntaje/20] + 12 notas mensuales."""
    nums = [_num(p) for p in puntajes if _es_num(p)]
    cantidad, total = len(nums), sum(nums)
    maximo = cantidad * 5
    pct = total / maximo if maximo else 0
    notas = []
    for k in range(12):
        if k < mes:
            vals = [_num(m[k]) for m in mensuales if m is not None and k < len(m) and _es_num(m[k])]
            notas.append(sum(vals) / (len(vals) * 5) * 20 if vals else 0)
        else:
            notas.append(0)
    return [cantidad, total, maximo, pct, pct * 20] + notas


def _copiar_estilo(origen, destino) -> None:
    if origen.has_style:
        destino._style = copy(origen._style)
    else:
        destino.style = "Normal"


def _limpiar(celda) -> None:
    if type(celda).__name__ == "MergedCell":
        return
    celda.value = None
    celda.style = "Normal"


def _ancho(ws: Worksheet, col: int) -> Optional[float]:
    """Ancho efectivo de una columna considerando dimensiones agrupadas (min..max)."""
    for dim in ws.column_dimensions.values():
        if dim.min is not None and dim.max is not None and dim.min <= col <= dim.max:
            return dim.width
    return None


def _oculta(ws: Worksheet, col: int) -> bool:
    for dim in ws.column_dimensions.values():
        if dim.min is not None and dim.max is not None and dim.min <= col <= dim.max:
            return bool(dim.hidden)
    return False


def _buscar_col_totales(modelo: Worksheet, desde: int) -> int:
    for c in range(desde, modelo.max_column + 1):
        v = modelo.cell(FILA_TITULO, c).value
        if isinstance(v, str) and v.strip().lower() == "cantidad de indicadores":
            return c
    raise ValueError(f"No se encontró 'Cantidad de Indicadores' en la fila {FILA_TITULO} de {modelo.title}")


def llenar_puntajes(wb, nombre_modelo: str, nombre_hoja: str, indicadores: List[Dict[str, Any]],
                    filas: List[Dict[str, Any]], anio: str, mes: int, por_centro: bool) -> Worksheet:
    modelo = wb[nombre_modelo]
    ws = wb.copy_worksheet(modelo)
    ws.title = nombre_hoja
    ws.sheet_state = "visible"

    col_cod, col_nombre, col_nivel, col_tipo = 3, 4, 5, 6
    ini = 7 if por_centro else 5                       # primera columna de indicador
    m_tot = _buscar_col_totales(modelo, ini)           # columnas modelo
    m_mes = m_tot + N_TOTALES
    m_fin = m_mes + N_MESES - 1
    m_ind_alt = ini + 1 if ini + 1 < m_tot else ini    # 2ª columna de indicador del modelo

    n = len(indicadores)
    tot = ini + n
    mes_ini = tot + N_TOTALES
    ultima = mes_ini + N_MESES - 1

    def col_modelo(c: int) -> int:
        if c < ini:
            return c
        if c < tot:
            return ini
        if c < mes_ini:
            return m_tot + (c - tot)
        return m_mes + (c - mes_ini)

    max_col = max(ws.max_column, modelo.max_column, ultima, m_fin + 2)
    max_row = max(ws.max_row, modelo.max_row)

    # --- merges: quitar los de encabezado desde la 1ª columna de indicador, los de datos y los sobrantes
    for rango in list(ws.merged_cells.ranges):
        en_encabezado = rango.max_row >= FILA_TITULO and rango.min_row <= FILA_GRUPO and rango.max_col >= ini
        if en_encabezado or rango.max_row >= FILA_DATOS or rango.max_col > ultima:
            ws.unmerge_cells(str(rango))

    # --- zona de encabezado (filas 1..9) desde la 1ª columna de indicador: estilos y valores
    for r in range(1, FILA_ENC_FIN + 1):
        for c in range(ini, max_col + 1):
            celda = ws.cell(r, c)
            if c > ultima:
                _limpiar(celda)
                continue
            mc = col_modelo(c)
            origen = modelo.cell(r, mc)
            if ini <= c < tot and not origen.has_style:
                origen = modelo.cell(r, m_ind_alt)
            _copiar_estilo(origen, celda)
            celda.value = None  # los encabezados se escriben abajo

    for i, ind in enumerate(indicadores):
        ws.cell(FILA_TITULO, ini + i, value=ind.get("titulo"))
        ws.merge_cells(start_row=FILA_TITULO, start_column=ini + i, end_row=FILA_ANIO, end_column=ini + i)
    i = 0
    while i < n:
        j = i
        grupo = indicadores[i].get("grupo")
        while j + 1 < n and indicadores[j + 1].get("grupo") == grupo:
            j += 1
        ws.cell(FILA_GRUPO, ini + i, value=grupo)
        if j > i:
            ws.merge_cells(start_row=FILA_GRUPO, start_column=ini + i, end_row=FILA_GRUPO, end_column=ini + j)
        i = j + 1
    for k in range(N_TOTALES):
        etiqueta = modelo.cell(FILA_TITULO, m_tot + k).value or TOTALES[k]
        ws.cell(FILA_TITULO, tot + k, value=etiqueta)
        ws.merge_cells(start_row=FILA_TITULO, start_column=tot + k, end_row=FILA_GRUPO, end_column=tot + k)
    ws.cell(FILA_ANIO, mes_ini, value=f"AÑO: {anio}")
    ws.merge_cells(start_row=FILA_ANIO, start_column=mes_ini, end_row=FILA_ANIO, end_column=ultima)
    for k in range(N_MESES):
        ws.cell(FILA_MES, mes_ini + k, value=modelo.cell(FILA_MES, m_mes + k).value or MESES[k])

    # --- anchos de columna desde la 1ª columna de indicador
    for clave in list(ws.column_dimensions.keys()):
        dim = ws.column_dimensions[clave]
        if dim.min is not None and dim.max is not None and dim.max >= ini:
            if dim.min < ini:  # dimensión agrupada que cruza el inicio: recortar
                dim.max = ini - 1
            else:
                del ws.column_dimensions[clave]
    for c in range(ini, ultima + 2):
        mc = col_modelo(c) if c <= ultima else m_fin + 1
        letra = get_column_letter(c)
        dim = ws.column_dimensions[letra]
        dim.min = dim.max = c
        ancho = _ancho(modelo, mc)
        if ancho is not None:
            dim.width = ancho
        if _oculta(modelo, mc):
            dim.hidden = True

    # --- datos
    for r in range(FILA_DATOS, max_row + 1):
        for c in range(1, max_col + 1):
            _limpiar(ws.cell(r, c))
    for fr in [fr for fr in ws.row_dimensions if fr >= FILA_DATOS]:   # ocultas/agrupadas de la plantilla
        del ws.row_dimensions[fr]

    fila_modelo_centro = FILA_MODELO_CENTRO if por_centro else FILA_MODELO_RED
    r = FILA_DATOS
    anterior = None
    for fila in filas:
        es_red = str(fila.get("tipo_fila", "")).upper() == "RED"
        if por_centro and es_red and anterior == "CENTRO":
            if fila.get("oculto"):
                ws.row_dimensions[r].hidden = True
            r += 1  # fila en blanco antes de la siguiente red
        rm =FILA_MODELO_RED if es_red else fila_modelo_centro
        for c in range(1, ultima + 1):
            _copiar_estilo(modelo.cell(rm, col_modelo(c)), ws.cell(r, c))
        altura = modelo.row_dimensions[rm].height
        if altura is not None:
            ws.row_dimensions[r].height = altura
        if por_centro and not es_red and fila.get("agrupar"):   # centro agrupado bajo la fila de su red
            ws.row_dimensions[r].outline_level = 1
        if fila.get("oculto"):   # NA en todos los indicadores: queda en la hoja pero oculta
            ws.row_dimensions[r].hidden = True

        ws.cell(r, col_nombre, value=fila.get("nombre"))
        if por_centro and not es_red:
            ws.cell(r, col_cod, value=fila.get("codcentro"))
            ws.cell(r, col_nivel, value=fila.get("nivel"))
            ws.cell(r, col_tipo, value=fila.get("tipo"))

        puntajes = list(fila.get("puntajes") or [])
        puntajes = (puntajes + [NA] * n)[:n]
        mensuales = list(fila.get("mensuales") or [])
        for i, p in enumerate(puntajes):
            ws.cell(r, ini + i, value=p)
        for k, v in enumerate(calcular_totales(puntajes, mensuales, mes)):
            ws.cell(r, tot + k, value=v)
        anterior = "RED" if es_red else "CENTRO"
        r += 1

    ws.freeze_panes = modelo.freeze_panes
    return ws
