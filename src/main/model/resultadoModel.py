"""Resultados del cálculo (los llena usp_tmi_calcular)."""

from sqlalchemy import Column, Float, ForeignKey, Integer, PrimaryKeyConstraint, String
from sqlalchemy.dialects.mssql import BIT, DATETIME, TINYINT

from src.main.model.base import AHORA, TMI_SCHEMA, Base, defecto
from src.main.model.variableModel import TmiVariable


class TmiVariablePivot(Base):
    __tablename__ = "tmi_variable_pivot"
    __table_args__ = (PrimaryKeyConstraint("anio", "codcentro", "id_variable", name="PK_tmi_variable_pivot"),
                      {"schema": TMI_SCHEMA})
    anio = Column(Integer, nullable=False, autoincrement=False)
    codcentro = Column(Integer, nullable=False, autoincrement=False)
    id_variable = Column(Integer, ForeignKey(TmiVariable.id), nullable=False, autoincrement=False)
    total = Column(Float)
    m01 = Column(Float)
    m02 = Column(Float)
    m03 = Column(Float)
    m04 = Column(Float)
    m05 = Column(Float)
    m06 = Column(Float)
    m07 = Column(Float)
    m08 = Column(Float)
    m09 = Column(Float)
    m10 = Column(Float)
    m11 = Column(Float)
    m12 = Column(Float)
    fecha_calculo = Column(DATETIME, nullable=False, server_default=AHORA)


class TmiResultado(Base):
    __tablename__ = "tmi_resultado"
    __table_args__ = (PrimaryKeyConstraint("periodo_corte", "id_indicador", "codcentro", "mes", name="PK_tmi_resultado"),
                      {"schema": TMI_SCHEMA})
    periodo_corte = Column(Integer, nullable=False, autoincrement=False)
    id_indicador = Column(Integer, nullable=False, autoincrement=False)
    codcentro = Column(Integer, nullable=False, autoincrement=False)
    mes = Column(TINYINT, nullable=False, autoincrement=False)
    numerador = Column(Float)
    denominador = Column(Float)
    valor = Column(Float)
    estandar = Column(Float)
    verde = Column(Float)
    acept = Column(Float)                                      # % Acept: límite para el puntaje 3 (en banda, el de arriba)
    aceptmenos = Column(Float)                                 # % Aceptmenos: solo banda, el de abajo
    puntaje = Column(String(2), nullable=False)                # 5 | 3 | 1 | 0 | NA
    motivo_na = Column(String(30))
    visible = Column(BIT, nullable=False, server_default=defecto(1))
    fecha_calculo = Column(DATETIME, nullable=False, server_default=AHORA)


class TmiResultadoIndicador(Base):
    """Resultado final por indicador (una fila por centro, como la hoja del Excel). periodo = mes en que se calculó
    (AAAAMM); total = valor al mes del periodo; periodo_01..12 = valor de cada mes (0 después del periodo,
    NULL si el mes es NA). Los periodos cerrados no se recalculan y su Excel se arma con lo guardado aquí."""
    __tablename__ = "tmi_resultado_indicador"
    __table_args__ = (PrimaryKeyConstraint("periodo", "id_indicador", "codcentro", name="PK_tmi_resultado_indicador"),
                      {"schema": TMI_SCHEMA})
    periodo = Column(Integer, nullable=False, autoincrement=False)
    anio = Column(Integer, nullable=False)
    id_indicador = Column(Integer, nullable=False, autoincrement=False)
    orden = Column(Integer)                                    # id del centro en tmi_centro
    orden_red = Column(Integer)                                # tmi_centro.orden: orden de la red en el reporte
    red = Column(String(100))
    codcentro = Column(Integer, nullable=False, autoincrement=False)
    centro = Column(String(200))
    nivel = Column(String(50))
    tipo = Column(String(50))
    categoria = Column(String(50))
    estandar = Column(Float)
    acept = Column(Float)                                      # % Acept (en banda, el de arriba)
    aceptmenos = Column(Float)                                 # % Aceptmenos (solo banda, el de abajo)
    total = Column(Float)
    puntaje = Column(String(2), nullable=False)
    motivo_na = Column(String(30))
    visible = Column(BIT, nullable=False, server_default=defecto(1))
    periodo_01 = Column(Float)
    periodo_02 = Column(Float)
    periodo_03 = Column(Float)
    periodo_04 = Column(Float)
    periodo_05 = Column(Float)
    periodo_06 = Column(Float)
    periodo_07 = Column(Float)
    periodo_08 = Column(Float)
    periodo_09 = Column(Float)
    periodo_10 = Column(Float)
    periodo_11 = Column(Float)
    periodo_12 = Column(Float)
    fecha_calculo = Column(DATETIME, nullable=False, server_default=AHORA)
