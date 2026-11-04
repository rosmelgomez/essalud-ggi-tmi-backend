"""Endpoints de estándares del TMI: tmi_estandar, estándares por tipo, nivel y categoría, tablas maestras,
estándares por indicador y % Acept."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user, nombre_usuario
from src.main.db.databaseConexion import get_db
from src.main.dtos.tmiDinamicoDto import (
    tmiEstandarClaveDto,
    tmiEstandarPeriodoDto,
    tmiIndicadorEstandarDto,
    tmiTipoEstandarDto,
    tmiToleranciaDto,
    tmiValorEstandarDto,
)
from src.main.dtos.tmiDto import (
    tmiEstandarCategoriaDto,
    tmiEstandarDto,
    tmiEstandarNivelDto,
    tmiEstandarTipoDto,
)
from src.main.repositories import estandarRep, tmiBaseRep

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/tmi",
    tags=["TMI Estándares"],
    dependencies=[Depends(get_current_user)],
)

routerDinamico = APIRouter(
    prefix="/tmi/dinamico",
    tags=["TMI Estándares"],
    dependencies=[Depends(get_current_user)],
)


# Endpoints tmi_estandar
@router.get("/lista-estandar")
async def queryEstandar(
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.estandarServ import queryEstandarServ
        return queryEstandarServ(db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar estandar: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de estándares.",
        )


@router.post("/create-estandar")
async def queryCreateEstandar(
    dto: tmiEstandarDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' agregando estándar: %s - %s", current_user.get("username"), dto.tipo, dto.indicador)
        from src.main.service.estandarServ import queryInsertEstandarServ
        return queryInsertEstandarServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al agregar el estándar: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al agregar el estándar.",
        )


@router.put("/update-estandar")
async def queryUpdateEstandar(
    dto: tmiEstandarDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' actualizando estándar ID %s", current_user.get("username"), dto.id)
        from src.main.service.estandarServ import queryUpdateEstandarServ
        return queryUpdateEstandarServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al actualizar estandar: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al actualizar el estándar.",
        )


@router.delete("/delete-estandar/{id}")
async def queryDeleteEstandar(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' eliminando fila %s de tmi_estandar", current_user.get("username"), id)
        from src.main.service.estandarServ import queryDeleteEstandarServ
        return queryDeleteEstandarServ(db, id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al eliminar el estándar: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al eliminar el estándar.",
        )


# Endpoints tmi_estandar_tipo
@router.get("/lista-estandar-tipo/{anio}")
async def queryEstandarTipo(
    anio: int,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.estandarServ import queryEstandarTipoServ
        return queryEstandarTipoServ(db, anio)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar estandar tipo: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de estándares por tipo.",
        )


@router.put("/update-estandar-tipo")
async def queryUpdateEstandarTipo(
    dto: tmiEstandarTipoDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        from src.main.service.estandarServ import queryUpdateEstandarTipoServ
        return queryUpdateEstandarTipoServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al actualizar estandar tipo: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al actualizar el estándar tipo.",
        )


@router.post("/create-estandar-tipo")
async def queryCreateEstandarTipo(
    dto: tmiEstandarTipoDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' agregando fila en año %s", current_user.get("username"), dto.anio)
        from src.main.service.estandarServ import queryInsertEstandarTipoServ
        return queryInsertEstandarTipoServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al agregar el estándar tipo: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al agregar el estándar tipo.",
        )


@router.delete("/delete-estandar-tipo/{id}")
async def queryDeleteEstandarTipo(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' eliminando fila %s de tmi_estandar_tipo", current_user.get("username"), id)
        from src.main.service.estandarServ import queryDeleteEstandarTipoServ
        return queryDeleteEstandarTipoServ(db, id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al eliminar el estándar tipo: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al eliminar el estándar tipo.",
        )


# Endpoints tmi_estandar_nivel
@router.get("/lista-estandar-nivel/{anio}")
async def queryEstandarNivel(
    anio: int,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.estandarServ import queryEstandarNivelServ
        return queryEstandarNivelServ(db, anio)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar estandar nivel: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de estándares por nivel.",
        )


@router.put("/update-estandar-nivel")
async def queryUpdateEstandarNivel(
    dto: tmiEstandarNivelDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        from src.main.service.estandarServ import queryUpdateEstandarNivelServ
        return queryUpdateEstandarNivelServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al actualizar estandar nivel: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al actualizar el estándar nivel.",
        )


@router.post("/create-estandar-nivel")
async def queryCreateEstandarNivel(
    dto: tmiEstandarNivelDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' agregando fila en año %s", current_user.get("username"), dto.anio)
        from src.main.service.estandarServ import queryInsertEstandarNivelServ
        return queryInsertEstandarNivelServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al agregar el estándar nivel: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al agregar el estándar nivel.",
        )


@router.delete("/delete-estandar-nivel/{id}")
async def queryDeleteEstandarNivel(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' eliminando fila %s de tmi_estandar_nivel", current_user.get("username"), id)
        from src.main.service.estandarServ import queryDeleteEstandarNivelServ
        return queryDeleteEstandarNivelServ(db, id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al eliminar el estándar nivel: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al eliminar el estándar nivel.",
        )


# Endpoints tmi_estandar_categoria
@router.get("/lista-estandar-categoria/{anio}")
async def queryEstandarCategoria(
    anio: int,
    db: Session = Depends(get_db),
):
    try:
        from src.main.service.estandarServ import queryEstandarCategoriaServ
        return queryEstandarCategoriaServ(db, anio)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al consultar estandar categoria: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al consultar la lista de estándares por categoría.",
        )


@router.put("/update-estandar-categoria")
async def queryUpdateEstandarCategoria(
    dto: tmiEstandarCategoriaDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        from src.main.service.estandarServ import queryUpdateEstandarCategoriaServ
        return queryUpdateEstandarCategoriaServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al actualizar estandar categoria: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al actualizar el estándar categoría.",
        )


@router.post("/create-estandar-categoria")
async def queryCreateEstandarCategoria(
    dto: tmiEstandarCategoriaDto,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' agregando fila en año %s", current_user.get("username"), dto.anio)
        from src.main.service.estandarServ import queryInsertEstandarCategoriaServ
        return queryInsertEstandarCategoriaServ(db, dto)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al agregar el estándar categoría: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al agregar el estándar categoría.",
        )


@router.delete("/delete-estandar-categoria/{id}")
async def queryDeleteEstandarCategoria(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info("Usuario '%s' eliminando fila %s de tmi_estandar_categoria", current_user.get("username"), id)
        from src.main.service.estandarServ import queryDeleteEstandarCategoriaServ
        return queryDeleteEstandarCategoriaServ(db, id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error al eliminar el estándar categoría: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al eliminar el estándar categoría.",
        )


# estándares del indicador (unión por nivel, categoría y/o tipo y por periodo)
@routerDinamico.get("/indicadores/{id}/estandares")
async def listaIndicadorEstandares(id: int, db: Session = Depends(get_db)):
    return estandarRep.queryIndicadorEstandaresTMI(db, id)


@routerDinamico.post("/indicador-estandar")
async def crearIndicadorEstandar(dto: tmiIndicadorEstandarDto, db: Session = Depends(get_db)):
    if dto.nivel is None and dto.categoria is None and dto.tipo is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seleccione al menos Nivel, Categoría o Tipo (o combinación de ellos).",
        )
    return tmiBaseRep.queryInsertarFila(db, "tmi_indicador_estandar", dto.model_dump())


@routerDinamico.put("/indicador-estandar/{id}")
async def actualizarIndicadorEstandar(id: int, dto: tmiIndicadorEstandarDto, db: Session = Depends(get_db)):
    if dto.nivel is None and dto.categoria is None and dto.tipo is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seleccione al menos Nivel, Categoría o Tipo (o combinación de ellos).",
        )
    return tmiBaseRep.queryActualizarFila(db, "tmi_indicador_estandar", id, dto.model_dump())


@routerDinamico.delete("/indicador-estandar/{id}")
async def eliminarIndicadorEstandar(id: int, db: Session = Depends(get_db)):
    return tmiBaseRep.queryEliminarFila(db, "tmi_indicador_estandar", id)


# estándares específicos de centro
# tablas maestras de estándares: tipos (NIVEL, NIVEL_TIPO, TIPO, CATEGORIA...) y sus claves
@routerDinamico.get("/tipos-estandar")
async def listaTiposEstandar(db: Session = Depends(get_db)):
    return estandarRep.queryTiposEstandarTMI(db)


@routerDinamico.post("/tipos-estandar")
async def crearTipoEstandar(dto: tmiTipoEstandarDto, db: Session = Depends(get_db)):
    return tmiBaseRep.queryInsertarFila(db, "tmi_tipo_estandar", dto.model_dump())


@routerDinamico.put("/tipos-estandar/{id}")
async def actualizarTipoEstandar(id: int, dto: tmiTipoEstandarDto, db: Session = Depends(get_db)):
    return tmiBaseRep.queryActualizarFila(db, "tmi_tipo_estandar", id, dto.model_dump())


@routerDinamico.delete("/tipos-estandar/{id}")
async def eliminarTipoEstandar(id: int, db: Session = Depends(get_db)):
    return tmiBaseRep.queryEliminarFila(db, "tmi_tipo_estandar", id)


@routerDinamico.get("/estandar-claves")
async def listaEstandarClaves(db: Session = Depends(get_db)):
    return estandarRep.queryEstandarClavesTMI(db)


@routerDinamico.post("/estandar-claves")
async def crearEstandarClave(dto: tmiEstandarClaveDto, db: Session = Depends(get_db)):
    return tmiBaseRep.queryInsertarFila(db, "tmi_estandar", dto.model_dump())


@routerDinamico.put("/estandar-claves/{id}")
async def actualizarEstandarClave(id: int, dto: tmiEstandarClaveDto, db: Session = Depends(get_db)):
    return tmiBaseRep.queryActualizarFila(db, "tmi_estandar", id, dto.model_dump())


@routerDinamico.delete("/estandar-claves/{id}")
async def eliminarEstandarClave(id: int, db: Session = Depends(get_db)):
    return tmiBaseRep.queryEliminarFila(db, "tmi_estandar", id)


@routerDinamico.get("/indicadores/{id}/valores-estandar/{anio}")
async def valoresEstandarIndicador(id: int, anio: int, db: Session = Depends(get_db)):
    """Claves del tipo de estándar del indicador con su estándar por mes (tablas de nivel, tipo o categoría)."""
    return estandarRep.queryValoresEstandarIndicadorTMI(db, id, anio)


@routerDinamico.put("/indicadores/{id}/valores-estandar")
async def guardarValorEstandarIndicador(id: int, dto: tmiValorEstandarDto, db: Session = Depends(get_db)):
    return estandarRep.queryGuardarValorEstandarTMI(db, id, dto.model_dump())


@routerDinamico.get("/estandares-periodo/{anio}/{mes}")
async def estandaresPeriodoTMI(anio: int, mes: int, db: Session = Depends(get_db)):
    """Estándar de cada indicador activo solo en las claves de su base_estandar: fijo del año y valor del mes."""
    if not 1 <= mes <= 12:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El mes debe estar entre 1 y 12.")
    return estandarRep.queryEstandaresPeriodoTMI(db, anio, mes)


@routerDinamico.put("/indicadores/{id}/estandar-periodo")
async def guardarEstandarPeriodo(id: int, dto: tmiEstandarPeriodoDto, db: Session = Depends(get_db)):
    return estandarRep.queryGuardarEstandarPeriodoTMI(db, id, dto.model_dump())


@routerDinamico.get("/aceptacion/{anio}/{mes}")
async def aceptacionTMI(anio: int, mes: int, db: Session = Depends(get_db)):
    """% Acept de los indicadores activos: porcentaje y estándar del mes por clave (el % Acept se calcula)."""
    if not 1 <= mes <= 12:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El mes debe estar entre 1 y 12.")
    return estandarRep.queryAceptacionTMI(db, anio, mes)


@routerDinamico.put("/indicadores/{id}/tolerancia")
async def guardarToleranciaIndicador(id: int, dto: tmiToleranciaDto, db: Session = Depends(get_db),
                                     current_user: dict = Depends(get_current_user)):
    return estandarRep.queryGuardarToleranciaTMI(db, id, dto.model_dump(), nombre_usuario(current_user))
