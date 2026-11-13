"""Crea al iniciar las tablas que falten, desde los modelos de esta carpeta (como ddl-auto de Spring Boot).
Los .sql de src/resources solo cargan datos, vistas y procedimientos."""

import logging

from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

from src.main.db.databaseConexion import SQLALCHEMY_DATABASE_URL
from src.main.model import (centroModel, cierreModel, estandarModel, historialModel, indicadorModel,
                            variableModel)
from src.main.model.base import TMI_SCHEMA, Base

# cada módulo registra sus tablas en Base.metadata al importarse
MODELOS = (variableModel, indicadorModel, estandarModel, centroModel, cierreModel, historialModel)

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
# y las del resultado guardado: el cálculo es siempre en tiempo real y el cierre solo guarda la copia de los datos
_TABLAS_QUITADAS = ["tmi_variable_pivot", "categoria_centro", "tmi_categoria_centro",
                    "tmi_resultado", "tmi_resultado_indicador", "tmi_resultado_termino"]


# columnas nuevas en tablas que ya existen (create_all no las agrega): tabla -> [(columna, tipo SQL)]
_COLUMNAS_AGREGADAS = {
    # regla de nulos por indicador (por defecto, el comportamiento anterior: letra sin dato = 0, división entre 0 = NA)
    "tmi_indicador": [("formula_plantilla", "NVARCHAR(2000) NULL"),
                      ("si_variable_nula", "VARCHAR(4) NOT NULL CONSTRAINT DF_tmi_indicador_si_variable_nula DEFAULT 'CERO'"),
                      ("si_division_cero", "VARCHAR(4) NOT NULL CONSTRAINT DF_tmi_indicador_si_division_cero DEFAULT 'NA'")],
    # resultado propio de cada mes excluido ('0' o 'NA'); NULL = el de la columna resultado
    "tmi_exclusion_centro_indicador": [
        (f"res_{m:02d}", f"VARCHAR(2) NULL CONSTRAINT ck_tmi_exclusion_res_{m:02d} CHECK (res_{m:02d} IN ('NA', '0'))")
        for m in range(1, 13)],
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
    """Cambios de estructura que create_all no hace: quita tablas que ya no se usan y agrega columnas nuevas."""
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
