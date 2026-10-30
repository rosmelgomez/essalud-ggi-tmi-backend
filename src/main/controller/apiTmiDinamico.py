"""Endpoints del TMI dinámico: mantenimiento de variables, indicadores y estándares por centro,
cálculo y Excel desde la plantilla vacía (src/resources/sql/tmi)."""

import asyncio
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from src.main.core.security import get_current_user
from src.main.db.databaseConexion import get_db
from src.main.dtos.tmiDinamicoDto import (
    tmiCentroEstandarDto,
    tmiEstandarClaveDto,
    tmiFormulaDto,
    tmiIndicadorAmbitoDto,
    tmiIndicadorDto,
    tmiIndicadorEstandarDto,
    tmiIndicadorVariableDto,
    tmiTipoEstandarDto,
    tmiVariableComponenteDto,
    tmiToleranciaDto,
    tmiValorEstandarDto,
    tmiVariableDto,
    tmiVariableLogicaDto,
)
from src.main.repositories import tmiDinamicoRep as rep

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/tmi/dinamico",
    tags=["TMI dinámico"],
    dependencies=[Depends(get_current_user)],
)


def _usuario(current_user: dict) -> str:
    return (current_user or {}).get("username")


def _periodo(periodo: str) -> int:
    from src.main.service.excelDinamicoServ import _validar_periodo
    try:
        return _validar_periodo(periodo)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# catálogos
@router.get("/catalogo/grupos")
async def catalogoGrupos(db: Session = Depends(get_db)):
    return rep.queryCatalogoGruposTMI(db)


@router.get("/catalogo/grupos-reporte")
async def catalogoGruposReporte(db: Session = Depends(get_db)):
    return rep.queryCatalogoGruposReporteTMI(db)


@router.get("/catalogo/actividades")
async def catalogoActividades(db: Session = Depends(get_db)):
    return rep.queryCatalogoActividadesTMI(db)


@router.get("/catalogo/grupo-actividad-servicio")
async def catalogoGrupoActividadServicio(db: Session = Depends(get_db)):
    """Relación grupo -> actividad -> servicio para elegir la lógica de las variables en cascada."""
    return rep.queryGrupoActividadServicioTMI(db)


@router.get("/catalogo/servicios/{tipgrupo}/{actividad}")
async def catalogoServicios(tipgrupo: int, actividad: int, db: Session = Depends(get_db)):
    return rep.queryCatalogoServiciosTMI(db, tipgrupo, actividad)


@router.get("/catalogo/tipos-calculo")
async def catalogoTiposCalculo(db: Session = Depends(get_db)):
    return rep.queryCatalogoTiposCalculoTMI(db)


@router.get("/catalogo/centros")
async def catalogoCentros(db: Session = Depends(get_db)):
    return rep.queryCatalogoCentrosTMI(db)


# variables
@router.get("/variables")
async def listaVariables(db: Session = Depends(get_db)):
    return rep.queryVariablesTMI(db)


@router.post("/variables")
async def crearVariable(dto: tmiVariableDto, db: Session = Depends(get_db),
                        current_user: dict = Depends(get_current_user)):
    return rep.queryInsertarFila(db, "tmi_variable", dto.model_dump(), _usuario(current_user))


@router.put("/variables/{id}")
async def actualizarVariable(id: int, dto: tmiVariableDto, db: Session = Depends(get_db),
                             current_user: dict = Depends(get_current_user)):
    r = rep.queryActualizarVariableTMI(db, id, dto.model_dump(), _usuario(current_user))
    rep.regenerarFormulasVariable(db, id)
    return r


@router.delete("/variables/{id}")
async def eliminarVariable(id: int, db: Session = Depends(get_db)):
    return rep.queryEliminarVariable(db, id)


@router.get("/variables/{id}/componentes")
async def listaComponentes(id: int, db: Session = Depends(get_db)):
    """Variables que suma una variable compuesta."""
    return rep.queryVariableComponentesTMI(db, id)


@router.post("/componentes")
async def crearComponente(dto: tmiVariableComponenteDto, db: Session = Depends(get_db)):
    r = rep.queryInsertarComponenteTMI(db, dto.model_dump())
    rep.regenerarFormulasVariable(db, dto.id_variable)
    return r


@router.delete("/componentes/{id}")
async def eliminarComponente(id: int, db: Session = Depends(get_db)):
    id_var = rep.queryVariableDeFila(db, "tmi_variable_componente", id)
    r = rep.queryEliminarFila(db, "tmi_variable_componente", id)
    if id_var:
        rep.regenerarFormulasVariable(db, id_var)
    return r


@router.get("/variables/{id}/logica")
async def listaLogica(id: int, db: Session = Depends(get_db)):
    return rep.queryVariableLogicaTMI(db, id)


@router.post("/logica")
async def crearLogica(dto: tmiVariableLogicaDto, db: Session = Depends(get_db)):
    r = rep.queryInsertarFila(db, "tmi_variable_logica", dto.model_dump())
    rep.regenerarFormulasVariable(db, dto.id_variable)
    return r


@router.put("/logica/{id}")
async def actualizarLogica(id: int, dto: tmiVariableLogicaDto, db: Session = Depends(get_db)):
    r = rep.queryActualizarFila(db, "tmi_variable_logica", id, dto.model_dump())
    rep.regenerarFormulasVariable(db, dto.id_variable)
    return r


@router.delete("/logica/{id}")
async def eliminarLogica(id: int, db: Session = Depends(get_db)):
    id_var = rep.queryVariableDeFila(db, "tmi_variable_logica", id)
    r = rep.queryEliminarFila(db, "tmi_variable_logica", id)
    if id_var:
        rep.regenerarFormulasVariable(db, id_var)
    return r


# indicadores
# el % Acept (tolerancia) solo se cambia con PUT /indicadores/{id}/tolerancia (pestaña % Acept)
_SIN_TOLERANCIA = {"tipo_tolerancia", "tolerancia", "tolerancia_menos"}


@router.get("/indicadores")
async def listaIndicadores(db: Session = Depends(get_db)):
    return rep.queryIndicadoresTMI(db)


@router.post("/indicadores")
async def crearIndicador(dto: tmiIndicadorDto, db: Session = Depends(get_db),
                         current_user: dict = Depends(get_current_user)):
    return rep.queryInsertarFila(db, "tmi_indicador", dto.model_dump(), _usuario(current_user))


@router.put("/indicadores/{id}")
async def actualizarIndicador(id: int, dto: tmiIndicadorDto, db: Session = Depends(get_db),
                              current_user: dict = Depends(get_current_user)):
    return rep.queryActualizarFila(db, "tmi_indicador", id, dto.model_dump(exclude=_SIN_TOLERANCIA),
                                   _usuario(current_user))


@router.put("/indicadores/{id}/formula")
async def guardarFormulaIndicador(id: int, dto: tmiFormulaDto, db: Session = Depends(get_db),
                                  current_user: dict = Depends(get_current_user)):
    """Guarda la fórmula con letras ((A - B) / C), la variable de cada letra y la fórmula interna que genera."""
    return rep.queryGuardarFormulaTMI(db, id, dto.formula_alias, dto.variables, _usuario(current_user))


@router.post("/formula/analizar")
async def analizarFormula(dto: tmiFormulaDto, db: Session = Depends(get_db)):
    """Valida la fórmula con letras y devuelve la fórmula interna y sus términos con la descripción de la DIM."""
    return rep.queryAnalizarFormulaTMI(db, dto.formula_alias, dto.variables)


@router.get("/indicadores/{id}/consulta/{periodo}")
async def consultaIndicador(id: int, periodo: int, db: Session = Depends(get_db)):
    """Query que calcula el indicador directo de TOTALIZADO3 para el periodo (AAAAMM)."""
    return rep.queryConsultaIndicadorTMI(db, id, periodo)


@router.get("/indicadores/{id}/resultado-directo/{periodo}")
async def resultadoDirectoIndicador(id: int, periodo: int, db: Session = Depends(get_db)):
    """Ejecuta ese query: valor de la fórmula por centro y mes (sin estándares ni exclusiones)."""
    return rep.queryResultadoDirectoTMI(db, id, periodo)


@router.delete("/indicadores/{id}")
async def eliminarIndicador(id: int, db: Session = Depends(get_db)):
    return rep.queryEliminarIndicador(db, id)


@router.get("/indicadores/{id}/letras")
async def listaLetras(id: int, db: Session = Depends(get_db)):
    return rep.queryIndicadorLetrasTMI(db, id)


@router.post("/letras")
async def crearLetra(dto: tmiIndicadorVariableDto, db: Session = Depends(get_db)):
    return rep.queryInsertarFila(db, "tmi_indicador_variable", dto.model_dump())


@router.delete("/letras/{id}")
async def eliminarLetra(id: int, db: Session = Depends(get_db)):
    return rep.queryEliminarFila(db, "tmi_indicador_variable", id)


@router.get("/indicadores/{id}/ambito")
async def listaAmbito(id: int, db: Session = Depends(get_db)):
    return rep.queryIndicadorAmbitoTMI(db, id)


@router.post("/ambito")
async def crearAmbito(dto: tmiIndicadorAmbitoDto, db: Session = Depends(get_db)):
    if (dto.red is None and dto.nivel is None and dto.categoria is None
            and dto.tipo is None and dto.codcentro is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Indique al menos nivel, categoría, tipo, red o centro.",
        )
    return rep.queryInsertarFila(db, "tmi_indicador_ambito", dto.model_dump())


@router.delete("/ambito/{id}")
async def eliminarAmbito(id: int, db: Session = Depends(get_db)):
    return rep.queryEliminarFila(db, "tmi_indicador_ambito", id)


# estándares del indicador (unión por nivel, categoría y/o tipo y por periodo)
@router.get("/indicadores/{id}/estandares")
async def listaIndicadorEstandares(id: int, db: Session = Depends(get_db)):
    return rep.queryIndicadorEstandaresTMI(db, id)


@router.post("/indicador-estandar")
async def crearIndicadorEstandar(dto: tmiIndicadorEstandarDto, db: Session = Depends(get_db)):
    if dto.nivel is None and dto.categoria is None and dto.tipo is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seleccione al menos Nivel, Categoría o Tipo (o combinación de ellos).",
        )
    return rep.queryInsertarFila(db, "tmi_indicador_estandar", dto.model_dump())


@router.put("/indicador-estandar/{id}")
async def actualizarIndicadorEstandar(id: int, dto: tmiIndicadorEstandarDto, db: Session = Depends(get_db)):
    if dto.nivel is None and dto.categoria is None and dto.tipo is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seleccione al menos Nivel, Categoría o Tipo (o combinación de ellos).",
        )
    return rep.queryActualizarFila(db, "tmi_indicador_estandar", id, dto.model_dump())


@router.delete("/indicador-estandar/{id}")
async def eliminarIndicadorEstandar(id: int, db: Session = Depends(get_db)):
    return rep.queryEliminarFila(db, "tmi_indicador_estandar", id)


# estándares específicos de centro
# tablas maestras de estándares: tipos (NIVEL, NIVEL_TIPO, TIPO, CATEGORIA...) y sus claves
@router.get("/tipos-estandar")
async def listaTiposEstandar(db: Session = Depends(get_db)):
    return rep.queryTiposEstandarTMI(db)


@router.post("/tipos-estandar")
async def crearTipoEstandar(dto: tmiTipoEstandarDto, db: Session = Depends(get_db)):
    return rep.queryInsertarFila(db, "tmi_tipo_estandar", dto.model_dump())


@router.put("/tipos-estandar/{id}")
async def actualizarTipoEstandar(id: int, dto: tmiTipoEstandarDto, db: Session = Depends(get_db)):
    return rep.queryActualizarFila(db, "tmi_tipo_estandar", id, dto.model_dump())


@router.delete("/tipos-estandar/{id}")
async def eliminarTipoEstandar(id: int, db: Session = Depends(get_db)):
    return rep.queryEliminarFila(db, "tmi_tipo_estandar", id)


@router.get("/estandar-claves")
async def listaEstandarClaves(db: Session = Depends(get_db)):
    return rep.queryEstandarClavesTMI(db)


@router.post("/estandar-claves")
async def crearEstandarClave(dto: tmiEstandarClaveDto, db: Session = Depends(get_db)):
    return rep.queryInsertarFila(db, "tmi_estandar", dto.model_dump())


@router.put("/estandar-claves/{id}")
async def actualizarEstandarClave(id: int, dto: tmiEstandarClaveDto, db: Session = Depends(get_db)):
    return rep.queryActualizarFila(db, "tmi_estandar", id, dto.model_dump())


@router.delete("/estandar-claves/{id}")
async def eliminarEstandarClave(id: int, db: Session = Depends(get_db)):
    return rep.queryEliminarFila(db, "tmi_estandar", id)


@router.get("/indicadores/{id}/valores-estandar/{anio}")
async def valoresEstandarIndicador(id: int, anio: int, db: Session = Depends(get_db)):
    """Claves del tipo de estándar del indicador con su estándar por mes (tablas de nivel, tipo o categoría)."""
    return rep.queryValoresEstandarIndicadorTMI(db, id, anio)


@router.put("/indicadores/{id}/valores-estandar")
async def guardarValorEstandarIndicador(id: int, dto: tmiValorEstandarDto, db: Session = Depends(get_db)):
    return rep.queryGuardarValorEstandarTMI(db, id, dto.model_dump())


@router.get("/aceptacion/{anio}/{mes}")
async def aceptacionTMI(anio: int, mes: int, db: Session = Depends(get_db)):
    """% Acept de los indicadores activos: porcentaje y estándar del mes por clave (el % Acept se calcula)."""
    if not 1 <= mes <= 12:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El mes debe estar entre 1 y 12.")
    return rep.queryAceptacionTMI(db, anio, mes)


@router.put("/indicadores/{id}/tolerancia")
async def guardarToleranciaIndicador(id: int, dto: tmiToleranciaDto, db: Session = Depends(get_db),
                                     current_user: dict = Depends(get_current_user)):
    return rep.queryGuardarToleranciaTMI(db, id, dto.model_dump(), _usuario(current_user))


@router.get("/centro-estandar/{anio}")
async def listaCentroEstandar(anio: int, db: Session = Depends(get_db)):
    return rep.queryCentroEstandarTMI(db, anio)


@router.post("/centro-estandar")
async def crearCentroEstandar(dto: tmiCentroEstandarDto, db: Session = Depends(get_db)):
    return rep.queryInsertarFila(db, "tmi_centro_estandar", dto.model_dump())


@router.put("/centro-estandar/{id}")
async def actualizarCentroEstandar(id: int, dto: tmiCentroEstandarDto, db: Session = Depends(get_db)):
    return rep.queryActualizarFila(db, "tmi_centro_estandar", id, dto.model_dump())


@router.delete("/centro-estandar/{id}")
async def eliminarCentroEstandar(id: int, db: Session = Depends(get_db)):
    return rep.queryEliminarFila(db, "tmi_centro_estandar", id)


# ejecución, validación, cálculo y Excel
@router.post("/ejecutar-sql")
async def ejecutarSqlTMI():
    """Vuelve a ejecutar los scripts de src/resources/sql/tmi (también corren al iniciar la aplicación)."""
    from src.main.db.sqlRunner import ejecutar_scripts
    resultado = await asyncio.to_thread(ejecutar_scripts)
    if any(estado != "OK" for estado in resultado.values()):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=resultado)
    return resultado


@router.get("/validar-config")
async def validarConfigTMI(db: Session = Depends(get_db)):
    return rep.queryValidarConfigTMI(db)


def periodo_calculable() -> str:
    """Periodo que se puede calcular hoy: el mes anterior (el cierre de M genera M-1)."""
    from datetime import date
    from src.main.service.cierreServ import periodo_a_generar
    return periodo_a_generar(date.today())


def se_puede_calcular(periodo: str) -> bool:
    """Se calcula cualquier periodo hasta el mes anterior (nunca uno futuro). Con TMI_CALCULO_SOLO_PERIODO_ANTERIOR=true,
    solo el mes anterior."""
    from src.main.core.tmiConfig import TMI_CALCULO_SOLO_PERIODO_ANTERIOR
    if TMI_CALCULO_SOLO_PERIODO_ANTERIOR:
        return periodo == periodo_calculable()
    return periodo <= periodo_calculable()


@router.get("/periodo-calculo")
async def periodoCalculoTMI(db: Session = Depends(get_db)):
    """Periodo que se puede calcular y periodos con resultado guardado (para el Excel)."""
    from src.main.core.tmiConfig import TMI_CALCULO_SOLO_PERIODO_ANTERIOR
    return {"periodo_calculo": periodo_calculable(),
            "solo_periodo_anterior": TMI_CALCULO_SOLO_PERIODO_ANTERIOR,
            "periodos": rep.queryPeriodosResultadoTMI(db)}


@router.post("/calcular/{periodo}")
def calcularTMI(periodo: str, db: Session = Depends(get_db)):
    # def (no async): FastAPI lo corre en un hilo aparte; el cálculo es largo y no debe bloquear el resto de la API
    p = _periodo(periodo)
    if not se_puede_calcular(periodo):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No se puede calcular {periodo}: el último periodo que se puede calcular es "
                                   f"{periodo_calculable()}.")
    errores = rep.queryValidarConfigTMI(db)
    if errores:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errores)
    return {"periodo": periodo, "puntajes": rep.queryCalcularTMI(db, p)}


@router.get("/resultado/{periodo}/{id_indicador}")
def resultadoIndicador(periodo: str, id_indicador: int, db: Session = Depends(get_db)):
    return rep.queryResultadoIndicadorTMI(db, _periodo(periodo), id_indicador)


@router.get("/generar-excel/{periodo}")
def generarExcelTMIDinamico(periodo: str, calcular: bool = True, indicadores: Optional[str] = None,
                            db: Session = Depends(get_db)):
    """Excel del periodo. indicadores = ids separados por coma (1,4,7) para generar solo esas hojas; sin él, todos."""
    try:
        ids = [int(x) for x in indicadores.split(",") if x.strip()] if indicadores else None
        from src.main.service.excelServ import MESES_NOMBRE
        from src.main.service.excelDinamicoServ import generar_excel_tmi_dinamico
        # los periodos cerrados no se recalculan: el Excel sale del resultado guardado
        buffer = generar_excel_tmi_dinamico(db, periodo, calcular=calcular and se_puede_calcular(periodo), ids=ids)
        filename = f"TMI_Prelim_Salud_{MESES_NOMBRE[int(periodo[4:]) - 1].capitalize()}_{periodo[:4]}.xlsx"
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Error al generar excel TMI dinámico: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al generar el Excel del TMI.",
        )
