"""Base de los modelos del TMI: las tablas se crean desde estas clases al iniciar (como ddl-auto de Spring Boot).

Solo se crean las tablas que faltan: create_all no agrega ni cambia columnas de una tabla que ya existe.
Los repositorios siguen consultando con SQL (text); los modelos solo definen la estructura de las tablas."""

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase

from src.main.core.tmiConfig import TMI_DB

# base.esquema de las tablas tmi_* (SQL Server acepta el nombre en dos partes: [base].[dbo])
TMI_SCHEMA = f"{TMI_DB.strip('[]')}.dbo"

AHORA = text("GETDATE()")


def defecto(valor) -> text:
    """DEFAULT de la columna en la tabla (los INSERT con SQL lo usan cuando no mandan el valor)."""
    return text(f"'{valor}'") if isinstance(valor, str) else text(str(int(valor) if isinstance(valor, bool) else valor))


class Base(DeclarativeBase):
    pass
