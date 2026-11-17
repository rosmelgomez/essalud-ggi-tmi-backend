"""Copias de TOTALIZADO3 por periodo (TOTALIZADO3_BACKUP)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.main.security.jwtRequestFilter import get_current_user
from src.main.db.databaseConexion import get_db
from src.main.service import backupServ

router = APIRouter(
    prefix="/backup",
    tags=["TMI Copias de TOTALIZADO3"],
    dependencies=[Depends(get_current_user)],
)


@router.get("")
def backupsTMI(db: Session = Depends(get_db)):
    """Copias de TOTALIZADO3 guardadas por periodo."""
    return backupServ.backupsServ(db)


@router.post("/{periodo}")
def backupTMI(periodo: str, reemplazar: bool = False, db: Session = Depends(get_db),
              current_user: dict = Depends(get_current_user)):
    """Copia TOTALIZADO3 (enero..periodo) como copia del periodo. Si ya existe no se toca, salvo reemplazar=true."""
    return backupServ.backupServ(db, periodo, (current_user or {}).get("username"), reemplazar)
