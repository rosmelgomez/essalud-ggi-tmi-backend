"""Estándares: tablas maestras, valores por tipo, nivel y categoría, estándares por indicador y % Acept."""

from sqlalchemy import CheckConstraint, Column, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.mssql import BIT, DATETIME

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
    nivel_centro = Column(String(50), nullable=False)
    anio = Column(Integer, nullable=False)


class TmiEstandarCategoria(_EstandarMensual, Base):
    __tablename__ = "tmi_estandar_categoria"
    __table_args__ = {"schema": TMI_SCHEMA}
    id = Column(Integer, primary_key=True)
    id_indicador = Column(Integer, ForeignKey(TmiIndicador.id), nullable=False)
    categoria_centro = Column(String(50), nullable=False)
    anio = Column(Integer, nullable=False)


class TmiIndicadorEstandar(Base):
    """Estándares del indicador por nivel, categoría, tipo o combinación de ellos, y por periodo (AAAAMM)."""
    __tablename__ = "tmi_indicador_estandar"
    __table_args__ = {"schema": TMI_SCHEMA}
    id = Column(Integer, primary_key=True)
    id_indicador = Column(Integer, ForeignKey(TmiIndicador.id), nullable=False)
    nivel = Column(String(50))
    categoria = Column(String(50))
    tipo = Column(String(50))
    periodo_desde = Column(Integer, nullable=False, server_default=defecto(200001))
    periodo_hasta = Column(Integer, nullable=False, server_default=defecto(999912))
    estandar = Column(Float, nullable=False)
    acept = Column(Float)                                      # % Acept (en banda, el de arriba)
    aceptmenos = Column(Float)                                 # % Aceptmenos (solo banda, el de abajo)
    activo = Column(BIT, nullable=False, server_default=defecto(1))


class TmiIndicadorTolerancia(Base):
    """% Acept por año: mes = 0 es el fijo del año; mes = 1..12 el valor de cada mes, que toma el fijo en su
    fecha de cierre."""
    __tablename__ = "tmi_indicador_tolerancia"
    __table_args__ = (
        CheckConstraint("mes BETWEEN 0 AND 12", name="CK_tmi_indicador_tolerancia_mes"),
        CheckConstraint("tipo_tolerancia IN ('REL', 'ABS')", name="CK_tmi_indicador_tolerancia_tipo"),
        UniqueConstraint("id_indicador", "anio", "mes", name="UX_tmi_indicador_tolerancia"),
        {"schema": TMI_SCHEMA},
    )
    id = Column(Integer, primary_key=True)
    id_indicador = Column(Integer, ForeignKey(TmiIndicador.id), nullable=False)
    anio = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    tipo_tolerancia = Column(String(3), nullable=False, server_default=defecto("REL"))
    tolerancia = Column(Float, nullable=False)
    tolerancia_menos = Column(Float)
    usuario_modificacion = Column(String(200))
    fecha_modificacion = Column(DATETIME)
