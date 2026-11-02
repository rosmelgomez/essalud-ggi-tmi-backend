"""DTOs del TMI dinámico (tablas de src/resources/sql/tmi)."""

import re
from typing import Dict, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class tmiVariableDto(BaseModel):
    """El cálculo es de la variable (como en Generar_pivot.sql): todos sus conjuntos se combinan con OR y se
    calcula SUMA o MEDIANA por servicio. La mediana del periodo como total anual solo aplica a MEDIANA."""
    nombre: str = Field(min_length=1, max_length=200)
    descripcion: Optional[str] = Field(default=None, max_length=200)
    agregacion: Literal["SUMA", "MEDIANA"] = "SUMA"
    total_anual: Literal["SUMA_MESES", "MEDIANA_PERIODO"] = "SUMA_MESES"
    activo: bool = True

    @model_validator(mode="after")
    def _total_segun_calculo(self):
        if self.agregacion == "SUMA":
            self.total_anual = "SUMA_MESES"
        return self


class tmiVariableComponenteDto(BaseModel):
    """Variable compuesta: id_variable suma el valor de id_variable_componente (además de su propia lógica)."""
    id_variable: int
    id_variable_componente: int
    activo: bool = True


class tmiVariableLogicaDto(BaseModel):
    id_variable: int
    tipgrupo: int
    actividad: int
    servicio: Optional[int] = None
    condicion_hoja: Optional[str] = Field(default=None, max_length=20)
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
    # La fórmula se guarda con PUT /indicadores/{id}/formula; crear o editar el indicador no la cambia.
    tipo_calculo: str = "MENSUAL"
    sin_datos_anio: Literal["MOSTRAR", "NA", "OCULTAR"] = "NA"
    base_estandar: str = Field(default="TIPO", min_length=1, max_length=30)   # tmi_tipo_estandar.codigo (FK)
    sentido: Literal["MENOR", "MAYOR", "BANDA"] = "MENOR"
    tipo_tolerancia: Literal["REL", "ABS"] = "REL"   # % Acept: REL = % del estándar | ABS = puntos
    tolerancia: float = 0.1
    tolerancia_menos: Optional[float] = None       # banda: % hacia abajo (None = el mismo que hacia arriba)
    decimales: Optional[int] = Field(default=None, ge=0, le=10)
    cero_es_logro: bool = False
    mostrar_no_aplica: bool = True
    activo: bool = True
    formato: Literal["NUMERO", "PORCENTAJE"] = "NUMERO"   # formato de los valores en el Excel


class tmiTipoEstandarDto(BaseModel):
    """Tabla maestra de tipos de estándar (NIVEL, NIVEL_TIPO, TIPO, CATEGORIA...)."""
    codigo: str = Field(min_length=1, max_length=30, pattern=r"^[A-Z0-9_]+$")
    descripcion: str = Field(min_length=1, max_length=100)
    orden: Optional[int] = None
    activo: bool = True


class tmiEstandarClaveDto(BaseModel):
    """Clave de un tipo de estándar: de qué tabla sale el valor (fuente) y a qué valor del centro corresponde."""
    tipo_estandar: str = Field(min_length=1, max_length=30)
    orden: Optional[int] = None
    fuente: Literal["NIVEL", "TIPO", "CATEGORIA"]
    clave: str = Field(min_length=1, max_length=50)
    descripcion: Optional[str] = Field(default=None, max_length=100)
    prioridad: int = Field(default=1, ge=1, le=99)
    activo: bool = True


class tmiValorEstandarDto(BaseModel):
    """Estándar de un indicador para una clave y año (se guarda en tmi_estandar_nivel / _tipo / _categoria)."""
    anio: int = Field(ge=2000, le=2100)
    fuente: Literal["NIVEL", "TIPO", "CATEGORIA"]
    clave: str = Field(min_length=1, max_length=50)
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


class tmiToleranciaDto(BaseModel):
    """Porcentaje con que se calcula el % Acept de un indicador: estándar ± tolerancia (REL = % del estándar,
    ABS = puntos). En banda, tolerancia = hacia arriba y tolerancia_menos = hacia abajo."""
    tipo_tolerancia: Literal["REL", "ABS"] = "REL"
    tolerancia: float = Field(ge=0, le=100)
    tolerancia_menos: Optional[float] = Field(default=None, ge=0, le=100)
    tolerancia_fijo: Optional[float] = Field(default=None, ge=0, le=100)
    tolerancia_menos_fijo: Optional[float] = Field(default=None, ge=0, le=100)
    anio: Optional[int] = Field(default=None, ge=2000, le=2100)
    mes: Optional[int] = Field(default=None, ge=1, le=12)


class tmiFormulaDto(BaseModel):
    """Fórmula del indicador escrita con letras: (A - B) / C, y la variable de cada letra {"A": id_variable}.
    El backend la expande a términos de TOTALIZADO3 (src/main/core/tmiFormula.py)."""
    formula_alias: str = Field(min_length=1, max_length=500)
    variables: Dict[str, int] = Field(default_factory=dict)

    @field_validator("variables")
    @classmethod
    def _letras(cls, v: Dict[str, int]) -> Dict[str, int]:
        malas = [k for k in v if not re.fullmatch(r"[A-Z]", k)]
        if malas:
            raise ValueError(f"Letras no válidas: {malas} (solo A-Z)")
        if len(set(v.values())) < len(v):
            raise ValueError("Una variable solo puede tener una letra")
        return v


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
    aceptmenos: Optional[float] = None   # % Aceptmenos (solo banda)
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
