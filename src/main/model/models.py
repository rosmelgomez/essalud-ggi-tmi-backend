

from sqlalchemy import Double
from src.main.db.databaseConexion import Base
from sqlalchemy import Column, Integer, String

class cierre (Base):
    __tablename__ = "cierre"
    id = Column(Integer,primary_key=True)
    fecha_cierre = Column(String(50))
    periodo = Column(String(50))
    estado = Column(String(50))   

class estandares(Base):
    __tablename__ = "estandares"
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


class centros_tmi(Base):
    __tablename__ = "centros_tmi"
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
    
class hsitoricoEstandarCentros(Base):
    __tablename__ = "hsitorico_estandar_centros"
    id = Column(Integer,primary_key=True)
    codcentro = Column(String(50))
    fecha = Column(String(50))
    periodo = Column(String(50))
    estandar = Column(Double())
    acept = Column(Double())
    aceptmenos = Column(Double())
    centro = Column(String(50))