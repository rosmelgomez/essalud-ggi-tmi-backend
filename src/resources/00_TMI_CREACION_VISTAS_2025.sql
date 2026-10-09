
USE pentahodev_prueba

/*0- ELIMINACION DE VISTAS*/
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



/*1- CREACION DE CENTROS POR VARIABLE */
CREATE VIEW TMI_CENTROS_CE_Concent
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Consultas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Consultantes al Establecimiento')
go

CREATE VIEW TMI_CENTROS_CE_GCHProg
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Horas Médicas Efectivas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Horas Médicas Programadas')

go
CREATE VIEW TMI_CENTROS_CE_Recetas
AS
SELECT DISTINCT Red, codcentro, Centro
FROM        pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Actividades Intermedias - Recetas Despachadas de C. E')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Consultas')
go
CREATE VIEW TMI_CENTROS_CE_RHrMedico
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Consultas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Horas Médicas Efectivas')
go

CREATE VIEW TMI_CENTROS_Em_PrioI_II
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Emergencia - Prioridad I', 'Emergencia - Prioridad II', 'Emergencia - Total de Atenciones'))
go
CREATE VIEW TMI_CENTROS_Em_PrioIV_V
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Emergencia - Prioridad IV', 'Emergencia - Prioridad V', 'Emergencia - Total de Atenciones'))
go
CREATE VIEW TMI_CENTROS_H_Estancias
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Estancias')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Egresos')
go
CREATE VIEW TMI_CENTROS_H_ISust
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Hospitalizacion - Días Cama Disponible', 'Hospitalizacion - Pacientes Días', 'Hospitalizacion - Egresos'))
go
CREATE VIEW TMI_CENTROS_H_OCama
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Pacientes Días')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Días Cama Disponible')
go
CREATE VIEW TMI_CENTROS_H_RCama
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Hospitalizacion - Egresos', 'Hospitalizacion -  Camas Hospitalarias'))
go
CREATE VIEW TMI_CENTROS_H_TBMHosp
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Defunciones después de 48 horas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Egresos')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Defunciones antes de 48 horas')
go
CREATE VIEW TMI_CENTROS_O_Concent
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Odontología - Sesiones Odontológicas', 'Odontología - Consultantes de Odontología'))
go
CREATE VIEW TMI_CENTROS_O_GCHOdon
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Odontología - Horas Odontológicas Efectivas', 'Odontología - Horas Odontológicas Programadas'))
go
CREATE VIEW TMI_CENTROS_O_HrOdont
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Odontología - Sesiones Odontológicas', 'Odontología - Horas Odontológicas Efectivas'))
go
CREATE VIEW TMI_CENTROS_O_NTOdontS
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Odontología - Trabajos Odontológicos', 'Odontología - Diagnóstico por imágenes', 'Odontología - Procedimientos Especiales')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Odontología - Sesiones Odontológicas')
go
CREATE VIEW TMI_CENTROS_Qx_GCHProg
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Centro Quirúrgico - Horas Uso de Sala', 'Centro Quirúrgico - Horas Programadas Intervenc.Quirurgicas'))
go
CREATE VIEW TMI_CENTROS_Qx_HTCesareas
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Centro Obstétrico - Cesáreas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Centro Obstétrico - Total de Partos')
go
CREATE VIEW TMI_CENTROS_Qx_IAlta
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 'Centro Quirúrgico - Cirugías sin clasificación de complejidad', 
                      'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 
                      'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 
                      'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'))
go
CREATE VIEW TMI_CENTROS_Qx_IMenor
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento', 
                      'Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                      'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                      'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'))
go
CREATE VIEW TMI_CENTROS_Qx_IntSusp
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Centro Quirúrgico - Operaciones Suspendidas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Centro Quirúrgico - Intervenc.Quirurgicas Programadas')
go
CREATE VIEW TMI_CENTROS_Qx_RendSO
AS
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                      'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                      'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento', 
                      'Centro Quirúrgico -  Salas Quirúrgicas Funcionales'))
  
                      
/*2- CREACION DE VISTAS CON DATOS FUENTE*/
CREATE VIEW CE_Concent
AS
SELECT DISTINCT 
  D.id AS ORDEN, D.red, D.codcentro, D.centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], CASE WHEN A.[Total] = 0 OR
  B.[Total] = 0 THEN 0 ELSE (A.[Total] * 1.00) / B.[Total] END AS Total, 
  CASE WHEN A.[202601] = 0 OR B.[202601] = 0 THEN 0 ELSE (A.[202601] * 1.00) / B.[202601] END AS [202601], 
  CASE WHEN A.[202602] = 0 OR B.[202602] = 0 THEN 0 ELSE ((A.[202601] + A.[202602]) * 1.00) / (B.[202601] + B.[202602]) END AS [202602], 
  CASE WHEN A.[202603] = 0 OR B.[202603] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603]) * 1.00) / (B.[202601] + B.[202602] + B.[202603]) END AS [202603], 
  CASE WHEN A.[202604] = 0 OR B.[202604] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604]) END AS [202604], 
  CASE WHEN A.[202605] = 0 OR B.[202605] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605]) END AS [202605], 
  CASE WHEN A.[202606] = 0 OR B.[202606] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606]) END AS [202606], 
  CASE WHEN A.[202607] = 0 OR B.[202607] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607]) END AS [202607], 
  CASE WHEN A.[202608] = 0 OR B.[202608] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608]) END AS [202608], 
  CASE WHEN A.[202609] = 0 OR B.[202609] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609]) END AS [202609], 
  CASE WHEN A.[202610] = 0 OR B.[202610] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610]) END AS [202610], 
  CASE WHEN A.[202611] = 0 OR B.[202611] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611]) END AS [202611], 
  CASE WHEN A.[202612] = 0 OR B.[202612] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]+ A.[202612]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611] + B.[202612]) END AS [202612]
FROM (
      SELECT DISTINCT Red, codcentro, Centro
      FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE     variable IN ('Consulta Externa - Consultas')
      UNION
      SELECT DISTINCT Red, codcentro, Centro
      FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE     variable IN ('Consulta Externa - Consultantes al Establecimiento')) AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM       pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Consulta Externa - Consultas'))) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM       pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      (Variable IN ('Consulta Externa - Consultantes al Establecimiento'))) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept ,cen.red, cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_nivel est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.nivel_centro = cen.nivel AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Concentracion de Consultas' and est.periodo = '202607') AS D ON CEN.codcentro = D.codcentro
go
/*--ESTE VIEW NO SIRVE
CREATE VIEW CE_GCHProg
AS
SELECT DISTINCT 
                      D.ID AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.NIVEL, D.TIPO, D.GCHP_Estandar AS Estandar, D.[GCHP_%Acept] AS [% Acept], 
                      CASE WHEN A.[Total] <> 0 OR B.[Total] <> 0 THEN (A.[Total] * 1.00) / B.[Total] ELSE 0 END AS Total, 
                      CASE WHEN A.[202601] <> 0 OR
                      B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END AS [202601], CASE WHEN A.[202602] <> 0 OR
                      B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END AS [202602], CASE WHEN A.[202603] <> 0 OR
                      B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END AS [202603], CASE WHEN A.[202604] <> 0 OR
                      B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END AS [202604], CASE WHEN A.[202605] <> 0 OR
                      B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END AS [202605], CASE WHEN A.[202606] <> 0 OR
                      B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END AS [202606], CASE WHEN A.[202607] <> 0 OR
                      B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END AS [202607], CASE WHEN A.[202608] <> 0 OR
                      B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END AS [202608], CASE WHEN A.[202609] <> 0 OR
                      B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END AS [202609], CASE WHEN A.[202610] <> 0 OR
                      B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END AS [202610], CASE WHEN A.[202611] <> 0 OR
                      B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END AS [202611], CASE WHEN A.[202612] <> 0 OR
                      B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END AS [202612]
FROM         dbo.TMI_CENTROS_CE_GCHProg AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Consulta Externa - Horas Médicas Efectivas'))) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      (Variable IN ('Consulta Externa - Horas Médicas Programadas'))) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SELECT     Red, ORDEN, ORDEN_TIPO, codcentro, TIPO, NIVEL, NIVEL_ESTANDAR, CENTRO, ESTADO, CE_Estandar, [CE_%Acept], [CE_%Aceptmenos], 
                                                   RHM_Estandar, [RHM_%Acept], [RHM_%Aceptmenos], GCHP_Estandar, [GCHP_%Acept], [GCHP_%Aceptmenos], PRC_Estandar, [PRC_%Acept], 
                                                   [PRC_%Aceptmenos], PE_Estandar, [PE_%Acept], [PE_%Aceptmenos], POC_Estandar, [POC_%Acept], [POC_%Aceptmenos], IS_Estandar, [IS_%Acept], 
                                                   [IS_%Aceptmenos], RC_Estandar, [RC_%Acept], [RC_%Aceptmenos], TNMH_Estandar, [TNMH_%Acept], [TNMH_%Aceptmenos], PIM_Estandar, 
                                                   [PIM_%Acept], [PIM_%Aceptmenos], PIAC_Estandar, [PIAC_%Acept], [PIAC_%Aceptmenos], PHQE_Estandar, [PHQE_%Acept], [PHQE_%Aceptmenos], 
                                                   RSO_Estandar, [RSO_%Acept], [RSO_%Aceptmenos], POS_Estandar, [POS_%Acept], [POS_%Aceptmenos], TC_Estandar, [TC_%Acept], [TC_%Aceptmenos], 
                                                   PIV_Estandar, [PIV_%Acept], [PIV_%Aceptmenos], PII_Estandar, [PII_%Acept], [PII_%Aceptmenos], CSO_Estandar, [CSO_%Acept], [CSO_%Aceptmenos], 
                                                   RHO_Estandar, [RHO_%Acept], [RHO_%Aceptmenos], GCHO_Estandar, [GCHO_%Acept], [GCHO_%Aceptmenos], NTOS_Estandar, [NTOS_%Acept], 
                                                   [NTOS_%Aceptmenos], ID
                            FROM          dbo.TMI_ESTANDARES_D) AS D ON CEN.codcentro = D.codcentro
go*/
--09.05.2026
/*Grado de Cumplimiento de Horas Programadas*/
CREATE VIEW CE_GCHProg
AS
SELECT DISTINCT 
                      D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria  AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
                      CASE WHEN B.[Total] <> 0 THEN (A.[Total] * 1.00) / B.[Total] ELSE 0 END AS Total, 
                      CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END AS [202601], 
                      CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END AS [202602], 
                      CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END AS [202603], 
                      CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END AS [202604], 
                      CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END AS [202605], 
                      CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END AS [202606], 
                      CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END AS [202607], 
                      CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END AS [202608], 
                      CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END AS [202609], 
                      CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END AS [202610], 
                      CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END AS [202611], 
                      CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END AS [202612]
FROM (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Horas Médicas Efectivas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Horas Médicas Programadas')) AS CEN 
LEFT OUTER JOIN
				  (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
										   [202609], [202610], [202611], [202612], Variable
					FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
					WHERE      (Variable IN ('Consulta Externa - Horas Médicas Efectivas'))) AS A ON CEN.codcentro = A.codcentro 
LEFT OUTER JOIN
                  (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                           [202609], [202610], [202611], [202612], Variable
                    FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                    WHERE      (Variable IN ('Consulta Externa - Horas Médicas Programadas'))) AS B ON CEN.codcentro = B.codcentro 
LEFT OUTER JOIN
                  (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
                   FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
                   JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                   WHERE est.indicador = 'Grado de Cumplimiento de Horas Programadas' AND est.periodo= '202608') AS D ON CEN.codcentro = D.codcentro
go

/* Promedio de Recetas por Consultas*/
CREATE VIEW CE_Recetas
AS
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept],

    -- TOTAL
    ISNULL((ISNULL(A.[Total],0) * 1.00) / NULLIF(ISNULL(B.[Total],0),0),0) AS Total,

    -- MESES INDIVIDUALES
    ISNULL((ISNULL(A.[202601],0) * 1.00) / NULLIF(ISNULL(B.[202601],0),0),0) AS [202601],
    ISNULL((ISNULL(A.[202602],0) * 1.00) / NULLIF(ISNULL(B.[202602],0),0),0) AS [202602],
    ISNULL((ISNULL(A.[202603],0) * 1.00) / NULLIF(ISNULL(B.[202603],0),0),0) AS [202603],
    ISNULL((ISNULL(A.[202604],0) * 1.00) / NULLIF(ISNULL(B.[202604],0),0),0) AS [202604],
    ISNULL((ISNULL(A.[202605],0) * 1.00) / NULLIF(ISNULL(B.[202605],0),0),0) AS [202605],
    ISNULL((ISNULL(A.[202606],0) * 1.00) / NULLIF(ISNULL(B.[202606],0),0),0) AS [202606],
    ISNULL((ISNULL(A.[202607],0) * 1.00) / NULLIF(ISNULL(B.[202607],0),0),0) AS [202607],
    ISNULL((ISNULL(A.[202608],0) * 1.00) / NULLIF(ISNULL(B.[202608],0),0),0) AS [202608],
    ISNULL((ISNULL(A.[202609],0) * 1.00) / NULLIF(ISNULL(B.[202609],0),0),0) AS [202609],
    ISNULL((ISNULL(A.[202610],0) * 1.00) / NULLIF(ISNULL(B.[202610],0),0),0) AS [202610],
    ISNULL((ISNULL(A.[202611],0) * 1.00) / NULLIF(ISNULL(B.[202611],0),0),0) AS [202611],
    ISNULL((ISNULL(A.[202612],0) * 1.00) / NULLIF(ISNULL(B.[202612],0),0),0) AS [202612]

FROM (
SELECT DISTINCT Red, codcentro, Centro
FROM        pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Actividades Intermedias - Recetas Despachadas de C. E')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Consultas')) CEN

LEFT JOIN (
    SELECT *
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Actividades Intermedias - Recetas Despachadas de C. E') A ON CEN.codcentro = A.codcentro
LEFT JOIN (
    SELECT *
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Consulta Externa - Consultas') B ON CEN.codcentro = B.codcentro
LEFT JOIN (
    SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
    FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
    WHERE est.indicador = 'Promedio de Recetas por Consultas' AND est.periodo= '202608') AS D ON CEN.codcentro = D.codcentro


/*SELECT DISTINCT 
                      D.ID AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.NIVEL, D.TIPO, D.PRC_Estandar AS Estandar, D.[PRC_%Acept] AS [% Acept], CASE WHEN A.[Total] <> 0 OR
                      B.[Total] <> 0 THEN (A.[Total] * 1.00) / B.[Total] ELSE 0 END AS Total, CASE WHEN A.[202601] <> 0 OR
                      B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END AS [202601], CASE WHEN A.[202602] <> 0 OR
                      B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END AS [202602], CASE WHEN A.[202603] <> 0 OR
                      B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END AS [202603], CASE WHEN A.[202604] <> 0 OR
                      B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END AS [202604], CASE WHEN A.[202605] <> 0 OR
                      B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END AS [202605], CASE WHEN A.[202606] <> 0 OR
                      B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END AS [202606], CASE WHEN A.[202607] <> 0 OR
                      B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END AS [202607], CASE WHEN A.[202608] <> 0 OR
                      B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END AS [202608], CASE WHEN A.[202609] <> 0 OR
                      B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END AS [202609], CASE WHEN A.[202610] <> 0 OR
                      B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END AS [202610], CASE WHEN A.[202611] <> 0 OR
                      B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END AS [202611], CASE WHEN A.[202612] <> 0 OR
                      B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END AS [202612]
FROM         dbo.TMI_CENTROS_CE_Recetas AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Actividades Intermedias - Recetas Despachadas de C. E'))) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      (Variable IN ('Consulta Externa - Consultas'))) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SELECT     Red, ORDEN, ORDEN_TIPO, codcentro, TIPO, NIVEL, NIVEL_ESTANDAR, CENTRO, ESTADO, CE_Estandar, [CE_%Acept], [CE_%Aceptmenos], 
                                                   RHM_Estandar, [RHM_%Acept], [RHM_%Aceptmenos], GCHP_Estandar, [GCHP_%Acept], [GCHP_%Aceptmenos], PRC_Estandar, [PRC_%Acept], 
                                                   [PRC_%Aceptmenos], PE_Estandar, [PE_%Acept], [PE_%Aceptmenos], POC_Estandar, [POC_%Acept], [POC_%Aceptmenos], IS_Estandar, [IS_%Acept], 
                                                   [IS_%Aceptmenos], RC_Estandar, [RC_%Acept], [RC_%Aceptmenos], TNMH_Estandar, [TNMH_%Acept], [TNMH_%Aceptmenos], PIM_Estandar, 
                                                   [PIM_%Acept], [PIM_%Aceptmenos], PIAC_Estandar, [PIAC_%Acept], [PIAC_%Aceptmenos], PHQE_Estandar, [PHQE_%Acept], [PHQE_%Aceptmenos], 
                                                   RSO_Estandar, [RSO_%Acept], [RSO_%Aceptmenos], POS_Estandar, [POS_%Acept], [POS_%Aceptmenos], TC_Estandar, [TC_%Acept], [TC_%Aceptmenos], 
                                                   PIV_Estandar, [PIV_%Acept], [PIV_%Aceptmenos], PII_Estandar, [PII_%Acept], [PII_%Aceptmenos], CSO_Estandar, [CSO_%Acept], [CSO_%Aceptmenos], 
                                                   RHO_Estandar, [RHO_%Acept], [RHO_%Aceptmenos], GCHO_Estandar, [GCHO_%Acept], [GCHO_%Aceptmenos], NTOS_Estandar, [NTOS_%Acept], 
                                                   [NTOS_%Aceptmenos], ID
                            FROM          dbo.TMI_ESTANDARES_D) AS D ON CEN.codcentro = D.codcentro*/

go

/*Rendimiento Hora Medico*/
CREATE VIEW CE_RHrMedico
AS
/*nivel*/
SELECT DISTINCT 
                D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
                CASE WHEN B.[Total] <> 0 THEN (A.[Total] * 1.00) / B.[Total] ELSE 0 END AS Total, CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) 
                / B.[202601] ELSE 0 END AS [202601], CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END AS [202602], 
                CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END AS [202603], CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) 
                / B.[202604] ELSE 0 END AS [202604], CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END AS [202605], 
                CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END AS [202606], CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) 
                / B.[202607] ELSE 0 END AS [202607], CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END AS [202608], 
                CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END AS [202609], CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) 
                / B.[202610] ELSE 0 END AS [202610], CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END AS [202611], 
                CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END AS [202612]
FROM         (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Consultas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Horas Médicas Efectivas')) AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Consulta Externa - Consultas'))) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      (Variable IN ('Consulta Externa - Horas Médicas Efectivas'))) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_nivel est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.nivel_centro = cen.nivel AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Rendimiento Hora Medico' AND est.periodo = '202608' ) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo NOT IN ('CNSR','IPO','INCOR')

/* tipo*/
SELECT DISTINCT 
                D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
                CASE WHEN B.[Total] <> 0 THEN (A.[Total] * 1.00) / B.[Total] ELSE 0 END AS Total, CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) 
                / B.[202601] ELSE 0 END AS [202601], CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END AS [202602], 
                CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END AS [202603], CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) 
                / B.[202604] ELSE 0 END AS [202604], CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END AS [202605], 
                CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END AS [202606], CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) 
                / B.[202607] ELSE 0 END AS [202607], CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END AS [202608], 
                CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END AS [202609], CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) 
                / B.[202610] ELSE 0 END AS [202610], CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END AS [202611], 
                CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END AS [202612]
FROM         (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Consultas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026) AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Consulta Externa - Consultas'))) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      (Variable IN ('Consulta Externa - Horas Médicas Efectivas'))) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Rendimiento Hora Medico' AND est.periodo = '202608' ) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo IN ('CNSR','IPO','INCOR')


/**/
WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, 
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Consulta Externa - Consultas'
),
B AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, 
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
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
    CASE WHEN B.[Total]  <> 0 THEN (A.[Total]  * 1.00) / B.[Total]  ELSE 0 END AS Total,
    CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END AS [202601],
    CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END AS [202602],
    CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END AS [202603],
    CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END AS [202604],
    CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END AS [202605],
    CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END AS [202606],
    CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END AS [202607],
    CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END AS [202608],
    CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END AS [202609],
    CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END AS [202610],
    CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END AS [202611],
    CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END AS [202612]
FROM CEN_NIVEL AS CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept, cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
    FROM pentahodev_prueba.dbo.tmi_estandar_nivel est
    JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.nivel_centro = cen.nivel AND est.periodo = cen.periodo
    WHERE est.indicador = 'Rendimiento Hora Medico' AND est.periodo = '202608'
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo NOT IN ('CNSR','IPO','INCOR')

UNION ALL

SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
    CASE WHEN B.[Total]  <> 0 THEN (A.[Total]  * 1.00) / B.[Total]  ELSE 0 END AS Total,
    CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END AS [202601],
    CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END AS [202602],
    CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END AS [202603],
    CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END AS [202604],
    CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END AS [202605],
    CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END AS [202606],
    CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END AS [202607],
    CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END AS [202608],
    CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END AS [202609],
    CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END AS [202610],
    CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END AS [202611],
    CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END AS [202612]
FROM CEN_TIPO AS CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept, cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
    FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
    WHERE est.indicador = 'Rendimiento Hora Medico' AND est.periodo = '202608'
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo IN ('CNSR','IPO','INCOR')

ORDER BY ORDEN;




/*% Prioridad I y II con respecto al Total de Emergencias*/
go         
CREATE VIEW Em_PrioI_II
AS
SELECT DISTINCT 
                      D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
                      CASE WHEN X.[Total] <> 0 THEN ((ISNULL(A.[Total], 0)) * 1.00) / X.[Total] ELSE 0 END AS Total, 
                      CASE WHEN X.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / X.[202601] ELSE 0 END AS [202601], 
                      CASE WHEN X.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / X.[202602] ELSE 0 END AS [202602], 
                      CASE WHEN X.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / X.[202603] ELSE 0 END AS [202603], 
                      CASE WHEN X.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / X.[202604] ELSE 0 END AS [202604], 
                      CASE WHEN X.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / X.[202605] ELSE 0 END AS [202605], 
                      CASE WHEN X.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / X.[202606] ELSE 0 END AS [202606], 
                      CASE WHEN X.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / X.[202607] ELSE 0 END AS [202607], 
                      CASE WHEN X.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / X.[202608] ELSE 0 END AS [202608], 
                      CASE WHEN X.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / X.[202609] ELSE 0 END AS [202609], 
                      CASE WHEN X.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / X.[202610] ELSE 0 END AS [202610], 
                      CASE WHEN X.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / X.[202611] ELSE 0 END AS [202611], 
                      CASE WHEN X.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / X.[202612] ELSE 0 END AS [202612]
FROM        (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Emergencia - Prioridad I', 'Emergencia - Prioridad II', 'Emergencia - Total de Atenciones'))) AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
                                                   SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
                                                   SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
                            FROM        pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Emergencia - Prioridad I', 'Emergencia - Prioridad II'))
                            GROUP BY Red, Centro, nivel, codcentro, Año) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM        pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      (Variable IN ('Emergencia - Total de Atenciones'))) AS X ON CEN.codcentro = X.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                           WHERE est.indicador = '% Prioridad I y II con respecto al Total de Emergencias' AND est.periodo= '202608') AS D ON CEN.codcentro = D.codcentro
go

/*% Prioridad IV y V con respecto al Total de Emergencias*/
CREATE VIEW Em_PrioIV_V
AS
SELECT DISTINCT 
                       D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
                      CASE WHEN X.[Total] <> 0 THEN ((ISNULL(A.[Total], 0)) * 1.00) / X.[Total] ELSE 0 END AS Total, 
                      CASE WHEN X.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / X.[202601] ELSE 0 END AS [202601], 
                      CASE WHEN X.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / X.[202602] ELSE 0 END AS [202602], 
                      CASE WHEN X.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / X.[202603] ELSE 0 END AS [202603], 
                      CASE WHEN X.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / X.[202604] ELSE 0 END AS [202604], 
                      CASE WHEN X.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / X.[202605] ELSE 0 END AS [202605], 
                      CASE WHEN X.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / X.[202606] ELSE 0 END AS [202606], 
                      CASE WHEN X.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / X.[202607] ELSE 0 END AS [202607], 
                      CASE WHEN X.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / X.[202608] ELSE 0 END AS [202608], 
                      CASE WHEN X.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / X.[202609] ELSE 0 END AS [202609], 
                      CASE WHEN X.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / X.[202610] ELSE 0 END AS [202610], 
                      CASE WHEN X.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / X.[202611] ELSE 0 END AS [202611], 
                      CASE WHEN X.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / X.[202612] ELSE 0 END AS [202612]
FROM         (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Emergencia - Prioridad IV', 'Emergencia - Prioridad V', 'Emergencia - Total de Atenciones'))) AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
                                                   SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
                                                   SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
                            FROM       pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Emergencia - Prioridad IV', 'Emergencia - Prioridad V'))
                            GROUP BY Red, Centro, nivel, codcentro, Año) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM        pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      (Variable IN ('Emergencia - Total de Atenciones'))) AS X ON CEN.codcentro = X.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.categoria
                           FROM [pentahodev_prueba].[dbo].[tmi_estandar_tipo] est
                           JOIN [pentahodev_prueba].[dbo].[tmi_centro] cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                           WHERE est.indicador = '% Prioridad IV y V con respecto al Total de Emergencias' AND est.periodo = '202608') AS D ON CEN.codcentro = D.codcentro
WHERE     (D.tipo IN ('H.N.', 'H.IV', 'H.III', 'H.II', 'H.I'))

go

/*Promedio Dia Estancia*/
CREATE VIEW H_Estancias
AS
SELECT DISTINCT 
                      D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
                      CASE WHEN A.[Total] <> 0 OR B.[Total] <> 0 THEN (A.[Total] * 1.00) / B.[Total] ELSE 0 END AS Total, 
                      CASE WHEN A.[202601] <> 0 OR B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END AS [202601], 
                      CASE WHEN A.[202602] <> 0 OR B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END AS [202602], 
                      CASE WHEN A.[202603] <> 0 OR B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END AS [202603], 
                      CASE WHEN A.[202604] <> 0 OR B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END AS [202604], 
                      CASE WHEN A.[202605] <> 0 OR B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END AS [202605], 
                      CASE WHEN A.[202606] <> 0 OR B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END AS [202606], 
                      CASE WHEN A.[202607] <> 0 OR B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END AS [202607], 
                      CASE WHEN A.[202608] <> 0 OR B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END AS [202608], 
                      CASE WHEN A.[202609] <> 0 OR B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END AS [202609], 
                      CASE WHEN A.[202610] <> 0 OR B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END AS [202610], 
                      CASE WHEN A.[202611] <> 0 OR B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END AS [202611], 
                      CASE WHEN A.[202612] <> 0 OR B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END AS [202612]
FROM         (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Estancias')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Egresos')) AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Hospitalizacion - Estancias'))) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      (Variable IN ('Hospitalizacion - Egresos'))) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.categoria
                           FROM [pentahodev_prueba].[dbo].[tmi_estandar_tipo] est
                           JOIN [pentahodev_prueba].[dbo].[tmi_centro] cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Promedio Dia Estancia' AND est.periodo = '202608') AS D ON CEN.codcentro = D.codcentro
go

/*Intervalo de Sustitución*/
CREATE VIEW H_ISust
AS
SELECT DISTINCT 
                      D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.aceptmenos AS [% Aceptmenos], D.acept AS [% Acept],
                      CASE WHEN x.[Total] <> 0 THEN ((isnull(A.[Total], 0) - isnull(B.[Total], 0)) * 1.00) / x.[Total] ELSE 0 END AS Total, 
                      CASE WHEN x.[202601] <> 0 THEN ((isnull(A.[202601], 0) - isnull(B.[202601], 0)) * 1.00) / x.[202601] ELSE 0 END AS [202601], 
                      CASE WHEN x.[202602] <> 0 THEN ((isnull(A.[202602], 0) - isnull(B.[202602], 0)) * 1.00) / x.[202602] ELSE 0 END AS [202602], 
                      CASE WHEN x.[202603] <> 0 THEN ((isnull(A.[202603], 0) - isnull(B.[202603], 0)) * 1.00) / x.[202603] ELSE 0 END AS [202603], 
                      CASE WHEN x.[202604] <> 0 THEN ((isnull(A.[202604], 0) - isnull(B.[202604], 0)) * 1.00) / x.[202604] ELSE 0 END AS [202604], 
                      CASE WHEN x.[202605] <> 0 THEN ((isnull(A.[202605], 0) - isnull(B.[202605], 0)) * 1.00) / x.[202605] ELSE 0 END AS [202605], 
                      CASE WHEN x.[202606] <> 0 THEN ((isnull(A.[202606], 0) - isnull(B.[202606], 0)) * 1.00) / x.[202606] ELSE 0 END AS [202606], 
                      CASE WHEN x.[202607] <> 0 THEN ((isnull(A.[202607], 0) - isnull(B.[202607], 0)) * 1.00) / x.[202607] ELSE 0 END AS [202607], 
                      CASE WHEN x.[202608] <> 0 THEN ((isnull(A.[202608], 0) - isnull(B.[202608], 0)) * 1.00) / x.[202608] ELSE 0 END AS [202608], 
                      CASE WHEN x.[202609] <> 0 THEN ((isnull(A.[202609], 0) - isnull(B.[202609], 0)) * 1.00) / x.[202609] ELSE 0 END AS [202609], 
                      CASE WHEN x.[202610] <> 0 THEN ((isnull(A.[202610], 0) - isnull(B.[202610], 0)) * 1.00) / x.[202610] ELSE 0 END AS [202610], 
                      CASE WHEN x.[202611] <> 0 THEN ((isnull(A.[202611], 0) - isnull(B.[202611], 0)) * 1.00) / x.[202611] ELSE 0 END AS [202611], 
                      CASE WHEN x.[202612] <> 0 THEN ((isnull(A.[202612], 0) - isnull(B.[202612], 0)) * 1.00) / x.[202612] ELSE 0 END AS [202612]
FROM         (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Hospitalizacion - Días Cama Disponible', 'Hospitalizacion - Pacientes Días', 'Hospitalizacion - Egresos'))) AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM      pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Hospitalizacion - Días Cama Disponible'))) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM      pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_2
                            WHERE      (Variable IN ('Hospitalizacion - Pacientes Días'))) AS B ON A.codcentro = B.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM      pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE     (Variable IN ('Hospitalizacion - Egresos'))) AS x ON CEN.codcentro = x.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , est.aceptmenos , cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Intervalo de Sustitución' AND est.periodo = '202608') AS D ON CEN.codcentro = D.codcentro

go

/*Porcentaje de Ocupación de Cama*/
CREATE VIEW H_OCama
AS
SELECT DISTINCT 
                      D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.tipo AS TIPO, D.estandar AS Estandar, D.aceptmenos AS [% Aceptmenos], D.acept AS [% Acept],
                      CASE WHEN B.[Total]  <> 0 THEN  (A.[Total] * 1.00) / B.[Total] ELSE 0 END AS Total, 
                      CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END AS [202601], 
                      CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END AS [202602], 
                      CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END AS [202603], 
                      CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END AS [202604], 
                      CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END AS [202605], 
                      CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END AS [202606], 
                      CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END AS [202607], 
                      CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END AS [202608], 
                      CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END AS [202609], 
                      CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END AS [202610], 
                      CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END AS [202611], 
                      CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END AS [202612]
FROM        (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Pacientes Días')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Días Cama Disponible')) AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Hospitalizacion - Pacientes Días'))) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      (Variable IN ('Hospitalizacion - Días Cama Disponible'))) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , est.aceptmenos , cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Porcentaje de Ocupación de Cama' AND est.periodo = '202608') AS D ON CEN.codcentro = D.codcentro
go

--hay un problema acà 08.05.2026
/*CORREGIDO 14.08.2026
CREATE VIEW H_RCama
AS
SELECT DISTINCT 
                      D.ID AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.NIVEL, D.TIPO, D.RC_Estandar AS Estandar, D.[RC_%Aceptmenos] AS [% Aceptmenos], 
                      D.[RC_%Acept] AS [% Acept], CASE WHEN A.[Total] <> 0 OR
                      B.[Total] <> 0 THEN (A.[Total] * 1.00) / B.[Total] ELSE 0 END AS Total, CASE WHEN A.[202601] <> 0 OR
                      B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END AS [202601], CASE WHEN A.[202602] <> 0 OR
                      B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END AS [202602], CASE WHEN A.[202603] <> 0 OR
                      B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END AS [202603], CASE WHEN A.[202604] <> 0 OR
                      B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END AS [202604], CASE WHEN A.[202605] <> 0 OR
                      B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END AS [202605], CASE WHEN A.[202606] <> 0 OR
                      B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END AS [202606], CASE WHEN A.[202607] <> 0 OR
                      B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END AS [202607], CASE WHEN A.[202608] <> 0 OR
                      B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END AS [202608], CASE WHEN A.[202609] <> 0 OR
                      B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END AS [202609], CASE WHEN A.[202610] <> 0 OR
                      B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END AS [202610], CASE WHEN A.[202611] <> 0 OR
                      B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END AS [202611], CASE WHEN A.[202612] <> 0 OR
                      B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END AS [202612]
FROM         dbo.TMI_CENTROS_H_RCama AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Hospitalizacion - Egresos'))) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      (Variable IN ('Hospitalizacion -  Camas Hospitalarias'))) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SELECT     Red, ORDEN, ORDEN_TIPO, codcentro, TIPO, NIVEL, NIVEL_ESTANDAR, CENTRO, ESTADO, CE_Estandar, [CE_%Acept], [CE_%Aceptmenos], 
                                                   RHM_Estandar, [RHM_%Acept], [RHM_%Aceptmenos], GCHP_Estandar, [GCHP_%Acept], [GCHP_%Aceptmenos], PRC_Estandar, [PRC_%Acept], 
                                                   [PRC_%Aceptmenos], PE_Estandar, [PE_%Acept], [PE_%Aceptmenos], POC_Estandar, [POC_%Acept], [POC_%Aceptmenos], IS_Estandar, [IS_%Acept], 
                                                   [IS_%Aceptmenos], RC_Estandar, [RC_%Acept], [RC_%Aceptmenos], TNMH_Estandar, [TNMH_%Acept], [TNMH_%Aceptmenos], PIM_Estandar, 
                                                   [PIM_%Acept], [PIM_%Aceptmenos], PIAC_Estandar, [PIAC_%Acept], [PIAC_%Aceptmenos], PHQE_Estandar, [PHQE_%Acept], [PHQE_%Aceptmenos], 
                                                   RSO_Estandar, [RSO_%Acept], [RSO_%Aceptmenos], POS_Estandar, [POS_%Acept], [POS_%Aceptmenos], TC_Estandar, [TC_%Acept], [TC_%Aceptmenos], 
                                                   PIV_Estandar, [PIV_%Acept], [PIV_%Aceptmenos], PII_Estandar, [PII_%Acept], [PII_%Aceptmenos], CSO_Estandar, [CSO_%Acept], [CSO_%Aceptmenos], 
                                                   RHO_Estandar, [RHO_%Acept], [RHO_%Aceptmenos], GCHO_Estandar, [GCHO_%Acept], [GCHO_%Aceptmenos], NTOS_Estandar, [NTOS_%Acept], 
                                                   [NTOS_%Aceptmenos], ID
                            FROM          dbo.TMI_ESTANDARES_D) AS D ON CEN.codcentro = D.codcentro*/
--SELECT * FROM H_RCama  

/*Rendimiento Cama*/
CREATE VIEW H_RCama
AS
SELECT DISTINCT 
                      D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.tipo AS TIPO, D.estandar AS Estandar, D.aceptmenos AS [% Aceptmenos], D.acept AS [% Acept], 
                      CASE WHEN B.[Total] <> 0 THEN (A.[Total] * 1.00) / B.[Total] ELSE 0 END AS Total, 
                      CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END AS [202601], 
                      CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END AS [202602], 
                      CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END AS [202603], 
                      CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END AS [202604], 
                      CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END AS [202605], 
                      CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END AS [202606], 
                      CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END AS [202607], 
                      CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END AS [202608], 
                      CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END AS [202609], 
                      CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END AS [202610], 
                      CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END AS [202611], 
                      CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END AS [202612]                    
                      
FROM         (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Hospitalizacion - Egresos', 'Hospitalizacion -  Camas Hospitalarias'))) AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Hospitalizacion - Egresos'))) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      (Variable IN ('Hospitalizacion -  Camas Hospitalarias'))) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , est.aceptmenos , cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Rendimiento Cama'AND est.periodo = '202608') AS D ON CEN.codcentro = D.codcentro                            

go

/*Tasa Neta de Mortalidad Hospitalaria*/
CREATE VIEW H_TBMHosp
AS
SELECT DISTINCT 
                      D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.tipo AS TIPO, D.estandar AS Estandar, D.aceptmenos AS [% Aceptmenos], D.acept AS [% Acept], 
                      CASE WHEN (isnull(B.[Total], 0) - isnull(x.[Total], 0)) <> 0 THEN ((isnull(A.[Total], 0)) * 1.00) / (isnull(B.[Total], 0) - isnull(x.[Total], 0)) ELSE 0 END AS Total, 
                      CASE WHEN (isnull(B.[202601], 0) - isnull(x.[202601], 0)) <> 0 THEN ((isnull(A.[202601], 0)) * 1.00) / (isnull(B.[202601], 0) - isnull(x.[202601], 0)) ELSE 0 END AS [202601], 
                      CASE WHEN (isnull(B.[202602], 0) - isnull(x.[202602], 0)) <> 0 THEN ((isnull(A.[202602], 0)) * 1.00) / (isnull(B.[202602], 0) - isnull(x.[202602], 0)) ELSE 0 END AS [202602], 
                      CASE WHEN (isnull(B.[202603], 0) - isnull(x.[202603], 0)) <> 0 THEN ((isnull(A.[202603], 0)) * 1.00) / (isnull(B.[202603], 0) - isnull(x.[202603], 0)) ELSE 0 END AS [202603], 
                      CASE WHEN (isnull(B.[202604], 0) - isnull(x.[202604], 0)) <> 0 THEN ((isnull(A.[202604], 0)) * 1.00) / (isnull(B.[202604], 0) - isnull(x.[202604], 0)) ELSE 0 END AS [202604], 
                      CASE WHEN (isnull(B.[202605], 0) - isnull(x.[202605], 0)) <> 0 THEN ((isnull(A.[202605], 0)) * 1.00) / (isnull(B.[202605], 0) - isnull(x.[202605], 0)) ELSE 0 END AS [202605], 
                      CASE WHEN (isnull(B.[202606], 0) - isnull(x.[202606], 0)) <> 0 THEN ((isnull(A.[202606], 0)) * 1.00) / (isnull(B.[202606], 0) - isnull(x.[202606], 0)) ELSE 0 END AS [202606], 
                      CASE WHEN (isnull(B.[202607], 0) - isnull(x.[202607], 0)) <> 0 THEN ((isnull(A.[202607], 0)) * 1.00) / (isnull(B.[202607], 0) - isnull(x.[202607], 0)) ELSE 0 END AS [202607], 
                      CASE WHEN (isnull(B.[202608], 0) - isnull(x.[202608], 0)) <> 0 THEN ((isnull(A.[202608], 0)) * 1.00) / (isnull(B.[202608], 0) - isnull(x.[202608], 0)) ELSE 0 END AS [202608], 
                      CASE WHEN (isnull(B.[202609], 0) - isnull(x.[202609], 0)) <> 0 THEN ((isnull(A.[202609], 0)) * 1.00) / (isnull(B.[202609], 0) - isnull(x.[202609], 0)) ELSE 0 END AS [202609], 
                      CASE WHEN (isnull(B.[202610], 0) - isnull(x.[202610], 0)) <> 0 THEN ((isnull(A.[202610], 0)) * 1.00) / (isnull(B.[202610], 0) - isnull(x.[202610], 0)) ELSE 0 END AS [202610], 
                      CASE WHEN (isnull(B.[202611], 0) - isnull(x.[202611], 0)) <> 0 THEN ((isnull(A.[202611], 0)) * 1.00) / (isnull(B.[202611], 0) - isnull(x.[202611], 0)) ELSE 0 END AS [202611], 
                      CASE WHEN (isnull(B.[202612], 0) - isnull(x.[202612], 0)) <> 0 THEN ((isnull(A.[202612], 0)) * 1.00) / (isnull(B.[202612], 0) - isnull(x.[202612], 0)) ELSE 0 END AS [202612]
FROM        (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Defunciones después de 48 horas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Egresos')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Hospitalizacion - Defunciones antes de 48 horas')) AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Hospitalizacion - Defunciones después de 48 horas'))) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_2
                            WHERE      (Variable IN ('Hospitalizacion - Egresos'))) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      (Variable IN ('Hospitalizacion - Defunciones antes de 48 horas'))) AS x ON CEN.codcentro = x.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , est.aceptmenos , cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Tasa Neta de Mortalidad Hospitalaria' AND est.periodo = '202608') AS D ON CEN.codcentro = D.codcentro
go

/*Concentración de Sesiones Odontológicas*/
CREATE VIEW O_Concent
AS
/*SELECT DISTINCT 
    D.ID AS ORDEN,
    CEN.Red,
    CEN.codcentro,
    CEN.Centro,
    D.NIVEL,
    D.TIPO,
    D.CSO_Estandar AS Estandar,
    D.[CSO_%Acept] AS [% Acept],

    -- TOTAL
    ISNULL( (ISNULL(A.[Total],0) * 1.00) / NULLIF(ISNULL(B.[Total],0),0) , 0) AS Total,

    -- MESES INDIVIDUALES
    ISNULL( (ISNULL(A.[202601],0) * 1.00) / NULLIF(ISNULL(B.[202601],0),0) , 0) AS [202601],
    ISNULL( (ISNULL(A.[202602],0) * 1.00) / NULLIF(ISNULL(B.[202602],0),0) , 0) AS [202602],
    ISNULL( (ISNULL(A.[202603],0) * 1.00) / NULLIF(ISNULL(B.[202603],0),0) , 0) AS [202603],
    ISNULL( (ISNULL(A.[202604],0) * 1.00) / NULLIF(ISNULL(B.[202604],0),0) , 0) AS [202604],
    ISNULL( (ISNULL(A.[202605],0) * 1.00) / NULLIF(ISNULL(B.[202605],0),0) , 0) AS [202605],
    ISNULL( (ISNULL(A.[202606],0) * 1.00) / NULLIF(ISNULL(B.[202606],0),0) , 0) AS [202606],
    ISNULL( (ISNULL(A.[202607],0) * 1.00) / NULLIF(ISNULL(B.[202607],0),0) , 0) AS [202607],
    ISNULL( (ISNULL(A.[202608],0) * 1.00) / NULLIF(ISNULL(B.[202608],0),0) , 0) AS [202608],
    ISNULL( (ISNULL(A.[202609],0) * 1.00) / NULLIF(ISNULL(B.[202609],0),0) , 0) AS [202609],
    ISNULL( (ISNULL(A.[202610],0) * 1.00) / NULLIF(ISNULL(B.[202610],0),0) , 0) AS [202610],
    ISNULL( (ISNULL(A.[202611],0) * 1.00) / NULLIF(ISNULL(B.[202611],0),0) , 0) AS [202611],
    ISNULL( (ISNULL(A.[202612],0) * 1.00) / NULLIF(ISNULL(B.[202612],0),0) , 0) AS [202612]

FROM dbo.TMI_CENTROS_O_Concent CEN

LEFT JOIN (
    SELECT *
    FROM dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Odontología - Sesiones Odontológicas'
) A 
    ON CEN.codcentro = A.codcentro

LEFT JOIN (
    SELECT *
    FROM dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable = 'Odontología - Consultantes de Odontología'
) B 
    ON CEN.codcentro = B.codcentro

LEFT JOIN dbo.TMI_ESTANDARES_D D
    ON CEN.codcentro = D.codcentro*/

SELECT DISTINCT 
                      D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
                      CASE WHEN A.[Total] <> 0 OR B.[Total] <> 0 THEN (A.[Total] * 1.00) / B.[Total] ELSE 0 END AS Total, 
                      CASE WHEN A.[202601] <> 0 OR B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END AS [202601], 
                      CASE WHEN A.[202602] <> 0 OR B.[202602] <> 0 THEN ((A.[202601] + A.[202602]) * 1.00) / (B.[202601] + B.[202602]) ELSE 0 END AS [202602], 
                      CASE WHEN A.[202603] <> 0 OR B.[202603] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603]) * 1.00) / (B.[202601] + B.[202602] + B.[202603]) ELSE 0 END AS [202603], 
                      CASE WHEN A.[202604] <> 0 OR B.[202604] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604]) ELSE 0 END AS [202604], 
                      CASE WHEN A.[202605] <> 0 OR B.[202605] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605]) ELSE 0 END AS [202605], 
                      CASE WHEN A.[202606] <> 0 OR B.[202606] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606]) ELSE 0 END AS [202606], 
                      CASE WHEN A.[202607] <> 0 OR B.[202607] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607]) ELSE 0 END AS [202607], 
                      CASE WHEN A.[202608] <> 0 OR B.[202608] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608]) ELSE 0 END AS [202608], 
                      CASE WHEN A.[202609] <> 0 OR B.[202609] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609]) ELSE 0 END AS [202609], 
                      CASE WHEN A.[202610] <> 0 OR B.[202610] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610]) ELSE 0 END AS [202610], 
                      CASE WHEN A.[202611] <> 0 OR B.[202611] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611]) ELSE 0 END AS [202611], 
                      CASE WHEN A.[202612] <> 0 OR B.[202612] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611] + A.[202612]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611] + B.[202612]) ELSE 0 END AS [202612]
FROM         (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     (Variable IN ('Odontología - Sesiones Odontológicas', 'Odontología - Consultantes de Odontología'))) AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Odontología - Sesiones Odontológicas'))) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      (Variable IN ('Odontología - Consultantes de Odontología'))) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_nivel est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.nivel_centro = cen.nivel AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Concentración de Sesiones Odontológicas' AND est.periodo = '202609') AS D ON CEN.codcentro = D.codcentro
go

/*Grado de Cumplimiento de Hora Odontólogo*/
CREATE VIEW O_GCHOdon
AS
SELECT DISTINCT 
                     D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
                      CASE WHEN B.[Total] <> 0 THEN (A.[Total] * 1.00) / B.[Total] ELSE 0 END AS Total, 
                      CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END AS [202601], 
                      CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END AS [202602], 
                      CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END AS [202603], 
                      CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END AS [202604], 
                      CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END AS [202605], 
                      CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END AS [202606], 
                      CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END AS [202607], 
                      CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END AS [202608], 
                      CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END AS [202609], 
                      CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END AS [202610], 
                      CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END AS [202611], 
                      CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END AS [202612]
FROM         (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     Variable IN ('Odontología - Horas Odontológicas Efectivas', 'Odontología - Horas Odontológicas Programadas')) AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      Variable IN ('Odontología - Horas Odontológicas Efectivas')) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE    Variable IN ('Odontología - Horas Odontológicas Programadas')) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , est.aceptmenos , cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Grado de Cumplimiento de Hora Odontólogo' AND est.periodo= '202608') AS D ON CEN.codcentro = D.codcentro
go

/*Rendimiento de Hora Odontológica*/
CREATE VIEW O_HrOdont
AS
SELECT DISTINCT 
                      D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
                      CASE WHEN B.[Total] <> 0 THEN (A.[Total] * 1.00) / B.[Total] ELSE 0 END AS Total, 
                      CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END AS [202601], 
                      CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END AS [202602], 
                      CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END AS [202603], 
                      CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END AS [202604], 
                      CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END AS [202605], 
                      CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END AS [202606], 
                      CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END AS [202607], 
                      CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END AS [202608], 
                      CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END AS [202609], 
                      CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END AS [202610], 
                      CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END AS [202611], 
                      CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END AS [202612]
FROM         (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     Variable IN ('Odontología - Sesiones Odontológicas', 'Odontología - Horas Odontológicas Efectivas')) AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Odontología - Sesiones Odontológicas'))) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      (Variable IN ('Odontología - Horas Odontológicas Efectivas'))) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_nivel est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.nivel_centro = cen.nivel AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Rendimiento de Hora Odontológica' AND est.periodo = '202609') AS D ON CEN.codcentro = D.codcentro
go

/*Número de trabajos Odontológicos por Sesión*/
CREATE VIEW O_NTOdontS
AS
SELECT DISTINCT 
                      D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
                      CASE WHEN B.[Total] <> 0 THEN (ISNULL(A.[Total], 0) * 1.00) / B.[Total] ELSE 0 END AS Total, 
                      CASE WHEN B.[202601] <> 0 THEN (ISNULL(A.[202601], 0) * 1.00) / B.[202601] ELSE 0 END AS [202601], 
                      CASE WHEN B.[202602] <> 0 THEN (ISNULL(A.[202602], 0) * 1.00) / B.[202602] ELSE 0 END AS [202602], 
                      CASE WHEN B.[202603] <> 0 THEN (ISNULL(A.[202603], 0) * 1.00) / B.[202603] ELSE 0 END AS [202603], 
                      CASE WHEN B.[202604] <> 0 THEN (ISNULL(A.[202604], 0) * 1.00) / B.[202604] ELSE 0 END AS [202604], 
                      CASE WHEN B.[202605] <> 0 THEN (ISNULL(A.[202605], 0) * 1.00) / B.[202605] ELSE 0 END AS [202605], 
                      CASE WHEN B.[202606] <> 0 THEN (ISNULL(A.[202606], 0) * 1.00) / B.[202606] ELSE 0 END AS [202606], 
                      CASE WHEN B.[202607] <> 0 THEN (ISNULL(A.[202607], 0) * 1.00) / B.[202607] ELSE 0 END AS [202607], 
                      CASE WHEN B.[202608] <> 0 THEN (ISNULL(A.[202608], 0) * 1.00) / B.[202608] ELSE 0 END AS [202608], 
                      CASE WHEN B.[202609] <> 0 THEN (ISNULL(A.[202609], 0) * 1.00) / B.[202609] ELSE 0 END AS [202609], 
                      CASE WHEN B.[202610] <> 0 THEN (ISNULL(A.[202610], 0) * 1.00) / B.[202610] ELSE 0 END AS [202610], 
                      CASE WHEN B.[202611] <> 0 THEN (ISNULL(A.[202611], 0) * 1.00) / B.[202611] ELSE 0 END AS [202611], 
                      CASE WHEN B.[202612] <> 0 THEN (ISNULL(A.[202612], 0) * 1.00) / B.[202612] ELSE 0 END AS [202612]
FROM  (
       SELECT DISTINCT Red, codcentro, Centro
       FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
       WHERE     variable IN ('Odontología - Trabajos Odontológicos', 'Odontología - Diagnóstico por imágenes', 'Odontología - Procedimientos Especiales')
       UNION
       SELECT DISTINCT Red, codcentro, Centro
       FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
       WHERE     variable IN ('Odontología - Sesiones Odontológicas')
) AS CEN LEFT OUTER JOIN (
                            SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
                                                   SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
                                                   SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE  Variable IN ('Odontología - Trabajos Odontológicos', 'Odontología - Diagnóstico por imágenes', 'Odontología - Procedimientos Especiales')
                            GROUP BY Red, Centro, nivel, codcentro, Año
                          ) AS A ON CEN.codcentro = A.codcentro 
          LEFT OUTER JOIN (
                            SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                            [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE  Variable IN ('Odontología - Sesiones Odontológicas')
                          ) AS B ON CEN.codcentro = B.codcentro 
          LEFT OUTER JOIN (
                            SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , est.aceptmenos , cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.categoria
                            FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
                            JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                            WHERE est.indicador = 'Número de trabajos Odontológicos por Sesión' AND est.periodo = '202609'
                          ) AS D ON CEN.codcentro = D.codcentro
WHERE     (A.Total * 1.00 / B.Total IS NOT NULL)
go

/*Porcentaje de Horas Quirúrgicas Efectivas*/
CREATE VIEW Qx_GCHProg
AS
SELECT DISTINCT 
                      D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
                      CASE WHEN B.[Total] <> 0 THEN ((ISNULL(A.[Total], 0)) * 1.00) / B.[Total] ELSE 0 END AS Total, 
                      CASE WHEN B.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / B.[202601] ELSE 0 END AS [202601], 
                      CASE WHEN B.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / B.[202602] ELSE 0 END AS [202602], 
                      CASE WHEN B.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / B.[202603] ELSE 0 END AS [202603], 
                      CASE WHEN B.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / B.[202604] ELSE 0 END AS [202604], 
                      CASE WHEN B.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / B.[202605] ELSE 0 END AS [202605], 
                      CASE WHEN B.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / B.[202606] ELSE 0 END AS [202606], 
                      CASE WHEN B.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / B.[202607] ELSE 0 END AS [202607], 
                      CASE WHEN B.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / B.[202608] ELSE 0 END AS [202608], 
                      CASE WHEN B.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / B.[202609] ELSE 0 END AS [202609], 
                      CASE WHEN B.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / B.[202610] ELSE 0 END AS [202610], 
                      CASE WHEN B.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / B.[202611] ELSE 0 END AS [202611], 
                      CASE WHEN B.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / B.[202612] ELSE 0 END AS [202612]
FROM (
      SELECT DISTINCT Red, codcentro, Centro
      FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE     Variable IN ('Centro Quirúrgico - Horas Uso de Sala', 'Centro Quirúrgico - Horas Programadas Intervenc.Quirurgicas')
) AS CEN LEFT OUTER JOIN (
                          SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE     Variable IN ('Centro Quirúrgico - Horas Uso de Sala')
                           ) AS A ON CEN.codcentro = A.codcentro 
                           LEFT OUTER JOIN (
                            SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                            [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      Variable IN ('Centro Quirúrgico - Horas Programadas Intervenc.Quirurgicas')
                          ) AS B ON CEN.codcentro = B.codcentro 
                          LEFT OUTER JOIN (
                          SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , est.aceptmenos , cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Porcentaje de Horas Quirúrgicas Efectivas' AND est.periodo = '202608'
                          ) AS D ON CEN.codcentro = D.codcentro
go

/*Tasa de Cesáreas*/
CREATE VIEW Qx_HTCesareas
AS
SELECT DISTINCT 
                      D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
                      CASE WHEN B.[Total] <> 0 THEN ((ISNULL(A.[Total], 0)) * 1.00) / B.[Total] ELSE NULL END AS Total, CASE WHEN B.[202601] <> 0 AND 
                      A.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / B.[202601] ELSE NULL END AS [202601], CASE WHEN B.[202602] <> 0 AND 
                      A.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / B.[202602] ELSE NULL END AS [202602], CASE WHEN B.[202603] <> 0 AND 
                      A.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / B.[202603] ELSE NULL END AS [202603], CASE WHEN B.[202604] <> 0 AND 
                      A.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / B.[202604] ELSE NULL END AS [202604], CASE WHEN B.[202605] <> 0 AND 
                      A.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / B.[202605] ELSE NULL END AS [202605], CASE WHEN B.[202606] <> 0 AND 
                      A.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / B.[202606] ELSE NULL END AS [202606], CASE WHEN B.[202607] <> 0 AND 
                      A.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / B.[202607] ELSE NULL END AS [202607], CASE WHEN B.[202608] <> 0 AND 
                      A.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / B.[202608] ELSE NULL END AS [202608], CASE WHEN B.[202609] <> 0 AND 
                      A.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / B.[202609] ELSE NULL END AS [202609], CASE WHEN B.[202610] <> 0 AND 
                      A.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / B.[202610] ELSE NULL END AS [202610], CASE WHEN B.[202611] <> 0 AND 
                      A.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / B.[202611] ELSE NULL END AS [202611], CASE WHEN B.[202612] <> 0 AND 
                      A.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / B.[202612] ELSE NULL END AS [202612]
FROM        (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Centro Obstétrico - Cesáreas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Centro Obstétrico - Total de Partos')) AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Centro Obstétrico - Cesáreas'))) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      Variable IN ('Centro Obstétrico - Total de Partos')
                          ) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , est.aceptmenos , cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Tasa de Cesáreas' AND est.periodo = '202608') AS D ON CEN.codcentro = D.codcentro
go   

/*Porcentaje de Intervenciones de Alta Complejidad*/
CREATE VIEW Qx_IAlta
AS
SELECT DISTINCT 
                      D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
                      CASE WHEN B.[Total] <> 0 THEN ((ISNULL(A.[Total], 0)) * 1.00) / B.[Total] ELSE 0 END AS Total, 
                      CASE WHEN B.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / B.[202601] ELSE 0 END AS [202601], 
                      CASE WHEN B.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / B.[202602] ELSE 0 END AS [202602], 
                      CASE WHEN B.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / B.[202603] ELSE 0 END AS [202603], 
                      CASE WHEN B.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / B.[202604] ELSE 0 END AS [202604], 
                      CASE WHEN B.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / B.[202605] ELSE 0 END AS [202605], 
                      CASE WHEN B.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / B.[202606] ELSE 0 END AS [202606], 
                      CASE WHEN B.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / B.[202607] ELSE 0 END AS [202607], 
                      CASE WHEN B.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / B.[202608] ELSE 0 END AS [202608], 
                      CASE WHEN B.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / B.[202609] ELSE 0 END AS [202609], 
                      CASE WHEN B.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / B.[202610] ELSE 0 END AS [202610], 
                      CASE WHEN B.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / B.[202611] ELSE 0 END AS [202611], 
                      CASE WHEN B.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / B.[202612] ELSE 0 END AS [202612]
FROM         (
SELECT DISTINCT Red, codcentro, Centro
FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     Variable IN ('Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 'Centro Quirúrgico - Cirugías sin clasificación de complejidad', 
                      'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 
                      'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 
                      'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento')) AS CEN 
                      LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      Variable IN ('Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad')) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
                                                   SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
                                                   SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      Variable IN ('Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                                                   'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                                                   'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento')
                            GROUP BY Red, Centro, nivel, codcentro, Año) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , est.aceptmenos , cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Porcentaje de Intervenciones de Alta Complejidad' AND est.periodo = '202608') AS D ON CEN.codcentro = D.codcentro
WHERE     (A.Red IN ('ANCASH', 'APURIMAC', 'AREQUIPA', 'AYACUCHO', 'CAJAMARCA', 'CUSCO', 'HUANCAVELICA', 'HUANUCO', 'HUARAZ', 'ICA', 'RED JAEN', 'INCOR', 'JULIACA', 
                      'JUNIN', 'LA LIBERTAD', 'LAMBAYEQUE', 'LORETO', 'MADRE DE DIOS', 'MOQUEGUA', 'MOYOBAMBA', 'PASCO', 'PIURA', 'PUNO', 'REBAGLIATI', 'SABOGAL', 'TACNA', 
                      'TARAPOTO', 'TUMBES', 'RED PRESTACIONAL ALMENARA', 'RED PRESTACIONAL REBAGLIATI', 'RED PRESTACIONAL SABOGAL'))
go

/*Porcentaje de Intervenciones Menores*/
CREATE VIEW Qx_IMenor
AS
SELECT DISTINCT 
                      D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
                      CASE WHEN X.[Total] <> 0 THEN ((ISNULL(A.[Total], 0)) * 1.00) / X.[Total] ELSE 0 END AS Total, 
                      CASE WHEN X.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / X.[202601] ELSE 0 END AS [202601], 
                      CASE WHEN X.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / X.[202602] ELSE 0 END AS [202602], 
                      CASE WHEN X.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / X.[202603] ELSE 0 END AS [202603], 
                      CASE WHEN X.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / X.[202604] ELSE 0 END AS [202604], 
                      CASE WHEN X.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / X.[202605] ELSE 0 END AS [202605], 
                      CASE WHEN X.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / X.[202606] ELSE 0 END AS [202606], 
                      CASE WHEN X.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / X.[202607] ELSE 0 END AS [202607], 
                      CASE WHEN X.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / X.[202608] ELSE 0 END AS [202608], 
                      CASE WHEN X.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / X.[202609] ELSE 0 END AS [202609], 
                      CASE WHEN X.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / X.[202610] ELSE 0 END AS [202610], 
                      CASE WHEN X.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / X.[202611] ELSE 0 END AS [202611], 
                      CASE WHEN X.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / X.[202612] ELSE 0 END AS [202612]
FROM         (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     Variable IN ('Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento', 
                      'Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                      'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                      'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento')) AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
                                                   SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
                                                   SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'))
                            GROUP BY Red, Centro, nivel, codcentro, Año) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
                                                   SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
                                                   SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      (Variable IN ('Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                                                   'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                                                   'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'))
                            GROUP BY Red, Centro, nivel, codcentro, Año) AS X ON CEN.codcentro = X.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , est.aceptmenos , cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Porcentaje de Intervenciones Menores' AND est.periodo = '202608') AS D ON CEN.codcentro = D.codcentro
go

/*Porcentaje de Operaciones Suspendidas*/
CREATE VIEW Qx_IntSusp
AS
SELECT DISTINCT 
                      D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
                      CASE WHEN B.[Total] <> 0 THEN ((ISNULL(A.[Total], 0)) * 1.00) / B.[Total] ELSE NULL END AS Total, 
                      CASE WHEN B.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / B.[202601] ELSE NULL END AS [202601], 
                      CASE WHEN B.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / B.[202602] ELSE NULL END AS [202602], 
                      CASE WHEN B.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / B.[202603] ELSE NULL END AS [202603], 
                      CASE WHEN B.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / B.[202604] ELSE NULL END AS [202604], 
                      CASE WHEN B.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / B.[202605] ELSE NULL END AS [202605], 
                      CASE WHEN B.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / B.[202606] ELSE NULL END AS [202606], 
                      CASE WHEN B.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / B.[202607] ELSE NULL END AS [202607], 
                      CASE WHEN B.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / B.[202608] ELSE NULL END AS [202608], 
                      CASE WHEN B.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / B.[202609] ELSE NULL END AS [202609], 
                      CASE WHEN B.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / B.[202610] ELSE NULL END AS [202610], 
                      CASE WHEN B.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / B.[202611] ELSE NULL END AS [202611], 
                      CASE WHEN B.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / B.[202612] ELSE NULL END AS [202612]
FROM         (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Centro Quirúrgico - Operaciones Suspendidas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Centro Quirúrgico - Intervenc.Quirurgicas Programadas')) AS CEN LEFT OUTER JOIN
                          (SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                           FROM  pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                           WHERE Variable IN ('Centro Quirúrgico - Operaciones Suspendidas')) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                           FROM  pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                           WHERE Variable IN ('Centro Quirúrgico - Intervenc.Quirurgicas Programadas')) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , est.aceptmenos , cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Porcentaje de Operaciones Suspendidas' AND est.periodo = '202609') AS D ON CEN.codcentro = D.codcentro


go

/*Rendimiento de Sala de Operaciones*/
CREATE VIEW Qx_RendSO
AS
SELECT DISTINCT 
                      D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 
                      CASE WHEN B.[Total] <> 0 THEN ((ISNULL(A.[Total], 0)) * 1.00) / B.[Total] ELSE 0 END AS Total, 
                      CASE WHEN B.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / B.[202601] ELSE 0 END AS [202601], 
                      CASE WHEN B.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / B.[202602] ELSE 0 END AS [202602], 
                      CASE WHEN B.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / B.[202603] ELSE 0 END AS [202603], 
                      CASE WHEN B.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / B.[202604] ELSE 0 END AS [202604], 
                      CASE WHEN B.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / B.[202605] ELSE 0 END AS [202605], 
                      CASE WHEN B.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / B.[202606] ELSE 0 END AS [202606], 
                      CASE WHEN B.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / B.[202607] ELSE 0 END AS [202607], 
                      CASE WHEN B.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / B.[202608] ELSE 0 END AS [202608], 
                      CASE WHEN B.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / B.[202609] ELSE 0 END AS [202609], 
                      CASE WHEN B.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / B.[202610] ELSE 0 END AS [202610], 
                      CASE WHEN B.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / B.[202611] ELSE 0 END AS [202611], 
                      CASE WHEN B.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / B.[202612] ELSE 0 END AS [202612]
FROM         (
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     Variable IN ('Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                      'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                      'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento', 
                      'Centro Quirúrgico -  Salas Quirúrgicas Funcionales')) AS CEN LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, SUM(Total) AS Total, SUM([202601]) AS [202601], SUM([202602]) AS [202602], SUM([202603]) AS [202603], 
                                                   SUM([202604]) AS [202604], SUM([202605]) AS [202605], SUM([202606]) AS [202606], SUM([202607]) AS [202607], SUM([202608]) AS [202608], 
                                                   SUM([202609]) AS [202609], SUM([202610]) AS [202610], SUM([202611]) AS [202611], SUM([202612]) AS [202612]
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
                            WHERE      (Variable IN ('Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 
                                                   'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 
                                                   'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'))
                            GROUP BY Red, Centro, nivel, codcentro, Año) AS A ON CEN.codcentro = A.codcentro LEFT OUTER JOIN
                          (SELECT     Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
                                                   [202609], [202610], [202611], [202612], Variable
                            FROM          pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026 AS CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026_1
                            WHERE      Variable IN ('Centro Quirúrgico -  Salas Quirúrgicas Funcionales')) AS B ON CEN.codcentro = B.codcentro LEFT OUTER JOIN
                          (SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , est.aceptmenos , cen.codcentro, cen.centro, cen.tipo, cen.nivel, cen.categoria
                           FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
                           JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
                           WHERE est.indicador = 'Rendimiento de Sala de Operaciones' AND est.periodo = '202608') AS D ON CEN.codcentro = D.codcentro




/**correr el archivo 
01_TMI_PROCESAMIENTO_GENERAL_2026_f.sql
**/







                      