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

class tmiEstandarDto(BaseModel):
    id: Optional[int] = None
    tipo: str
    indicador: str
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None

class tmiEstandarTipoDto(BaseModel):
    id: Optional[int] = None
    id_estandar: int
    tipo_centro: str
    anio: int 
    estandar_01: float
    estandar_02: float
    estandar_03: float
    estandar_04: float
    estandar_05: float
    estandar_06: float
    estandar_07: float
    estandar_08: float
    estandar_09: float
    estandar_10: float
    estandar_11: float
    estandar_12: float  

class tmiEstandarNivelDto(BaseModel):
    id: Optional[int] = None
    id_estandar: int
    nivel_centro: str
    anio: int 
    estandar_01: float
    estandar_02: float
    estandar_03: float
    estandar_04: float
    estandar_05: float
    estandar_06: float
    estandar_07: float
    estandar_08: float
    estandar_09: float
    estandar_10: float
    estandar_11: float
    estandar_12: float

class tmiEstandarCategoriaDto(BaseModel):
    id: Optional[int] = None
    id_estandar: int
    categoria_centro: str
    anio: int 
    estandar_01: float
    estandar_02: float
    estandar_03: float
    estandar_04: float
    estandar_05: float
    estandar_06: float
    estandar_07: float
    estandar_08: float
    estandar_09: float
    estandar_10: float
    estandar_11: float
    estandar_12: float

class centroTmiDto(BaseModel):
    id: Optional[int] = None
    red: str
    orden: str
    orden_tipo: str
    codcentro: str
    centro:str
    categoria: Optional[str] = None
    nivel: str
    tipo: str
    anio: int 
    flag_01: Optional[bool] = None
    flag_02: Optional[bool] = None
    flag_03: Optional[bool] = None
    flag_04: Optional[bool] = None
    flag_05: Optional[bool] = None
    flag_06: Optional[bool] = None
    flag_07: Optional[bool] = None
    flag_08: Optional[bool] = None
    flag_09: Optional[bool] = None
    flag_10: Optional[bool] = None
    flag_11: Optional[bool] = None
    flag_12: Optional[bool] = None

