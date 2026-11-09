"""Crea al iniciar las tablas que falten, desde los modelos de esta carpeta (como ddl-auto de Spring Boot).
Los .sql de src/resources solo cargan datos, vistas y procedimientos."""

import logging

from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

from src.main.db.databaseConexion import SQLALCHEMY_DATABASE_URL
from src.main.model import (centroModel, cierreModel, estandarModel, historialModel, indicadorModel, resultadoModel,
                            variableModel)
from src.main.model.base import TMI_SCHEMA, Base

# cada módulo registra sus tablas en Base.metadata al importarse
MODELOS = (variableModel, indicadorModel, estandarModel, centroModel, resultadoModel, cierreModel, historialModel)

logger = logging.getLogger(__name__)


def crear_tablas() -> None:
    """CREATE TABLE de cada modelo cuya tabla no existe. No agrega ni cambia columnas de las tablas existentes."""
    engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
    try:
        _migrar_tablas(engine)
        Base.metadata.create_all(engine)
    except Exception as e:
        # otro worker la creó al mismo tiempo (error 2714: el objeto ya existe)
        if "2714" not in str(e):
            raise
    finally:
        engine.dispose()
    logger.info("Tablas del TMI verificadas (%s)", len(Base.metadata.tables))


# columnas que ya no tiene tmi_resultado: el cálculo es solo del mes de corte, y el valor y el puntaje de cada mes
# están en la fila de su propio periodo de corte
_COLUMNAS_QUITADAS = {"tmi_resultado": ["numerador", "denominador"] + [f"p{m:02d}" for m in range(1, 13)]
                                       + [f"m{m:02d}" for m in range(1, 13)]}


# tablas que cambiaron de nombre (sp_rename: conservan sus datos) y sus restricciones
_TABLAS_RENOMBRADAS = [("nivel_centro", "tmi_nivel_estandar_centro"),
                       ("cierre", "tmi_cierre"), ("cierre_calendario", "tmi_cierre_calendario"),
                       ("tipo_centro", "tmi_tipo_centro")]
_RESTRICCIONES_RENOMBRADAS = [("UX_nivel_centro", "UX_tmi_nivel_estandar_centro"),
                              ("UQ_cierre_periodo", "UQ_tmi_cierre_periodo"), ("CK_cierre_estado", "CK_tmi_cierre_estado"),
                              ("UQ_cierre_calendario_anio", "UQ_tmi_cierre_calendario_anio"),
                              ("CK_cierre_calendario_dia", "CK_tmi_cierre_calendario_dia"),
                              ("UX_tipo_centro", "UX_tmi_tipo_centro")]


# tablas que ya no se usan: tmi_variable_pivot (el cálculo lee TOTALIZADO3 por periodo, ya no hay pivot de variables)
# y el catálogo de categorías (el cálculo une el centro con los estándares por nivel_estandar y tipo)
_TABLAS_QUITADAS = ["tmi_variable_pivot", "categoria_centro", "tmi_categoria_centro"]


# columnas nuevas en tablas que ya existen (create_all no las agrega): tabla -> [(columna, tipo SQL)]
_COLUMNAS_AGREGADAS = {
    "tmi_resultado_indicador": [("nivel_estandar", "VARCHAR(50) NULL")],
    # regla de nulos por indicador (por defecto, el comportamiento anterior: letra sin dato = 0, división entre 0 = NA)
    "tmi_indicador": [("si_variable_nula", "VARCHAR(4) NOT NULL CONSTRAINT DF_tmi_indicador_si_variable_nula DEFAULT 'CERO'"),
                      ("si_division_cero", "VARCHAR(4) NOT NULL CONSTRAINT DF_tmi_indicador_si_division_cero DEFAULT 'NA'")],
}


def _renombrar_tablas(conexion) -> None:
    """Renombra las tablas de nombre anterior conservando sus datos. Si ya existen las dos (el backend creó la nueva
    vacía), se queda la que tiene datos."""
    base, esquema = TMI_SCHEMA.rsplit(".", 1)
    # OBJECT_ID(nombre, NULL) devuelve NULL: sin tipo se llama con un solo argumento
    existe = lambda n, tipo: conexion.execute(text("SELECT OBJECT_ID(:t, :k)" if tipo else "SELECT OBJECT_ID(:t)"),
                                              {"t": f"{TMI_SCHEMA}.{n}", "k": tipo}).scalar() is not None
    filas = lambda n: conexion.execute(text(f"SELECT COUNT(*) FROM {TMI_SCHEMA}.{n}")).scalar()
    renombrar = lambda viejo, nuevo, clase: conexion.execute(text(
        f"EXEC {base}.sys.sp_rename N'{esquema}.{viejo}', N'{nuevo}'{', N' + repr(clase) if clase else ''}"))
    for viejo, nuevo in _TABLAS_RENOMBRADAS:
        if not existe(viejo, "U"):
            continue
        if existe(nuevo, "U"):
            if filas(nuevo) == 0:
                conexion.execute(text(f"DROP TABLE {TMI_SCHEMA}.{nuevo}"))
            elif filas(viejo) == 0:
                conexion.execute(text(f"DROP TABLE {TMI_SCHEMA}.{viejo}"))
                continue
            else:
                logger.warning("%s y %s tienen datos: no se renombra", viejo, nuevo)
                continue
        renombrar(viejo, nuevo, None)
        logger.info("Tabla renombrada: %s -> %s", viejo, nuevo)
    for viejo, nuevo in _RESTRICCIONES_RENOMBRADAS:
        if existe(viejo, None) and not existe(nuevo, None):
            renombrar(viejo, nuevo, "OBJECT")


def _migrar_tablas(engine) -> None:
    """Cambios de estructura que create_all no hace: quita tablas que ya no se usan, agrega columnas nuevas y quita las
    que ya no están en los modelos."""
    with engine.begin() as conexion:
        _renombrar_tablas(conexion)
        for tabla in _TABLAS_QUITADAS:
            nombre = f"{TMI_SCHEMA}.{tabla}"
            if conexion.execute(text("SELECT OBJECT_ID(:t, 'U')"), {"t": nombre}).scalar() is not None:
                conexion.execute(text(f"DROP TABLE {nombre}"))
                logger.info("%s: tabla quitada", tabla)
        for tabla, columnas in _COLUMNAS_AGREGADAS.items():
            nombre = f"{TMI_SCHEMA}.{tabla}"
            if conexion.execute(text("SELECT OBJECT_ID(:t)"), {"t": nombre}).scalar() is None:
                continue   # la crea create_all con todas sus columnas
            for columna, tipo in columnas:
                if conexion.execute(text("SELECT COL_LENGTH(:t, :c)"), {"t": nombre, "c": columna}).scalar() is None:
                    conexion.execute(text(f"ALTER TABLE {nombre} ADD {columna} {tipo}"))
                    logger.info("%s: columna agregada %s", tabla, columna)
        for tabla, columnas in _COLUMNAS_QUITADAS.items():
            nombre = f"{TMI_SCHEMA}.{tabla}"
            existentes = [c for c in columnas
                          if conexion.execute(text("SELECT COL_LENGTH(:t, :c)"), {"t": nombre, "c": c}).scalar() is not None]
            if existentes:
                conexion.execute(text(f"ALTER TABLE {nombre} DROP COLUMN {', '.join(existentes)}"))
                logger.info("%s: columnas quitadas %s", tabla, ", ".join(existentes))
