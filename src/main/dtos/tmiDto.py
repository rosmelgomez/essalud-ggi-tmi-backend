from typing import Optional
from pydantic import BaseModel

class cierreDto(BaseModel):
    id: int
    fecha_cierre: str
    periodo: str
    estado: str

class tmiEstandarTipoDto(BaseModel):
    id: int
    tipo: str
    indicador: str
    tipo_centro: str
    anio: int 
    mes: int 
    periodo: str
    estandar: float
    acept: float
    aceptmenos: float

class tmiEstandarNivelDto(BaseModel):
    id: int
    tipo: str
    indicador: str
    nivel_centro: str
    anio: int 
    mes : int 
    periodo: str
    estandar: float
    acept: float
    aceptmenos: float

class tmiEstandarCategoriaDto(BaseModel):
    id: int
    tipo: str
    indicador: str
    categoria_centro: str
    anio: int 
    mes: int 
    periodo: str
    estandar: float
    acept: float
    aceptmenos: float

class centroTmiDto(BaseModel):
    id: int
    red: str
    codred: str
    orden: str
    orden_tipo: str
    codcentro: str
    categoria: str
    nivel: str
    tipo: str
    centro:str
    estado: str 
    anio: int 
    mes: int 
    periodo:str

