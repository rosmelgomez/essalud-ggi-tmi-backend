"""Crea TMI_PLANTILLA_BASE.xlsx (plantilla vacía) a partir de TMI_PLANTILLA.xlsx.

    python src/resources/plantillas/crear_plantilla_base.py

La plantilla base no tiene datos ni filas de centros. Conserva Resumen, Estandares, Definición y tres hojas
modelo ocultas que el generador (excelDinamicoServ.py) copia en tiempo de ejecución:
  _MODELO_INDICADOR    filas 1-9 encabezado, fila 8 TOTAL NACIONAL, fila 10 modelo RED, fila 11 modelo CENTRO
                       y en E11 las reglas de formato condicional (verde / ámbar / rojo según el puntaje)
  _MODELO_PUNTAJES     encabezado + fila 10 modelo RED + fila 11 modelo CENTRO
  _MODELO_PUNTAJES_RED encabezado + fila 10 modelo RED
"""

from pathlib import Path

from openpyxl import load_workbook
from openpyxl.formatting.formatting import ConditionalFormattingList

DIR = Path(__file__).resolve().parent
ORIGEN = DIR / "TMI_PLANTILLA.xlsx"
DESTINO = DIR / "TMI_PLANTILLA_BASE.xlsx"

HOJA_MODELO_INDICADOR = "H_% O.Cama"      # tiene la columna N (Rojo +); el generador la oculta si no es BANDA
FIJAS = {"Resumen", "Estandares", "Definición", "Definición_", "Puntajes", "Puntajes_RED", HOJA_MODELO_INDICADOR}


def _limpiar_valores(ws, filas, desde_col=1):
    for r in filas:
        for c in range(desde_col, ws.max_column + 1):
            ws.cell(r, c).value = None


def main():
    wb = load_workbook(ORIGEN)

    # 1. Hojas de indicador: queda una sola como modelo
    for ws in list(wb.worksheets):
        if ws.title not in FIJAS:
            wb.remove(ws)

    ind = wb[HOJA_MODELO_INDICADOR]
    ind.title = "_MODELO_INDICADOR"
    reglas = list(ind.conditional_formatting)[0].rules
    if ind.max_row > 11:
        ind.delete_rows(12, ind.max_row - 11)
    ind["C3"] = None                     # título del indicador
    ind["S5"] = None                     # AÑO
    ind["C8"] = None                     # puntaje nacional
    _limpiar_valores(ind, [10, 11])
    ind.conditional_formatting = ConditionalFormattingList()
    for regla in reglas:                 # se guardan en E11; el generador las copia al rango escrito
        ind.conditional_formatting.add("E11", regla)

    # 2. Puntajes y Puntajes_RED sin datos
    pun = wb["Puntajes"]
    pun.title = "_MODELO_PUNTAJES"
    if pun.max_row > 11:
        pun.delete_rows(12, pun.max_row - 11)
    _limpiar_valores(pun, [10, 11])
    pun["AG5"] = None

    red = wb["Puntajes_RED"]
    red.title = "_MODELO_PUNTAJES_RED"
    if red.max_row > 10:
        red.delete_rows(11, red.max_row - 10)
    _limpiar_valores(red, [10])
    red["AE5"] = None

    for ws in (ind, pun, red):
        ws.sheet_state = "hidden"
    wb["Resumen"]["B9"] = None
    wb.active = wb.sheetnames.index("Resumen")
    wb.save(DESTINO)
    print(f"Plantilla creada: {DESTINO}")


if __name__ == "__main__":
    main()
