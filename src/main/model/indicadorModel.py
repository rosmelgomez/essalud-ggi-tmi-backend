"""Indicadores definidos por el usuario: secciones del reporte, fórmula, letras y ámbito."""

from sqlalchemy import CHAR, CheckConstraint, Column, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.mssql import BIT, DATE, NVARCHAR

from src.main.model.base import TMI_SCHEMA, Base, defecto
from src.main.model.variableModel import TmiVariable


class TmiTipoCalculo(Base):
    __tablename__ = "tmi_tipo_calculo"
    __table_args__ = {"schema": TMI_SCHEMA}
    codigo = Column(String(20), primary_key=True)
    descripcion = Column(String(200), nullable=False)


class TmiIndicador(Base):
    # base_estandar -> tmi_tipo_estandar.codigo: la FK la crea 03_datos.sql cuando los datos la cumplen
    __tablename__ = "tmi_indicador"
    __table_args__ = (
        CheckConstraint("formato IN ('NUMERO', 'PORCENTAJE')", name="CK_tmi_indicador_formato"),
        {"schema": TMI_SCHEMA},
    )
    id = Column(Integer, primary_key=True)                     # = id_indicador de las tablas de estándar
    grupo = Column(Integer)                                    # sección del reporte: DIM_GRUPO.tipgrupo
    indicador = Column(String(200))
    usuario_creacion = Column(String(200))
    usuario_modificacion = Column(String(200))
    fecha_creacion = Column(DATE)
    fecha_modificacion = Column(DATE)
    # hoja del Excel
    codigo = Column(String(20))                                # CE_Concent
    nombre_hoja = Column(String(31))                           # máx. 31 caracteres, sin [ ] : * ? / \
    titulo_hoja = Column(String(200))
    orden = Column(Integer)
    tipo_calculo = Column(String(20))                          # tmi_tipo_calculo: MENSUAL | ACUMULADO
    sin_datos_anio = Column(String(7), nullable=False, server_default=defecto("NA"))   # MOSTRAR (0) | NA | OCULTAR
    base_estandar = Column(String(30))                         # tmi_tipo_estandar.codigo (TIPO, NIVEL, NIVEL_TIPO...)
    sentido = Column(String(5))                                # MENOR | MAYOR | BANDA
    tipo_tolerancia = Column(String(3))                        # REL | ABS
    tolerancia = Column(Float)
    tolerancia_menos = Column(Float)                           # % Acept hacia abajo en banda (NULL = el de arriba)
    decimales = Column(Integer)
    cero_es_logro = Column(BIT, nullable=False, server_default=defecto(0))
    mostrar_no_aplica = Column(BIT, nullable=False, server_default=defecto(1))
    activo = Column(BIT, nullable=False, server_default=defecto(1))
    # fórmula con letras ((A - B) / C), fórmula con términos de TOTALIZADO3 ([3;50#0] - [3;49#0]) / [3;47#0]
    # y la expresión SQL sobre los términos (src/main/core/tmiFormula.py)
    formula_alias = Column(NVARCHAR(500))
    formula = Column(NVARCHAR(2000))
    formula_sql = Column(NVARCHAR(None))
    formato = Column(String(12), nullable=False, server_default=defecto("NUMERO"))     # NUMERO | PORCENTAJE


class TmiIndicadorTermino(Base):
    """Términos de la fórmula: una fila por término y servicio (servicio NULL = todos los servicios)."""
    __tablename__ = "tmi_indicador_termino"
    __table_args__ = {"schema": TMI_SCHEMA}
    id = Column(Integer, primary_key=True)
    id_indicador = Column(Integer, ForeignKey(TmiIndicador.id), nullable=False)
    codigo = Column(String(5), nullable=False)                 # T1, T2... (columna de la fórmula en formula_sql)
    tipgrupo = Column(Integer, nullable=False)
    actividad = Column(Integer, nullable=False)
    servicio = Column(Integer)
    mediana = Column(BIT, nullable=False, server_default=defecto(0))   # 1 = MEDIANA([..])
    texto = Column(String(60), nullable=False)                 # [g;a#s] como está en la fórmula


class TmiIndicadorVariable(Base):
    """Variable de cada letra de la fórmula (una variable por letra)."""
    __tablename__ = "tmi_indicador_variable"
    __table_args__ = (
        UniqueConstraint("id_indicador", "letra", "id_variable", name="UX_tmi_indicador_variable"),
        CheckConstraint("letra LIKE '[A-Z]'", name="CK_tmi_indicador_variable_letra"),
        {"schema": TMI_SCHEMA},
    )
    id = Column(Integer, primary_key=True)
    id_indicador = Column(Integer, ForeignKey(TmiIndicador.id), nullable=False)
    letra = Column(CHAR(1), nullable=False)
    id_variable = Column(Integer, ForeignKey(TmiVariable.id), nullable=False)


class TmiIndicadorAmbito(Base):
    """Qué centros entran a un indicador (por nivel, categoría, tipo, red o centro, y por periodo).
    Sin filas = todos. incluir = 1 lista blanca, 0 lista negra."""
    __tablename__ = "tmi_indicador_ambito"
    __table_args__ = {"schema": TMI_SCHEMA}
    id = Column(Integer, primary_key=True)
    id_indicador = Column(Integer, ForeignKey(TmiIndicador.id), nullable=False)
    red = Column(String(100))
    nivel = Column(String(50))                                 # valor de tmi_centro.nivel_estandar
    categoria = Column(String(50))
    tipo = Column(String(50))
    codcentro = Column(Integer)
    incluir = Column(BIT, nullable=False, server_default=defecto(1))
    periodo_desde = Column(Integer, nullable=False, server_default=defecto(200001))
    periodo_hasta = Column(Integer, nullable=False, server_default=defecto(999912))
