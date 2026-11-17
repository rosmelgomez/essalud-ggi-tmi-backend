"""Endpoints de indicadores del TMI dinámico: mantenimiento, fórmula con letras, ámbito y consulta directa."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user, nombre_usuario
from src.main.db.databaseConexion import get_db
from src.main.dtos.tmiDinamicoDto import tmiFormulaDto, tmiIndicadorDto
from src.main.service import indicadorServ

router = APIRouter(
    prefix="/indicador",
    tags=["TMI Indicadores"],
    dependencies=[Depends(get_current_user)],
)


# indicadores
@router.get("/indicadores")
async def listaIndicadores(db: Session = Depends(get_db)):
    return indicadorServ.listaIndicadoresServ(db)


@router.post("/indicadores")
async def crearIndicador(dto: tmiIndicadorDto, db: Session = Depends(get_db),
                         current_user: dict = Depends(get_current_user)):
    return indicadorServ.crearIndicadorServ(db, dto, nombre_usuario(current_user))


@router.put("/indicadores/{id}")
async def actualizarIndicador(id: int, dto: tmiIndicadorDto, db: Session = Depends(get_db),
                              current_user: dict = Depends(get_current_user)):
    """El % Acept (acept, aceptmenos) no se cambia aquí: solo con PUT /estandar/indicadores/{id}/acept."""
    return indicadorServ.actualizarIndicadorServ(db, id, dto, nombre_usuario(current_user))


@router.put("/indicadores/{id}/formula")
async def guardarFormulaIndicador(id: int, dto: tmiFormulaDto, db: Session = Depends(get_db),
                                  current_user: dict = Depends(get_current_user)):
    """Guarda la fórmula con letras ((A - B) / C), la variable de cada letra y la fórmula interna que genera."""
    return indicadorServ.guardarFormulaServ(db, id, dto, nombre_usuario(current_user))


@router.post("/formula/analizar")
async def analizarFormula(dto: tmiFormulaDto, db: Session = Depends(get_db)):
    """Valida la fórmula con letras y devuelve la fórmula interna y sus términos con la descripción de la DIM."""
    return indicadorServ.analizarFormulaServ(db, dto)


@router.get("/indicadores/{id}/consulta/{periodo}")
async def consultaIndicador(id: int, periodo: int, con_estandares: bool = False, db: Session = Depends(get_db)):
    """Query que calcula el indicador directo de TOTALIZADO3 para el periodo (AAAAMM). con_estandares=true agrega el
    estándar del mes de corte (con el específico de cada centro) y las exclusiones; sin él, solo la fórmula."""
    return indicadorServ.consultaIndicadorServ(db, id, periodo, con_estandares)


@router.delete("/indicadores/{id}")
async def eliminarIndicador(id: int, db: Session = Depends(get_db)):
    return indicadorServ.eliminarIndicadorServ(db, id)


# letras de la fórmula
@router.get("/indicadores/{id}/letras")
async def listaLetras(id: int, db: Session = Depends(get_db)):
    return indicadorServ.listaLetrasServ(db, id)


