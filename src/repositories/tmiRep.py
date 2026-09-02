from sqlalchemy.orm import decl_base
from sqlalchemy.orm import decl_base
from sqlalchemy.orm import decl_base
from src.dtos.tmiDto import estandaresDto
from src.db.databaseConexion import SessionLocal
from fastapi import HTTPException
from sqlalchemy import text


def queryEstandares(db: SessionLocal):
    try:
        query = f"""
        SElECT est.*
        FROM [pentahodev_prueba].[dbo].[estandares] est
        """
        result = db.execute(text(query))
        return result.fetchall()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryEstandaresByCentro(db: SessionLocal, codcentro:str):
    try:
        query = f"""
          SElECT est.*, cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.nivel_estandar
          FROM [pentahodev_prueba].[dbo].[estandares] est
          JOIN [pentahodev_prueba].[dbo].[centros_tmi] cen ON est.nivel_estandar_centro = cen.nivel_estandar
          WHERE cen.codcentro = :codcentro
        """
        result = db.execute(text(query), {"codcentro": codcentro})
        return result.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryUpdateEstandares(db: SessionLocal, dto:estandaresDto):
    try:
        query = f"""
        USE [pentahodev_prueba]
        GO

        UPDATE [dbo].[estandares]
          SET [id] = :id
          ,[orden_indicador] = :orden_indicador
          ,[codigo_unico] = :codigo_unico
          ,[tipo] = :tipo
          ,[indicador] = :indicador
          ,[nivel_centro] = :nivel_centro
          ,[tipo_centro] = :tipo_centro
          ,[nivel_estandar_centro] = :nivel_estandar_centro
          ,[estandar] = :estandar
          ,[acept] = :acept
          ,[aceptmenos] = :aceptmenos
        WHERE id = :id
        """

        result = db.execute(text(query), {"dto": dto})
        db.commit()
        return result.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def queryDropVIstas(db: SessionLocal):
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

def queryCreacionCentrosVariables(db: SessionLocal):
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

def queryCreacionVistasCE(db: SessionLocal):
    try:
        query = f"""

        """
        result = db.execute(text(query))
        db.commit()
        return result.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))











