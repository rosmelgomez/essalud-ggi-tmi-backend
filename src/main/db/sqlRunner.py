"""Ejecuta los scripts SQL del TMI dinámico (equivalente a ExecuteQuery de essalud-gcpp-backend).

Se llama al iniciar la aplicación (app.py) y también se puede correr a mano:

    python -m src.main.db.sqlRunner

Los scripts son idempotentes: crean tablas, vistas y procedimientos si faltan, y cargan los datos
iniciales sin pisar lo que el usuario ya modificó. Separan lotes con GO, como en SSMS.
Si se borra una tabla, al reiniciar se vuelve a crear y se carga su semilla (SEMILLAS) porque queda vacía.
Marcadores que se reemplazan antes de ejecutar:
    {{TMI_DB}}       base de las tablas tmi_*                 (TMI_DB, por defecto DB_NAME)
    {{TOTALIZADO3}}  tabla de hechos                          (TMI_TOTALIZADO3)
    {{DIM}}          base.esquema de DIM_GRUPO / DIM_ACTIVIDAD (TMI_DIM)
TOTALIZADO3 y las DIM pueden estar en otro servidor: se usa un servidor vinculado y nombre de 4 partes en el .env
(TMI_TOTALIZADO3 = [SRV_DW].pentahodev_dw.dbo.TOTALIZADO3 ; TMI_DIM = [SRV_DW].pentahodev_dw.dbo).
"""

import logging
import re
from pathlib import Path
from typing import Dict, List

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from src.main.core.tmiConfig import TMI_DB, TMI_DIM, TMI_TOTALIZADO3
from src.main.db.databaseConexion import SQLALCHEMY_DATABASE_URL

logger = logging.getLogger(__name__)

RESOURCES_DIR = Path(__file__).resolve().parents[2] / "resources"
SQL_DIR = RESOURCES_DIR / "sql" / "tmi"

# Orden de ejecución
SQL_SCRIPTS = [
    "01_tablas.sql",
    "02_vistas_adaptadoras.sql",
    "03_datos.sql",
    "04_procedimientos.sql",
]

# Datos iniciales de centros y estándares: se cargan solo si la tabla está vacía (recién creada).
# Van después de 03_datos.sql porque los estándares referencian a tmi_indicador.
SEMILLAS = [
    ("tmi_centro", "centro/insert_centros_tmi.sql"),
    ("tmi_estandar_tipo", "estandares/insert_estandares_tipo.sql"),
    ("tmi_estandar_nivel", "estandares/insert_estandares_nivel.sql"),
    ("tmi_estandar_acept", "estandares/insert_estandares_acept.sql"),
]

_GO = re.compile(r"^\s*GO\s*;?\s*$", re.IGNORECASE | re.MULTILINE)
# 1 a 4 partes separadas por punto (servidor.base.esquema.objeto); entre corchetes se aceptan guion, espacio y "\"
# (nombres de servidor como [SRV-DW] o [SERVIDOR\INSTANCIA]), nunca comillas, punto y coma ni corchetes sueltos.
_PARTE = r"(?:\[[A-Za-z0-9_\- \\]+\]|[A-Za-z0-9_]+)"
_NOMBRE_SEGURO = re.compile(rf"^{_PARTE}(?:\.{_PARTE}){{0,3}}$")


def _validar_nombre(valor: str, variable: str) -> str:
    if not _NOMBRE_SEGURO.match(valor):
        raise ValueError(f"{variable} tiene caracteres no permitidos: {valor!r}")
    return valor


def _marcadores() -> Dict[str, str]:
    return {
        "{{TMI_DB}}": _validar_nombre(TMI_DB, "TMI_DB"),
        "{{TOTALIZADO3}}": _validar_nombre(TMI_TOTALIZADO3, "TMI_TOTALIZADO3"),
        "{{DIM}}": _validar_nombre(TMI_DIM, "TMI_DIM"),
    }


def lotes(script: str, carpeta: Path = SQL_DIR) -> List[str]:
    """Reemplaza marcadores y separa el script en lotes por GO."""
    texto = (carpeta / script).read_text(encoding="utf-8-sig")
    for marcador, valor in _marcadores().items():
        texto = texto.replace(marcador, valor)
    return [lote.strip() for lote in _GO.split(texto) if lote.strip()]


def ejecutar_scripts(scripts: List[str] = None) -> Dict[str, str]:
    """Ejecuta los scripts en orden. Si un lote falla se registra el error, se detiene ese script y se
    sigue con el siguiente (como ExecuteQuery, que no detiene el arranque de la aplicación)."""
    resultado: Dict[str, str] = {}
    # Conexión propia (sin pool): el USE no debe quedar en las conexiones que usa la API
    engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
    conexion = engine.raw_connection()
    try:
        # autocommit en la conexión pyodbc real (el envoltorio de SQLAlchemy no lo propaga)
        dbapi = getattr(conexion, "driver_connection", None) or conexion.connection
        dbapi.autocommit = True
        cursor = dbapi.cursor()
        cursor.execute(f"USE [{_validar_nombre(TMI_DB, 'TMI_DB').strip('[]')}]")
        # Las fuentes se resuelven recién al ejecutar los procedimientos: se avisa aquí si no existen
        for variable, objeto in (("TMI_TOTALIZADO3", TMI_TOTALIZADO3), ("TMI_DIM", f"{TMI_DIM}.DIM_GRUPO")):
            # se consulta la tabla (OBJECT_ID no ve las tablas de un servidor vinculado)
            try:
                cursor.execute(f"SELECT TOP 0 1 FROM {_validar_nombre(objeto, variable)}")
                while cursor.nextset():
                    pass
            except Exception as e:
                resultado[variable] = f"AVISO: no se puede leer {objeto}; revise {variable} en el .env ({e})"
                logger.error("Fuente del TMI no accesible: %s (variable %s del .env): %s", objeto, variable, e)
        for script in scripts or SQL_SCRIPTS:
            if script == "04_procedimientos.sql" and scripts is None:
                _cargar_semillas(cursor, resultado)
            _ejecutar(cursor, script, SQL_DIR, resultado)
    finally:
        conexion.close()
        engine.dispose()
    return resultado


def _ejecutar(cursor, script: str, carpeta: Path, resultado: Dict[str, str]) -> None:
    try:
        for numero, lote in enumerate(lotes(script, carpeta), start=1):
            try:
                cursor.execute(lote)
                while cursor.nextset():
                    pass
            except Exception as e:
                raise RuntimeError(f"lote {numero}: {e}") from e
        resultado[script] = "OK"
        logger.info("Script SQL ejecutado: %s", script)
    except Exception as e:
        resultado[script] = f"ERROR {e}"
        logger.error("Error al ejecutar el script SQL %s: %s", script, e)


def _cargar_semillas(cursor, resultado: Dict[str, str]) -> None:
    for tabla, archivo in SEMILLAS:
        if cursor.execute("SELECT OBJECT_ID(?)", f"dbo.{tabla}").fetchone()[0] is None:
            continue
        if cursor.execute(f"SELECT TOP 1 1 FROM dbo.{tabla}").fetchone() is not None:
            continue   # ya tiene datos: no se pisa lo que cargó el usuario
        _ejecutar(cursor, archivo, RESOURCES_DIR, resultado)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    for nombre, estado in ejecutar_scripts().items():
        print(f"{nombre}: {estado}")
