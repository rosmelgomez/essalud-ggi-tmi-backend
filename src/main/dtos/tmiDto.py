from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

class cierreDto(BaseModel):
    id: int
    periodo: str
    fecha_cierre: date
    estado: str
    fecha_ejecucion: Optional[datetime] = None
    filas_insertadas: Optional[int] = None
    mensaje: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    usuario_modifica: Optional[str] = None

class cierreUpdateDto(BaseModel):
    fecha_cierre: date

class tmiEstandarTipoDto(BaseModel):
    id: Optional[int] = None
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
    id: Optional[int] = None
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
    id: Optional[int] = None
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
    id: Optional[int] = None
    red: str
    codred: Optional[str] = None
    orden: str
    orden_tipo: str
    codcentro: str
    categoria: Optional[str] = None
    nivel: str
    tipo: str
    centro:str
    estado: str 
    anio: int 
    mes: int 
    periodo:str

