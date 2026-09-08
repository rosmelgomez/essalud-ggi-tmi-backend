

from sqlalchemy import Double
from src.main.db.databaseConexion import Base
from sqlalchemy import Column, Integer, String

class cierre (Base):
    __tablename__ = "cierre"
    id = Column(Integer,primary_key=True)
    fecha_cierre = Column(String(50))
    año= Column(Integer(50))
    periodo = Column(String(50))
    estado = Column(String(50))   

class tmi_estandar(Base):
    __tablename__ = "tmi_estandar"
    id = Column(Integer,primary_key=True)
    orden_indicador = Column(Integer())
    codigo_unico = Column(String(50))
    tipo = Column(String(50))
    indicador = Column(String(50))
    nivel_centro = Column(String(50))
    tipo_centro = Column(String(50))
    nivel_estandar_centro = Column(String(50))
    estandar = Column(Double())
    acept=Column(Double())
    aceptmenos= Column(Double())
    periodo=Column(String(50))


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


