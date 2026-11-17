"""Servicios de las copias de TOTALIZADO3 por periodo (TOTALIZADO3_BACKUP)."""

import logging
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.main.repositories import backupRep
from src.main.service.calculoServ import periodo_valido, se_puede_calcular

logger = logging.getLogger(__name__)


def backupsServ(db: Session):
    """Copias de TOTALIZADO3 guardadas por periodo."""
    return backupRep.queryBackupsTMI(db)


def backupServ(db: Session, periodo: str, usuario: Optional[str] = None, reemplazar: bool = False):
    """Copia TOTALIZADO3 (enero..periodo) como copia del periodo. Si ya existe no se toca, salvo reemplazar=true.
    TOTALIZADO3 solo se lee."""
    p = periodo_valido(periodo)
    if not se_puede_calcular(periodo):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El periodo {periodo} todavía no se puede copiar.")
    logger.info("Usuario '%s' copiando TOTALIZADO3 del periodo %s (reemplazar=%s)", usuario, periodo, reemplazar)
    return backupRep.queryBackupTotalizado3TMI(db, p, usuario, reemplazar)
