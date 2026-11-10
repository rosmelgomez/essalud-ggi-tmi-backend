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
    "tmi_resultado_indicador": [("nivel_estandar", "VARCHAR(50) NULL"),
                                ("origen_datos", "VARCHAR(10) NOT NULL CONSTRAINT DF_tmi_resultado_indicador_origen "
                                                 "DEFAULT 'ACTUAL'"), ("periodo_backup", "INT NULL")],
    # justificación del cálculo: de dónde salieron los datos (los resultados anteriores se calcularon con TOTALIZADO3
    # de ese momento: ACTUAL) y la fórmula con la que se calculó
    "tmi_resultado": [("origen_datos", "VARCHAR(10) NOT NULL CONSTRAINT DF_tmi_resultado_origen_datos DEFAULT 'ACTUAL' "
                                      "CONSTRAINT CK_tmi_resultado_origen CHECK (origen_datos IN ('ACTUAL', 'BACKUP'))"),
                      ("periodo_backup", "INT NULL"), ("tipo_calculo", "VARCHAR(20) NULL"),
                      ("formula_alias", "NVARCHAR(500) NULL"), ("formula", "NVARCHAR(2000) NULL"),
                      ("formula_desarrollo", "NVARCHAR(4000) NULL"), ("usuario_calculo", "NVARCHAR(50) NULL")],
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


# tablas que guardan el cálculo con la copia del cierre (BACKUP) y el de los datos actuales (ACTUAL) del mismo periodo
_CLAVES_ORIGEN = {"tmi_resultado": "periodo_corte, origen_datos, id_indicador, codcentro",
                  "tmi_resultado_indicador": "periodo, origen_datos, id_indicador, codcentro"}


def _clave_resultado(conexion) -> None:
    for tabla, columnas in _CLAVES_ORIGEN.items():
        _clave_con_origen(conexion, tabla, columnas)


def _clave_con_origen(conexion, tabla: str, columnas: str) -> None:
    """La clave de la tabla pasa a incluir origen_datos (las filas que ya había quedan como ACTUAL)."""
    nombre = f"{TMI_SCHEMA}.{tabla}"
    if conexion.execute(text("SELECT OBJECT_ID(:t, 'U')"), {"t": nombre}).scalar() is None:
        return
    # la columna se agregó antes como NULL: se completa y pasa a NOT NULL con su valor por defecto
    nula = conexion.execute(text("SELECT is_nullable FROM sys.columns WHERE object_id = OBJECT_ID(:t) "
                                 "AND name = 'origen_datos'"), {"t": nombre}).scalar()
    if nula:
        conexion.execute(text(f"UPDATE {nombre} SET origen_datos = 'ACTUAL' WHERE origen_datos IS NULL"))
        conexion.execute(text(f"ALTER TABLE {nombre} ALTER COLUMN origen_datos VARCHAR(10) NOT NULL"))
        tiene_defecto = conexion.execute(text("SELECT default_object_id FROM sys.columns WHERE object_id = OBJECT_ID(:t) "
                                              "AND name = 'origen_datos'"), {"t": nombre}).scalar()
        if not tiene_defecto:
            conexion.execute(text(f"ALTER TABLE {nombre} ADD CONSTRAINT DF_{tabla}_origen DEFAULT 'ACTUAL' "
                                  "FOR origen_datos"))
    con_origen = conexion.execute(text("""
        SELECT COUNT(*) FROM sys.indexes i
        JOIN sys.index_columns ic ON ic.object_id = i.object_id AND ic.index_id = i.index_id
        JOIN sys.columns c ON c.object_id = ic.object_id AND c.column_id = ic.column_id
        WHERE i.object_id = OBJECT_ID(:t) AND i.is_primary_key = 1 AND c.name = 'origen_datos'"""), {"t": nombre}).scalar()
    if con_origen:
        return
    pk = conexion.execute(text("SELECT name FROM sys.indexes WHERE object_id = OBJECT_ID(:t) AND is_primary_key = 1"),
                          {"t": nombre}).scalar()
    if pk:
        conexion.execute(text(f"ALTER TABLE {nombre} DROP CONSTRAINT [{pk}]"))
    conexion.execute(text(f"ALTER TABLE {nombre} ADD CONSTRAINT PK_{tabla} PRIMARY KEY ({columnas})"))
    logger.info("%s: clave con origen_datos", tabla)


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
        _clave_resultado(conexion)
        for tabla, columnas in _COLUMNAS_QUITADAS.items():
            nombre = f"{TMI_SCHEMA}.{tabla}"
            existentes = [c for c in columnas
                          if conexion.execute(text("SELECT COL_LENGTH(:t, :c)"), {"t": nombre, "c": c}).scalar() is not None]
            if existentes:
                conexion.execute(text(f"ALTER TABLE {nombre} DROP COLUMN {', '.join(existentes)}"))
                logger.info("%s: columnas quitadas %s", tabla, ", ".join(existentes))
