"""Centros: tmi_centro, estándar propio de centro y exclusión de centro por indicador."""

from sqlalchemy import CheckConstraint, Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.mssql import BIT

from src.main.model.base import TMI_SCHEMA, Base, defecto
from src.main.model.estandarModel import _EstandarMensual
from src.main.model.indicadorModel import TmiIndicador


class TmiCentro(Base):
    __tablename__ = "tmi_centro"
    __table_args__ = {"schema": TMI_SCHEMA}
    id = Column(Integer, primary_key=True)
    red = Column(String(100))
    orden = Column(String(50))
    orden_tipo = Column(String(50))
    codcentro = Column(String(50))
    centro = Column(String(100))
    categoria = Column(String(50))
    nivel = Column(String(50))
    tipo = Column(String(50))
    flag = Column(BIT)                                         # 0 = el centro no se muestra


class TmiCentroEstandar(_EstandarMensual, Base):
    """Estándar específico de un centro (gana sobre tipo, nivel y categoría)."""
    __tablename__ = "tmi_centro_estandar"
    __table_args__ = {"schema": TMI_SCHEMA}
    id = Column(Integer, primary_key=True)
    id_centro = Column(Integer)
    codcentro = Column(String(50), nullable=False)
    id_indicador = Column(Integer, ForeignKey(TmiIndicador.id), nullable=False)
    anio = Column(Integer, nullable=False)
    aplica = Column(BIT, nullable=False, server_default=defecto(1))    # 0 = NA
    acept = Column(Float)                                      # % Acept propio
    sustento = Column(String(300))


class TmiExclusionCentroIndicador(Base):
    """Exclusión por periodo: excl_MM = 1 -> NA ese mes. id_indicador NULL = todos los indicadores del centro.
    El sinónimo tmi_exclusion_centro_estandar (nombre anterior) se crea en 02_vistas_adaptadoras.sql."""
    __tablename__ = "tmi_exclusion_centro_indicador"
    __table_args__ = (
        CheckConstraint("resultado IN ('NA', '0')", name="ck_tmi_exclusion_resultado"),
        {"schema": TMI_SCHEMA},
    )
    id = Column(Integer, primary_key=True)
    id_centro = Column(Integer)
    codcentro = Column(String(50))
    id_indicador = Column(Integer, ForeignKey(TmiIndicador.id))
    anio = Column(Integer, nullable=False)
    excl_01 = Column(BIT)
    excl_02 = Column(BIT)
    excl_03 = Column(BIT)
    excl_04 = Column(BIT)
    excl_05 = Column(BIT)
    excl_06 = Column(BIT)
    excl_07 = Column(BIT)
    excl_08 = Column(BIT)
    excl_09 = Column(BIT)
    excl_10 = Column(BIT)
    excl_11 = Column(BIT)
    excl_12 = Column(BIT)
    motivo = Column(String(300))
    # cómo queda el mes excluido en el resultado final: 'NA' (no aplica) o '0' (puntaje 0, valor 0)
    resultado = Column(String(2), nullable=False, server_default=defecto("NA"))
