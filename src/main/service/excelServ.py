"""Generación del Excel del TMI (Tablero de Monitoreo de Gestión) a partir de las
consultas de vistas (CE_Concent hacia abajo) de src/main/repositories/tmiRep.py.

Replica, para un periodo dado, la estructura de TMI_Prelim_Salud_Julio_2026.xlsx:
una hoja por indicador, agrupada por Red Asistencial / Establecimiento, con las
columnas Nivel, Tipo, Valor Real, Estandar, Verde/Rojo y el detalle mensual Ene-Dic.

Nota: la columna "Puntaje" (semáforo de 1 a 5) y las filas "TOTAL NACIONAL" /
"RED ASISTENCIAL ..." del archivo original se calculan en una vista aparte
(TMI_PUNTAJES_CENTRO_INDICADORES, fuera de la sección "consulta de vistas") y no
están disponibles en estas consultas, por lo que aquí se dejan en blanco.
"""

import io
from typing import Any, Callable, Dict, List, Optional

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from sqlalchemy.orm import Session

from src.main.service.tmiServ import (
    queryCE_ConcentServ,
    queryCE_RHrMedicoServ,
    queryCE_GCHProgServ,
    queryCE_RecetasServ,
    queryH_EstanciasServ,
    queryH_OCamasServ,
    queryH_ISustServ,
    queryH_RCamaServ,
    queryH_TBMHospServ,
    queryQx_IMenorServ,
    queryQx_IAltaServ,
    queryQx_GCHProgServ,
    queryQx_RendSOServ,
    queryQx_IntSuspServ,
    queryQx_HTCesareasServ,
    queryEm_PrioIV_VServ,
    queryEm_PrioI_IIServ,
    queryO_ConcentServ,
    queryO_HrOdontServ,
    queryO_GCHOdonServ,
    queryO_NTOdontSServ,
)

MESES_LABEL = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

# Orden y metadatos de cada hoja, replicando TMI_Prelim_Salud_Julio_2026.xlsx.
# doble_banda=True => el indicador tiene rango de aceptación (Rojo -/Rojo +),
# como Porcentaje de Ocupación de Cama.
REPORTS: List[Dict[str, Any]] = [
    {"sheet": "C.E_Concent.", "titulo": "CONCENTRACION DE CONSULTAS", "fn": queryCE_ConcentServ, "doble_banda": False},
    {"sheet": "C.E_R.Hr.Medico", "titulo": "RENDIMIENTO HORA MEDICO", "fn": queryCE_RHrMedicoServ, "doble_banda": False},
    {"sheet": "C.E_G.C.H.Prog", "titulo": "GRADO DE CUMPLIMIENTO DE HORAS PROGRAMADAS", "fn": queryCE_GCHProgServ, "doble_banda": False},
    {"sheet": "C.E_Recetas", "titulo": "PROMEDIO DE RECETAS POR CONSULTAS", "fn": queryCE_RecetasServ, "doble_banda": False},
    {"sheet": "H_Estancias", "titulo": "PROMEDIO DIA ESTANCIA", "fn": queryH_EstanciasServ, "doble_banda": False},
    {"sheet": "H_% O.Cama", "titulo": "PORCENTAJE DE OCUPACION DE CAMA", "fn": queryH_OCamasServ, "doble_banda": True},
    {"sheet": "H_I.Sust.", "titulo": "INTERVALO DE SUSTITUCION", "fn": queryH_ISustServ, "doble_banda": False},
    {"sheet": "H_R.Cama", "titulo": "RENDIMIENTO CAMA", "fn": queryH_RCamaServ, "doble_banda": False},
    {"sheet": "H_T.B.M.Hosp", "titulo": "TASA NETA DE MORTALIDAD HOSPITALARIA", "fn": queryH_TBMHospServ, "doble_banda": False},
    {"sheet": "Qx_I.Menor", "titulo": "PORCENTAJE DE INTERVENCIONES MENORES", "fn": queryQx_IMenorServ, "doble_banda": False},
    {"sheet": "Qx_I.Alta", "titulo": "PORCENTAJE DE INTERVENCIONES DE ALTA COMPLEJIDAD", "fn": queryQx_IAltaServ, "doble_banda": False},
    {"sheet": "Qx_G.C.H.Prog", "titulo": "PORCENTAJE DE HORAS QUIRURGICAS EFECTIVAS", "fn": queryQx_GCHProgServ, "doble_banda": False},
    {"sheet": "Qx_Rend.SO", "titulo": "RENDIMIENTO DE SALA DE OPERACIONES", "fn": queryQx_RendSOServ, "doble_banda": False},
    {"sheet": "Qx.Int.Susp", "titulo": "PORCENTAJE DE OPERACIONES SUSPENDIDAS", "fn": queryQx_IntSuspServ, "doble_banda": False},
    {"sheet": "H_T.Cesareas", "titulo": "TASA DE CESAREAS", "fn": queryQx_HTCesareasServ, "doble_banda": False},
    {"sheet": "Em_Prio.IV_V", "titulo": "% PRIORIDAD IV y V CON RESPECTO AL TOTAL DE EMERGENCIAS", "fn": queryEm_PrioIV_VServ, "doble_banda": False},
    {"sheet": "Em_Prio.I_II", "titulo": "% PRIORIDAD I Y II CON RESPECTO AL TOTAL DE EMERGENCIAS", "fn": queryEm_PrioI_IIServ, "doble_banda": False},
    {"sheet": "O_Concent.", "titulo": "CONCENTRACIÓN DE SESIONES ODONTOLÓGICAS", "fn": queryO_ConcentServ, "doble_banda": False},
    {"sheet": "O_Hr.Odont", "titulo": "RENDIMIENTO HORA ODONTOLÓGICA", "fn": queryO_HrOdontServ, "doble_banda": False},
    {"sheet": "O_G.C.H.Odon", "titulo": "GRADO DE CUMPLIMIENTO DE HORA ODONTÓLOGO", "fn": queryO_GCHOdonServ, "doble_banda": False},
    {"sheet": "O_N.T.Odont.S", "titulo": "NÚMERO DE TRABAJOS ODONTOLÓGICOS POR SESIÓN", "fn": queryO_NTOdontSServ, "doble_banda": False},
]

TITLE_FONT = Font(bold=True, size=12)
SUBTITLE_FONT = Font(bold=True, size=11)
HEADER_FONT = Font(bold=True, color="FFFFFF")
HEADER_FILL = PatternFill("solid", fgColor="4472C4")
TOTAL_FONT = Font(bold=True)
TOTAL_FILL = PatternFill("solid", fgColor="FBD5B5")
RED_FONT = Font(bold=True)
RED_FILL = PatternFill("solid", fgColor="D9E1F2")
CENTER = Alignment(horizontal="center", vertical="center")
LEFT = Alignment(horizontal="left", vertical="center")
RIGHT = Alignment(horizontal="right", vertical="center")
THIN_BOTTOM = Border(bottom=Side(style="thin", color="808080"))

FIRST_COL = 3  # columna C: primera columna con datos/banners
FIRST_MONTH_COL = 19  # columna S
LAST_HEADER_COL = FIRST_MONTH_COL + len(MESES_LABEL) - 1  # columna AD

# Anchos de columna calcados de TMI_Prelim_Salud_Julio_2026.xlsx para que
# ninguna cabecera (p.ej. "Red Asistencial / Establecimientos") quede cortada.
COLUMN_WIDTHS: Dict[int, float] = {
    1: 4.3, 2: 3.6, 3: 5.9, 4: 5.7, 5: 4.0, 6: 6.4, 7: 37.1,
    8: 7.6, 9: 6.6, 10: 7.7, 11: 6.7, 12: 4.7, 13: 4.1, 14: 4.7,
    15: 2.0, 16: 2.6, 17: 3.7, 18: 6.3,
}


def _fill_row_banner(ws, row: int, fill: PatternFill) -> None:
    for col in range(FIRST_COL, LAST_HEADER_COL + 1):
        ws.cell(row=row, column=col).fill = fill


def _month_keys(anio: str) -> List[str]:
    return [f"{anio}{m:02d}" for m in range(1, 13)]


def _write_headers(ws, titulo: str, anio: str, doble_banda: bool) -> None:
    ws["C1"] = "CRITERIOS DE EVALUACION"
    ws["C1"].font = TITLE_FONT
    ws["C3"] = titulo
    ws["C3"].font = TITLE_FONT
    ws["S5"] = f"AÑO: {anio}"
    ws["S5"].font = SUBTITLE_FONT

    headers = {
        3: ("Puntaje", CENTER),
        5: ("Red Asistencial / Establecimientos", LEFT),
        8: ("Nivel", RIGHT),
        9: ("Tipo", RIGHT),
        10: ("Valor Real", RIGHT),
        11: ("Estandar", RIGHT),
        12: ("Verde", RIGHT),
        13: ("Rojo -" if doble_banda else "Rojo", RIGHT),
        18: ("Anual ", CENTER),
    }
    if doble_banda:
        headers[14] = ("Rojo +", RIGHT)
    for i, label in enumerate(MESES_LABEL):
        headers[FIRST_MONTH_COL + i] = (label, RIGHT)

    # Rellena TODA la fila (incluyendo columnas sin texto, p.ej. F/G) para que
    # la cabecera se vea como una barra continua, igual que en el original.
    for col in range(FIRST_COL, LAST_HEADER_COL + 1):
        cell = ws.cell(row=6, column=col)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = CENTER
        cell.border = THIN_BOTTOM

    for col, (label, align) in headers.items():
        cell = ws.cell(row=6, column=col, value=label)
        cell.alignment = align

    ws.cell(row=8, column=7, value="TOTAL NACIONAL")
    _fill_row_banner(ws, 8, TOTAL_FILL)
    for col in range(FIRST_COL, LAST_HEADER_COL + 1):
        ws.cell(row=8, column=col).font = TOTAL_FONT


def _write_data(ws, data: List[Dict[str, Any]], anio: str, doble_banda: bool) -> None:
    if not data:
        ws.cell(row=10, column=7, value="Sin datos para el periodo consultado")
        return

    month_keys = _month_keys(anio)

    reds = sorted({(row.get("Red") or "").strip() for row in data if row.get("Red")})

    row_idx = 10
    for red in reds:
        centros = [r for r in data if (r.get("Red") or "").strip() == red]
        centros.sort(key=lambda r: (r.get("ORDEN") or 0, r.get("Centro") or ""))

        ws.cell(row=row_idx, column=7, value=f"RED ASISTENCIAL {red}")
        _fill_row_banner(ws, row_idx, RED_FILL)
        for col in range(FIRST_COL, LAST_HEADER_COL + 1):
            ws.cell(row=row_idx, column=col).font = RED_FONT
        row_idx += 1

        for centro in centros:
            estandar = centro.get("Estandar")
            ws.cell(row=row_idx, column=4, value=centro.get("ORDEN"))
            ws.cell(row=row_idx, column=5, value="=")
            ws.cell(row=row_idx, column=6, value=centro.get("codcentro"))
            ws.cell(row=row_idx, column=7, value=centro.get("Centro"))
            ws.cell(row=row_idx, column=8, value=centro.get("NIVEL"))
            ws.cell(row=row_idx, column=9, value=centro.get("TIPO"))
            ws.cell(row=row_idx, column=10, value=centro.get("Total"))
            ws.cell(row=row_idx, column=11, value=estandar)
            ws.cell(row=row_idx, column=12, value=estandar)
            if doble_banda:
                ws.cell(row=row_idx, column=13, value=centro.get("% Aceptmenos"))
                ws.cell(row=row_idx, column=14, value=centro.get("% Acept"))
            else:
                ws.cell(row=row_idx, column=13, value=centro.get("% Acept"))
            for i, mkey in enumerate(month_keys):
                ws.cell(row=row_idx, column=FIRST_MONTH_COL + i, value=centro.get(mkey))
            row_idx += 1

        row_idx += 1  # fila en blanco entre redes, como en el archivo original


def _autosize(ws) -> None:
    for col, width in COLUMN_WIDTHS.items():
        ws.column_dimensions[get_column_letter(col)].width = width
    for col in range(FIRST_MONTH_COL, LAST_HEADER_COL + 1):
        ws.column_dimensions[get_column_letter(col)].width = 7
    ws.row_dimensions[6].height = 18
    ws.freeze_panes = "C7"


def generar_excel_tmi(db: Session, periodo: str) -> io.BytesIO:
    """Genera el libro TMI completo (una hoja por indicador) para el `periodo` dado.

    `periodo` tiene formato AAAAMM (p.ej. "202607"), igual que el resto de
    endpoints de este microservicio.
    """
    if not periodo or len(periodo) < 4:
        raise ValueError("El periodo debe tener formato AAAAMM.")
    anio = periodo[:4]

    wb = Workbook()
    wb.remove(wb.active)

    for cfg in REPORTS:
        ws = wb.create_sheet(cfg["sheet"][:31])
        doble_banda = cfg["doble_banda"]
        _write_headers(ws, cfg["titulo"], anio, doble_banda)
        data = cfg["fn"](db, periodo)
        _write_data(ws, data, anio, doble_banda)
        _autosize(ws)

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer
