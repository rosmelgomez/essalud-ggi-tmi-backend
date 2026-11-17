"""Validación de la configuración del TMI (usp_tmi_validar_config)."""

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.repositories.tmiBaseRep import crear_tablas_formula, name_server, quitar_tablas_formula


def queryValidarConfigTMI(db: Session):
    """Problemas de configuración. La fórmula de cada indicador la lee Python y la pasa en #formula y #termino."""
    try:
        crear_tablas_formula(db)
        result = db.execute(text(f"EXEC {name_server}.usp_tmi_validar_config"))
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        quitar_tablas_formula(db)

