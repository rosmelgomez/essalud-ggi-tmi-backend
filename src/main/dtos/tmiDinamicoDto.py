"""DTOs del TMI dinámico (tablas de src/resources/sql/tmi)."""

import re
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class tmiVariableDto(BaseModel):
    """El cálculo es de la variable (como en Generar_pivot.sql): todos sus conjuntos se combinan con OR y se
    calcula SUMA o MEDIANA por servicio en el mes; total_anual dice cómo se acumula enero..mes: SUMA_MESES (suma de
    los meses) o MEDIANA_PERIODO (mediana de todas las filas del periodo, como el Total de CONSO1..CONSO14.sql;
    SUMA + MEDIANA_PERIODO es CONSO11). Una variable MEDIANA siempre acumula con MEDIANA_PERIODO."""
    nombre: str = Field(min_length=1, max_length=200)
    descripcion: Optional[str] = Field(default=None, max_length=200)
    agregacion: Literal["SUMA", "MEDIANA"] = "SUMA"
    total_anual: Literal["SUMA_MESES", "MEDIANA_PERIODO"] = "SUMA_MESES"
    activo: bool = True

    @model_validator(mode="after")
    def _mediana_del_periodo(self):
        if self.agregacion == "MEDIANA":
            self.total_anual = "MEDIANA_PERIODO"
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
    tipo_acept: Literal["REL", "ABS"] = "REL"   # % Acept: REL = % del estándar | ABS = puntos
    acept: float = 0.1
    aceptmenos: Optional[float] = None       # banda: % hacia abajo (None = el mismo que hacia arriba)
    decimales: Optional[int] = Field(default=None, ge=0, le=10)
    cero_es_logro: bool = False
    mostrar_no_aplica: bool = True
    activo: bool = True
    formato: Literal["NUMERO", "PORCENTAJE"] = "NUMERO"   # formato de los valores en el Excel
    # regla de nulos de la fórmula: letra sin dato (CERO = vale 0, NA = el mes queda NA) y división entre 0 (NA o 0).
    # CERO + CERO = ISNULL(ISNULL(A,0) / NULLIF(ISNULL(B,0),0), 0) de 00_TMI_CREACION_VISTAS_2025.sql
    si_variable_nula: Literal["CERO", "NA"] = "CERO"
    si_division_cero: Literal["NA", "CERO"] = "NA"


class tmiEstandarPeriodoValorDto(BaseModel):
    """Estándar de una clave (nivel, tipo o categoría) de la base del indicador:
    fijo = el del año (lo toman los meses al cerrar); mes = el del periodo, solo si el mes ya cerró."""
    fuente: Literal["NIVEL", "TIPO", "CATEGORIA"]
    clave: str = Field(min_length=1, max_length=50)
    fijo: Optional[float] = Field(default=None, ge=0)
    mes: Optional[float] = Field(default=None, ge=0)


class tmiEstandarPeriodoDto(BaseModel):
    """Estándares de un indicador para un periodo: un valor por clave de su base_estandar."""
    anio: int = Field(ge=2000, le=2100)
    mes: int = Field(ge=1, le=12)
    valores: List[tmiEstandarPeriodoValorDto] = Field(min_length=1)


class tmiToleranciaDto(BaseModel):
    """Porcentaje con que se calcula el % Acept de un indicador: estándar ± tolerancia (REL = % del estándar,
    ABS = puntos). En banda, acept = hacia arriba y aceptmenos = hacia abajo."""
    tipo_acept: Literal["REL", "ABS"] = "REL"
    acept: float = Field(ge=0, le=100)
    aceptmenos: Optional[float] = Field(default=None, ge=0, le=100)
    acept_fijo: Optional[float] = Field(default=None, ge=0, le=100)
    aceptmenos_fijo: Optional[float] = Field(default=None, ge=0, le=100)
    anio: Optional[int] = Field(default=None, ge=2000, le=2100)
    mes: Optional[int] = Field(default=None, ge=1, le=12)


class tmiFormulaDto(BaseModel):
    """Fórmula del indicador escrita con letras: (A - B) / C, y la variable de cada letra {"A": id_variable}.
    El backend la expande a términos de TOTALIZADO3 (src/main/core/tmiFormula.py)."""
    formula_alias: str = Field(min_length=1, max_length=500)
    variables: Dict[str, int] = Field(default_factory=dict)
    # solo para la vista previa (POST /formula/analizar): al guardar se usa la regla de nulos del indicador
    si_variable_nula: Literal["CERO", "NA"] = "CERO"
    si_division_cero: Literal["NA", "CERO"] = "NA"

    @field_validator("variables")
    @classmethod
    def _letras(cls, v: Dict[str, int]) -> Dict[str, int]:
        malas = [k for k in v if not re.fullmatch(r"[A-Z]", k)]
        if malas:
            raise ValueError(f"Letras no válidas: {malas} (solo A-Z)")
        if len(set(v.values())) < len(v):
            raise ValueError("Una variable solo puede tener una letra")
        return v


class tmiCentroEstandarDto(BaseModel):
    codcentro: str = Field(min_length=1, max_length=50)
    id_indicador: int
    anio: int
    aplica: bool = True
    est_fijo: Optional[float] = None      # el que toma cada mes en su fecha de cierre
    # alta: periodo en pantalla (1-12). Si el centro ya tiene registro del indicador en el año, solo cambia ese periodo
    mes: Optional[int] = Field(default=None, ge=1, le=12)
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
    sustento: Optional[str] = Field(default=None, max_length=300)
