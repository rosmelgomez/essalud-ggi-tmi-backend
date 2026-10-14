from datetime import datetime
from sqlalchemy.orm import Session
from src.main.dtos.tmiDto import (
    centroTmiDto,
    tmiEstandarTipoDto,
    tmiEstandarNivelDto,
    tmiEstandarCategoriaDto,
)
from fastapi import HTTPException
from sqlalchemy import text


### tmi_centro 
def queryCentrosTMI(db: Session, anio:int):
    try:
        query = f"""
        SElECT * FROM [pentahodev_prueba_01].[dbo].[tmi_centro]
        WHERE periodo = :anio
        """
        result = db.execute(text(query), {"anio": anio})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertCentrosTMI(db: Session, centro:centroTmiDto):
    try:
        query = """
INSERT INTO pentahodev_prueba_01.dbo.tmi_centro
(red,orden,orden_tipo,codcentro,centro,categoria,nivel,tipo,anio, flag_01, flag_02, flag_03, flag_04, flag_05, flag_06, flag_07, flag_08, flag_09, flag_10, flag_11, flag_12)
VALUES 
(:red,:orden,:orden_tipo,:codcentro,:centro,:categoria,:nivel,:tipo,:anio, :flag_01, :flag_02, :flag_03, :flag_04, :flag_05, :flag_06, :flag_07, :flag_08, :flag_09, :flag_10, :flag_11, :flag_12)
        """
        result = db.execute(text(query), {"centro": centro})
        db.commit()
        return {"message": "Centros TMI insertados correctamente", "rows_inserted": result.rowcount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateCentrosTMI(db: Session, dto:centroTmiDto):
    try:
        query = f"""
        UPDATE pentahodev_prueba_01.dbo.tmi_centro
            SET red = :red
            ,orden = :orden
            ,orden_tipo = :orden_tipo
            ,codcentro = :codcentro
            ,centro = :centro
            ,categoria = :categoria
            ,nivel = :nivel
            ,tipo = :tipo
            ,anio = :anio
            ,flag_01 = :flag_01
            ,flag_02 = :flag_02
            ,flag_03 = :flag_03
            ,flag_04 = :flag_04
            ,flag_05 = :flag_05
            ,flag_06 = :flag_06
            ,flag_07 = :flag_07
            ,flag_08 = :flag_08
            ,flag_09 = :flag_09
            ,flag_10 = :flag_10
            ,flag_11 = :flag_11
            ,flag_12 = :flag_12

        WHERE (:id IS NOT NULL AND id = :id) OR (:id IS NULL AND codcentro = :codcentro AND anio = :anio)
        """
        params = dto.model_dump() if hasattr(dto, "model_dump") else dto.dict()
        result = db.execute(text(query), params)
        db.commit()
        return {"message": "Centro TMI actualizado correctamente", "rows_affected": result.rowcount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

### tmi_estandar
def queryEstandar(db: Session ):
    try:
        query = """
        SELECT * FROM pentahodev_prueba_01.dbo.tmi_estandar
        """
        result = db.execute(text(query))
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertEstandar(db: Session, estandar: tmiEstandarTipoDto):
    try:
        query = """
        INSERT INTO pentahodev_prueba_01.dbo.tmi_estandar
        (tipo ,indicador ,fecha_creacion ,fecha_modificacion)
        VALUES (:tipo ,:indicador ,:fecha_creacion ,:fecha_modificacion)
        """
        params = estandar.model_dump() if hasattr(estandar, "model_dump") else estandar.dict()
        result = db.execute(text(query), params)
        db.commit()
        return {"message": "Estándar insertado correctamente", "rows_inserted": result.rowcount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateEstandar(db: Session, dto: tmiEstandarTipoDto):
    try:
        query = """
        UPDATE dbo.tmi_estandar
            SET tipo = :tipo
            ,indicador = :indicador
            ,fecha_creacion = :fecha_creacion
            ,fecha_modificacion = :fecha_modificacion
        WHERE (:id IS NOT NULL AND id = :id) OR (:id IS NULL AND indicador = :indicador)
        """
        params = dto.model_dump() if hasattr(dto, "model_dump") else dto.dict()
        result = db.execute(text(query), params)
        db.commit()
        return {"message": "Estándar actualizado correctamente", "rows_affected": result.rowcount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryDeleteEstandar(db: Session, id: int):
    try:
        query = """
        DELETE FROM dbo.tmi_estandar
        WHERE id = :id
        """
        result = db.execute(text(query), {"id": id})
        db.commit()
        return {"message": "Estándar eliminado correctamente", "rows_deleted": result.rowcount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

### tmi_estandar_tipo
def queryEstandarTipo(db: Session, anio: int):
    try:
        query = """
        SELECT est_t.id, est.tipo, est.indicador, est_t.tipo_centro, est_t.anio, est_t.estandar_01, est_t.estandar_02, est_t.estandar_03, est_t.estandar_04,est_t.estandar_05, 
        est_t.estandar_06, est_t.estandar_07, est_t.estandar_08, est_t.estandar_09, est_t.estandar_10, est_t.estandar_11, est_t.estandar_12
        FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_t
        JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_t.id_estandar = est.id
        WHERE anio =:anio
        """
        result = db.execute(text(query), {"anio": anio})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertEstandarTipo(db: Session, estandar_tipo: tmiEstandarTipoDto):
    try:
        query = """
        INSERT INTO pentahodev_prueba_01.dbo.tmi_estandar_tipo
        (tipo ,indicador ,tipo_centro ,anio ,estandar_01 ,estandar_02 ,estandar_03 ,estandar_04 ,estandar_05 ,estandar_06 ,estandar_07 ,estandar_08 ,estandar_09 ,estandar_10 ,estandar_11 ,estandar_12)
        VALUES (:tipo ,:indicador ,:tipo_centro ,:anio ,:estandar_01 ,:estandar_02 ,:estandar_03 ,:estandar_04 ,:estandar_05 ,:estandar_06 ,:estandar_07 ,:estandar_08 ,:estandar_09 ,:estandar_10 ,:estandar_11 ,:estandar_12)
        """
        params = estandar_tipo.model_dump() if hasattr(estandar_tipo, "model_dump") else estandar_tipo.dict()
        result = db.execute(text(query), params)
        db.commit()
        return {"message": "Estándares por Tipo insertados correctamente", "rows_inserted": result.rowcount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateEstandarTipo(db: Session, dto: tmiEstandarTipoDto):
    try:
        query = """
        UPDATE dbo.tmi_estandar_tipo
            SET tipo = :tipo
            ,indicador = :indicador
            ,tipo_centro = :tipo_centro
            ,anio = :anio
            ,estandar_01 = :estandar_01
            ,estandar_02 = :estandar_02
            ,estandar_03 = :estandar_03
            ,estandar_04 = :estandar_04
            ,estandar_05 = :estandar_05
            ,estandar_06 = :estandar_06
            ,estandar_07 = :estandar_07
            ,estandar_08 = :estandar_08
            ,estandar_09 = :estandar_09
            ,estandar_10 = :estandar_10
            ,estandar_11 = :estandar_11
            ,estandar_12 = :estandar_12

        WHERE (:id IS NOT NULL AND id = :id) OR (:id IS NULL AND tipo_centro = :tipo_centro AND anio = :anio)
        """
        params = dto.model_dump() if hasattr(dto, "model_dump") else dto.dict()
        result = db.execute(text(query), params)
        db.commit()
        return {"message": "Estándar Tipo actualizado correctamente", "rows_affected": result.rowcount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


### tmi_estandar_nivel
def queryEstandarNivel(db: Session, anio: int):
    try:
        query = """
        SELECT est_n.id, est.tipo, est.indicador, est_n.nivel_centro, est_n.anio, est_n.estandar_01, est_n.estandar_02, est_n.estandar_03, est_n.estandar_04,est_n.estandar_05, 
        est_n.estandar_06, est_n.estandar_07, est_n.estandar_08, est_n.estandar_09, est_n.estandar_10, est_n.estandar_11, est_n.estandar_12
        FROM pentahodev_prueba_01.dbo.tmi_estandar_nivel est_n
        JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_n.id_estandar = est.id
        WHERE anio = :anio
        """
        result = db.execute(text(query), {"anio": anio})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertEstandarNivel(db: Session, periodo_actual: str, periodo_anterior: str):
    try:
        anio = periodo_actual[0:4]
        mes = periodo_actual[4:6]

        query = """
        INSERT INTO pentahodev_prueba.dbo.tmi_estandar_nivel
        (tipo ,indicador ,nivel_centro ,anio ,mes ,periodo ,estandar ,acept ,aceptmenos)
        SELECT tipo ,indicador ,nivel_centro ,:anio ,:mes ,:periodo_actual ,estandar ,acept ,aceptmenos
        FROM pentahodev_prueba.dbo.tmi_estandar_nivel
        WHERE periodo = :periodo_anterior
        """
        result = db.execute(text(query), {"periodo_anterior": periodo_anterior, "periodo_actual": periodo_actual, "anio": anio, "mes": mes})
        db.commit()
        return {"message": "Estándares por Nivel insertados correctamente", "rows_inserted": result.rowcount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateEstandarNivel(db: Session, dto: tmiEstandarNivelDto):
    try:
        query = """
        UPDATE pentahodev_prueba.dbo.tmi_estandar_nivel
            SET tipo = :tipo
            ,indicador = :indicador
            ,nivel_centro = :nivel_centro
            ,anio = :anio
            ,mes = :mes
            ,periodo = :periodo
            ,estandar_01 = :estandar_01
            ,estandar_02 = :estandar_02
            ,estandar_03 = :estandar_03
            ,estandar_04 = :estandar_04
            ,estandar_05 = :estandar_05
            ,estandar_06 = :estandar_06
            ,estandar_07 = :estandar_07
            ,estandar_08 = :estandar_08
            ,estandar_09 = :estandar_09
            ,estandar_10 = :estandar_10
            ,estandar_11 = :estandar_11
            ,estandar_12 = :estandar_12

        WHERE (:id IS NOT NULL AND id = :id) OR (:id IS NULL AND nivel_centro = :nivel_centro AND periodo = :periodo)
        """
        params = dto.model_dump() if hasattr(dto, "model_dump") else dto.dict()
        result = db.execute(text(query), params)
        db.commit()
        return {"message": "Estándar Nivel actualizado correctamente", "rows_affected": result.rowcount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

### tmi_estandar_categoria
def queryEstandarCategoria(db: Session, periodo: str):
    try:
        query = """
        SELECT * FROM pentahodev_prueba.dbo.tmi_estandar_categoria
        WHERE periodo = :periodo
        """
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryInsertEstandarCategoria(db: Session, periodo_actual: str, periodo_anterior: str):
    try:
        query = """
        INSERT INTO pentahodev_prueba.dbo.tmi_estandar_categoria
        (tipo, indicador, categoria_centro, anio, mes, periodo, estandar, acept, aceptmenos)
        SELECT tipo, indicador, categoria_centro, CAST(SUBSTRING(:periodo_actual, 1, 4) AS INT), CAST(SUBSTRING(:periodo_actual, 5, 2) AS INT), :periodo_actual, estandar, acept, aceptmenos
        FROM pentahodev_prueba.dbo.tmi_estandar_categoria
        WHERE periodo = :periodo_anterior
        """
        result = db.execute(text(query), {"periodo_actual": periodo_actual, "periodo_anterior": periodo_anterior})
        db.commit()
        return {"message": "Estándares por Categoría insertados correctamente", "rows_inserted": result.rowcount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateEstandarCategoria(db: Session, dto: tmiEstandarCategoriaDto):
    try:
        query = """
        UPDATE pentahodev_prueba.dbo.tmi_estandar_categoria
            SET [tipo] = :tipo
            ,[indicador] = :indicador
            ,[categoria_centro] = :categoria_centro
            ,[anio] = :anio
            ,[mes] = :mes
            ,[periodo] = :periodo
            ,[estandar] = :estandar
            ,[acept] = :acept
            ,[aceptmenos] = :aceptmenos
        WHERE (:id IS NOT NULL AND id = :id) OR (:id IS NULL AND categoria_centro = :categoria_centro AND periodo = :periodo)
        """
        params = dto.model_dump() if hasattr(dto, "model_dump") else dto.dict()
        result = db.execute(text(query), params)
        db.commit()
        return {"message": "Estándar Categoría actualizado correctamente", "rows_affected": result.rowcount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


### alta de filas (centros y estándares)
# columnas que identifican una fila dentro de su periodo (para no duplicarla)
CLAVES_TABLA = {
    "tmi_centro": ["codcentro"],
    "tmi_estandar": ["id_estandar"],
    "tmi_estandar_tipo": ["indicador", "tipo_centro"],
    "tmi_estandar_nivel": ["indicador", "nivel_centro"],
    "tmi_estandar_categoria": ["indicador", "categoria_centro"],
}

COLUMNAS_TABLA = {
    "tmi_centro": ["red", "codred", "orden", "orden_tipo", "codcentro", "categoria", "nivel", "tipo", "centro", "estado", "anio", "mes", "periodo"],
    "tmi_estandar_tipo": ["tipo", "indicador", "tipo_centro", "anio", "mes", "periodo", "estandar", "acept", "aceptmenos"],
    "tmi_estandar_nivel": ["tipo", "indicador", "nivel_centro", "anio", "mes", "periodo", "estandar", "acept", "aceptmenos"],
    "tmi_estandar_categoria": ["tipo", "indicador", "categoria_centro", "anio", "mes", "periodo", "estandar", "acept", "aceptmenos"],
}


def queryPeriodoDeFila(db: Session, tabla: str, id: int):
    query = f"SELECT periodo FROM pentahodev_prueba.dbo.{tabla} WHERE id = :id"
    periodo = db.execute(text(query), {"id": id}).scalar()
    return str(periodo).strip() if periodo is not None else None


def queryContarFilasPeriodo(db: Session, tabla: str, periodo: str) -> int:
    query = f"SELECT COUNT(*) FROM pentahodev_prueba.dbo.{tabla} WHERE periodo = :periodo"
    return db.execute(text(query), {"periodo": periodo}).scalar() or 0


def queryExisteFilaPeriodo(db: Session, tabla: str, params: dict, excluir_id=None) -> bool:
    condiciones = " AND ".join(f"{c} = :{c}" for c in CLAVES_TABLA[tabla])
    query = f"""
    SELECT COUNT(*) FROM pentahodev_prueba.dbo.{tabla}
    WHERE periodo = :periodo AND {condiciones} AND (:excluir_id IS NULL OR id <> :excluir_id)
    """
    return db.execute(text(query), {**params, "excluir_id": excluir_id}).scalar() > 0


def queryCreateFila(db: Session, tabla: str, params: dict):
    try:
        columnas = COLUMNAS_TABLA[tabla]
        query = f"""
        INSERT INTO pentahodev_prueba.dbo.{tabla} ({", ".join(columnas)})
        OUTPUT INSERTED.id
        VALUES ({", ".join(":" + c for c in columnas)})
        """
        nuevo_id = db.execute(text(query), {c: params.get(c) for c in columnas}).scalar()
        db.commit()
        return {"message": "Fila agregada correctamente", "id": nuevo_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


### consultar estandares tipo por centro
def queryEstandaresTipoCentro(db: Session, codcentro:str, periodo:str):
    try:
        query = f"""
            SELECT est.*, cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.periodo
            FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
            JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo
            WHERE cen.codcentro = :codcentro AND est.periodo = :periodo
        """
        result = db.execute(text(query), {"codcentro": codcentro, "periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

### consultar estandares nivel por centro
def queryEstandarNivelCentro(db: Session, codcentro:str , periodo:str) :
    try:
        query = f"""
            SELECT est.*, cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.periodo
            FROM pentahodev_prueba.dbo.tmi_estandar_nivel est
            JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.nivel_centro = cen.nivel
            WHERE cen.codcentro = :codcentro AND est.periodo = :periodo
        """
        result = db.execute(text(query), {"codcentro": codcentro, "periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


### consulta de vistas
##CE_Concent
def queryCE_ConcentRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Consulta Externa - Consultas'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Consulta Externa - Consultantes al Establecimiento'
),
CEN AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable IN ('Consulta Externa - Consultas', 'Consulta Externa - Consultantes al Establecimiento')
)
SELECT DISTINCT 
    D.id AS ORDEN, D.red AS Red, D.codcentro, D.centro AS Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar* 1.1  AS [% Acept],

    CASE 
        WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
        ) > 0
        THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
        ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
        )
        ELSE 0 
    END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN A.[202601] = 0 OR B.[202601] = 0 THEN 0 ELSE (A.[202601] * 1.00) / B.[202601] END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN A.[202602] = 0 OR B.[202602] = 0 THEN 0 ELSE ((A.[202601] + A.[202602]) * 1.00) / (B.[202601] + B.[202602]) END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN A.[202603] = 0 OR B.[202603] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603]) * 1.00) / (B.[202601] + B.[202602] + B.[202603]) END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN A.[202604] = 0 OR B.[202604] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604]) END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN A.[202605] = 0 OR B.[202605] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605]) END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN A.[202606] = 0 OR B.[202606] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606]) END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN A.[202607] = 0 OR B.[202607] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607]) END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN A.[202608] = 0 OR B.[202608] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608]) END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN A.[202609] = 0 OR B.[202609] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609]) END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN A.[202610] = 0 OR B.[202610] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610]) END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN A.[202611] = 0 OR B.[202611] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611]) END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN A.[202612] = 0 OR B.[202612] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]+ A.[202612]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611] + B.[202612]) END ELSE 0 END AS [202612]
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (        
        SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_nivel.estandar_01
            WHEN 2  THEN est_nivel.estandar_02
            WHEN 3  THEN est_nivel.estandar_03
            WHEN 4  THEN est_nivel.estandar_04
            WHEN 5  THEN est_nivel.estandar_05
            WHEN 6  THEN est_nivel.estandar_06
            WHEN 7  THEN est_nivel.estandar_07
            WHEN 8  THEN est_nivel.estandar_08
            WHEN 9  THEN est_nivel.estandar_09
            WHEN 10 THEN est_nivel.estandar_10
            WHEN 11 THEN est_nivel.estandar_11
            WHEN 12 THEN est_nivel.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_nivel est_nivel
    JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_nivel.id_estandar 
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_nivel.nivel_centro = cen.nivel AND est_nivel.anio = cen.anio
    WHERE est.indicador = 'Concentracion de Consultas' AND est_nivel.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
ORDER BY ORDEN asc;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

##CE_GCHProg
def queryCE_GCHProgRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Consulta Externa - Horas Médicas Efectivas'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Consulta Externa - Horas Médicas Programadas'
),
CEN AS (
     SELECT DISTINCT Red, codcentro, Centro
     FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
     WHERE     variable IN ('Consulta Externa - Horas Médicas Efectivas')
     UNION
     SELECT DISTINCT Red, codcentro, Centro
     FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
     WHERE     variable IN ('Consulta Externa - Horas Médicas Programadas')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar*0.95 AS [% Acept],
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
         
        SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.estandar_01
            WHEN 2  THEN est_tipo.estandar_02
            WHEN 3  THEN est_tipo.estandar_03
            WHEN 4  THEN est_tipo.estandar_04
            WHEN 5  THEN est_tipo.estandar_05
            WHEN 6  THEN est_tipo.estandar_06
            WHEN 7  THEN est_tipo.estandar_07
            WHEN 8  THEN est_tipo.estandar_08
            WHEN 9  THEN est_tipo.estandar_09
            WHEN 10 THEN est_tipo.estandar_10
            WHEN 11 THEN est_tipo.estandar_11
            WHEN 12 THEN est_tipo.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar 
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo AND est_tipo.anio = cen.anio
    WHERE est.indicador = 'Grado de Cumplimiento de Horas Programadas' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## CE_Recetas
def queryCE_RecetasRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Actividades Intermedias - Recetas Despachadas de C. E'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Consulta Externa - Consultas'
),
CEN AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     variable IN ('Actividades Intermedias - Recetas Despachadas de C. E')
    UNION
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     variable IN ('Consulta Externa - Consultas')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar*1.1 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  THEN ISNULL((ISNULL(A.[202601],0) * 1.00) / NULLIF(ISNULL(B.[202601],0),0),0) ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN ISNULL((ISNULL(A.[202602],0) * 1.00) / NULLIF(ISNULL(B.[202602],0),0),0) ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN ISNULL((ISNULL(A.[202603],0) * 1.00) / NULLIF(ISNULL(B.[202603],0),0),0) ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN ISNULL((ISNULL(A.[202604],0) * 1.00) / NULLIF(ISNULL(B.[202604],0),0),0) ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN ISNULL((ISNULL(A.[202605],0) * 1.00) / NULLIF(ISNULL(B.[202605],0),0),0) ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN ISNULL((ISNULL(A.[202606],0) * 1.00) / NULLIF(ISNULL(B.[202606],0),0),0) ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN ISNULL((ISNULL(A.[202607],0) * 1.00) / NULLIF(ISNULL(B.[202607],0),0),0) ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN ISNULL((ISNULL(A.[202608],0) * 1.00) / NULLIF(ISNULL(B.[202608],0),0),0) ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN ISNULL((ISNULL(A.[202609],0) * 1.00) / NULLIF(ISNULL(B.[202609],0),0),0) ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN ISNULL((ISNULL(A.[202610],0) * 1.00) / NULLIF(ISNULL(B.[202610],0),0),0) ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN ISNULL((ISNULL(A.[202611],0) * 1.00) / NULLIF(ISNULL(B.[202611],0),0),0) ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN ISNULL((ISNULL(A.[202612],0) * 1.00) / NULLIF(ISNULL(B.[202612],0),0),0) ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.estandar_01
            WHEN 2  THEN est_tipo.estandar_02
            WHEN 3  THEN est_tipo.estandar_03
            WHEN 4  THEN est_tipo.estandar_04
            WHEN 5  THEN est_tipo.estandar_05
            WHEN 6  THEN est_tipo.estandar_06
            WHEN 7  THEN est_tipo.estandar_07
            WHEN 8  THEN est_tipo.estandar_08
            WHEN 9  THEN est_tipo.estandar_09
            WHEN 10 THEN est_tipo.estandar_10
            WHEN 11 THEN est_tipo.estandar_11
            WHEN 12 THEN est_tipo.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar 
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo AND est_tipo.anio = cen.anio
    WHERE est.indicador = 'Promedio de Recetas por Consultas' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## CE_RHrMedico
def queryCE_RHrMedicoRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Consulta Externa - Consultas'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Consulta Externa - Horas Médicas Efectivas'
),
CEN_NIVEL AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE variable IN ('Consulta Externa - Consultas', 'Consulta Externa - Horas Médicas Efectivas')
),
CEN_TIPO AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar *0.9  AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN_NIVEL AS CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_nivel.estandar_01
            WHEN 2  THEN est_nivel.estandar_02
            WHEN 3  THEN est_nivel.estandar_03
            WHEN 4  THEN est_nivel.estandar_04
            WHEN 5  THEN est_nivel.estandar_05
            WHEN 6  THEN est_nivel.estandar_06
            WHEN 7  THEN est_nivel.estandar_07
            WHEN 8  THEN est_nivel.estandar_08
            WHEN 9  THEN est_nivel.estandar_09
            WHEN 10 THEN est_nivel.estandar_10
            WHEN 11 THEN est_nivel.estandar_11
            WHEN 12 THEN est_nivel.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_nivel est_nivel
    JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_nivel.id_estandar
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_nivel.nivel_centro = cen.nivel AND est_nivel.anio = cen.anio
    WHERE est.indicador = 'Rendimiento Hora Medico' AND est_nivel.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo NOT IN ('CNSR','IPO','INCOR')

UNION ALL

SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar *0.9 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

    FROM CEN_TIPO AS CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.estandar_01
            WHEN 2  THEN est_tipo.estandar_02
            WHEN 3  THEN est_tipo.estandar_03
            WHEN 4  THEN est_tipo.estandar_04
            WHEN 5  THEN est_tipo.estandar_05
            WHEN 6  THEN est_tipo.estandar_06
            WHEN 7  THEN est_tipo.estandar_07
            WHEN 8  THEN est_tipo.estandar_08
            WHEN 9  THEN est_tipo.estandar_09
            WHEN 10 THEN est_tipo.estandar_10
            WHEN 11 THEN est_tipo.estandar_11
            WHEN 12 THEN est_tipo.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo AND est_tipo.anio = cen.anio
    WHERE est.indicador = 'Rendimiento Hora Medico' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo IN ('CNSR','IPO','INCOR')
ORDER BY ORDEN;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Em_PrioI_II
def queryEm_PrioI_IIRep(db: Session, periodo:str): 
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
               SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
               SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
               FROM        pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
               WHERE      (Variable IN ('Emergencia - Prioridad I', 'Emergencia - Prioridad II'))
               GROUP BY Red, Centro, nivel, codcentro, Año
),
X AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Emergencia - Total de Atenciones'
),
CEN AS (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Emergencia - Prioridad I', 'Emergencia - Prioridad II', 'Emergencia - Total de Atenciones'))
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.9 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(X.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(X.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN X.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / X.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN X.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / X.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN X.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / X.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN X.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / X.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN X.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / X.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN X.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / X.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN X.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / X.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN X.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / X.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN X.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / X.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN X.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / X.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN X.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / X.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN X.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / X.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN X ON CEN.codcentro = X.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.estandar_01
            WHEN 2  THEN est_tipo.estandar_02
            WHEN 3  THEN est_tipo.estandar_03
            WHEN 4  THEN est_tipo.estandar_04
            WHEN 5  THEN est_tipo.estandar_05
            WHEN 6  THEN est_tipo.estandar_06
            WHEN 7  THEN est_tipo.estandar_07
            WHEN 8  THEN est_tipo.estandar_08
            WHEN 9  THEN est_tipo.estandar_09
            WHEN 10 THEN est_tipo.estandar_10
            WHEN 11 THEN est_tipo.estandar_11
            WHEN 12 THEN est_tipo.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo AND est_tipo.anio = cen.anio
    WHERE est.indicador = '% Prioridad I y II con respecto al Total de Emergencias' AND est_tipo.anio = @Anio
 ) AS D ON CEN.codcentro = D.codcentro
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Em_PrioIV_V
def queryEm_PrioIV_VRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
            SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
            SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
            SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
            FROM       pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
            WHERE      (Variable IN ('Emergencia - Prioridad IV', 'Emergencia - Prioridad V'))
            GROUP BY Red, Centro, nivel, codcentro, Año),
X AS (
       SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
       [202601],[202602],[202603],[202604],[202605],[202606],
       [202607],[202608],[202609],[202610],[202611],[202612], Variable
       FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
       WHERE Variable = 'Emergencia - Total de Atenciones'
),
CEN AS (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Emergencia - Prioridad IV', 'Emergencia - Prioridad V', 'Emergencia - Total de Atenciones'))
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar* 0.9 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(X.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(X.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN X.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / X.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN X.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / X.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN X.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / X.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN X.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / X.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN X.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / X.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN X.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / X.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN X.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / X.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN X.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / X.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN X.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / X.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN X.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / X.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN X.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / X.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN X.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / X.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN X ON CEN.codcentro = X.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.estandar_01
            WHEN 2  THEN est_tipo.estandar_02
            WHEN 3  THEN est_tipo.estandar_03
            WHEN 4  THEN est_tipo.estandar_04
            WHEN 5  THEN est_tipo.estandar_05
            WHEN 6  THEN est_tipo.estandar_06
            WHEN 7  THEN est_tipo.estandar_07
            WHEN 8  THEN est_tipo.estandar_08
            WHEN 9  THEN est_tipo.estandar_09
            WHEN 10 THEN est_tipo.estandar_10
            WHEN 11 THEN est_tipo.estandar_11
            WHEN 12 THEN est_tipo.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo AND est_tipo.anio = cen.anio
    WHERE est.indicador = '% Prioridad IV y V con respecto al Total de Emergencias' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo IN ('H.N.', 'H.IV', 'H.III', 'H.II', 'H.I')
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## H_Estancias
def queryH_EstanciasRep(db: Session, periodo:str):
    try:    
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion - Estancias'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion - Egresos'
),
CEN AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     variable IN ('Hospitalizacion - Estancias')
    UNION
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     variable IN ('Hospitalizacion - Egresos')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 1.2 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.estandar_01
            WHEN 2  THEN est_tipo.estandar_02
            WHEN 3  THEN est_tipo.estandar_03
            WHEN 4  THEN est_tipo.estandar_04
            WHEN 5  THEN est_tipo.estandar_05
            WHEN 6  THEN est_tipo.estandar_06
            WHEN 7  THEN est_tipo.estandar_07
            WHEN 8  THEN est_tipo.estandar_08
            WHEN 9  THEN est_tipo.estandar_09
            WHEN 10 THEN est_tipo.estandar_10
            WHEN 11 THEN est_tipo.estandar_11
            WHEN 12 THEN est_tipo.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo AND est_tipo.anio = cen.anio
    WHERE est.indicador = 'Promedio Dia Estancia' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## H_ISust
def queryH_ISustRep(db: Session, periodo:str):
    try:    
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion - Días Cama Disponible'
),
B AS (
     SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
            [202601],[202602],[202603],[202604],[202605],[202606],
            [202607],[202608],[202609],[202610],[202611],[202612], Variable
     FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
     WHERE Variable = 'Hospitalizacion - Pacientes Días'
),
x AS (
     SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
     [202609], [202610], [202611], [202612], Variable
     FROM   pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
     WHERE  Variable IN ('Hospitalizacion - Egresos')
),
CEN AS (
     SELECT DISTINCT Red, codcentro, Centro
     FROM   pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
     WHERE  variable IN ('Hospitalizacion - Días Cama Disponible', 'Hospitalizacion - Pacientes Días', 'Hospitalizacion - Egresos')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 1.2 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(x.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(x.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(x.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(x.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(x.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(x.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(x.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(x.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(x.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(x.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(x.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(x.[202612],0) ELSE 0 END
         ) <> 0
    THEN ((
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) - (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(x.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(x.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(x.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(x.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(x.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(x.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(x.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(x.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(x.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(x.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(x.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(x.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN x.[202601] <> 0 THEN ((isnull(A.[202601], 0) - isnull(B.[202601], 0)) * 1.00) / x.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN x.[202602] <> 0 THEN ((isnull(A.[202602], 0) - isnull(B.[202602], 0)) * 1.00) / x.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN x.[202603] <> 0 THEN ((isnull(A.[202603], 0) - isnull(B.[202603], 0)) * 1.00) / x.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN x.[202604] <> 0 THEN ((isnull(A.[202604], 0) - isnull(B.[202604], 0)) * 1.00) / x.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN x.[202605] <> 0 THEN ((isnull(A.[202605], 0) - isnull(B.[202605], 0)) * 1.00) / x.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN x.[202606] <> 0 THEN ((isnull(A.[202606], 0) - isnull(B.[202606], 0)) * 1.00) / x.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN x.[202607] <> 0 THEN ((isnull(A.[202607], 0) - isnull(B.[202607], 0)) * 1.00) / x.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN x.[202608] <> 0 THEN ((isnull(A.[202608], 0) - isnull(B.[202608], 0)) * 1.00) / x.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN x.[202609] <> 0 THEN ((isnull(A.[202609], 0) - isnull(B.[202609], 0)) * 1.00) / x.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN x.[202610] <> 0 THEN ((isnull(A.[202610], 0) - isnull(B.[202610], 0)) * 1.00) / x.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN x.[202611] <> 0 THEN ((isnull(A.[202611], 0) - isnull(B.[202611], 0)) * 1.00) / x.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN x.[202612] <> 0 THEN ((isnull(A.[202612], 0) - isnull(B.[202612], 0)) * 1.00) / x.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN x ON CEN.codcentro = x.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est.estandar_01
            WHEN 2  THEN est.estandar_02
            WHEN 3  THEN est.estandar_03
            WHEN 4  THEN est.estandar_04
            WHEN 5  THEN est.estandar_05
            WHEN 6  THEN est.estandar_06
            WHEN 7  THEN est.estandar_07
            WHEN 8  THEN est.estandar_08
            WHEN 9  THEN est.estandar_09
            WHEN 10 THEN est.estandar_10
            WHEN 11 THEN est.estandar_11
            WHEN 12 THEN est.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.anio = cen.anio
    WHERE est.indicador = 'Intervalo de Sustitución' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

##H_OCamas
def queryH_OCamasRep(db: Session, periodo:str):
    try:    
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion - Pacientes Días'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion - Días Cama Disponible'
),
CEN AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     variable IN ('Hospitalizacion - Pacientes Días')
    UNION
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     variable IN ('Hospitalizacion - Días Cama Disponible')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.tipo AS TIPO, D.estandar AS Estandar, D.estandar * 0.95 AS [% Aceptmenos], D.estandar * 1.05 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est.estandar_01
            WHEN 2  THEN est.estandar_02
            WHEN 3  THEN est.estandar_03
            WHEN 4  THEN est.estandar_04
            WHEN 5  THEN est.estandar_05
            WHEN 6  THEN est.estandar_06
            WHEN 7  THEN est.estandar_07
            WHEN 8  THEN est.estandar_08
            WHEN 9  THEN est.estandar_09
            WHEN 10 THEN est.estandar_10
            WHEN 11 THEN est.estandar_11
            WHEN 12 THEN est.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.anio = cen.anio
    WHERE est.indicador = 'Porcentaje de Ocupación de Cama' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## H_RCama
def queryH_RCamaRep(db: Session, periodo:str):
    try:    
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); 

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion - Egresos'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion -  Camas Hospitalarias'
),
CEN AS (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Hospitalizacion - Egresos', 'Hospitalizacion -  Camas Hospitalarias')))
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.tipo AS TIPO, D.estandar AS Estandar, D.estandar * 0.8 AS [% Acept],
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 * (
            CASE WHEN @Mes>=1  AND B.[202601] > 0 THEN 1 ELSE 0 END +
            CASE WHEN @Mes>=2  AND B.[202602] > 0 THEN 1 ELSE 0 END +
            CASE WHEN @Mes>=3  AND B.[202603] > 0 THEN 1 ELSE 0 END +
            CASE WHEN @Mes>=4  AND B.[202604] > 0 THEN 1 ELSE 0 END +
            CASE WHEN @Mes>=5  AND B.[202605] > 0 THEN 1 ELSE 0 END +
            CASE WHEN @Mes>=6  AND B.[202606] > 0 THEN 1 ELSE 0 END +
            CASE WHEN @Mes>=7  AND B.[202607] > 0 THEN 1 ELSE 0 END +
            CASE WHEN @Mes>=8  AND B.[202608] > 0 THEN 1 ELSE 0 END +
            CASE WHEN @Mes>=9  AND B.[202609] > 0 THEN 1 ELSE 0 END +
            CASE WHEN @Mes>=10 AND B.[202610] > 0 THEN 1 ELSE 0 END +
            CASE WHEN @Mes>=11 AND B.[202611] > 0 THEN 1 ELSE 0 END +
            CASE WHEN @Mes>=12 AND B.[202612] > 0 THEN 1 ELSE 0 END
         ) / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est.estandar_01
            WHEN 2  THEN est.estandar_02
            WHEN 3  THEN est.estandar_03
            WHEN 4  THEN est.estandar_04
            WHEN 5  THEN est.estandar_05
            WHEN 6  THEN est.estandar_06
            WHEN 7  THEN est.estandar_07
            WHEN 8  THEN est.estandar_08
            WHEN 9  THEN est.estandar_09
            WHEN 10 THEN est.estandar_10
            WHEN 11 THEN est.estandar_11
            WHEN 12 THEN est.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.anio = cen.anio
    WHERE est.indicador = 'Rendimiento Cama' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## H_TBMHosp
def queryH_TBMHospRep(db: Session, periodo:str):
    try:    
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); ;

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion - Defunciones después de 48 horas'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Hospitalizacion - Egresos'
),
x AS (
      SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, 
             [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
             [202609], [202610], [202611], [202612], Variable
      FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
      WHERE Variable IN ('Hospitalizacion - Defunciones antes de 48 horas')),
CEN AS (
      SELECT DISTINCT Red, codcentro, Centro
      FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE variable IN ('Hospitalizacion - Defunciones después de 48 horas')
      UNION
      SELECT DISTINCT Red, codcentro, Centro
      FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE variable IN ('Hospitalizacion - Egresos')
      UNION
      SELECT DISTINCT Red, codcentro, Centro
      FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE variable IN ('Hospitalizacion - Defunciones antes de 48 horas')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.tipo AS TIPO, D.estandar AS Estandar, D.estandar * 1.1 AS [% Acept], 
    CASE WHEN  (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) - (
            CASE WHEN @Mes>=1  THEN ISNULL(x.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(x.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(x.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(x.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(x.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(x.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(x.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(x.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(x.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(x.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(x.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(x.[202612],0) ELSE 0 END
         )
         <> 0
    THEN ((
            CASE WHEN @Mes>=1  THEN (ISNULL(A.[202601],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=2  THEN (ISNULL(A.[202602],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=3  THEN (ISNULL(A.[202603],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=4  THEN (ISNULL(A.[202604],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=5  THEN (ISNULL(A.[202605],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=6  THEN (ISNULL(A.[202606],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=7  THEN (ISNULL(A.[202607],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=8  THEN (ISNULL(A.[202608],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=9  THEN (ISNULL(A.[202609],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=10 THEN (ISNULL(A.[202610],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=11 THEN (ISNULL(A.[202611],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=12 THEN (ISNULL(A.[202612],0))* 1.00 ELSE 0 END
         ) / ((
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) - (
            CASE WHEN @Mes>=1  THEN ISNULL(x.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(x.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(x.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(x.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(x.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(x.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(x.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(x.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(x.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(x.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(x.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(x.[202612],0) ELSE 0 END
         )))
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN (isnull(B.[202601], 0) - isnull(x.[202601], 0)) <> 0 THEN ((isnull(A.[202601], 0)) * 1.00) / (isnull(B.[202601], 0) - isnull(x.[202601], 0)) ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN (isnull(B.[202602], 0) - isnull(x.[202602], 0)) <> 0 THEN ((isnull(A.[202602], 0)) * 1.00) / (isnull(B.[202602], 0) - isnull(x.[202602], 0)) ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN (isnull(B.[202603], 0) - isnull(x.[202603], 0)) <> 0 THEN ((isnull(A.[202603], 0)) * 1.00) / (isnull(B.[202603], 0) - isnull(x.[202603], 0)) ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN (isnull(B.[202604], 0) - isnull(x.[202604], 0)) <> 0 THEN ((isnull(A.[202604], 0)) * 1.00) / (isnull(B.[202604], 0) - isnull(x.[202604], 0)) ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN (isnull(B.[202605], 0) - isnull(x.[202605], 0)) <> 0 THEN ((isnull(A.[202605], 0)) * 1.00) / (isnull(B.[202605], 0) - isnull(x.[202605], 0)) ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN (isnull(B.[202606], 0) - isnull(x.[202606], 0)) <> 0 THEN ((isnull(A.[202606], 0)) * 1.00) / (isnull(B.[202606], 0) - isnull(x.[202606], 0)) ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN (isnull(B.[202607], 0) - isnull(x.[202607], 0)) <> 0 THEN ((isnull(A.[202607], 0)) * 1.00) / (isnull(B.[202607], 0) - isnull(x.[202607], 0)) ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN (isnull(B.[202608], 0) - isnull(x.[202608], 0)) <> 0 THEN ((isnull(A.[202608], 0)) * 1.00) / (isnull(B.[202608], 0) - isnull(x.[202608], 0)) ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN (isnull(B.[202609], 0) - isnull(x.[202609], 0)) <> 0 THEN ((isnull(A.[202609], 0)) * 1.00) / (isnull(B.[202609], 0) - isnull(x.[202609], 0)) ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN (isnull(B.[202610], 0) - isnull(x.[202610], 0)) <> 0 THEN ((isnull(A.[202610], 0)) * 1.00) / (isnull(B.[202610], 0) - isnull(x.[202610], 0)) ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN (isnull(B.[202611], 0) - isnull(x.[202611], 0)) <> 0 THEN ((isnull(A.[202611], 0)) * 1.00) / (isnull(B.[202611], 0) - isnull(x.[202611], 0)) ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN (isnull(B.[202612], 0) - isnull(x.[202612], 0)) <> 0 THEN ((isnull(A.[202612], 0)) * 1.00) / (isnull(B.[202612], 0) - isnull(x.[202612], 0)) ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN x ON CEN.codcentro = x.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est.estandar_01
            WHEN 2  THEN est.estandar_02
            WHEN 3  THEN est.estandar_03
            WHEN 4  THEN est.estandar_04
            WHEN 5  THEN est.estandar_05
            WHEN 6  THEN est.estandar_06
            WHEN 7  THEN est.estandar_07
            WHEN 8  THEN est.estandar_08
            WHEN 9  THEN est.estandar_09
            WHEN 10 THEN est.estandar_10
            WHEN 11 THEN est.estandar_11
            WHEN 12 THEN est.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.anio = cen.anio
    WHERE est.indicador = 'Tasa Neta de Mortalidad Hospitalaria' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## O_Concent
def queryO_ConcentRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT); ;

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Odontología - Sesiones Odontológicas'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Odontología - Consultantes de Odontología'
),
CEN AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     Variable IN ('Odontología - Sesiones Odontológicas', 'Odontología - Consultantes de Odontología')
)
SELECT DISTINCT 
    D.id AS ORDEN, D.red AS Red, D.codcentro, D.centro AS Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 1.1 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN A.[202601] <> 0 OR B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN A.[202602] <> 0 OR B.[202602] <> 0 THEN ((A.[202601] + A.[202602]) * 1.00) / (B.[202601] + B.[202602]) ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN A.[202603] <> 0 OR B.[202603] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603]) * 1.00) / (B.[202601] + B.[202602] + B.[202603]) ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN A.[202604] <> 0 OR B.[202604] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604]) ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN A.[202605] <> 0 OR B.[202605] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605]) ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN A.[202606] <> 0 OR B.[202606] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606]) ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN A.[202607] <> 0 OR B.[202607] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607]) ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN A.[202608] <> 0 OR B.[202608] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608]) ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN A.[202609] <> 0 OR B.[202609] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609]) ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN A.[202610] <> 0 OR B.[202610] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610]) ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN A.[202611] <> 0 OR B.[202611] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611]) ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN A.[202612] <> 0 OR B.[202612] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611] + A.[202612]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611] + B.[202612]) ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est.estandar_01
            WHEN 2  THEN est.estandar_02
            WHEN 3  THEN est.estandar_03
            WHEN 4  THEN est.estandar_04
            WHEN 5  THEN est.estandar_05
            WHEN 6  THEN est.estandar_06
            WHEN 7  THEN est.estandar_07
            WHEN 8  THEN est.estandar_08
            WHEN 9  THEN est.estandar_09
            WHEN 10 THEN est.estandar_10
            WHEN 11 THEN est.estandar_11
            WHEN 12 THEN est.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_nivel est
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est.nivel_centro = cen.nivel AND est.anio = cen.anio
    WHERE est.indicador = 'Concentración de Sesiones Odontológicas' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## O_GCHOdon
def queryO_GCHOdonRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Odontología - Horas Odontológicas Efectivas'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Odontología - Horas Odontológicas Programadas'
),
CEN AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     Variable IN ('Odontología - Sesiones Odontológicas', 'Odontología - Horas Odontológicas Efectivas')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.95 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
            CASE WHEN ( CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END) ELSE 0 END AS [202601],
            CASE WHEN ( CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END) ELSE 0 END AS [202602],
            CASE WHEN ( CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END) ELSE 0 END AS [202603],
            CASE WHEN ( CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END) ELSE 0 END AS [202604],
            CASE WHEN ( CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END) ELSE 0 END AS [202605],
            CASE WHEN ( CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END) ELSE 0 END AS [202606],
            CASE WHEN ( CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END) ELSE 0 END AS [202607],
            CASE WHEN ( CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END) ELSE 0 END AS [202608],
            CASE WHEN ( CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END) ELSE 0 END AS [202609],
            CASE WHEN ( CASE WHEN @Mes>=10  THEN ISNULL(B.[202610],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=10  THEN ISNULL(A.[202610],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=10  THEN ISNULL(B.[202610],0) ELSE 0 END) ELSE 0 END AS [202610],
            CASE WHEN ( CASE WHEN @Mes>=11  THEN ISNULL(B.[202611],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=11  THEN ISNULL(A.[202611],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=11  THEN ISNULL(B.[202611],0) ELSE 0 END) ELSE 0 END AS [202611],
            CASE WHEN ( CASE WHEN @Mes>=12  THEN ISNULL(B.[202612],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=12  THEN ISNULL(A.[202612],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=12  THEN ISNULL(B.[202612],0) ELSE 0 END) ELSE 0 END AS [202612]
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est.estandar_01
            WHEN 2  THEN est.estandar_02
            WHEN 3  THEN est.estandar_03
            WHEN 4  THEN est.estandar_04
            WHEN 5  THEN est.estandar_05
            WHEN 6  THEN est.estandar_06
            WHEN 7  THEN est.estandar_07
            WHEN 8  THEN est.estandar_08
            WHEN 9  THEN est.estandar_09
            WHEN 10 THEN est.estandar_10
            WHEN 11 THEN est.estandar_11
            WHEN 12 THEN est.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.anio = cen.anio
    WHERE est.indicador = 'Grado de Cumplimiento de Hora Odontólogo' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## O_HrOdont
def queryO_HrOdontRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (
        SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608],
           [202609], [202610], [202611], [202612], Variable
         FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
         WHERE      Variable IN ('Odontología - Sesiones Odontológicas')
),
B AS (
        SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608],
            [202609], [202610], [202611], [202612], Variable
         FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
         WHERE     Variable IN ('Odontología - Horas Odontológicas Efectivas')
),
CEN_NIVEL AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE variable IN ('Odontología - Sesiones Odontológicas', 'Odontología - Horas Odontológicas Efectivas')
),
CEN_TIPO AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
)
SELECT DISTINCT
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.9 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]
FROM CEN_NIVEL AS CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est.estandar_01
            WHEN 2  THEN est.estandar_02
            WHEN 3  THEN est.estandar_03
            WHEN 4  THEN est.estandar_04
            WHEN 5  THEN est.estandar_05
            WHEN 6  THEN est.estandar_06
            WHEN 7  THEN est.estandar_07
            WHEN 8  THEN est.estandar_08
            WHEN 9  THEN est.estandar_09
            WHEN 10 THEN est.estandar_10
            WHEN 11 THEN est.estandar_11
            WHEN 12 THEN est.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_nivel est
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est.nivel_centro = cen.nivel AND est.anio = cen.anio
    WHERE est.indicador = 'Rendimiento de Hora Odontológica' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo NOT IN ('CNSR','IPO','INCOR')

UNION ALL

SELECT DISTINCT
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.9 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]
FROM CEN_TIPO AS CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est.estandar_01
            WHEN 2  THEN est.estandar_02
            WHEN 3  THEN est.estandar_03
            WHEN 4  THEN est.estandar_04
            WHEN 5  THEN est.estandar_05
            WHEN 6  THEN est.estandar_06
            WHEN 7  THEN est.estandar_07
            WHEN 8  THEN est.estandar_08
            WHEN 9  THEN est.estandar_09
            WHEN 10 THEN est.estandar_10
            WHEN 11 THEN est.estandar_11
            WHEN 12 THEN est.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.anio = cen.anio
    WHERE est.indicador = 'Rendimiento de Hora Odontológica' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo IN ('CNSR','IPO','INCOR')
ORDER BY ORDEN;
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## O_NTOdontS
def queryO_NTOdontSRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (
           SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
           SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
           SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
           FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
           WHERE  Variable IN ('Odontología - Trabajos Odontológicos', 'Odontología - Diagnóstico por imágenes', 'Odontología - Procedimientos Especiales')
           GROUP BY Red, Centro, nivel, codcentro, Año),
B AS (
           SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
           [202609], [202610], [202611], [202612], Variable
           FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
           WHERE  Variable IN ('Odontología - Sesiones Odontológicas')
),
CEN AS (
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE     variable IN ('Odontología - Trabajos Odontológicos', 'Odontología - Diagnóstico por imágenes', 'Odontología - Procedimientos Especiales')
    UNION
    SELECT DISTINCT Red, codcentro, Centro
    FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.9 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
            CASE WHEN ( CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END) ELSE 0 END AS [202601],
            CASE WHEN ( CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END) ELSE 0 END AS [202602],
            CASE WHEN ( CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END) ELSE 0 END AS [202603],
            CASE WHEN ( CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END) ELSE 0 END AS [202604],
            CASE WHEN ( CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END) ELSE 0 END AS [202605],
            CASE WHEN ( CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END) ELSE 0 END AS [202606],
            CASE WHEN ( CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END) ELSE 0 END AS [202607],
            CASE WHEN ( CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END) ELSE 0 END AS [202608],
            CASE WHEN ( CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END) ELSE 0 END AS [202609],
            CASE WHEN ( CASE WHEN @Mes>=10  THEN ISNULL(B.[202610],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=10  THEN ISNULL(A.[202610],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=10  THEN ISNULL(B.[202610],0) ELSE 0 END) ELSE 0 END AS [202610],
            CASE WHEN ( CASE WHEN @Mes>=11  THEN ISNULL(B.[202611],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=11  THEN ISNULL(A.[202611],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=11  THEN ISNULL(B.[202611],0) ELSE 0 END) ELSE 0 END AS [202611],
            CASE WHEN ( CASE WHEN @Mes>=12  THEN ISNULL(B.[202612],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=12  THEN ISNULL(A.[202612],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=12  THEN ISNULL(B.[202612],0) ELSE 0 END) ELSE 0 END AS [202612]
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est.estandar_01
            WHEN 2  THEN est.estandar_02
            WHEN 3  THEN est.estandar_03
            WHEN 4  THEN est.estandar_04
            WHEN 5  THEN est.estandar_05
            WHEN 6  THEN est.estandar_06
            WHEN 7  THEN est.estandar_07
            WHEN 8  THEN est.estandar_08
            WHEN 9  THEN est.estandar_09
            WHEN 10 THEN est.estandar_10
            WHEN 11 THEN est.estandar_11
            WHEN 12 THEN est.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.anio = cen.anio
    WHERE est.indicador = 'Número de trabajos Odontológicos por Sesión' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE     (A.Total * 1.00 / B.Total IS NOT NULL)
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_GCHProg
def queryQx_GCHProgRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (
      SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                             [202609], [202610], [202611], [202612], Variable
      FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE     Variable IN ('Centro Quirúrgico - Horas Uso de Sala')
),
B AS (
      SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
      [202609], [202610], [202611], [202612], Variable
      FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
      WHERE      Variable IN ('Centro Quirúrgico - Horas Programadas Intervenc.Quirurgicas')
),
CEN AS (
      SELECT DISTINCT Red, codcentro, Centro
      FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE     Variable IN ('Centro Quirúrgico - Horas Uso de Sala', 'Centro Quirúrgico - Horas Programadas Intervenc.Quirurgicas')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.90 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN B.[202601] <> 0 THEN (ISNULL(A.[202601], 0) * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN B.[202602] <> 0 THEN (ISNULL(A.[202602], 0) * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN B.[202603] <> 0 THEN (ISNULL(A.[202603], 0) * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN B.[202604] <> 0 THEN (ISNULL(A.[202604], 0) * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN B.[202605] <> 0 THEN (ISNULL(A.[202605], 0) * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN B.[202606] <> 0 THEN (ISNULL(A.[202606], 0) * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN B.[202607] <> 0 THEN (ISNULL(A.[202607], 0) * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN B.[202608] <> 0 THEN (ISNULL(A.[202608], 0) * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN B.[202609] <> 0 THEN (ISNULL(A.[202609], 0) * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN B.[202610] <> 0 THEN (ISNULL(A.[202610], 0) * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN B.[202611] <> 0 THEN (ISNULL(A.[202611], 0) * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN B.[202612] <> 0 THEN (ISNULL(A.[202612], 0) * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est.estandar_01
            WHEN 2  THEN est.estandar_02
            WHEN 3  THEN est.estandar_03
            WHEN 4  THEN est.estandar_04
            WHEN 5  THEN est.estandar_05
            WHEN 6  THEN est.estandar_06
            WHEN 7  THEN est.estandar_07
            WHEN 8  THEN est.estandar_08
            WHEN 9  THEN est.estandar_09
            WHEN 10 THEN est.estandar_10
            WHEN 11 THEN est.estandar_11
            WHEN 12 THEN est.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.anio = cen.anio
    WHERE est.indicador = 'Porcentaje de Horas Quirúrgicas Efectivas' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_HTCesareas
def queryQx_HTCesareasRep(db: Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (   
           SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
           [202609], [202610], [202611], [202612], Variable
           FROM  pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
           WHERE    Variable IN ('Centro Obstétrico - Cesáreas')
),
B AS (
     SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
     [202609], [202610], [202611], [202612], Variable
     FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
     WHERE      Variable IN ('Centro Obstétrico - Total de Partos')
),
CEN AS (
        SELECT DISTINCT Red, codcentro, Centro
        FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
        WHERE     variable IN ('Centro Obstétrico - Cesáreas')
        UNION
        SELECT DISTINCT Red, codcentro, Centro
        FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
        WHERE     variable IN ('Centro Obstétrico - Total de Partos')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 1.1 AS [% Acept],
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE NULL END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN B.[202601] <> 0 AND A.[202601] <> 0 THEN (ISNULL(A.[202601], 0) * 1.00) / B.[202601] ELSE NULL END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN B.[202602] <> 0 AND A.[202602] <> 0 THEN (ISNULL(A.[202602], 0) * 1.00) / B.[202602] ELSE NULL END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN B.[202603] <> 0 AND A.[202603] <> 0 THEN (ISNULL(A.[202603], 0) * 1.00) / B.[202603] ELSE NULL END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN B.[202604] <> 0 AND A.[202604] <> 0 THEN (ISNULL(A.[202604], 0) * 1.00) / B.[202604] ELSE NULL END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN B.[202605] <> 0 AND A.[202605] <> 0 THEN (ISNULL(A.[202605], 0) * 1.00) / B.[202605] ELSE NULL END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN B.[202606] <> 0 AND A.[202606] <> 0 THEN (ISNULL(A.[202606], 0) * 1.00) / B.[202606] ELSE NULL END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN B.[202607] <> 0 AND A.[202607] <> 0 THEN (ISNULL(A.[202607], 0) * 1.00) / B.[202607] ELSE NULL END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN B.[202608] <> 0 AND A.[202608] <> 0 THEN (ISNULL(A.[202608], 0) * 1.00) / B.[202608] ELSE NULL END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN B.[202609] <> 0 AND A.[202609] <> 0 THEN (ISNULL(A.[202609], 0) * 1.00) / B.[202609] ELSE NULL END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN B.[202610] <> 0 AND A.[202610] <> 0 THEN (ISNULL(A.[202610], 0) * 1.00) / B.[202610] ELSE NULL END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN B.[202611] <> 0 AND A.[202611] <> 0 THEN (ISNULL(A.[202611], 0) * 1.00) / B.[202611] ELSE NULL END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN B.[202612] <> 0 AND A.[202612] <> 0 THEN (ISNULL(A.[202612], 0) * 1.00) / B.[202612] ELSE NULL END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est.estandar_01
            WHEN 2  THEN est.estandar_02
            WHEN 3  THEN est.estandar_03
            WHEN 4  THEN est.estandar_04
            WHEN 5  THEN est.estandar_05
            WHEN 6  THEN est.estandar_06
            WHEN 7  THEN est.estandar_07
            WHEN 8  THEN est.estandar_08
            WHEN 9  THEN est.estandar_09
            WHEN 10 THEN est.estandar_10
            WHEN 11 THEN est.estandar_11
            WHEN 12 THEN est.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.anio = cen.anio
    WHERE est.indicador = 'Tasa de Cesáreas' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_IAlta
def queryQx_IAltaRep(db:Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (   
           SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
           [202609], [202610], [202611], [202612], Variable
           FROM  pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
           WHERE    Variable IN ('Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad')
),
B AS (
      SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
      SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
      SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
      FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
      WHERE      Variable IN ('Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                             'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                             'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento')
      GROUP BY Red, Centro, nivel, codcentro, Año
),
CEN AS (
SELECT DISTINCT Red, codcentro, Centro
FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     Variable IN ('Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 'Centro Quirúrgico - Cirugías sin clasificación de complejidad', 
                      'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 
                      'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 
                      'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.8 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
            CASE WHEN ( CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END) ELSE 0 END AS [202601],
            CASE WHEN ( CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END) ELSE 0 END AS [202602],
            CASE WHEN ( CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END) ELSE 0 END AS [202603],
            CASE WHEN ( CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END) ELSE 0 END AS [202604],
            CASE WHEN ( CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END) ELSE 0 END AS [202605],
            CASE WHEN ( CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END) ELSE 0 END AS [202606],
            CASE WHEN ( CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END) ELSE 0 END AS [202607],
            CASE WHEN ( CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END) ELSE 0 END AS [202608],
            CASE WHEN ( CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END) ELSE 0 END AS [202609],
            CASE WHEN ( CASE WHEN @Mes>=10  THEN ISNULL(B.[202610],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=10  THEN ISNULL(A.[202610],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=10  THEN ISNULL(B.[202610],0) ELSE 0 END) ELSE 0 END AS [202610],
            CASE WHEN ( CASE WHEN @Mes>=11  THEN ISNULL(B.[202611],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=11  THEN ISNULL(A.[202611],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=11  THEN ISNULL(B.[202611],0) ELSE 0 END) ELSE 0 END AS [202611],
            CASE WHEN ( CASE WHEN @Mes>=12  THEN ISNULL(B.[202612],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=12  THEN ISNULL(A.[202612],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=12  THEN ISNULL(B.[202612],0) ELSE 0 END) ELSE 0 END AS [202612]
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est.estandar_01
            WHEN 2  THEN est.estandar_02
            WHEN 3  THEN est.estandar_03
            WHEN 4  THEN est.estandar_04
            WHEN 5  THEN est.estandar_05
            WHEN 6  THEN est.estandar_06
            WHEN 7  THEN est.estandar_07
            WHEN 8  THEN est.estandar_08
            WHEN 9  THEN est.estandar_09
            WHEN 10 THEN est.estandar_10
            WHEN 11 THEN est.estandar_11
            WHEN 12 THEN est.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.anio = cen.anio
    WHERE est.indicador = 'Porcentaje de Intervenciones de Alta Complejidad' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE     (A.Red IN ('ANCASH', 'APURIMAC', 'AREQUIPA', 'AYACUCHO', 'CAJAMARCA', 'CUSCO', 'HUANCAVELICA', 'HUANUCO', 'HUARAZ', 'ICA', 'RED JAEN', 'INCOR', 'JULIACA', 
                      'JUNIN', 'LA LIBERTAD', 'LAMBAYEQUE', 'LORETO', 'MADRE DE DIOS', 'MOQUEGUA', 'MOYOBAMBA', 'PASCO', 'PIURA', 'PUNO', 'REBAGLIATI', 'SABOGAL', 'TACNA', 
                      'TARAPOTO', 'TUMBES', 'RED PRESTACIONAL ALMENARA', 'RED PRESTACIONAL REBAGLIATI', 'RED PRESTACIONAL SABOGAL'))
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_IMenor
def queryQx_IMenorRep(db:Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (
          SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
                   SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
                   SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
           FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
           WHERE      (Variable IN ('Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'))
           GROUP BY Red, Centro, nivel, codcentro, Año
),
X AS (SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
                   SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
                   SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
           FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
           WHERE      (Variable IN ('Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                                  'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                                  'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'))
           GROUP BY Red, Centro, nivel, codcentro, Año
),
CEN AS (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     Variable IN ('Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento', 
                      'Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                      'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                      'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'))
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 1.2 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(X.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(X.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN X.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / X.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN X.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / X.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN X.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / X.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN X.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / X.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN X.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / X.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN X.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / X.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN X.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / X.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN X.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / X.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN X.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / X.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN X.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / X.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN X.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / X.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN X.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / X.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN X ON CEN.codcentro = X.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est.estandar_01
            WHEN 2  THEN est.estandar_02
            WHEN 3  THEN est.estandar_03
            WHEN 4  THEN est.estandar_04
            WHEN 5  THEN est.estandar_05
            WHEN 6  THEN est.estandar_06
            WHEN 7  THEN est.estandar_07
            WHEN 8  THEN est.estandar_08
            WHEN 9  THEN est.estandar_09
            WHEN 10 THEN est.estandar_10
            WHEN 11 THEN est.estandar_11
            WHEN 12 THEN est.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.anio = cen.anio
    WHERE est.indicador = 'Porcentaje de Intervenciones Menores' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_IntSusp
def queryQx_IntSuspRep(db:Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (
      SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
      [202609], [202610], [202611], [202612], Variable
      FROM  pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE Variable IN ('Centro Quirúrgico - Operaciones Suspendidas')),
B AS (
      SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
      [202609], [202610], [202611], [202612], Variable
      FROM  pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
      WHERE Variable IN ('Centro Quirúrgico - Intervenc.Quirurgicas Programadas')
),
CEN AS (
      SELECT DISTINCT Red, codcentro, Centro
      FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE     variable IN ('Centro Quirúrgico - Operaciones Suspendidas')
      UNION
      SELECT DISTINCT Red, codcentro, Centro
      FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE     variable IN ('Centro Quirúrgico - Intervenc.Quirurgicas Programadas')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 1.1 AS [% Acept],
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE NULL END AS Total,
    CASE WHEN @Mes >= 1  THEN CASE WHEN B.[202601] <> 0 THEN (ISNULL(A.[202601], 0) * 1.00) / B.[202601] ELSE NULL END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  THEN CASE WHEN B.[202602] <> 0 THEN (ISNULL(A.[202602], 0) * 1.00) / B.[202602] ELSE NULL END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  THEN CASE WHEN B.[202603] <> 0 THEN (ISNULL(A.[202603], 0) * 1.00) / B.[202603] ELSE NULL END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  THEN CASE WHEN B.[202604] <> 0 THEN (ISNULL(A.[202604], 0) * 1.00) / B.[202604] ELSE NULL END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  THEN CASE WHEN B.[202605] <> 0 THEN (ISNULL(A.[202605], 0) * 1.00) / B.[202605] ELSE NULL END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  THEN CASE WHEN B.[202606] <> 0 THEN (ISNULL(A.[202606], 0) * 1.00) / B.[202606] ELSE NULL END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  THEN CASE WHEN B.[202607] <> 0 THEN (ISNULL(A.[202607], 0) * 1.00) / B.[202607] ELSE NULL END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  THEN CASE WHEN B.[202608] <> 0 THEN (ISNULL(A.[202608], 0) * 1.00) / B.[202608] ELSE NULL END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  THEN CASE WHEN B.[202609] <> 0 THEN (ISNULL(A.[202609], 0) * 1.00) / B.[202609] ELSE NULL END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 THEN CASE WHEN B.[202610] <> 0 THEN (ISNULL(A.[202610], 0) * 1.00) / B.[202610] ELSE NULL END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 THEN CASE WHEN B.[202611] <> 0 THEN (ISNULL(A.[202611], 0) * 1.00) / B.[202611] ELSE NULL END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 THEN CASE WHEN B.[202612] <> 0 THEN (ISNULL(A.[202612], 0) * 1.00) / B.[202612] ELSE NULL END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est.estandar_01
            WHEN 2  THEN est.estandar_02
            WHEN 3  THEN est.estandar_03
            WHEN 4  THEN est.estandar_04
            WHEN 5  THEN est.estandar_05
            WHEN 6  THEN est.estandar_06
            WHEN 7  THEN est.estandar_07
            WHEN 8  THEN est.estandar_08
            WHEN 9  THEN est.estandar_09
            WHEN 10 THEN est.estandar_10
            WHEN 11 THEN est.estandar_11
            WHEN 12 THEN est.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.anio = cen.anio
    WHERE est.indicador = 'Porcentaje de Operaciones Suspendidas' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Qx_RendSO
def queryQx_RendSORep(db:Session, periodo:str):
    try:
        query = """
SET NOCOUNT ON;
DECLARE @Periodo CHAR(6) = :periodo;         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (
        SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
                       SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
                       SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
        FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
        WHERE      (Variable IN ('Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                       'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                       'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'))
        GROUP BY Red, Centro, nivel, codcentro, Año
),
B AS (
        SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                     [202609], [202610], [202611], [202612], Variable
        FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
        WHERE      Variable IN ('Centro Quirúrgico -  Salas Quirúrgicas Funcionales')
),
CEN AS (
        SELECT DISTINCT Red, codcentro, Centro
        FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
        WHERE     Variable IN ('Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                              'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                              'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento', 
                              'Centro Quirúrgico -  Salas Quirúrgicas Funcionales')
)
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.9 AS [% Acept],
    CASE WHEN (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00  / (
            CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN ( CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END) ELSE 0 END AS [202601],
    CASE WHEN ( CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END) ELSE 0 END AS [202602],
    CASE WHEN ( CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END) ELSE 0 END AS [202603],
    CASE WHEN ( CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END) ELSE 0 END AS [202604],
    CASE WHEN ( CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END) ELSE 0 END AS [202605],
    CASE WHEN ( CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END) ELSE 0 END AS [202606],
    CASE WHEN ( CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END) ELSE 0 END AS [202607],
    CASE WHEN ( CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END) ELSE 0 END AS [202608],
    CASE WHEN ( CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END) ELSE 0 END AS [202609],
    CASE WHEN ( CASE WHEN @Mes>=10  THEN ISNULL(B.[202610],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=10  THEN ISNULL(A.[202610],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=10  THEN ISNULL(B.[202610],0) ELSE 0 END) ELSE 0 END AS [202610],
    CASE WHEN ( CASE WHEN @Mes>=11  THEN ISNULL(B.[202611],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=11  THEN ISNULL(A.[202611],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=11  THEN ISNULL(B.[202611],0) ELSE 0 END) ELSE 0 END AS [202611],
    CASE WHEN ( CASE WHEN @Mes>=12  THEN ISNULL(B.[202612],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=12  THEN ISNULL(A.[202612],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=12  THEN ISNULL(B.[202612],0) ELSE 0 END) ELSE 0 END AS [202612]
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est.estandar_01
            WHEN 2  THEN est.estandar_02
            WHEN 3  THEN est.estandar_03
            WHEN 4  THEN est.estandar_04
            WHEN 5  THEN est.estandar_05
            WHEN 6  THEN est.estandar_06
            WHEN 7  THEN est.estandar_07
            WHEN 8  THEN est.estandar_08
            WHEN 9  THEN est.estandar_09
            WHEN 10 THEN est.estandar_10
            WHEN 11 THEN est.estandar_11
            WHEN 12 THEN est.estandar_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.anio = cen.anio
    WHERE est.indicador = 'Rendimiento de Sala de Operaciones' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
"""
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def queryDeleteFila(db: Session, tabla: str, id: int):
    try:
        query = f"DELETE FROM pentahodev_prueba_01.dbo.{tabla} WHERE id = :id"
        result = db.execute(text(query), {"id": id})
        db.commit()
        return {"message": "Fila eliminada correctamente", "rows_affected": result.rowcount}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
