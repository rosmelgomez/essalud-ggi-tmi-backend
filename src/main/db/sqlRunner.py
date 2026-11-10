"""Ejecuta los scripts SQL del TMI dinámico (equivalente a ExecuteQuery de essalud-gcpp-backend).

Se llama al iniciar la aplicación (app.py) y también se puede correr a mano:

    python -m src.main.db.sqlRunner

Antes de los scripts se crean las tablas que falten desde los modelos (src/main/model/tablas.py).
Los scripts son idempotentes: crean vistas y procedimientos si faltan, y cargan los datos
iniciales sin pisar lo que el usuario ya modificó. Separan lotes con GO, como en SSMS.
Si se borra una tabla, al reiniciar el modelo la vuelve a crear y se carga su semilla (SEMILLAS) porque queda vacía.
Marcadores que se reemplazan antes de ejecutar:
    {{TMI_DB}}       base de todas las tablas del sistema      (la de la conexión: DB_NAME)
    {{TOTALIZADO3}}  tabla de hechos                          (pentahodevDW + .TOTALIZADO3)
    {{DIM}}          base.esquema de DIM_GRUPO / DIM_ACTIVIDAD (pentahodevDW)
TOTALIZADO3 y las DIM pueden estar en otro servidor: se usa un servidor vinculado y nombre de 4 partes en el .env
(pentahodevDW = [SRV_DW].pentahodev_dw.dbo).
"""

import logging
import re
from pathlib import Path
from typing import Dict, List

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from src.main.core import tmiFormula
from src.main.core.tmiConfig import TMI_DB, TMI_DIM, TMI_TOTALIZADO3
from src.main.db.databaseConexion import SQLALCHEMY_DATABASE_URL
from src.main.model.tablas import crear_tablas

logger = logging.getLogger(__name__)

RESOURCES_DIR = Path(__file__).resolve().parents[2] / "resources"
SQL_DIR = RESOURCES_DIR / "sql" / "tmi"

# Orden de ejecución
SQL_SCRIPTS = [
    "02_vistas_adaptadoras.sql",
    "03_datos.sql",
    "05_variables_pivot.sql",   # variables de Generar_pivot.sql (una sola vez; no pisa cambios del usuario)
    "04_procedimientos.sql",
    "06_historial.sql",         # triggers del historial de cambios de la configuración (tmi_config_historial)
]

# Datos iniciales de centros y estándares: se cargan solo si la tabla está vacía (recién creada).
# Van después de 03_datos.sql porque los estándares referencian a tmi_indicador.
SEMILLAS = [
    ("tmi_centro", "centro/insert_centros_tmi.sql"),
    ("tmi_exclusion_centro_indicador", "centro/insert_exclusiones_centro.sql"),   # después de tmi_centro: toma su id
    ("tmi_estandar_tipo", "estandares/insert_nivel_estandar_centro.sql"),
    ("tmi_estandar_nivel", "estandares/insert_estandares_nivel.sql"),
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
        "{{TOTALIZADO3}}": _validar_nombre(TMI_TOTALIZADO3, "pentahodevDW"),
        "{{DIM}}": _validar_nombre(TMI_DIM, "pentahodevDW"),
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
    try:
        crear_tablas()
        resultado["tablas"] = "OK"
    except Exception as e:
        resultado["tablas"] = f"ERROR {e}"
        logger.error("Error al crear las tablas del TMI desde los modelos: %s", e)
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
        for variable, objeto in (("pentahodevDW", TMI_TOTALIZADO3), ("pentahodevDW", f"{TMI_DIM}.DIM_GRUPO")):
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
        if scripts is None or "03_datos.sql" in scripts:
            _sincronizar_formulas(cursor, resultado)
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


def _sincronizar_formulas(cursor, resultado: Dict[str, str]) -> None:
    """Regenera la fórmula interna de cada indicador: desde la fórmula con letras (formula_alias) y las variables
    actuales de cada letra cuando la tiene, y luego sus términos (tmi_indicador_termino) y formula_sql."""
    errores = []
    try:
        if cursor.execute("SELECT COL_LENGTH('dbo.tmi_indicador', 'formula_alias')").fetchone()[0] is None:
            return
        for id_ind, codigo, alias in cursor.execute(
                "SELECT id, codigo, formula_alias FROM dbo.tmi_indicador WHERE NULLIF(LTRIM(formula_alias), '') IS NOT NULL").fetchall():
            try:
                mapa = {}
                for letra, nombre, agregacion, id_var in cursor.execute(
                        """SELECT iv.letra, v.nombre, v.agregacion, v.id FROM dbo.tmi_indicador_variable iv
                           JOIN dbo.tmi_variable v ON v.id = iv.id_variable WHERE iv.id_indicador = ?""", id_ind).fetchall():
                    conjuntos = cursor.execute(tmiFormula.SQL_CONJUNTOS.format(esq="dbo", p="?"), id_var, id_var).fetchall()
                    mapa[letra] = tmiFormula.expresion_variable(nombre, agregacion, conjuntos)[0]
                formula = tmiFormula.expandir_alias(alias, mapa)
                cursor.execute("UPDATE dbo.tmi_indicador SET formula = ? WHERE id = ?", formula, id_ind)
            except tmiFormula.ErrorFormula as e:
                errores.append(f"{codigo}: {e} (se mantiene la fórmula anterior)")
        # regla de nulos de cada indicador (si la tabla aún no tiene las columnas: CERO / NA, el comportamiento anterior)
        con_regla = cursor.execute("SELECT COL_LENGTH('dbo.tmi_indicador', 'si_division_cero')").fetchone()[0] is not None
        regla = "si_variable_nula, si_division_cero" if con_regla else "'CERO', 'NA'"
        for id_ind, codigo, texto, si_variable_nula, si_division_cero in cursor.execute(
                f"SELECT id, codigo, formula, {regla} FROM dbo.tmi_indicador "
                "WHERE NULLIF(LTRIM(formula), '') IS NOT NULL").fetchall():
            try:
                f = tmiFormula.analizar(texto, si_variable_nula, si_division_cero)
            except tmiFormula.ErrorFormula as e:
                errores.append(f"{codigo}: {e}")
                cursor.execute("UPDATE dbo.tmi_indicador SET formula_sql = NULL, formula_plantilla = NULL WHERE id = ?", id_ind)
                cursor.execute("DELETE FROM dbo.tmi_indicador_termino WHERE id_indicador = ?", id_ind)
                continue
            cursor.execute("DELETE FROM dbo.tmi_indicador_termino WHERE id_indicador = ?", id_ind)
            for r in tmiFormula.filas_termino(f):
                cursor.execute("""INSERT INTO dbo.tmi_indicador_termino (id_indicador, codigo, tipgrupo, actividad, servicio,
                                  mediana, texto) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                               id_ind, r["codigo"], r["tipgrupo"], r["actividad"], r["servicio"], r["mediana"], r["texto"])
            cursor.execute("UPDATE dbo.tmi_indicador SET formula_sql = ?, formula_plantilla = ? WHERE id = ?",
                           f.sql, tmiFormula.plantilla(f), id_ind)
        resultado["formulas"] = "OK" if not errores else "AVISO: " + "; ".join(errores)
    except Exception as e:
        resultado["formulas"] = f"ERROR {e}"
        logger.error("Error al regenerar las fórmulas de los indicadores: %s", e)


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
