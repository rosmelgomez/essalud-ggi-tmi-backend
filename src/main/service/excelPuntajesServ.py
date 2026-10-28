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
    """[cantidad, total, máximo, %, puntaje/20] + 12 notas mensuales (misma regla que excelServ)."""
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

    fila_modelo_centro = FILA_MODELO_CENTRO if por_centro else FILA_MODELO_RED
    r = FILA_DATOS
    anterior = None
    for fila in filas:
        es_red = str(fila.get("tipo_fila", "")).upper() == "RED"
        if por_centro and es_red and anterior == "CENTRO":
            r += 1  # fila en blanco antes de la siguiente red
        rm = FILA_MODELO_RED if es_red else fila_modelo_centro
        for c in range(1, ultima + 1):
            _copiar_estilo(modelo.cell(rm, col_modelo(c)), ws.cell(r, c))
        altura = modelo.row_dimensions[rm].height
        if altura is not None:
            ws.row_dimensions[r].height = altura

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


if __name__ == "__main__":
    import os
    import tempfile
    from pathlib import Path

    from openpyxl import load_workbook

    plantilla = Path(__file__).resolve().parents[2] / "resources" / "plantillas" / "TMI_PLANTILLA_BASE.xlsx"
    wb = load_workbook(plantilla)

    inds = [
        {"codigo": "I1", "titulo": "Concentracion De Consultas", "grupo": "Consulta Externa"},
        {"codigo": "I2", "titulo": "Rendimiento Hora Medico", "grupo": "Consulta Externa"},
        {"codigo": "I3", "titulo": "Promedio Dia Estancia", "grupo": "Hospitalización"},
        {"codigo": "I4", "titulo": "Porcentaje De Ocupacion De Cama", "grupo": "Hospitalización"},
        {"codigo": "I5", "titulo": "Rendimiento Cama", "grupo": "Hospitalización"},
    ]

    def mens(base):
        return [[(base + i) % 6 if k < 7 else None for k in range(12)] for i in range(5)]

    filas_c, filas_r = [], []
    for nr, red in enumerate(["RED A", "RED B"]):
        pr = [5, 3, NA, 1, 5] if nr == 0 else [3, 3, 3, 3, 3]
        mr = mens(nr)
        mr[2] = [NA] * 12
        filas_r.append({"tipo_fila": "RED", "codcentro": None, "nombre": red, "nivel": None, "tipo": None,
                        "puntajes": pr, "mensuales": mr})
        filas_c.append(dict(filas_r[-1]))
        for k in range(3):
            filas_c.append({"tipo_fila": "CENTRO", "codcentro": 100 * (nr + 1) + k, "nombre": f"Centro {nr}-{k}",
                            "nivel": "II", "tipo": "H", "puntajes": [5, 5, 3, NA, 1],
                            "mensuales": mens(k + 1)})

    llenar_puntajes(wb, "_MODELO_PUNTAJES", "Puntajes", inds, filas_c, "2026", 7, True)
    llenar_puntajes(wb, "_MODELO_PUNTAJES_RED", "Puntajes_RED", inds, filas_r, "2026", 7, False)
    fd, ruta = tempfile.mkstemp(suffix=".xlsx")
    os.close(fd)
    wb.save(ruta)

    wb2 = load_workbook(ruta)
    assert wb2.sheetnames[-2:] == ["Puntajes", "Puntajes_RED"], wb2.sheetnames
    assert "_MODELO_PUNTAJES" in wb2.sheetnames and "_MODELO_PUNTAJES_RED" in wb2.sheetnames

    def verificar(ws, ini, filas, por_centro):
        assert ws.sheet_state == "visible"
        merges = {str(m) for m in ws.merged_cells.ranges}
        L = get_column_letter
        tot, mes_ini = ini + 5, ini + 10
        ultima = mes_ini + 11
        for i in range(5):
            assert ws.cell(3, ini + i).value == inds[i]["titulo"]
            assert f"{L(ini + i)}3:{L(ini + i)}5" in merges
        assert ws.cell(6, ini).value == "Consulta Externa" and ws.cell(6, ini + 2).value == "Hospitalización"
        assert f"{L(ini)}6:{L(ini + 1)}6" in merges and f"{L(ini + 2)}6:{L(ini + 4)}6" in merges
        for k, t in enumerate(TOTALES):
            assert ws.cell(3, tot + k).value == t, (ws.cell(3, tot + k).value, t)
            assert f"{L(tot + k)}3:{L(tot + k)}6" in merges
        assert ws.cell(5, mes_ini).value == "AÑO: 2026"
        assert f"{L(mes_ini)}5:{L(ultima)}5" in merges
        assert [ws.cell(6, mes_ini + k).value for k in range(12)] == MESES
        assert all(m.max_col <= ultima for m in ws.merged_cells.ranges), merges
        for r in range(1, ws.max_row + 1):
            for c in range(ultima + 1, ws.max_column + 1):
                assert ws.cell(r, c).value is None, (r, c, ws.cell(r, c).value)
        assert ws.freeze_panes == wb2["_MODELO_PUNTAJES" if por_centro else "_MODELO_PUNTAJES_RED"].freeze_panes
        assert ws.column_dimensions[L(ini + 4)].width == ws.column_dimensions[L(ini)].width
        # filas de datos
        r = 10
        anterior = None
        usadas = 0
        for f in filas:
            if por_centro and f["tipo_fila"] == "RED" and anterior == "CENTRO":
                assert all(ws.cell(r, c).value is None for c in range(1, ultima + 1)), r
                r += 1
            assert ws.cell(r, 4).value == f["nombre"]
            if por_centro and f["tipo_fila"] == "CENTRO":
                assert ws.cell(r, 3).value == f["codcentro"] and ws.cell(r, 5).value == "II" and ws.cell(r, 6).value == "H"
            assert [ws.cell(r, ini + i).value for i in range(5)] == f["puntajes"]
            esperado = calcular_totales(f["puntajes"], f["mensuales"], 7)
            obtenido = [ws.cell(r, tot + k).value for k in range(17)]
            assert all(abs(a - b) < 1e-9 for a, b in zip(obtenido, esperado)), (r, obtenido, esperado)
            assert all(v == 0 for v in obtenido[5 + 7:])
            anterior = f["tipo_fila"]
            r += 1
            usadas += 1
        assert all(ws.cell(rr, 4).value is None for rr in range(r, ws.max_row + 1))
        return r

    ws_c = wb2["Puntajes"]
    fin = verificar(ws_c, 7, filas_c, True)
    assert fin == 10 + len(filas_c) + 1, fin  # 8 filas + 1 en blanco entre redes
    # valores concretos: RED A -> puntajes 5,3,NA,1,5 => cantidad 4, total 14, máx 20, 70%, 14
    assert [ws_c.cell(10, c).value for c in range(12, 17)] == [4, 14, 20, 0.7, 14.0]
    # centro: 5,5,3,NA,1 => 4, 14, 20, 0.7, 14
    assert [ws_c.cell(11, c).value for c in range(12, 17)] == [4, 14, 20, 0.7, 14.0]
    # nota mensual Ene de Centro 0-0 (mens(1)): valores 1,2,3,4,5 => 15/25*20 = 12
    assert abs(ws_c.cell(11, 17).value - 12.0) < 1e-9
    # RED A Ene (mens(0) con indicador 3 en NA): 0,1,3,4 => 8/20*20 = 8
    assert abs(ws_c.cell(10, 17).value - 8.0) < 1e-9
    assert ws_c.cell(14, 4).value is None and ws_c.cell(15, 4).value == "RED B"
    assert ws_c.cell(10, 7).number_format == wb2["_MODELO_PUNTAJES"]["G10"].number_format
    assert ws_c.cell(11, 7).number_format == wb2["_MODELO_PUNTAJES"]["G11"].number_format

    ws_r = wb2["Puntajes_RED"]
    fin = verificar(ws_r, 5, filas_r, False)
    assert fin == 12
    assert [ws_r.cell(11, c).value for c in range(10, 15)] == [5, 15, 25, 0.6, 12.0]
    assert ws_r.column_dimensions["C"].hidden

    os.remove(ruta)
    print("OK: Puntajes y Puntajes_RED verificados")
