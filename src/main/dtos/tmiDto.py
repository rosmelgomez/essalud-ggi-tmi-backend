from pydantic import BaseModel

class cierreDto(BaseModel):
    id: int
    fecha_cierre:str
    periodo:str
    estado:str

class estandaresDto(BaseModel):
    id: int
    orden_indicador: int
    codigo_unico: str
    tipo: str
    indicador: str
    nivel_centro: str
    tipo_centro: str
    nivel_estandar_centro: str
    estandar: float
    acept: float
    aceptmenos: float

class centroTmiDto(BaseModel):
   id: int
   red: str
   orden: int
   orden_tipo: str
   codcentro: str
   tipo: str
   nivel: str
   nivel_estandar: str  
   centro: str
   estado: str 


class historicoEstandarCentrosDto(BaseModel):
    id:int
    codcentro:str
    fecha: str
    periodo:str
    estandar:float
    acept:float
    aceptmenos:float
    centro:str