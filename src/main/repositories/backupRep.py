"""Copias de TOTALIZADO3 por periodo (TOTALIZADO3_BACKUP)."""

from typing import Optional

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.main.repositories.tmiBaseRep import name_server, _consulta


def queryHayBackupTMI(db: Session, periodo: int) -> bool:
    """True si TOTALIZADO3_BACKUP tiene la copia del periodo (AAAAMM)."""
    return db.execute(text(f"SELECT CASE WHEN EXISTS (SELECT 1 FROM {name_server}.TOTALIZADO3_BACKUP "
                           f"WHERE periodo_backup = :p) THEN 1 ELSE 0 END"), {"p": int(periodo)}).scalar() == 1


def queryBackupsTMI(db: Session):
    """Copias de TOTALIZADO3 guardadas: periodo, filas, fecha y usuario de la copia (de la más reciente a la más antigua)."""
    return _consulta(db, f"""
        SELECT periodo_backup, COUNT(*) AS filas, MAX(fecha_backup) AS fecha_backup, MAX(usuario_backup) AS usuario_backup
        FROM {name_server}.TOTALIZADO3_BACKUP
        GROUP BY periodo_backup
        ORDER BY periodo_backup DESC""")


def queryBackupTotalizado3TMI(db: Session, periodo: int, usuario: Optional[str] = None, reemplazar: bool = False):
    """Copia TOTALIZADO3 (enero..periodo) en TOTALIZADO3_BACKUP con periodo_backup = periodo. TOTALIZADO3 solo se
    lee. Si la copia ya existe no se toca, salvo reemplazar. Devuelve {copiado, filas}."""
    try:
        fila = db.execute(text(f"EXEC {name_server}.usp_tmi_backup_totalizado3 @PERIODO = :p, @USUARIO = :u, "
                               f"@REEMPLAZAR = :r"), {"p": int(periodo), "u": usuario, "r": 1 if reemplazar else 0}
                          ).mappings().first()
        db.commit()
        return {"periodo": int(periodo), "copiado": bool(fila["copiado"]), "filas": fila["filas"]}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
