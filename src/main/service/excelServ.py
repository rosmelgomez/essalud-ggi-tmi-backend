"""Generación del Excel del TMI (Tablero de Monitoreo de Gestión) para un periodo.

El libro se arma sobre la plantilla src/resources/plantillas/TMI_PLANTILLA.xlsx
(copia de TMI_Prelim_Salud_Julio_2026.xlsx), de modo que conserva hojas, logos,
estilos, filas/columnas ocultas y formato condicional. Para el periodo consultado
se llenan:

- las 21 hojas de indicadores (valores mensuales, Valor Real, Estándar, Verde/Rojo,
  Puntaje por establecimiento, Puntaje por red y TOTAL NACIONAL),
- Puntajes (por red y establecimiento) y Puntajes_RED,
- el título de Resumen y el año de cada hoja.

Reglas de puntaje (deducidas de TMI_Prelim_Salud_Julio_2026.xlsx):
- Verde = Estándar; Rojo = % Acept (en Ocupación de Cama: Rojo - / Rojo +).
- Indicador de incremento (Rojo < Verde): 5 si valor >= Verde, 3 si >= Rojo, 1 si no.
- Indicador de disminución (Rojo > Verde): 5 si valor <= Verde, 3 si <= Rojo, 1 si no.
- Ocupación de Cama: 5 dentro de la franja media entre Verde y cada Rojo, 3 entre
  Rojo - y Rojo +, 1 fuera.
- Valor 0 => puntaje 0 (sin actividad), salvo en indicadores donde 0 es un buen
  resultado (mortalidad, operaciones suspendidas, cesáreas).
- Sin datos, sin estándar o estándar 0 (no aplica a ese tipo de centro) => "NA".
- Red = promedio de los puntajes de sus establecimientos (3 decimales).
- TOTAL NACIONAL = promedio de las redes, sin las redes "- APP" (3 decimales).
- Puntajes: cantidad de indicadores, puntaje total, máximo (cantidad x 5), % y
  puntaje sobre 20, tanto del periodo como de cada mes.
"""

import io
import logging
import posixpath
import re
import zipfile
from decimal import Decimal
from pathlib import Path
from statistics import mean
from typing import Any, Callable, Dict, List, Optional

from openpyxl import load_workbook
from sqlalchemy.orm import Session

from src.main.repositories.tmiRep import queryCentrosTMI
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

logger = logging.getLogger(__name__)

PLANTILLA = Path(__file__).resolve().parents[2] / "resources" / "plantillas" / "TMI_PLANTILLA.xlsx"

MESES_NOMBRE = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO",
                "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]

# Hojas de indicadores en el orden de la plantilla (y de las columnas de Puntajes).
# doble_banda: Ocupación de Cama (Rojo - / Rojo +).
# cero_valido: el valor 0 es un buen resultado y se evalúa con la regla normal.
# decimales: redondeo del valor antes de compararlo con el estándar.
REPORTS: List[Dict[str, Any]] = [
    {"sheet": "C.E_Concent.", "fn": queryCE_ConcentServ},
    {"sheet": "C.E_R.Hr.Medico", "fn": queryCE_RHrMedicoServ, "decimales": 2},
    {"sheet": "C.E_G.C.H.Prog", "fn": queryCE_GCHProgServ},
    {"sheet": "C.E_Recetas", "fn": queryCE_RecetasServ, "decimales": 2},
    {"sheet": "H_Estancias", "fn": queryH_EstanciasServ},
    {"sheet": "H_% O.Cama", "fn": queryH_OCamasServ, "doble_banda": True},
    {"sheet": "H_I.Sust.", "fn": queryH_ISustServ},
    {"sheet": "H_R.Cama", "fn": queryH_RCamaServ},
    {"sheet": "H_T.B.M.Hosp", "fn": queryH_TBMHospServ, "cero_valido": True},
    {"sheet": "Qx_I.Menor", "fn": queryQx_IMenorServ},
    {"sheet": "Qx_I.Alta", "fn": queryQx_IAltaServ},
    {"sheet": "Qx_G.C.H.Prog", "fn": queryQx_GCHProgServ},
    {"sheet": "Qx_Rend.SO", "fn": queryQx_RendSOServ},
    {"sheet": "Qx.Int.Susp", "fn": queryQx_IntSuspServ, "cero_valido": True},
    {"sheet": "H_T.Cesareas", "fn": queryQx_HTCesareasServ, "cero_valido": True},
    {"sheet": "Em_Prio.IV_V", "fn": queryEm_PrioIV_VServ},
    {"sheet": "Em_Prio.I_II", "fn": queryEm_PrioI_IIServ},
    {"sheet": "O_Concent.", "fn": queryO_ConcentServ},
    {"sheet": "O_Hr.Odont", "fn": queryO_HrOdontServ},
    {"sheet": "O_G.C.H.Odon", "fn": queryO_GCHOdonServ},
    {"sheet": "O_N.T.Odont.S", "fn": queryO_NTOdontSServ},
]

# Columnas de las hojas de indicadores
COL_PUNTAJE, COL_CODIGO, COL_COD, COL_CENTRO = 3, 4, 6, 7
COL_NIVEL, COL_TIPO, COL_VALOR, COL_ESTANDAR, COL_VERDE, COL_ROJO, COL_ROJO_MAS = 8, 9, 10, 11, 12, 13, 14
COL_MES1 = 19  # S
FILA_TOTAL, FILA_DATOS = 8, 10
CODIGO_PUNTAJE = {5: 1, 3: 2, 1: 3, 0: 3}  # columna D (oculta)

NA = "NA"


def _num(valor: Any) -> Optional[float]:
    if isinstance(valor, bool) or valor is None:
        return None
    if isinstance(valor, (int, float, Decimal)):
        return float(valor)
    return None


def _es_num(valor: Any) -> bool:
    return _num(valor) is not None


def _puntaje(cfg: Dict[str, Any], valor: Any, verde: Any, rojo: Any, rojo_mas: Any = None):
    j, v, r = _num(valor), _num(verde), _num(rojo)
    if j is None or v is None or r is None:
        return NA
    if cfg.get("decimales") is not None:
        j = round(j, cfg["decimales"])
    if j == 0 and not cfg.get("cero_valido"):
        return 0
    if cfg.get("doble_banda"):
        rm = _num(rojo_mas)
        if rm is None:
            return NA
        if (v + r) / 2 <= j <= (v + rm) / 2:
            return 5
        return 3 if r <= j <= rm else 1
    if r < v:  # incremento
        return 5 if j >= v else (3 if j >= r else 1)
    return 5 if j <= v else (3 if j <= r else 1)  # disminución


def _promedio(valores: List[Any]):
    nums = [_num(v) for v in valores if _es_num(v)]
    return round(mean(nums), 3) if nums else NA


def _filas_por_codigo(data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    filas: Dict[str, Dict[str, Any]] = {}
    for row in data:
        cod = str(row.get("codcentro") or "").strip()
        # CE_RHrMedico une nivel y tipo: se toma la fila que tenga estándar
        if cod and (cod not in filas or (filas[cod].get("Estandar") is None and row.get("Estandar") is not None)):
            filas[cod] = row
    return filas


def _llenar_indicador(ws, cfg: Dict[str, Any], data: List[Dict[str, Any]], red_de: Dict[str, str],
                      anio: str, mes: int) -> Dict[str, Any]:
    """Llena una hoja de indicador y devuelve los puntajes por centro y por red (periodo y mensuales)."""
    meses = [f"{anio}{m:02d}" for m in range(1, 13)]
    filas = _filas_por_codigo(data)
    doble = cfg.get("doble_banda", False)
    centros: Dict[str, Dict[str, Any]] = {}
    grupos: List[tuple] = []

    ws.cell(row=5, column=COL_MES1, value=f"AÑO: {anio}")
    for r in range(FILA_DATOS, ws.max_row + 1):
        cod_celda = ws.cell(r, COL_COD).value
        nombre = ws.cell(r, COL_CENTRO).value
        if cod_celda is None:
            if isinstance(nombre, str) and nombre.strip().upper().startswith("RED "):
                grupos.append((r, nombre.strip()))
            continue
        cod = str(cod_celda).strip()
        row = filas.get(cod)
        estandar = row.get("Estandar") if row else None

        # sin fila, sin estándar o estándar 0 (el indicador no aplica a ese tipo de centro) => NA
        if row is None or not _num(estandar):
            for c in (COL_PUNTAJE, COL_CODIGO, COL_NIVEL, COL_TIPO, COL_VALOR, COL_ESTANDAR, COL_VERDE, COL_ROJO):
                ws.cell(r, c, value=NA)
            if doble:
                ws.cell(r, COL_ROJO_MAS, value=NA)
            for i in range(12):
                ws.cell(r, COL_MES1 + i, value=NA)
            centros[cod] = {"p": NA, "m": [NA] * 12}
            continue

        rojo = row.get("% Aceptmenos") if doble else row.get("% Acept")
        rojo_mas = row.get("% Acept") if doble else None
        valores = [_num(row.get(k)) for k in meses]
        valor = valores[mes - 1]
        p = _puntaje(cfg, valor, estandar, rojo, rojo_mas)
        mensual = [_puntaje(cfg, valores[i], estandar, rojo, rojo_mas) if i < mes else None for i in range(12)]

        ws.cell(r, COL_PUNTAJE, value=p)
        ws.cell(r, COL_CODIGO, value=CODIGO_PUNTAJE.get(p, NA))
        ws.cell(r, COL_NIVEL, value=row.get("NIVEL"))
        ws.cell(r, COL_TIPO, value=row.get("TIPO"))
        ws.cell(r, COL_VALOR, value=valor if valor is not None else 0)
        ws.cell(r, COL_ESTANDAR, value=_num(estandar))
        ws.cell(r, COL_VERDE, value=_num(estandar))
        ws.cell(r, COL_ROJO, value=_num(rojo))
        if doble:
            ws.cell(r, COL_ROJO_MAS, value=_num(rojo_mas))
        for i in range(12):
            ws.cell(r, COL_MES1 + i, value=valores[i] if valores[i] is not None else 0)
        centros[cod] = {"p": p, "m": mensual}

    # puntaje por red: promedio de sus establecimientos
    redes: Dict[str, Dict[str, Any]] = {}
    for r, nombre in grupos:
        miembros = [c for cod, c in centros.items() if red_de.get(cod) == nombre]
        p = _promedio([c["p"] for c in miembros])
        mensual = [_promedio([c["m"][i] for c in miembros]) if i < mes else None for i in range(12)]
        ws.cell(r, COL_PUNTAJE, value=p)
        redes[nombre] = {"p": p, "m": mensual}

    ws.cell(FILA_TOTAL, COL_PUNTAJE, value=_promedio([d["p"] for n, d in redes.items() if "APP" not in n.upper()]))
    return {"centros": centros, "redes": redes}


def _escribir_resumen_puntajes(ws, fila: int, col_ini: int, puntajes: List[Any], mensuales: List[List[Any]], mes: int):
    """Escribe los 21 puntajes y las columnas de cantidad, total, máximo, %, puntaje /20 y meses."""
    for i, p in enumerate(puntajes):
        ws.cell(fila, col_ini + i, value=p)
    nums = [_num(p) for p in puntajes if _es_num(p)]
    cantidad, total = len(nums), sum(nums)
    maximo = cantidad * 5
    pct = total / maximo if maximo else 0
    c = col_ini + len(puntajes)
    for offset, valor in enumerate((cantidad, total, maximo, pct, pct * 20)):
        ws.cell(fila, c + offset, value=valor)
    for k in range(12):
        if k < mes:
            vals = [_num(m[k]) for m in mensuales if _es_num(m[k])]
            nota = sum(vals) / (len(vals) * 5) * 20 if vals else 0
        else:
            nota = 0
        ws.cell(fila, c + 5 + k, value=nota)


def _llenar_puntajes(ws, resultados: List[Dict[str, Any]], anio: str, mes: int, col_cod: int, col_nombre: int,
                     col_ini: int, col_anio: int) -> None:
    ws.cell(row=5, column=col_anio, value=f"AÑO: {anio}")
    for r in range(7, ws.max_row + 1):
        cod = ws.cell(r, col_cod).value
        nombre = ws.cell(r, col_nombre).value
        if cod not in (None, ""):
            datos = [res["centros"].get(str(cod).strip(), {"p": NA, "m": [NA] * 12}) for res in resultados]
        elif isinstance(nombre, str) and nombre.strip().upper().startswith("RED "):
            datos = [res["redes"].get(nombre.strip(), {"p": NA, "m": [NA] * 12}) for res in resultados]
        else:
            continue
        _escribir_resumen_puntajes(ws, r, col_ini, [d["p"] for d in datos], [d["m"] for d in datos], mes)


REL_DRAWING = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/drawing"
REL_IMAGE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
CONTENT_TYPES_IMAGEN = {"png": "image/png", "jpeg": "image/jpeg", "jpg": "image/jpeg", "gif": "image/gif",
                        "emf": "image/x-emf", "wmf": "image/x-wmf", "bmp": "image/bmp", "tiff": "image/tiff"}


def _rels(z: zipfile.ZipFile, parte: str) -> List[Dict[str, str]]:
    ruta = posixpath.join(posixpath.dirname(parte), "_rels", posixpath.basename(parte) + ".rels")
    if ruta not in z.namelist():
        return []
    return [dict(re.findall(r'(\w+)="([^"]*)"', m)) for m in re.findall(r"<Relationship\b([^>]*)/?>", z.read(ruta).decode("utf-8"))]


def _destino(parte: str, target: str) -> str:
    return target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join(posixpath.dirname(parte), target))


def _dibujo_por_hoja(z: zipfile.ZipFile) -> Dict[str, str]:
    """nombre de hoja -> parte xl/drawings/drawingN.xml"""
    wb_xml = z.read("xl/workbook.xml").decode("utf-8")
    hojas = dict((rid, nombre) for nombre, rid in re.findall(r'<sheet\b[^>]*name="([^"]*)"[^>]*r:id="([^"]*)"', wb_xml))
    resultado = {}
    for rel in _rels(z, "xl/workbook.xml"):
        if rel.get("Id") in hojas:
            hoja = _destino("xl/workbook.xml", rel["Target"])
            for r in _rels(z, hoja):
                if r.get("Type") == REL_DRAWING:
                    resultado[hojas[rel["Id"]]] = _destino(hoja, r["Target"])
    return resultado


def _restaurar_dibujos(generado: bytes) -> bytes:
    """openpyxl reescribe mal los logos de la plantilla (pierde el hipervínculo de la imagen y Excel
    tiene que reparar el archivo). Se reemplazan los dibujos del libro generado por los originales
    de la plantilla, con sus relaciones e imágenes."""
    with zipfile.ZipFile(PLANTILLA) as tpl, zipfile.ZipFile(io.BytesIO(generado)) as gen:
        dib_tpl, dib_gen = _dibujo_por_hoja(tpl), _dibujo_por_hoja(gen)
        reemplazos: Dict[str, bytes] = {}
        nuevas_imagenes: Dict[str, bytes] = {}
        imagenes_viejas = set()
        for hoja, parte_gen in dib_gen.items():
            parte_tpl = dib_tpl.get(hoja)
            if not parte_tpl:
                continue
            imagenes_viejas.update(_destino(parte_gen, r["Target"]) for r in _rels(gen, parte_gen) if r.get("Type") == REL_IMAGE)
            rels_xml = tpl.read(posixpath.join(posixpath.dirname(parte_tpl), "_rels", posixpath.basename(parte_tpl) + ".rels")).decode("utf-8")
            for r in _rels(tpl, parte_tpl):
                if r.get("Type") == REL_IMAGE:
                    origen = _destino(parte_tpl, r["Target"])
                    nombre = "tmi_" + posixpath.basename(origen)
                    nuevas_imagenes["xl/media/" + nombre] = tpl.read(origen)
                    rels_xml = rels_xml.replace(f'Target="{r["Target"]}"', f'Target="../media/{nombre}"')
            reemplazos[parte_gen] = tpl.read(parte_tpl)
            reemplazos[posixpath.join(posixpath.dirname(parte_gen), "_rels", posixpath.basename(parte_gen) + ".rels")] = rels_xml.encode("utf-8")

        content_types = gen.read("[Content_Types].xml").decode("utf-8")
        for ext in {n.rsplit(".", 1)[-1].lower() for n in nuevas_imagenes}:
            if f'Extension="{ext}"' not in content_types and ext in CONTENT_TYPES_IMAGEN:
                content_types = content_types.replace(
                    "</Types>", f'<Default Extension="{ext}" ContentType="{CONTENT_TYPES_IMAGEN[ext]}"/></Types>')
        reemplazos["[Content_Types].xml"] = content_types.encode("utf-8")

        salida = io.BytesIO()
        with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as out:
            for item in gen.infolist():
                if item.filename in imagenes_viejas:
                    continue
                out.writestr(item, reemplazos.get(item.filename, gen.read(item.filename)))
            for nombre, contenido in nuevas_imagenes.items():
                out.writestr(nombre, contenido)
    return salida.getvalue()


def generar_excel_tmi(db: Session, periodo: str) -> io.BytesIO:
    """Genera el libro TMI del `periodo` (AAAAMM) con la misma estructura que TMI_Prelim_Salud_Julio_2026.xlsx."""
    if not periodo or len(periodo) != 6 or not periodo.isdigit() or not 1 <= int(periodo[4:]) <= 12:
        raise ValueError("El periodo debe tener formato AAAAMM.")
    anio, mes = periodo[:4], int(periodo[4:])

    wb = load_workbook(PLANTILLA)
    red_de = {str(c["codcentro"]).strip(): str(c["red"] or "").strip() for c in queryCentrosTMI(db)}

    resultados = []
    for cfg in REPORTS:
        data = cfg["fn"](db, periodo)
        resultados.append(_llenar_indicador(wb[cfg["sheet"]], cfg, data, red_de, anio, mes))

    sin_plantilla = set(red_de) - set(resultados[0]["centros"])
    if sin_plantilla:
        logger.warning("Establecimientos de tmi_centro %s sin fila en la plantilla del Excel: %s",
                       periodo, sorted(sin_plantilla))

    # Puntajes: C=codcentro, D=nombre, G..AA indicadores, AG=año
    _llenar_puntajes(wb["Puntajes"], resultados, anio, mes, col_cod=3, col_nombre=4, col_ini=7, col_anio=33)
    # Puntajes_RED: C=codcentro (institutos), D=nombre, E..Y indicadores, AE=año
    _llenar_puntajes(wb["Puntajes_RED"], resultados, anio, mes, col_cod=3, col_nombre=4, col_ini=5, col_anio=31)

    wb["Resumen"]["B9"] = f"CIFRAS PRELIMINARES A {MESES_NOMBRE[mes - 1]} {anio} (*)"

    buffer = io.BytesIO()
    wb.save(buffer)
    return io.BytesIO(_restaurar_dibujos(buffer.getvalue()))
