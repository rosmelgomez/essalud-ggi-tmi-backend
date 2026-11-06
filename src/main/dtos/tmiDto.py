from datetime import date, datetime
from typing import Annotated, List, Literal, Optional
from xmlrpc.client import boolean
from pydantic import BaseModel, Field, model_validator


class _conIndicador(BaseModel):
    """id_indicador (DDL actual, -> tmi_indicador) o id_estandar (DDL anterior): se acepta cualquiera y se igualan."""
    id_indicador: Optional[int] = None
    id_estandar: Optional[int] = None

    @model_validator(mode="after")
    def _igualar_indicador(self):
        if self.id_indicador is None:
            self.id_indicador = self.id_estandar
        if self.id_estandar is None:
            self.id_estandar = self.id_indicador
        return self

_Dia = Optional[Annotated[int, Field(ge=1, le=31)]]


class cierreCalendarioDto(BaseModel):
    """Día de cierre de cada periodo del año: dia_fijo para todos; dia_MM solo donde ese periodo se cierra otro día."""
    dia_fijo: Annotated[int, Field(ge=1, le=31)]
    dia_01: _Dia = None
    dia_02: _Dia = None
    dia_03: _Dia = None
    dia_04: _Dia = None
    dia_05: _Dia = None
    dia_06: _Dia = None
    dia_07: _Dia = None
    dia_08: _Dia = None
    dia_09: _Dia = None
    dia_10: _Dia = None
    dia_11: _Dia = None
    dia_12: _Dia = None

class tmiEstandarDto(BaseModel):
    id: Optional[int] = None
    tipo: str
    indicador: str
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None

class tmiEstandarTipoDto(_conIndicador):
    id: Optional[int] = None
    tipo_centro: str
    anio: int 
    est_fijo: Optional[float] = None
    est_01: Optional[float] = None
    est_02: Optional[float] = None
    est_03: Optional[float] = None
    est_04: Optional[float] = None
    est_05: Optional[float] = None
    est_06: Optional[float] = None
    est_07: Optional[float] = None
    est_08: Optional[float] = None
    est_09: Optional[float] = None
    est_10: Optional[float] = None
    est_11: Optional[float] = None
    est_12: Optional[float] = None

class tmiEstandarNivelDto(_conIndicador):
    id: Optional[int] = None
    nivel_centro: str
    anio: int 
    est_fijo: Optional[float] = None
    est_01: Optional[float] = None
    est_02: Optional[float] = None
    est_03: Optional[float] = None
    est_04: Optional[float] = None
    est_05: Optional[float] = None
    est_06: Optional[float] = None
    est_07: Optional[float] = None
    est_08: Optional[float] = None
    est_09: Optional[float] = None
    est_10: Optional[float] = None
    est_11: Optional[float] = None
    est_12: Optional[float] = None

class tmiEstandarCategoriaDto(_conIndicador):
    id: Optional[int] = None
    categoria_centro: str
    anio: int 
    est_fijo: Optional[float] = None
    est_01: Optional[float] = None
    est_02: Optional[float] = None
    est_03: Optional[float] = None
    est_04: Optional[float] = None
    est_05: Optional[float] = None
    est_06: Optional[float] = None
    est_07: Optional[float] = None
    est_08: Optional[float] = None
    est_09: Optional[float] = None
    est_10: Optional[float] = None
    est_11: Optional[float] = None
    est_12: Optional[float] = None

class tmiCentroDto(BaseModel):
    id: Optional[int] = None
    codred: Optional[str] = None
    red: str
    orden: Optional[str] = None
    orden_tipo: Optional[str] = None
    codcentro: str
    centro:str
    categoria: Optional[str] = None
    nivel: Optional[str] = None             # nivel de atención (I, II, III): solo informativo, no entra al cálculo
    nivel_estandar: Optional[str] = None    # clave con la que el centro se une a los estándares de fuente NIVEL
    tipo: str
    flag: Optional[boolean] = True
    anio: Optional[int] = None
    flag_01: Optional[boolean] = None
    flag_02: Optional[boolean] = None
    flag_03: Optional[boolean] = None
    flag_04: Optional[boolean] = None
    flag_05: Optional[boolean] = None
    flag_06: Optional[boolean] = None
    flag_07: Optional[boolean] = None
    flag_08: Optional[boolean] = None
    flag_09: Optional[boolean] = None
    flag_10: Optional[boolean] = None
    flag_11: Optional[boolean] = None
    flag_12: Optional[boolean] = None

class tmiExclusionCentroEstandarDto(_conIndicador):
    id: Optional[int] = None
    id_centro: Optional[int] = None
    codcentro: Optional[str] = None
    anio: int
    excl_01: boolean = False
    excl_02: boolean = False
    excl_03: boolean = False
    excl_04: boolean = False
    excl_05: boolean = False
    excl_06: boolean = False
    excl_07: boolean = False
    excl_08: boolean = False
    excl_09: boolean = False
    excl_10: boolean = False
    excl_11: boolean = False
    excl_12: boolean = False
    motivo: Optional[str] = None
    # cómo queda el mes excluido en el resultado final: '0' (puntaje 0; por defecto) o 'NA' (no aplica)
    resultado: Literal["NA", "0"] = "0"
    # alta de varias exclusiones a la vez: un registro por indicador (si ya existe para el centro y año, se actualiza)
    ids_indicador: Optional[List[int]] = None
