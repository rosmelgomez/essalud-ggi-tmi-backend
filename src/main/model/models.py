

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
    mes = Column(Integer())
    periodo = Column(String(50))
    estandar = Column(Double())
    acept = Column(Double())
    aceptmenos = Column(Double())
    


class tmi_estandar_nivel(Base):
    __tablename__ = "tmi_estandar_nivel"
    id = Column(Integer,primary_key=True)
    tipo = Column(String(50))
    indicador = Column(String(50))
    nivel_centro = Column(String(50))
    anio = Column(Integer())
    mes = Column(Integer())
    periodo = Column(String(50))
    estandar = Column(Double())
    acept = Column(Double())
    aceptmenos = Column(Double())


class tmi_estandar_categoria(Base):
    __tablename__ = "tmi_estandar_categoria"
    id = Column(Integer,primary_key=True)
    tipo = Column(String(50))
    indicador = Column(String(50))
    categoria_centro = Column(String(50))
    anio = Column(Integer())
    mes = Column(Integer())
    periodo = Column(String(50))
    estandar = Column(Double())
    acept = Column(Double())
    aceptmenos = Column(Double())


class tmi_centro(Base):
    __tablename__ = "tmi_centro"
    id = Column(Integer,primary_key=True)
    red = Column(String(100))
    orden = Column(Integer(50))
    orden_tipo = Column(String(50))
    codcentro = Column(String(50))
    categoria = Column(String(50))
    nivel = Column(String(50))
    tipo = Column(String(50))
    centro = Column(String(100))
    estado = Column(String(50)) 
    anio = Column(Integer())
    mes = Column(Integer())
    periodo = Column(String(50))


