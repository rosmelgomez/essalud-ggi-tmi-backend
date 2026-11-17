"""Indicadores definidos por el usuario: secciones del reporte, fórmula, letras y ámbito."""

from sqlalchemy import CheckConstraint, Column, Integer, String
from sqlalchemy.dialects.mssql import BIT, DATE, NVARCHAR

from src.main.model.base import TMI_SCHEMA, Base, defecto


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
    # el % Acept (tipo_acept, acept, aceptmenos) está en tmi_indicador_acept, por año
    decimales = Column(Integer)
    cero_es_logro = Column(BIT, nullable=False, server_default=defecto(0))
    # regla de nulos de la fórmula (la elige el usuario por indicador; se aplica al leer la fórmula para calcular)
    si_variable_nula = Column(String(4), nullable=False, server_default=defecto("CERO"))   # CERO: ISNULL(letra,0) | NA: la letra sin dato deja el mes en NA
    si_division_cero = Column(String(4), nullable=False, server_default=defecto("NA"))     # NA: x/0 = NA | CERO: x/0 = 0
    mostrar_no_aplica = Column(BIT, nullable=False, server_default=defecto(1))
    activo = Column(BIT, nullable=False, server_default=defecto(1))
    # fórmula con letras ((A - B) / C) y fórmula con términos de TOTALIZADO3 ([3;50#0] - [3;49#0]) / [3;47#0]
    # (src/main/core/tmiFormula.py)
    formula_alias = Column(NVARCHAR(500))
    # la misma fórmula con el id de la variable de cada letra entre llaves: A / B -> {1} / {2} (A = variable 1)
    formula_variable = Column(NVARCHAR(500))
    formula = Column(NVARCHAR(2000))
    # los términos de la fórmula, la expresión SQL y la plantilla del desarrollo no se guardan: Python los lee de
    # formula cada vez que se calcula (tmiBaseRep.crear_tablas_formula -> #formula y #termino)
    formato = Column(String(12), nullable=False, server_default=defecto("NUMERO"))     # NUMERO | PORCENTAJE
