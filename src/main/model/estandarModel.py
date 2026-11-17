"""Estándares: tablas maestras, valores por tipo, nivel y categoría, estándares por indicador y % Acept."""

from sqlalchemy import CheckConstraint, Column, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.mssql import BIT

from src.main.model.base import TMI_SCHEMA, Base, defecto
from src.main.model.indicadorModel import TmiIndicador


class TmiTipoEstandar(Base):
    """Tipos de estándar (NIVEL, NIVEL_TIPO, TIPO, CATEGORIA). tmi_indicador.base_estandar -> codigo."""
    __tablename__ = "tmi_tipo_estandar"
    __table_args__ = (UniqueConstraint("codigo", name="UX_tmi_tipo_estandar"), {"schema": TMI_SCHEMA})
    id = Column(Integer, primary_key=True)
    codigo = Column(String(30), nullable=False)
    descripcion = Column(String(100), nullable=False)
    orden = Column(Integer)
    activo = Column(BIT, nullable=False, server_default=defecto(1))


class TmiEstandar(Base):
    """Claves de cada tipo: fuente = tabla de valores (nivel, tipo o categoría) y clave = valor del centro en
    tmi_centro. Si un centro cumple dos claves del mismo tipo, gana la de mayor prioridad."""
    __tablename__ = "tmi_estandar"
    __table_args__ = (
        CheckConstraint("fuente IN ('NIVEL', 'TIPO', 'CATEGORIA')", name="CK_tmi_estandar_fuente"),
        UniqueConstraint("tipo_estandar", "fuente", "clave", name="UX_tmi_estandar"),
        {"schema": TMI_SCHEMA},
    )
    id = Column(Integer, primary_key=True)
    tipo_estandar = Column(String(30), ForeignKey(TmiTipoEstandar.codigo, name="FK_tmi_estandar_tipo"), nullable=False)
    orden = Column(Integer)
    fuente = Column(String(10), nullable=False)
    clave = Column(String(50), nullable=False)
    descripcion = Column(String(100))
    prioridad = Column(Integer, nullable=False, server_default=defecto(1))
    activo = Column(BIT, nullable=False, server_default=defecto(1))


class _EstandarMensual:
    """Estándar del año: est_fijo (el que toma cada mes en su fecha de cierre) y el de cada mes."""
    est_fijo = Column(Float)
    est_01 = Column(Float)
    est_02 = Column(Float)
    est_03 = Column(Float)
    est_04 = Column(Float)
    est_05 = Column(Float)
    est_06 = Column(Float)
    est_07 = Column(Float)
    est_08 = Column(Float)
    est_09 = Column(Float)
    est_10 = Column(Float)
    est_11 = Column(Float)
    est_12 = Column(Float)


class TmiEstandarTipo(_EstandarMensual, Base):
    __tablename__ = "tmi_estandar_tipo"
    __table_args__ = (UniqueConstraint("id_indicador", "tipo_centro", "anio", name="UX_tmi_estandar_tipo"),
                      {"schema": TMI_SCHEMA})
    id = Column(Integer, primary_key=True)
    id_indicador = Column(Integer, ForeignKey(TmiIndicador.id), nullable=False)
    tipo_centro = Column(String(50), nullable=False)
    anio = Column(Integer, nullable=False)


class TmiEstandarNivel(_EstandarMensual, Base):
    __tablename__ = "tmi_estandar_nivel"
    __table_args__ = (UniqueConstraint("id_indicador", "nivel_centro", "anio", name="UX_tmi_estandar_nivel"),
                      {"schema": TMI_SCHEMA})
    id = Column(Integer, primary_key=True)
    id_indicador = Column(Integer, ForeignKey(TmiIndicador.id), nullable=False)
    nivel_centro = Column(String(50), nullable=False)          # valor de tmi_centro.nivel (I, II, III)
    anio = Column(Integer, nullable=False)


class TmiEstandarCategoria(_EstandarMensual, Base):
    __tablename__ = "tmi_estandar_categoria"
    __table_args__ = {"schema": TMI_SCHEMA}
    id = Column(Integer, primary_key=True)
    id_indicador = Column(Integer, ForeignKey(TmiIndicador.id), nullable=False)
    categoria_centro = Column(String(50), nullable=False)
    anio = Column(Integer, nullable=False)



class TmiIndicadorAcept(Base):
    """% Acept del indicador por año, como los estándares: acept_fijo / aceptmenos_fijo es el del año y cada mes
    (acept_MM / aceptmenos_MM) toma el fijo en su fecha de cierre; mientras está vacío, el mes usa el fijo.
    acept = hacia arriba (en MAYOR, hacia abajo); aceptmenos = hacia abajo en banda (NULL = el mismo que acept)."""
    __tablename__ = "tmi_indicador_acept"
    __table_args__ = (
        CheckConstraint("tipo_acept IN ('REL', 'ABS')", name="CK_tmi_indicador_acept_tipo"),
        UniqueConstraint("id_indicador", "anio", name="UX_tmi_indicador_acept"),
        {"schema": TMI_SCHEMA},
    )
    id = Column(Integer, primary_key=True)
    id_indicador = Column(Integer, ForeignKey(TmiIndicador.id), nullable=False)
    anio = Column(Integer, nullable=False)
    tipo_acept = Column(String(3), nullable=False, server_default=defecto("REL"))
    acept_fijo = Column(Float)
    acept_01 = Column(Float)
    acept_02 = Column(Float)
    acept_03 = Column(Float)
    acept_04 = Column(Float)
    acept_05 = Column(Float)
    acept_06 = Column(Float)
    acept_07 = Column(Float)
    acept_08 = Column(Float)
    acept_09 = Column(Float)
    acept_10 = Column(Float)
    acept_11 = Column(Float)
    acept_12 = Column(Float)
    aceptmenos_fijo = Column(Float)
    aceptmenos_01 = Column(Float)
    aceptmenos_02 = Column(Float)
    aceptmenos_03 = Column(Float)
    aceptmenos_04 = Column(Float)
    aceptmenos_05 = Column(Float)
    aceptmenos_06 = Column(Float)
    aceptmenos_07 = Column(Float)
    aceptmenos_08 = Column(Float)
    aceptmenos_09 = Column(Float)
    aceptmenos_10 = Column(Float)
    aceptmenos_11 = Column(Float)
    aceptmenos_12 = Column(Float)
