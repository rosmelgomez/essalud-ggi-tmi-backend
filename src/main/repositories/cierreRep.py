import os
import re
from datetime import date

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# Tabla de cierre (base.esquema.tabla). Configurable por .env
CIERRE_TABLA = os.getenv("CIERRE_TABLA", "pentahodev_prueba.dbo.cierre").strip()
if not re.fullmatch(r"[A-Za-z0-9_]+(\.[A-Za-z0-9_]+){0,2}", CIERRE_TABLA):
    raise RuntimeError("CIERRE_TABLA tiene un formato inválido")

# Tablas que se copian del periodo anterior en el cierre (solo lectura aquí)
TABLAS_CIERRE = {
    "tmi_centro": "pentahodev_prueba.dbo.tmi_centro",
    "tmi_estandar_tipo": "pentahodev_prueba.dbo.tmi_estandar_tipo",
    "tmi_estandar_nivel": "pentahodev_prueba.dbo.tmi_estandar_nivel",
    # desactivado por ahora: tmi_estandar_categoria aún no tiene datos
    # "tmi_estandar_categoria": "pentahodev_prueba.dbo.tmi_estandar_categoria",
}


### crear tabla cierre si no existe
def queryCrearTablaCierre(db: Session):
    query = f"""
    IF OBJECT_ID('{CIERRE_TABLA}', 'U') IS NULL
    BEGIN
        CREATE TABLE {CIERRE_TABLA} (
            id               INT IDENTITY(1,1) PRIMARY KEY,
            periodo          CHAR(6)        NOT NULL,
            fecha_cierre     DATE           NOT NULL,
            estado           VARCHAR(20)    NOT NULL CONSTRAINT DF_cierre_estado DEFAULT 'PENDIENTE',
            fecha_ejecucion  DATETIME2      NULL,
            filas_insertadas INT            NULL,
            mensaje          NVARCHAR(4000) NULL,
            fecha_creacion   DATETIME2      NOT NULL CONSTRAINT DF_cierre_fecha_creacion DEFAULT SYSDATETIME(),
            usuario_modifica VARCHAR(100)   NULL,
            CONSTRAINT UQ_cierre_periodo UNIQUE (periodo),
            CONSTRAINT CK_cierre_estado CHECK (estado IN ('PENDIENTE','EN_PROCESO','EJECUTADO','ERROR'))
        )
    END
    """
    try:
        db.execute(text(query))
        db.commit()
    except Exception as e:
        db.rollback()
        # otro worker la creó al mismo tiempo (error 2714: el objeto ya existe)
        if "2714" not in str(e):
            raise


### insertar fecha de cierre por defecto del periodo si no existe
def queryInsertCierreDefault(db: Session, periodo: str, fecha_cierre: date) -> bool:
    query = f"""
    INSERT INTO {CIERRE_TABLA} (periodo, fecha_cierre)
    SELECT :periodo, :fecha_cierre
    WHERE NOT EXISTS (SELECT 1 FROM {CIERRE_TABLA} WHERE periodo = :periodo)
    """
    try:
        result = db.execute(text(query), {"periodo": periodo, "fecha_cierre": fecha_cierre})
        db.commit()
        return result.rowcount > 0
    except IntegrityError:
        # otro worker insertó el mismo periodo
        db.rollback()
        return False


### listar cierres
def queryListaCierre(db: Session):
    query = f"""
    SELECT id, periodo, fecha_cierre, estado, fecha_ejecucion, filas_insertadas,
           mensaje, fecha_creacion, usuario_modifica
    FROM {CIERRE_TABLA}
    ORDER BY periodo DESC
    """
    result = db.execute(text(query))
    return [dict(row) for row in result.mappings()]


### actualizar fecha de cierre (no se permite si ya se ejecutó)
def queryUpdateFechaCierre(db: Session, periodo: str, fecha_cierre: date, usuario: str | None):
    query = f"""
    UPDATE {CIERRE_TABLA}
       SET fecha_cierre = :fecha_cierre,
           estado = 'PENDIENTE',
           mensaje = NULL,
           usuario_modifica = :usuario
     WHERE periodo = :periodo AND estado <> 'EJECUTADO'
    """
    result = db.execute(text(query), {"periodo": periodo, "fecha_cierre": fecha_cierre, "usuario": usuario})
    db.commit()
    return result.rowcount


### tomar los cierres cuya fecha ya llegó o ya pasó, de cualquier periodo (solo un worker los obtiene)
### un cierre en ERROR solo se reintenta el mismo día en que falló
def queryTomarCierresPendientes(db: Session, hoy: date):
    query = f"""
    UPDATE {CIERRE_TABLA}
       SET estado = 'EN_PROCESO',
           fecha_ejecucion = SYSDATETIME(),
           mensaje = NULL
    OUTPUT inserted.id, inserted.periodo
     WHERE fecha_cierre <= :hoy
       AND (estado = 'PENDIENTE'
            OR (estado = 'ERROR' AND CAST(fecha_ejecucion AS DATE) = CAST(SYSDATETIME() AS DATE)))
    """
    result = db.execute(text(query), {"hoy": hoy})
    rows = [dict(row) for row in result.mappings()]
    db.commit()
    # OUTPUT no garantiza orden: del más antiguo al más reciente, porque cada periodo copia del anterior
    return sorted(rows, key=lambda row: row["periodo"].strip())


### finalizar cierre (EJECUTADO / ERROR)
def queryFinalizarCierre(db: Session, id_cierre: int, estado: str, filas: int | None, mensaje: str | None):
    query = f"""
    UPDATE {CIERRE_TABLA}
       SET estado = :estado,
           filas_insertadas = :filas,
           mensaje = :mensaje,
           fecha_ejecucion = SYSDATETIME()
     WHERE id = :id
    """
    db.execute(text(query), {"id": id_cierre, "estado": estado, "filas": filas, "mensaje": (mensaje or "")[:4000] or None})
    db.commit()


### contar filas de un periodo en una tabla del cierre
def queryContarPeriodo(db: Session, tabla: str, periodo: str) -> int:
    query = f"SELECT COUNT(1) FROM {TABLAS_CIERRE[tabla]} WHERE periodo = :periodo"
    return db.execute(text(query), {"periodo": periodo}).scalar() or 0


### filas por periodo de una tabla del cierre (hasta el periodo indicado)
def queryConteoPorPeriodo(db: Session, tabla: str, hasta: str) -> dict[str, int]:
    query = f"""
    SELECT LTRIM(RTRIM(periodo)) AS periodo, COUNT(1) AS filas
    FROM {TABLAS_CIERRE[tabla]}
    WHERE periodo <= :hasta
    GROUP BY LTRIM(RTRIM(periodo))
    """
    return {row.periodo: row.filas for row in db.execute(text(query), {"hasta": hasta})}


### último periodo cuya fecha de cierre ya llegó
def queryUltimoPeriodoCierre(db: Session, hoy: date) -> str | None:
    query = f"SELECT MAX(periodo) FROM {CIERRE_TABLA} WHERE fecha_cierre <= :hoy"
    periodo = db.execute(text(query), {"hoy": hoy}).scalar()
    return periodo.strip() if periodo else None


### volver a PENDIENTE un cierre (datos nuevos o datos borrados)
def queryReabrirCierre(db: Session, id_cierre: int):
    query = f"""
    UPDATE {CIERRE_TABLA}
       SET estado = 'PENDIENTE',
           mensaje = NULL
     WHERE id = :id AND estado IN ('EJECUTADO', 'ERROR')
    """
    db.execute(text(query), {"id": id_cierre})
    db.commit()


### actualizar las filas del periodo de un cierre ya ejecutado
def queryActualizarFilasCierre(db: Session, id_cierre: int, filas: int):
    query = f"""
    UPDATE {CIERRE_TABLA}
       SET filas_insertadas = :filas
     WHERE id = :id AND estado = 'EJECUTADO' AND ISNULL(filas_insertadas, -1) <> :filas
    """
    db.execute(text(query), {"id": id_cierre, "filas": filas})
    db.commit()
