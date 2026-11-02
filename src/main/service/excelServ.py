"""Utilidades del Excel del TMI compartidas por excelDinamicoServ: nombres de los meses y restauración de los
dibujos (logos y botones con hipervínculo) de la plantilla src/resources/plantillas/TMI_PLANTILLA.xlsx."""

import io
import posixpath
import re
import zipfile
from pathlib import Path
from typing import Dict, List, Optional

PLANTILLA = Path(__file__).resolve().parents[2] / "resources" / "plantillas" / "TMI_PLANTILLA.xlsx"

MESES_NOMBRE = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO",
                "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]


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


def _restaurar_dibujos(generado: bytes, plantilla: Path = PLANTILLA,
                       hoja_origen: Optional[Dict[str, str]] = None) -> bytes:
    """openpyxl reescribe mal los logos de la plantilla (pierde el hipervínculo de la imagen y Excel
    tiene que reparar el archivo). Se reemplazan los dibujos del libro generado por los originales
    de la plantilla, con sus relaciones e imágenes.
    hoja_origen: hoja generada -> hoja de la plantilla de la que se copió (hojas creadas desde un modelo)."""
    hoja_origen = hoja_origen or {}
    with zipfile.ZipFile(plantilla) as tpl, zipfile.ZipFile(io.BytesIO(generado)) as gen:
        dib_tpl, dib_gen = _dibujo_por_hoja(tpl), _dibujo_por_hoja(gen)
        reemplazos: Dict[str, bytes] = {}
        nuevas_imagenes: Dict[str, bytes] = {}
        imagenes_viejas = set()
        for hoja, parte_gen in dib_gen.items():
            parte_tpl = dib_tpl.get(hoja_origen.get(hoja, hoja))
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
