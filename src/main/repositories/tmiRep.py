from datetime import datetime
from sqlalchemy.orm import Session
from src.main.dtos.tmiDto import estandarTmiDto
from src.main.dtos.tmiDto import centroTmiDto
from fastapi import HTTPException
from sqlalchemy import text

# consultar estandares para el periodo actual
def queryEstandares(db: Session, periodo:str):
    try:
        query = f"""
        SElECT est.*
        FROM [pentahodev_prueba].[dbo].[tmi_estandar] est
        WHERE periodo = :periodo
        """
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

### insertar estandares para el periodo actual de periodo anterior
def queryInsertEstandaresPeriodo(db: Session, periodo:str,periodoAnterior:str):
    try:
        query = f"""
        INSERT INTO [pentahodev_prueba].[dbo].[tmi_estandar]
        (orden_indicador, codigo_unico, tipo, indicador, nivel_centro, tipo_centro, nivel_estandar_centro, estandar, acept, aceptmenos, periodo)
        SELECT orden_indicador, codigo_unico, tipo, indicador, nivel_centro, tipo_centro, nivel_estandar_centro, estandar, acept, aceptmenos, :periodo
        FROM [pentahodev_prueba].[dbo].[tmi_estandar]
        WHERE periodo = :periodoAnterior
        """
        result = db.execute(text(query), {"periodoAnterior": periodoAnterior, "periodo": periodo})
        db.commit()
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

### consultar estandares por centro
def queryEstandaresByCentro(db: Session, codcentro:str, periodo:str):
    try:
        query = f"""
          SElECT est.*, cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.nivel_estandar, cen.periodo
          FROM [pentahodev_prueba].[dbo].[tmi_estandar] est
          JOIN [pentahodev_prueba].[dbo].[tmi_centro] cen ON est.nivel_estandar_centro = cen.nivel_estandar
          WHERE cen.codcentro = :codcentro AND est.periodo = :periodo
        """
        result = db.execute(text(query), {"codcentro": codcentro, "periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## actualizar estandares
def queryUpdateEstandares(db: Session, dto: estandarTmiDto):
    try:
        query = """
        UPDATE [dbo].[tmi_estandar]
          SET [orden_indicador] = :orden_indicador
          , [codigo_unico] = :codigo_unico
          , [tipo] = :tipo
          , [indicador] = :indicador
          , [nivel_centro] = :nivel_centro
          , [tipo_centro] = :tipo_centro
          , [nivel_estandar_centro] = :nivel_estandar_centro
          , [estandar] = :estandar
          , [acept] = :acept
          , [aceptmenos] = :aceptmenos
          , [periodo]  = :periodo
        WHERE id = :id AND periodo = :periodo
        """

        params = dto.model_dump() if hasattr(dto, "model_dump") else dto.dict()
        result = db.execute(text(query), params)
        db.commit()
        return {"message": "Estandar actualizado correctamente", "rows_affected": result.rowcount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

### consultar centros_tmi 
def queryCentrosTMI(db: Session, periodo:str):
    try:
        query = f"""
        SElECT * FROM [pentahodev_prueba].[dbo].[tmi_centro]
        WHERE periodo = :periodo
        """
        result = db.execute(text(query), {"periodo": periodo})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

 
### insertar centros_tmi para el periodo actual de periodo anterior
def queryInsertCentrosTMI(db: Session, periodo:str,periodoAnterior:str):
    try:
        query = f"""
        INSERT INTO [pentahodev_prueba].[dbo].[tmi_centro]
        (red, orden, orden_tipo, codcentro, tipo, nivel, nivel_estandar, centro, periodo) 
        SELECT red, orden, orden_tipo, codcentro, tipo, nivel, nivel_estandar, centro, :periodo
        FROM [pentahodev_prueba].[dbo].[tmi_centro]
        WHERE periodo = :periodoAnterior
        """
        result = db.execute(text(query), {"periodoAnterior": periodoAnterior, "periodo": periodo})
        db.commit()
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

### actualizar centros_tmi 
def queryUpdateCentrosTMI(db: Session, dto:centroTmiDto):
    try:
        query = f"""
        UPDATE [dbo].[centros_tmi]
            SET [id] = :id
            ,[red] = :red
            ,[orden] = :orden
            ,[orden_tipo] = :orden_tipo
            ,[codcentro] = :codcentro
            ,[tipo] = :tipo
            ,[nivel] = :nivel
            ,[nivel_estandar] = :nivel_estandar
            ,[centro] = :centro
            ,[estado] = :estado
            ,[periodo] = :periodo
        WHERE codcentro = :codcentro AND periodo = :periodo
        """
        params = dto.model_dump() if hasattr(dto, "model_dump") else dto.dict()
        result = db.execute(text(query), params)
        db.commit()
        return {"message": "Estandar actualizado correctamente", "rows_affected": result.rowcount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def formarFechaTMI(fecha:str) -> str:
    try:
        return fecha.split('-')[0] + fecha.split('-')[1]
    except Exception as e:
        return ""

def queryDiaEjecucion(db:Session, anio:int):
    try:
        query = f"""
        SELECT dia
        FROM [pentahodev_prueba].[dbo].[cierre]
        WHERE año = :anio
        """
        result = db.execute(text(query), {"anio": anio})
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def condicionEjecucion(db:Session):
    try:
        diaActual = datetime.now().day
        if diaActual == queryDiaEjecucion(db, datetime.now().year):
            queryDropVIstas(db)
            queryCreacionCentrosVariables(db)
            return True
        return False
    except Exception as e:
        return False




### consulta concentracion de consultas
def queryCEConcent(db: Session):
    try:
        query = f"""
        SElECT cen.id, est.tipo AS tipo_indicador, est.indicador , est.estandar, est.acept, est.aceptmenos, cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.nivel_estandar
        FROM [pentahodev_prueba].[dbo].[tmi_estandar] est
        JOIN [pentahodev_prueba].[dbo].[tmi_centro] cen ON est.nivel_estandar_centro = cen.nivel_estandar
        WHERE est.indicador = 'Concentracion de Consultas' AND est.periodo = '202608'
        """
        result = db.execute(text(query))
        db.commit()
        return [dict(row) for row in result.mappings()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryDropVIstas(db: Session):
    try:
        query = f"""
DROP VIEW TMI_CENTROS_CE_Concent
DROP VIEW TMI_CENTROS_CE_GCHProg
DROP VIEW TMI_CENTROS_CE_Recetas
DROP VIEW TMI_CENTROS_CE_RHrMedico
DROP VIEW TMI_CENTROS_Em_PrioI_II
DROP VIEW TMI_CENTROS_Em_PrioIV_V
DROP VIEW TMI_CENTROS_H_Estancias
DROP VIEW TMI_CENTROS_H_ISust
DROP VIEW TMI_CENTROS_H_OCama
DROP VIEW TMI_CENTROS_H_RCama
DROP VIEW TMI_CENTROS_H_TBMHosp
DROP VIEW TMI_CENTROS_O_Concent
DROP VIEW TMI_CENTROS_O_GCHOdon
DROP VIEW TMI_CENTROS_O_HrOdont
DROP VIEW TMI_CENTROS_O_NTOdontS
DROP VIEW TMI_CENTROS_Qx_GCHProg
DROP VIEW TMI_CENTROS_Qx_HTCesareas
DROP VIEW TMI_CENTROS_Qx_IAlta
DROP VIEW TMI_CENTROS_Qx_IMenor
DROP VIEW TMI_CENTROS_Qx_IntSusp
DROP VIEW TMI_CENTROS_Qx_RendSO
DROP VIEW CE_Concent
DROP VIEW CE_GCHProg
DROP VIEW CE_Recetas
DROP VIEW CE_RHrMedico
DROP VIEW Em_PrioI_II
DROP VIEW Em_PrioIV_V
DROP VIEW H_Estancias
DROP VIEW H_ISust
DROP VIEW H_OCama
DROP VIEW H_RCama
DROP VIEW H_TBMHosp
DROP VIEW O_Concent
DROP VIEW O_GCHOdon
DROP VIEW O_HrOdont
DROP VIEW O_NTOdontS
DROP VIEW Qx_GCHProg
DROP VIEW Qx_HTCesareas
DROP VIEW Qx_IAlta
DROP VIEW Qx_IMenor
DROP VIEW Qx_IntSusp
DROP VIEW Qx_RendSO
DROP VIEW TMI_PUNTAJES_CENTRO_INDICADORES
DROP VIEW TMI_Qx_HTCesareas_bi
        """
        result = db.execute(text(query))
        db.commit()
        return result.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryCreacionCentrosVariables(db: Session):
    try:
        query = f"""

CREATE VIEW TMI_CENTROS_CE_Concent
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Consultas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Consultantes al Establecimiento')
go

CREATE VIEW TMI_CENTROS_CE_GCHProg
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Horas Médicas Efectivas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Horas Médicas Programadas')

go
CREATE VIEW TMI_CENTROS_CE_Recetas
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Actividades Intermedias - Recetas Despachadas de C. E')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Consultas')
go
CREATE VIEW TMI_CENTROS_CE_RHrMedico
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Consultas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Horas Médicas Efectivas')
go

CREATE VIEW TMI_CENTROS_Em_PrioI_II
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Emergencia - Prioridad I', 'Emergencia - Prioridad II', 'Emergencia - Total de Atenciones'))
go
CREATE VIEW TMI_CENTROS_Em_PrioIV_V
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Emergencia - Prioridad IV', 'Emergencia - Prioridad V', 'Emergencia - Total de Atenciones'))
go
CREATE VIEW TMI_CENTROS_H_Estancias
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Estancias')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Egresos')
go
CREATE VIEW TMI_CENTROS_H_ISust
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Hospitalizacion - Días Cama Disponible', 'Hospitalizacion - Pacientes Días', 'Hospitalizacion - Egresos'))
go
CREATE VIEW TMI_CENTROS_H_OCama
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Pacientes Días')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Días Cama Disponible')
go
CREATE VIEW TMI_CENTROS_H_RCama
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Hospitalizacion - Egresos', 'Hospitalizacion -  Camas Hospitalarias'))
go
CREATE VIEW TMI_CENTROS_H_TBMHosp
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Defunciones después de 48 horas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Egresos')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Defunciones antes de 48 horas')
go
CREATE VIEW TMI_CENTROS_O_Concent
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Odontología - Sesiones Odontológicas', 'Odontología - Consultantes de Odontología'))
go
CREATE VIEW TMI_CENTROS_O_GCHOdon
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Odontología - Horas Odontológicas Efectivas', 'Odontología - Horas Odontológicas Programadas'))
go
CREATE VIEW TMI_CENTROS_O_HrOdont
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Odontología - Sesiones Odontológicas', 'Odontología - Horas Odontológicas Efectivas'))
go
CREATE VIEW TMI_CENTROS_O_NTOdontS
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Odontología - Trabajos Odontológicos', 'Odontología - Diagnóstico por imágenes', 'Odontología - Procedimientos Especiales')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Odontología - Sesiones Odontológicas')
go
CREATE VIEW TMI_CENTROS_Qx_GCHProg
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Centro Quirúrgico - Horas Uso de Sala', 'Centro Quirúrgico - Horas Programadas Intervenc.Quirurgicas'))
go
CREATE VIEW TMI_CENTROS_Qx_HTCesareas
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Centro Obstétrico - Cesáreas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Centro Obstétrico - Total de Partos')
go
CREATE VIEW TMI_CENTROS_Qx_IAlta
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 'Centro Quirúrgico - Cirugías sin clasificación de complejidad', 
                      'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 
                      'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 
                      'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'))
go
CREATE VIEW TMI_CENTROS_Qx_IMenor
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento', 
                      'Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                      'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                      'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'))
go
CREATE VIEW TMI_CENTROS_Qx_IntSusp
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Centro Quirúrgico - Operaciones Suspendidas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Centro Quirúrgico - Intervenc.Quirurgicas Programadas')
go
CREATE VIEW TMI_CENTROS_Qx_RendSO
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                      'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                      'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento', 
                      'Centro Quirúrgico -  Salas Quirúrgicas Funcionales'))
        """
        result = db.execute(text(query))
        db.commit()
        return result.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryCreacionVistasCE(db: Session):
    try:
        query = f"""

        """
        result = db.execute(text(query))
        db.commit()
        return result.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))











