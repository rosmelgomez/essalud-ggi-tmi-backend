

from sqlalchemy import Boolean, Double
from src.main.db.databaseConexion import Base
from sqlalchemy import Column, Date, DateTime, Integer, String

class cierre (Base):
    __tablename__ = "cierre"
    id = Column(Integer, primary_key=True)
    periodo = Column(String(6), nullable=False, unique=True)
    fecha_cierre = Column(Date(), nullable=False)
    estado = Column(String(20), nullable=False, default="PENDIENTE")
    fecha_ejecucion = Column(DateTime())
    filas_insertadas = Column(Integer())
    mensaje = Column(String(4000))
    fecha_creacion = Column(DateTime())
    usuario_modifica = Column(String(100))

class tmi_estandar(Base):
    __tablename__ = "tmi_estandar"
    id = Column(Integer,primary_key=True)
    tipo = Column(String(50))
    indicador = Column(String(50))
    ##anio = Column(Integer())

    

class tmi_estandar_tipo(Base):
    __tablename__ = "tmi_estandar_tipo"
    id = Column(Integer,primary_key=True)
    id_estandar = Column(Integer())
    tipo_centro = Column(String(50))
    anio = Column(Integer())
    estandar_01 = Column(Double())
    estandar_02 = Column(Double())
    estandar_03 = Column(Double())
    estandar_04 = Column(Double())
    estandar_05 = Column(Double())
    estandar_06 = Column(Double())
    estandar_07 = Column(Double())
    estandar_08 = Column(Double())
    estandar_09 = Column(Double())
    estandar_10 = Column(Double())
    estandar_11 = Column(Double())
    estandar_12 = Column(Double())


class tmi_estandar_nivel(Base):
    __tablename__ = "tmi_estandar_nivel"
    id = Column(Integer,primary_key=True)
    id_estandar = Column(Integer())
    nivel_centro = Column(String(50))
    anio = Column(Integer())
    estandar_01 = Column(Double())
    estandar_02 = Column(Double())
    estandar_03 = Column(Double())
    estandar_04 = Column(Double())
    estandar_05 = Column(Double())
    estandar_06 = Column(Double())
    estandar_07 = Column(Double())
    estandar_08 = Column(Double())
    estandar_09 = Column(Double())
    estandar_10 = Column(Double())
    estandar_11 = Column(Double())
    estandar_12 = Column(Double())


class tmi_estandar_categoria(Base):
    __tablename__ = "tmi_estandar_categoria"
    id = Column(Integer,primary_key=True)
    id_estandar = Column(Integer(), ForeignKey("tmi_estandar.id"))
    categoria_centro = Column(String(50))
    anio = Column(Integer())
    estandar_01 = Column(Double())
    estandar_02 = Column(Double())
    estandar_03 = Column(Double())
    estandar_04 = Column(Double())
    estandar_05 = Column(Double())
    estandar_06 = Column(Double())
    estandar_07 = Column(Double())
    estandar_08 = Column(Double())
    estandar_09 = Column(Double())
    estandar_10 = Column(Double())
    estandar_11 = Column(Double())
    estandar_12 = Column(Double())


class tmi_centro(Base):
    __tablename__ = "tmi_centro"
    id = Column(Integer,primary_key=True)
    red = Column(String(100))
    orden = Column(Integer(50))
    orden_tipo = Column(String(50))
    codcentro = Column(String(50))
    centro = Column(String(100))
    categoria = Column(String(50))
    nivel = Column(String(50))
    tipo = Column(String(50))
    anio = Column(Integer())
    flag_01 = Column(Boolean())
    flag_02 = Column(Boolean())
    flag_03 = Column(Boolean())
    flag_04 = Column(Boolean())
    flag_05 = Column(Boolean())
    flag_06 = Column(Boolean())
    flag_07 = Column(Boolean())
    flag_08 = Column(Boolean())
    flag_09 = Column(Boolean())
    flag_10 = Column(Boolean())
    flag_11 = Column(Boolean())
    flag_12 = Column(Boolean())


