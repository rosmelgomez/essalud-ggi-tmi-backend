from datetime import date

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.main.repositories.tmiBaseRep import name_server

# Tablas del cierre: en la misma base que las tablas tmi_* (TMI_DB)
CIERRE_TABLA = f"{name_server}.cierre"
# Calendario de cierre por año
CALENDARIO_TABLA = f"{name_server}.cierre_calendario"
COLS_DIAS = ", ".join(f"dia_{m:02d}" for m in range(1, 13))

# Tablas que se copian del periodo anterior en el cierre (solo lectura aquí)
TABLAS_CIERRE = {
    #"tmi_centro": f"{name_server}.tmi_centro",
    #"tmi_estandar_tipo": f"{name_server}.tmi_estandar_tipo",
    #"tmi_estandar_nivel": f"{name_server}.tmi_estandar_nivel",
    # desactivado por ahora: tmi_estandar_categoria aún no tiene datos
    # "tmi_estandar_categoria": f"{name_server}.tmi_estandar_categoria",
}


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


### reprogramar la fecha de un cierre que aún no se ejecutó (el calendario cambió)
def queryReprogramarCierre(db: Session, periodo: str, fecha_cierre: date, usuario: str | None) -> int:
    query = f"""
    UPDATE {CIERRE_TABLA}
       SET fecha_cierre = :fecha_cierre,
           estado = 'PENDIENTE',
           mensaje = NULL,
           usuario_modifica = :usuario
     WHERE periodo = :periodo AND estado IN ('PENDIENTE', 'ERROR') AND fecha_cierre <> :fecha_cierre
    """
    result = db.execute(text(query), {"periodo": periodo, "fecha_cierre": fecha_cierre, "usuario": usuario})
    db.commit()
    return result.rowcount


### hay cierres pendientes cuya fecha ya llegó
def queryHayCierresPorEjecutar(db: Session, hoy: date) -> bool:
    query = f"SELECT COUNT(1) FROM {CIERRE_TABLA} WHERE estado = 'PENDIENTE' AND fecha_cierre <= :hoy"
    return (db.execute(text(query), {"hoy": hoy}).scalar() or 0) > 0


### calendario de cierre: todos los años o uno
def queryCalendario(db: Session, anio: int | None = None):
    query = f"""
    SELECT id, anio, dia_fijo, {COLS_DIAS}, fecha_modificacion, usuario_modifica
    FROM {CALENDARIO_TABLA}
    {"WHERE anio = :anio" if anio is not None else ""}
    ORDER BY anio DESC
    """
    result = db.execute(text(query), {"anio": anio})
    return [dict(row) for row in result.mappings()]


### crea el calendario del año si no existe: el día general del año anterior o el día por defecto
def queryAsegurarCalendario(db: Session, anio: int, dia_defecto: int) -> bool:
    query = f"""
    INSERT INTO {CALENDARIO_TABLA} (anio, dia_fijo)
    SELECT :anio, COALESCE((SELECT dia_fijo FROM {CALENDARIO_TABLA} WHERE anio = :anio - 1), :dia)
    WHERE NOT EXISTS (SELECT 1 FROM {CALENDARIO_TABLA} WHERE anio = :anio)
    """
    try:
        result = db.execute(text(query), {"anio": anio, "dia": dia_defecto})
        db.commit()
        return result.rowcount > 0
    except IntegrityError:
        db.rollback()
        return False


### guardar el calendario del año (día general y día de cada periodo)
def queryGuardarCalendario(db: Session, anio: int, dia_fijo: int, dias: dict[str, int | None], usuario: str | None):
    params = {"anio": anio, "dia_fijo": dia_fijo, "usuario": usuario, **dias}
    sets = ", ".join(f"{c} = :{c}" for c in dias)
    result = db.execute(text(f"""
    UPDATE {CALENDARIO_TABLA}
       SET dia_fijo = :dia_fijo, {sets}, usuario_modifica = :usuario, fecha_modificacion = SYSDATETIME()
     WHERE anio = :anio
    """), params)
    if result.rowcount == 0:
        cols = ", ".join(dias)
        db.execute(text(f"""
        INSERT INTO {CALENDARIO_TABLA} (anio, dia_fijo, {cols}, usuario_modifica)
        VALUES (:anio, :dia_fijo, {", ".join(":" + c for c in dias)}, :usuario)
        """), params)
    db.commit()


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
