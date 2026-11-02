"""Tablas del cierre de periodos, en la base de la conexión como las tablas tmi_* (TMI_DB = DB_NAME):
cierre (ejecución de cada periodo) y cierre_calendario (día de cierre de cada periodo, definido por año)."""

from sqlalchemy import CHAR, CheckConstraint, Column, Integer, String, UniqueConstraint, text
from sqlalchemy.dialects.mssql import DATE, DATETIME2, NVARCHAR

from src.main.model.base import TMI_SCHEMA, Base, defecto


class Cierre(Base):
    __tablename__ = "cierre"
    __table_args__ = (
        UniqueConstraint("periodo", name="UQ_cierre_periodo"),
        CheckConstraint("estado IN ('PENDIENTE','EN_PROCESO','EJECUTADO','ERROR')", name="CK_cierre_estado"),
        {"schema": TMI_SCHEMA},
    )
    id = Column(Integer, primary_key=True)
    periodo = Column(CHAR(6), nullable=False)
    fecha_cierre = Column(DATE, nullable=False)
    estado = Column(String(20), nullable=False, server_default=defecto("PENDIENTE"))
    fecha_ejecucion = Column(DATETIME2)
    filas_insertadas = Column(Integer)
    mensaje = Column(NVARCHAR(4000))
    fecha_creacion = Column(DATETIME2, nullable=False, server_default=text("SYSDATETIME()"))
    usuario_modifica = Column(String(100))


class CierreCalendario(Base):
    """Día de cierre de cada periodo del año: dia_fijo para todos y dia_MM solo donde el periodo MM se cierra otro día.
    El periodo MM se cierra en el mes siguiente (dia_12 de 2026 es el día de enero de 2027)."""
    __tablename__ = "cierre_calendario"
    __table_args__ = (
        UniqueConstraint("anio", name="UQ_cierre_calendario_anio"),
        CheckConstraint("dia_fijo BETWEEN 1 AND 31", name="CK_cierre_calendario_dia"),
        {"schema": TMI_SCHEMA},
    )
    id = Column(Integer, primary_key=True)
    anio = Column(Integer, nullable=False)
    dia_fijo = Column(Integer, nullable=False)
    dia_01 = Column(Integer)
    dia_02 = Column(Integer)
    dia_03 = Column(Integer)
    dia_04 = Column(Integer)
    dia_05 = Column(Integer)
    dia_06 = Column(Integer)
    dia_07 = Column(Integer)
    dia_08 = Column(Integer)
    dia_09 = Column(Integer)
    dia_10 = Column(Integer)
    dia_11 = Column(Integer)
    dia_12 = Column(Integer)
    fecha_modificacion = Column(DATETIME2, nullable=False, server_default=text("SYSDATETIME()"))
    usuario_modifica = Column(String(100))
