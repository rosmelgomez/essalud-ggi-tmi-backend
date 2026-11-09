"""Endpoints de indicadores del TMI dinámico: mantenimiento, fórmula con letras, ámbito y consulta directa."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user, nombre_usuario
from src.main.db.databaseConexion import get_db
from src.main.dtos.tmiDinamicoDto import (
    tmiFormulaDto,
    tmiIndicadorAmbitoDto,
    tmiIndicadorDto,
    tmiIndicadorVariableDto,
)
from src.main.repositories import indicadorRep, tmiBaseRep

router = APIRouter(
    prefix="/tmi/dinamico",
    tags=["TMI Indicadores"],
    dependencies=[Depends(get_current_user)],
)


# indicadores
# el % Acept (tolerancia) solo se cambia con PUT /indicadores/{id}/tolerancia (pestaña % Acept)
_SIN_TOLERANCIA = {"tipo_tolerancia", "tolerancia", "tolerancia_menos"}


@router.get("/indicadores")
async def listaIndicadores(db: Session = Depends(get_db)):
    return indicadorRep.queryIndicadoresTMI(db)


@router.post("/indicadores")
async def crearIndicador(dto: tmiIndicadorDto, db: Session = Depends(get_db),
                         current_user: dict = Depends(get_current_user)):
    return tmiBaseRep.queryInsertarFila(db, "tmi_indicador", dto.model_dump(), nombre_usuario(current_user))


@router.put("/indicadores/{id}")
async def actualizarIndicador(id: int, dto: tmiIndicadorDto, db: Session = Depends(get_db),
                              current_user: dict = Depends(get_current_user)):
    respuesta = tmiBaseRep.queryActualizarFila(db, "tmi_indicador", id, dto.model_dump(exclude=_SIN_TOLERANCIA),
                                               nombre_usuario(current_user))
    # la regla de nulos (si_variable_nula / si_division_cero) va dentro de formula_sql: se regenera con la regla nueva
    respuesta["formula_sql"] = indicadorRep.queryRegenerarFormulaSqlTMI(db, id)
    return respuesta


@router.put("/indicadores/{id}/formula")
async def guardarFormulaIndicador(id: int, dto: tmiFormulaDto, db: Session = Depends(get_db),
                                  current_user: dict = Depends(get_current_user)):
    """Guarda la fórmula con letras ((A - B) / C), la variable de cada letra y la fórmula interna que genera."""
    return indicadorRep.queryGuardarFormulaTMI(db, id, dto.formula_alias, dto.variables, nombre_usuario(current_user))


@router.post("/formula/analizar")
async def analizarFormula(dto: tmiFormulaDto, db: Session = Depends(get_db)):
    """Valida la fórmula con letras y devuelve la fórmula interna y sus términos con la descripción de la DIM."""
    return indicadorRep.queryAnalizarFormulaTMI(db, dto.formula_alias, dto.variables,
                                                {"si_variable_nula": dto.si_variable_nula,
                                                 "si_division_cero": dto.si_division_cero})


@router.get("/indicadores/{id}/consulta/{periodo}")
async def consultaIndicador(id: int, periodo: int, con_estandares: bool = False, db: Session = Depends(get_db)):
    """Query que calcula el indicador directo de TOTALIZADO3 para el periodo (AAAAMM). con_estandares=true agrega el
    estándar del mes de corte (con el específico de cada centro) y las exclusiones; sin él, solo la fórmula."""
    return indicadorRep.queryConsultaIndicadorTMI(db, id, periodo, con_estandares)


@router.get("/indicadores/{id}/resultado-directo/{periodo}")
async def resultadoDirectoIndicador(id: int, periodo: int, db: Session = Depends(get_db)):
    """Ejecuta ese query: valor de la fórmula por centro y mes (sin estándares ni exclusiones)."""
    return indicadorRep.queryResultadoDirectoTMI(db, id, periodo)


@router.delete("/indicadores/{id}")
async def eliminarIndicador(id: int, db: Session = Depends(get_db)):
    return indicadorRep.queryEliminarIndicador(db, id)


@router.get("/indicadores/{id}/letras")
async def listaLetras(id: int, db: Session = Depends(get_db)):
    return indicadorRep.queryIndicadorLetrasTMI(db, id)


@router.post("/letras")
async def crearLetra(dto: tmiIndicadorVariableDto, db: Session = Depends(get_db)):
    return tmiBaseRep.queryInsertarFila(db, "tmi_indicador_variable", dto.model_dump())


@router.delete("/letras/{id}")
async def eliminarLetra(id: int, db: Session = Depends(get_db)):
    return tmiBaseRep.queryEliminarFila(db, "tmi_indicador_variable", id)


@router.get("/indicadores/{id}/ambito")
async def listaAmbito(id: int, db: Session = Depends(get_db)):
    return indicadorRep.queryIndicadorAmbitoTMI(db, id)


@router.post("/ambito")
async def crearAmbito(dto: tmiIndicadorAmbitoDto, db: Session = Depends(get_db)):
    if (dto.red is None and dto.nivel is None and dto.categoria is None
            and dto.tipo is None and dto.codcentro is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Indique al menos nivel, categoría, tipo, red o centro.",
        )
    return tmiBaseRep.queryInsertarFila(db, "tmi_indicador_ambito", dto.model_dump())


@router.delete("/ambito/{id}")
async def eliminarAmbito(id: int, db: Session = Depends(get_db)):
    return tmiBaseRep.queryEliminarFila(db, "tmi_indicador_ambito", id)
