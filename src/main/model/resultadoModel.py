"""Resultados del cálculo (los llena usp_tmi_calcular)."""

from sqlalchemy import BigInteger, CheckConstraint, Column, Float, Index, Integer, PrimaryKeyConstraint, String
from sqlalchemy.dialects.mssql import BIT, DATETIME, NVARCHAR

from src.main.model.base import AHORA, TMI_SCHEMA, Base, defecto


class TmiResultado(Base):
    """Resultado del cálculo: una fila por periodo de corte, indicador y centro (codcentro = código del centro en
    tmi_centro, no su id), con el valor (MENSUAL: el del mes; ACUMULADO: enero..corte), estándar y puntaje de ese
    periodo. Solo se calcula el mes de corte: el valor de cada mes es el de la fila de su periodo. Cada periodo
    calculado guarda sus filas: al cerrar el año hay 12 periodos.
    origen_datos: de dónde salieron los datos. BACKUP = la copia de TOTALIZADO3 del cierre del periodo
    (TOTALIZADO3_BACKUP, "como fue"); ACTUAL = TOTALIZADO3 de hoy. Los dos conviven: el oficial del periodo es BACKUP
    si existe, si no ACTUAL (vista vw_tmi_resultado). La fórmula y su desarrollo justifican cómo se llegó al valor;
    el valor de cada término está en tmi_resultado_termino."""
    __tablename__ = "tmi_resultado"
    __table_args__ = (PrimaryKeyConstraint("periodo_corte", "origen_datos", "id_indicador", "codcentro",
                                           name="PK_tmi_resultado"),
                      CheckConstraint("origen_datos IN ('ACTUAL', 'BACKUP')", name="CK_tmi_resultado_origen"),
                      {"schema": TMI_SCHEMA})
    periodo_corte = Column(Integer, nullable=False, autoincrement=False)
    origen_datos = Column(String(10), nullable=False, server_default=defecto("ACTUAL"))
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
    periodo_backup = Column(Integer)                           # copia de TOTALIZADO3_BACKUP usada (NULL = ACTUAL)
    tipo_calculo = Column(String(20))                          # MENSUAL | ACUMULADO, como estaba al calcular
    formula_alias = Column(NVARCHAR(500))                      # (A - B) / C, como estaba al calcular
    formula = Column(NVARCHAR(2000))                           # ([3;50] - [3;49]) / [3;47], como estaba al calcular
    formula_desarrollo = Column(NVARCHAR(4000))                # (135 - 20) / 160 = 0.71875
    usuario_calculo = Column(NVARCHAR(50))


class TmiResultadoTermino(Base):
    """Justificación del resultado: valor de cada término de la fórmula (T1, T2...) por periodo de corte, origen de
    los datos, indicador y centro, con su grupo, actividad y servicio (servicio NULL = todos). Una fila por término y
    servicio, como tmi_indicador_termino. valor_mes = el del mes de corte; valor = el que entró en la fórmula (en un
    indicador ACUMULADO, enero..corte sin los meses excluidos); filas = filas de TOTALIZADO3 que se sumaron."""
    __tablename__ = "tmi_resultado_termino"
    __table_args__ = (Index("IX_tmi_resultado_termino", "periodo_corte", "origen_datos", "id_indicador", "codcentro"),
                      {"schema": TMI_SCHEMA})
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    periodo_corte = Column(Integer, nullable=False)
    origen_datos = Column(String(10), nullable=False)
    id_indicador = Column(Integer, nullable=False)
    codcentro = Column(Integer, nullable=False)
    codigo = Column(String(5), nullable=False)                 # T1, T2...
    tipgrupo = Column(Integer, nullable=False)
    actividad = Column(Integer, nullable=False)
    servicio = Column(Integer)
    mediana = Column(BIT, nullable=False, server_default=defecto(0))
    texto = Column(String(60))                                 # [g;a#s] como está en la fórmula
    valor_mes = Column(Float)                                  # mes de corte
    valor = Column(Float)                                      # el que entró en la fórmula
    filas_mes = Column(Integer)                                # filas de TOTALIZADO3 del mes de corte
    filas = Column(Integer)                                    # filas de TOTALIZADO3 que entraron en valor


class Totalizado3Backup(Base):
    """Copia de TOTALIZADO3 por periodo: la misma estructura (mismas columnas, tipos y orden) más las columnas de la
    copia. La copia del periodo P tiene TOTALIZADO3 de enero a P de ese año tal como estaba al copiarse (al cierre de
    P, o cargada desde el backup del estadístico). Una copia guardada no se pisa salvo que se recargue a propósito.
    TOTALIZADO3 nunca se modifica: solo se lee para copiarlo."""
    __tablename__ = "TOTALIZADO3_BACKUP"
    __table_args__ = (PrimaryKeyConstraint("periodo_backup", "ID", name="PK_TOTALIZADO3_BACKUP"),
                      Index("IX_TOTALIZADO3_BACKUP_calculo", "periodo_backup", "periodo", "tipgrupo",
                            mssql_include=["codcentro_ses", "actividad", "servicio", "cantidad"]),
                      {"schema": TMI_SCHEMA})
    ID = Column(BigInteger, nullable=False, autoincrement=False)
    periodo = Column(Integer)
    codred_ses = Column(Integer)
    red_ses = Column(NVARCHAR(50))
    codcentro_ses = Column(Integer)
    desccentro_ses = Column(NVARCHAR(100))
    codredsgh = Column(Integer)
    redsgh = Column(NVARCHAR(50))
    codcentrosgh = Column(Integer)
    descripcionsgh = Column(NVARCHAR(50))
    nivel = Column(NVARCHAR(20))
    tipgrupo = Column(Integer)
    desctipgrupo = Column(NVARCHAR(100))
    actividad = Column(Integer)
    descactividad = Column(NVARCHAR(50))
    servicio = Column(Integer)
    descservicio = Column(NVARCHAR(50))
    cantidad = Column(Integer)
    usuariocrea = Column(NVARCHAR(20))
    fechacrea = Column(DATETIME)
    usuariomod = Column(NVARCHAR(20))
    fechamod = Column(DATETIME)
    tiponivel = Column(Integer)
    descnivel = Column(NVARCHAR(20))
    tipohoja = Column(Integer)
    # columnas de la copia
    periodo_backup = Column(Integer, nullable=False, autoincrement=False)   # AAAAMM: la copia del cierre de ese periodo
    fecha_backup = Column(DATETIME, nullable=False, server_default=AHORA)
    usuario_backup = Column(NVARCHAR(50))


class TmiResultadoIndicador(Base):
    """Resultado final por indicador (una fila por centro, como la hoja del Excel). periodo = mes en que se calculó
    (AAAAMM); total = valor al mes del periodo; periodo_01..12 = valor de cada mes, tomado de tmi_resultado de su
    propio periodo de corte (0 después del periodo; NULL si el mes es NA o no se calculó). Los periodos cerrados no se recalculan y su Excel se arma con lo guardado aquí."""
    __tablename__ = "tmi_resultado_indicador"
    __table_args__ = (PrimaryKeyConstraint("periodo", "origen_datos", "id_indicador", "codcentro",
                                           name="PK_tmi_resultado_indicador"),
                      {"schema": TMI_SCHEMA})
    periodo = Column(Integer, nullable=False, autoincrement=False)
    # de qué datos salió: BACKUP = copia del cierre (TOTALIZADO3_BACKUP); ACTUAL = TOTALIZADO3. Se guardan los dos;
    # el oficial (vw_tmi_resultado_indicador) es BACKUP si existe
    origen_datos = Column(String(10), nullable=False, server_default=defecto("ACTUAL"))
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
    periodo_backup = Column(Integer)
