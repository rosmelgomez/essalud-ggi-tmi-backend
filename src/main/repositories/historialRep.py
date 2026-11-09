"""Historial de cambios de la configuración del TMI (tmi_config_historial, lo llenan los triggers de 06_historial.sql)."""

import xml.etree.ElementTree as ET
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.repositories.tmiBaseRep import name_server

TABLAS = {
    "tmi_indicador": "Indicador",
    "tmi_indicador_estandar": "Estándar por nivel/categoría/tipo",
    "tmi_indicador_tolerancia": "% Acept del mes",
    "tmi_indicador_ambito": "Ámbito (centros del indicador)",
    "tmi_centro_estandar": "Estándar específico del centro",
    "tmi_exclusion_centro_indicador": "Exclusión de centro",
    "tmi_estandar_tipo": "Estándar por tipo",
    "tmi_estandar_nivel": "Estándar por nivel",
    "tmi_estandar_categoria": "Estándar por categoría",
    "tmi_estandar": "Claves del tipo de estándar",
    "tmi_tipo_estandar": "Tipo de estándar",
    "tmi_variable": "Variable",
    "tmi_variable_logica": "Lógica de variable",
    "tmi_variable_componente": "Componente de variable",
    "tmi_centro": "Centro",
}

ACCIONES = {"ALTA": "Creó", "CAMBIO": "Modificó", "BAJA": "Eliminó"}


def _fila(xml: Optional[str]) -> dict:
    """Atributos de <fila .../> (FOR XML RAW): una columna NULL no aparece."""
    if not xml:
        return {}
    try:
        return dict(ET.fromstring(xml).attrib)
    except ET.ParseError:
        return {}


def _valor(v: Optional[str]):
    """FOR XML escribe los FLOAT como 4.000000000000000e+000: se muestran como número."""
    if v is None:
        return None
    try:
        if "e" in v.lower() and any(c.isdigit() for c in v):
            n = float(v)
            return int(n) if n.is_integer() else round(n, 6)
    except ValueError:
        pass
    return v


def _cambios(accion: str, antes: dict, despues: dict) -> list:
    campos = [c for c in dict.fromkeys(list(antes) + list(despues)) if c != "id"]
    if accion == "CAMBIO":
        campos = [c for c in campos if antes.get(c) != despues.get(c)]
    return [{"campo": c, "antes": _valor(antes.get(c)), "despues": _valor(despues.get(c))} for c in campos]


def queryHistorialTMI(db: Session, id_indicador: Optional[int] = None, tabla: Optional[str] = None, limite: int = 200):
    if tabla is not None and tabla not in TABLAS:
        raise HTTPException(status_code=400, detail="Tabla no válida para el historial.")
    limite = max(1, min(int(limite), 1000))
    try:
        filas = db.execute(text(f"""
            SELECT TOP (:limite) h.id, h.fecha, h.usuario, h.tabla, h.id_registro, h.id_indicador,
                   i.codigo, i.indicador, h.accion, h.antes, h.despues
            FROM {name_server}.tmi_config_historial h
            LEFT JOIN {name_server}.tmi_indicador i ON i.id = h.id_indicador
            WHERE (:id_indicador IS NULL OR h.id_indicador = :id_indicador)
              AND (:tabla IS NULL OR h.tabla = :tabla)
            ORDER BY h.id DESC"""), {"limite": limite, "id_indicador": id_indicador, "tabla": tabla}).mappings().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return [{"id": f["id"], "fecha": f["fecha"], "usuario": f["usuario"], "tabla": f["tabla"],
             "que": TABLAS.get(f["tabla"], f["tabla"]), "id_registro": f["id_registro"],
             "id_indicador": f["id_indicador"], "codigo": f["codigo"], "indicador": f["indicador"],
             "accion": f["accion"], "accion_texto": ACCIONES.get(f["accion"], f["accion"]),
             "cambios": _cambios(f["accion"], _fila(f["antes"]), _fila(f["despues"]))}
            for f in filas]
