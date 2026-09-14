from typing import Optional
from pydantic import BaseModel

class cierreDto(BaseModel):
    id: Optional[int] = None
    fecha_cierre: Optional[str] = None
    periodo: Optional[str] = None
    estado: Optional[str] = None

class tmiEstandarTipoDto(BaseModel):
    id: Optional[int] = None
    tipo: Optional[str] = None
    indicador: Optional[str] = None
    tipo_centro: Optional[str] = None
    anio: Optional[int] = None
    mes: Optional[int] = None
    periodo: Optional[str] = None
    estandar: Optional[float] = None
    acept: Optional[float] = None
    aceptmenos: Optional[float] = None

class tmiEstandarNivelDto(BaseModel):
    id: Optional[int] = None
    tipo: Optional[str] = None
    indicador: Optional[str] = None
    nivel_centro: Optional[str] = None
    anio: Optional[int] = None
    mes: Optional[int] = None
    periodo: Optional[str] = None
    estandar: Optional[float] = None
    acept: Optional[float] = None
    aceptmenos: Optional[float] = None

class tmiEstandarCategoriaDto(BaseModel):
    id: Optional[int] = None
    tipo: Optional[str] = None
    indicador: Optional[str] = None
    categoria_centro: Optional[str] = None
    anio: Optional[int] = None
    mes: Optional[int] = None
    periodo: Optional[str] = None
    estandar: Optional[float] = None
    acept: Optional[float] = None
    aceptmenos: Optional[float] = None



class centroTmiDto(BaseModel):
    id: Optional[int] = None
    red: Optional[str] = None
    codred: Optional[str] = None
    orden: Optional[str] = None
    orden_tipo: Optional[str] = None
    codcentro: Optional[str] = None
    categoria: Optional[str] = None
    nivel: Optional[str] = None
    tipo: Optional[str] = None
    centro: Optional[str] = None
    estado: Optional[str] = None
    anio: Optional[int] = None
    mes: Optional[int] = None
    periodo: Optional[str] = None

