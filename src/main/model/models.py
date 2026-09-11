

from sqlalchemy import Double
from src.main.db.databaseConexion import Base
from sqlalchemy import Column, Integer, String

class cierre (Base):
    __tablename__ = "cierre"
    id = Column(Integer,primary_key=True)
    dia= Column(Integer(50))
    mes= Column(Integer(50))
    año= Column(Integer(50))
    fecha_creacion = Column(DateTime())
    estado = Column(String(50))   

class tmi_estandar_tipo(Base):
    __tablename__ = "tmi_estandar_tipo"
    id = Column(Integer,primary_key=True)
    tipo = Column(String(50))
    indicador = Column(String(50))
    tipo_centro = Column(String(50))
    anio = Column(Integer())
    periodo_01_estandar = Column(Double())
    periodo_02_estandar = Column(Double())
    periodo_03_estandar = Column(Double())
    periodo_04_estandar = Column(Double())
    periodo_05_estandar = Column(Double())
    periodo_06_estandar = Column(Double())
    periodo_07_estandar = Column(Double())
    periodo_08_estandar = Column(Double())
    periodo_09_estandar = Column(Double())
    periodo_10_estandar = Column(Double())
    periodo_11_estandar = Column(Double())
    periodo_12_estandar = Column(Double())
    


class tmi_estandar_nivel(Base):
    __tablename__ = "tmi_estandar_nivel"
    id = Column(Integer,primary_key=True)
    tipo = Column(String(50))
    indicador = Column(String(50))
    nivel_centro = Column(String(50))
    anio = Column(Integer())
    periodo_01_estandar = Column(Double())
    periodo_02_estandar = Column(Double())
    periodo_03_estandar = Column(Double())
    periodo_04_estandar = Column(Double())
    periodo_05_estandar = Column(Double())
    periodo_06_estandar = Column(Double())
    periodo_07_estandar = Column(Double())
    periodo_08_estandar = Column(Double())
    periodo_09_estandar = Column(Double())
    periodo_10_estandar = Column(Double())
    periodo_11_estandar = Column(Double())
    periodo_12_estandar = Column(Double())


class tmi_estandar_categoria(Base):
    __tablename__ = "tmi_estandar_categoria"
    id = Column(Integer,primary_key=True)
    tipo = Column(String(50))
    indicador = Column(String(50))
    categoria_centro = Column(String(50))
    anio = Column(Integer())
    periodo_01_estandar = Column(Double())
    periodo_02_estandar = Column(Double())
    periodo_03_estandar = Column(Double())
    periodo_04_estandar = Column(Double())
    periodo_05_estandar = Column(Double())
    periodo_06_estandar = Column(Double())
    periodo_07_estandar = Column(Double())
    periodo_08_estandar = Column(Double())
    periodo_09_estandar = Column(Double())
    periodo_10_estandar = Column(Double())
    periodo_11_estandar = Column(Double())
    periodo_12_estandar = Column(Double())


class tmi_centro(Base):
    __tablename__ = "tmi_centro"
    id = Column(Integer,primary_key=True)
    red = Column(String(100))
    orden = Column(Integer(50))
    orden_tipo = Column(String(50))
    codcentro = Column(String(50))
    tipo = Column(String(50))
    nivel = Column(String(50))
    nivel_estandar = Column(String(50))  
    centro = Column(String(100))
    estado = Column(String(50)) 
    periodo = Column(String(50))


