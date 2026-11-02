"""Crea al iniciar las tablas que falten, desde los modelos de esta carpeta (como ddl-auto de Spring Boot).
Los .sql de src/resources solo cargan datos, vistas y procedimientos."""

import logging

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from src.main.db.databaseConexion import SQLALCHEMY_DATABASE_URL
from src.main.model import centroModel, cierreModel, estandarModel, indicadorModel, resultadoModel, variableModel
from src.main.model.base import Base

# cada módulo registra sus tablas en Base.metadata al importarse
MODELOS = (variableModel, indicadorModel, estandarModel, centroModel, resultadoModel, cierreModel)

logger = logging.getLogger(__name__)


def crear_tablas() -> None:
    """CREATE TABLE de cada modelo cuya tabla no existe. No agrega ni cambia columnas de las tablas existentes."""
    engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        # otro worker la creó al mismo tiempo (error 2714: el objeto ya existe)
        if "2714" not in str(e):
            raise
    finally:
        engine.dispose()
    logger.info("Tablas del TMI verificadas (%s)", len(Base.metadata.tables))
