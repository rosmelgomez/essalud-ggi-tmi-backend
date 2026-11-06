"""Resultados del cálculo (los llena usp_tmi_calcular)."""

from sqlalchemy import Column, Float, Integer, PrimaryKeyConstraint, String
from sqlalchemy.dialects.mssql import BIT, DATETIME

from src.main.model.base import AHORA, TMI_SCHEMA, Base, defecto


class TmiResultado(Base):
    """Resultado del cálculo: una fila por periodo de corte, indicador y centro (codcentro = código del centro en
    tmi_centro, no su id), con el valor (MENSUAL: el del mes; ACUMULADO: enero..corte), estándar y puntaje de ese
    periodo. Solo se calcula el mes de corte: el valor de cada mes es el de la fila de su periodo. Cada periodo
    calculado guarda sus filas: al cerrar el año hay 12 periodos."""
    __tablename__ = "tmi_resultado"
    __table_args__ = (PrimaryKeyConstraint("periodo_corte", "id_indicador", "codcentro", name="PK_tmi_resultado"),
                      {"schema": TMI_SCHEMA})
    periodo_corte = Column(Integer, nullable=False, autoincrement=False)
    id_indicador = Column(Integer, nullable=False, autoincrement=False)
    codcentro = Column(Integer, nullable=False, autoincrement=False)
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
    (AAAAMM); total = valor al mes del periodo; periodo_01..12 = valor de cada mes, tomado de tmi_resultado de su
    propio periodo de corte (0 después del periodo; NULL si el mes es NA o no se calculó). Los periodos cerrados no se recalculan y su Excel se arma con lo guardado aquí."""
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
    nivel = Column(String(50))                                 # nivel del centro (I, II, III): el Excel usa nivel y tipo
    nivel_estandar = Column(String(50))                        # solo informativo: clave con la que se unió al estándar
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
