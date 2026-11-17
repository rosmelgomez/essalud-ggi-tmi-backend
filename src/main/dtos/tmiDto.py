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


class tmiCentroDto(BaseModel):
    id: Optional[int] = None
    codred: Optional[str] = None
    red: str
    codcentro: str
    centro:str
    categoria: Optional[str] = None
    nivel: Optional[str] = None             # nivel de atención (I, II, III): solo informativo, no entra al cálculo
    nivel_estandar: Optional[str] = None    # clave con la que el centro se une a los estándares de fuente NIVEL
    tipo: str
    flag: Optional[boolean] = True

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
    # cómo queda el mes excluido en el resultado final: 'NA' (no aplica; por defecto) o '0' (puntaje 0)
    resultado: Literal["NA", "0"] = "NA"
    # resultado propio de cada mes excluido; None = el de resultado
    res_01: Optional[Literal["NA", "0"]] = None
    res_02: Optional[Literal["NA", "0"]] = None
    res_03: Optional[Literal["NA", "0"]] = None
    res_04: Optional[Literal["NA", "0"]] = None
    res_05: Optional[Literal["NA", "0"]] = None
    res_06: Optional[Literal["NA", "0"]] = None
    res_07: Optional[Literal["NA", "0"]] = None
    res_08: Optional[Literal["NA", "0"]] = None
    res_09: Optional[Literal["NA", "0"]] = None
    res_10: Optional[Literal["NA", "0"]] = None
    res_11: Optional[Literal["NA", "0"]] = None
    res_12: Optional[Literal["NA", "0"]] = None
    # alta de varias exclusiones a la vez: un registro por indicador (si ya existe para el centro y año, se actualiza)
    ids_indicador: Optional[List[int]] = None
    # edición por periodo: solo cambia ese mes (1-12) del registro; los otros meses quedan como están
    mes: Optional[int] = Field(default=None, ge=1, le=12)
