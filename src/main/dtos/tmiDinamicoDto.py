"""DTOs del TMI dinámico (tablas de src/resources/sql/tmi)."""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class tmiVariableDto(BaseModel):
    nombre: str = Field(min_length=1, max_length=200)
    descripcion: Optional[str] = Field(default=None, max_length=200)
    total_anual: Literal["SUMA_MESES", "MEDIANA_PERIODO"] = "SUMA_MESES"
    activo: bool = True


class tmiVariableLogicaDto(BaseModel):
    id_variable: int
    tipgrupo: int
    actividad: int
    servicio: Optional[int] = None
    condicion_hoja: Optional[str] = Field(default=None, max_length=20)
    agregacion: Literal["SUMA", "MEDIANA"] = "SUMA"
    periodo_desde: int = Field(default=200001, ge=200001, le=999912)
    periodo_hasta: int = Field(default=999912, ge=200001, le=999912)
    activo: bool = True


class tmiIndicadorDto(BaseModel):
    grupo: Optional[int] = None
    indicador: str = Field(min_length=1, max_length=200)
    codigo: str = Field(min_length=1, max_length=20)
    nombre_hoja: str = Field(min_length=1, max_length=31, pattern=r"^[^\[\]:*?/\\]+$")
    titulo_hoja: Optional[str] = Field(default=None, max_length=200)
    orden: int = 1
    expr_numerador: str = Field(min_length=1, max_length=200, pattern=r"^[A-Z0-9 ().+*-]+$")
    expr_denominador: str = Field(min_length=1, max_length=200, pattern=r"^[A-Z0-9 ().+*-]+$")
    tipo_calculo: str = "MENSUAL"
    factor: float = 1
    den_cero: Literal["CERO", "NA"] = "CERO"
    num_cero_na: bool = False
    cero_si_letra_mes_0: bool = False
    sin_datos_anio: Literal["MOSTRAR", "NA", "OCULTAR"] = "NA"
    base_estandar: Literal[
        "TIPO", "NIVEL", "CATEGORIA",
        "TIPO_NIVEL", "TIPO_CATEGORIA", "NIVEL_CATEGORIA", "TIPO_NIVEL_CATEGORIA"
    ] = "TIPO"
    sentido: Literal["MENOR", "MAYOR", "BANDA"] = "MENOR"
    tipo_tolerancia: Literal["REL", "ABS"] = "REL"
    tolerancia: float = 0.1
    decimales: Optional[int] = Field(default=None, ge=0, le=10)
    cero_es_logro: bool = False
    mostrar_no_aplica: bool = True
    activo: bool = True
    formato: Literal["NUMERO", "PORCENTAJE"] = "NUMERO"   # formato de los valores en el Excel


class tmiIndicadorVariableDto(BaseModel):
    id_indicador: int
    letra: str = Field(pattern=r"^[A-Z]$")
    id_variable: int


class tmiIndicadorAmbitoDto(BaseModel):
    id_indicador: int
    red: Optional[str] = Field(default=None, max_length=100)
    nivel: Optional[str] = Field(default=None, max_length=50)
    categoria: Optional[str] = Field(default=None, max_length=50)
    tipo: Optional[str] = Field(default=None, max_length=50)
    codcentro: Optional[int] = None
    incluir: bool = True
    periodo_desde: int = 200001
    periodo_hasta: int = 999912


class tmiIndicadorEstandarDto(BaseModel):
    id_indicador: int
    nivel: Optional[str] = Field(default=None, max_length=50)
    categoria: Optional[str] = Field(default=None, max_length=50)
    tipo: Optional[str] = Field(default=None, max_length=50)
    periodo_desde: int = Field(default=202601, ge=200001, le=999912)
    periodo_hasta: int = Field(default=202612, ge=200001, le=999912)
    estandar: float
    acept: Optional[float] = None
    acept_mas: Optional[float] = None
    activo: bool = True


class tmiCentroEstandarDto(BaseModel):
    codcentro: str = Field(min_length=1, max_length=50)
    id_indicador: int
    anio: int
    aplica: bool = True
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
    acept: Optional[float] = None
    sustento: Optional[str] = Field(default=None, max_length=300)
