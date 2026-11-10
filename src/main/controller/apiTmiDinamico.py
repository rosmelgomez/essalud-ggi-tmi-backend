"""Endpoints del TMI dinámico: catálogos, ejecución de los scripts, validación, cálculo y Excel desde la
plantilla vacía (src/resources/sql/tmi)."""

import asyncio
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user
from src.main.db.databaseConexion import get_db
from src.main.repositories import tmiDinamicoRep

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/tmi/dinamico",
    tags=["TMI dinámico"],
    dependencies=[Depends(get_current_user)],
)


def _periodo(periodo: str) -> int:
    from src.main.service.excelDinamicoServ import _validar_periodo
    try:
        return _validar_periodo(periodo)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# catálogos
@router.get("/catalogo/grupos")
async def catalogoGrupos(db: Session = Depends(get_db)):
    return tmiDinamicoRep.queryCatalogoGruposTMI(db)


@router.get("/catalogo/grupos-reporte")
async def catalogoGruposReporte(db: Session = Depends(get_db)):
    return tmiDinamicoRep.queryCatalogoGruposReporteTMI(db)


@router.get("/catalogo/actividades")
async def catalogoActividades(db: Session = Depends(get_db)):
    return tmiDinamicoRep.queryCatalogoActividadesTMI(db)


@router.get("/catalogo/grupo-actividad-servicio")
async def catalogoGrupoActividadServicio(db: Session = Depends(get_db)):
    """Relación grupo -> actividad -> servicio para elegir la lógica de las variables en cascada."""
    return tmiDinamicoRep.queryGrupoActividadServicioTMI(db)


@router.get("/catalogo/servicios/{tipgrupo}/{actividad}")
async def catalogoServicios(tipgrupo: int, actividad: int, db: Session = Depends(get_db)):
    return tmiDinamicoRep.queryCatalogoServiciosTMI(db, tipgrupo, actividad)


@router.get("/catalogo/tipos-calculo")
async def catalogoTiposCalculo(db: Session = Depends(get_db)):
    return tmiDinamicoRep.queryCatalogoTiposCalculoTMI(db)


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
    return tmiDinamicoRep.queryValidarConfigTMI(db)


@router.get("/avisos-config/{periodo}")
def avisosConfigTMI(periodo: str, db: Session = Depends(get_db)):
    """Avisos de configuración incompleta para el periodo (no bloquean el cálculo): por indicador, centros sin
    estándar o sin % Acept que quedarían NA."""
    return tmiDinamicoRep.queryAvisosConfigTMI(db, _periodo(periodo))


@router.get("/historial")
def historialConfigTMI(id_indicador: Optional[int] = None, tabla: Optional[str] = None, limite: int = 200,
                       db: Session = Depends(get_db)):
    """Últimos cambios de la configuración (quién, cuándo, qué campo y su valor antes y después). Filtros opcionales:
    un indicador (id_indicador) o una tabla."""
    from src.main.repositories import historialRep
    return historialRep.queryHistorialTMI(db, id_indicador, tabla, limite)


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
    """Periodo que se puede calcular, último periodo con datos en TOTALIZADO3 (periodo_datos: si el mes anterior
    todavía no se cargó, la pantalla muestra y calcula hasta este) y periodos con resultado guardado (para el Excel)."""
    from src.main.core.tmiConfig import TMI_CALCULO_SOLO_PERIODO_ANTERIOR
    calculable = periodo_calculable()
    return {"periodo_calculo": calculable,
            "periodo_datos": tmiDinamicoRep.queryUltimoPeriodoDatosTMI(db, int(calculable)),
            "solo_periodo_anterior": TMI_CALCULO_SOLO_PERIODO_ANTERIOR,
            "periodos": tmiDinamicoRep.queryPeriodosResultadoTMI(db),
            # copias de TOTALIZADO3 guardadas al cierre: con ellas se calcula el periodo "como fue"
            "backups": tmiDinamicoRep.queryBackupsTMI(db)}


@router.post("/calcular/{periodo}")
def calcularTMI(periodo: str, origen: str = "ACTUAL", db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    """origen: ACTUAL = TOTALIZADO3 de hoy; BACKUP = la copia del cierre del periodo (como fue)."""
    # def (no async): FastAPI lo corre en un hilo aparte; el cálculo es largo y no debe bloquear el resto de la API
    p = _periodo(periodo)
    if not se_puede_calcular(periodo):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No se puede calcular {periodo}: el último periodo que se puede calcular es "
                                   f"{periodo_calculable()}.")
    errores = tmiDinamicoRep.queryValidarConfigTMI(db)
    if errores:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errores)
    origen = (origen or "ACTUAL").upper()
    usuario = (current_user or {}).get("username")
    logger.info("Usuario '%s' calculando %s con datos %s", usuario, periodo, origen)
    return {"periodo": periodo, "origen": origen,
            "puntajes": tmiDinamicoRep.queryCalcularTMI(db, p, origen, usuario)}


# ---------- copias de TOTALIZADO3 (TOTALIZADO3_BACKUP) y justificación del cálculo ----------
@router.get("/backup")
def backupsTMI(db: Session = Depends(get_db)):
    """Copias de TOTALIZADO3 guardadas por periodo."""
    return tmiDinamicoRep.queryBackupsTMI(db)


@router.post("/backup/{periodo}")
def backupTMI(periodo: str, reemplazar: bool = False, db: Session = Depends(get_db),
              current_user: dict = Depends(get_current_user)):
    """Copia TOTALIZADO3 (enero..periodo) como copia del periodo. Si ya existe no se toca, salvo reemplazar=true.
    TOTALIZADO3 solo se lee."""
    p = _periodo(periodo)
    if not se_puede_calcular(periodo):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El periodo {periodo} todavía no se puede copiar.")
    usuario = (current_user or {}).get("username")
    logger.info("Usuario '%s' copiando TOTALIZADO3 del periodo %s (reemplazar=%s)", usuario, periodo, reemplazar)
    return tmiDinamicoRep.queryBackupTotalizado3TMI(db, p, usuario, reemplazar)


@router.get("/justificacion/{periodo}/{id_indicador}")
def justificacionTMI(periodo: str, id_indicador: int, db: Session = Depends(get_db)):
    """Resultado de cada centro como fue (copia del cierre) y con los datos actuales, con la fórmula desarrollada."""
    return tmiDinamicoRep.queryJustificacionTMI(db, _periodo(periodo), id_indicador)


@router.get("/justificacion/{periodo}/{id_indicador}/{codcentro}/terminos")
def terminosJustificacionTMI(periodo: str, id_indicador: int, codcentro: int, db: Session = Depends(get_db)):
    """Valor de cada término (grupo, actividad, servicio) en cada cálculo guardado."""
    return tmiDinamicoRep.queryTerminosResultadoTMI(db, _periodo(periodo), id_indicador, codcentro)


@router.get("/justificacion/{periodo}/{id_indicador}/{codcentro}/filas")
def filasJustificacionTMI(periodo: str, id_indicador: int, codcentro: int, codigo: Optional[str] = None,
                          db: Session = Depends(get_db)):
    """Filas de TOTALIZADO3 que cambiaron desde la copia del cierre (cantidad antes y ahora, quién y cuándo)."""
    if codigo is not None and not (codigo.startswith("T") and codigo[1:].isdigit()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Término inválido")
    return tmiDinamicoRep.queryFilasCambiadasTMI(db, _periodo(periodo), id_indicador, codcentro, codigo)


@router.get("/resultado/{periodo}/{id_indicador}")
def resultadoIndicador(periodo: str, id_indicador: int, origen: Optional[str] = None, db: Session = Depends(get_db)):
    """origen: ACTUAL = calculado con TOTALIZADO3; BACKUP = con la copia del cierre (TOTALIZADO3_BACKUP); sin él, el oficial."""
    return tmiDinamicoRep.queryResultadoIndicadorTMI(db, _periodo(periodo), id_indicador, origen)


@router.get("/dashboard/periodos")
def periodosDashboardTMI(db: Session = Depends(get_db)):
    """Periodos con resultado guardado para el dashboard (pública, como /dashboard/{periodo})."""
    return tmiDinamicoRep.queryPeriodosResultadoTMI(db)


@router.get("/dashboard/{periodo}")
def dashboardTMI(periodo: str, db: Session = Depends(get_db)):
    """Datos del dashboard: resultado final guardado del periodo, con los puntajes calculados como en el Excel."""
    from src.main.service.dashboardServ import dashboard_tmi
    try:
        return dashboard_tmi(db, periodo)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/dashboard/{periodo}/excel")
def excelDashboardTMI(periodo: str, db: Session = Depends(get_db)):
    """Excel del periodo para los dashboards (pública, como /dashboard/{periodo}): el mismo de Administración, armado
    con el resultado guardado y con todos los indicadores. Nunca recalcula."""
    return _excel(db, periodo, calcular=False, indicadores=None)


@router.get("/generar-excel/{periodo}")
def generarExcelTMIDinamico(periodo: str, calcular: bool = True, indicadores: Optional[str] = None,
                            origen: Optional[str] = None, db: Session = Depends(get_db)):
    """Excel del periodo. indicadores = ids separados por coma (1,4,7) para generar solo esas hojas; sin él, todos.
    origen: ACTUAL (TOTALIZADO3) o BACKUP (copia del cierre); sin él, el oficial."""
    return _excel(db, periodo, calcular, indicadores, origen)


def _excel(db: Session, periodo: str, calcular: bool, indicadores: Optional[str], origen: Optional[str] = None):
    try:
        ids = [int(x) for x in indicadores.split(",") if x.strip()] if indicadores else None
        from src.main.service.excelServ import MESES_NOMBRE
        from src.main.service.excelDinamicoServ import generar_excel_tmi_dinamico
        # los periodos cerrados no se recalculan: el Excel sale del resultado guardado
        if origen is not None and origen.upper() not in ("ACTUAL", "BACKUP"):
            raise ValueError("El origen de los datos debe ser ACTUAL o BACKUP.")
        buffer = generar_excel_tmi_dinamico(db, periodo, calcular=calcular and se_puede_calcular(periodo), ids=ids,
                                            origen=origen.upper() if origen else None)
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
