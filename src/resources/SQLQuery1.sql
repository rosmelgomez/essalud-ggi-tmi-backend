
/*  CE_Concent - Concentracion de Consultas*/

DECLARE @Periodo CHAR(6) = '202608';          -- <-- único punto que cambias
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);

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
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Consultas')
UNION
SELECT DISTINCT Red, codcentro, Centro
FROM         pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
WHERE     variable IN ('Consulta Externa - Consultantes al Establecimiento'))
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 

    -- Total dinámico: suma solo los meses 1..@Mes
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
    CASE WHEN A.[202601] = 0 OR B.[202601] = 0 THEN 0 ELSE (A.[202601] * 1.00) / B.[202601] END AS [202601], CASE WHEN A.[202602] = 0 OR
  B.[202602] = 0 THEN 0 ELSE ((A.[202601] + A.[202602]) * 1.00) / (B.[202601] + B.[202602]) END AS [202602], CASE WHEN A.[202603] = 0 OR
  B.[202603] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603]) * 1.00) / (B.[202601] + B.[202602] + B.[202603]) END AS [202603], CASE WHEN A.[202604] = 0 OR
  B.[202604] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604]) END AS [202604], CASE WHEN A.[202605] = 0 OR
  B.[202605] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605]) END AS [202605], CASE WHEN A.[202606] = 0 OR
  B.[202606] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606]) END AS [202606], CASE WHEN A.[202607] = 0 OR
  B.[202607] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607]) END AS [202607], CASE WHEN A.[202608] = 0 OR
  B.[202608] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608]) END AS [202608], CASE WHEN A.[202609] = 0 OR
  B.[202609] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609]) END AS [202609], CASE WHEN A.[202610] = 0 OR
  B.[202610] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610]) END AS [202610], CASE WHEN A.[202611] = 0 OR
  B.[202611] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611]) END AS [202611], CASE WHEN A.[202612] = 0 OR
  B.[202612] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]+ A.[202612]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611] + B.[202612]) END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept, cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
    FROM pentahodev_prueba.dbo.tmi_estandar_nivel est
    JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.nivel_centro = cen.nivel AND est.periodo = cen.periodo
    WHERE est.indicador = 'Concentracion de Consultas' AND est.periodo = @Periodo
) AS D ON CEN.codcentro = D.codcentro


/* CE_GCHProg - Grado de Cumplimiento de Horas Programadas*/

DECLARE @Periodo CHAR(6) = '202608';          -- <-- único punto que cambias
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);

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
WHERE     variable IN ('Consulta Externa - Horas Médicas Programadas'))
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 

    -- Total dinámico: suma solo los meses 1..@Mes
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
    CASE WHEN A.[202601] = 0 OR B.[202601] = 0 THEN 0 ELSE (A.[202601] * 1.00) / B.[202601] END AS [202601], CASE WHEN A.[202602] = 0 OR
  B.[202602] = 0 THEN 0 ELSE ((A.[202601] + A.[202602]) * 1.00) / (B.[202601] + B.[202602]) END AS [202602], CASE WHEN A.[202603] = 0 OR
  B.[202603] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603]) * 1.00) / (B.[202601] + B.[202602] + B.[202603]) END AS [202603], CASE WHEN A.[202604] = 0 OR
  B.[202604] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604]) END AS [202604], CASE WHEN A.[202605] = 0 OR
  B.[202605] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605]) END AS [202605], CASE WHEN A.[202606] = 0 OR
  B.[202606] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606]) END AS [202606], CASE WHEN A.[202607] = 0 OR
  B.[202607] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607]) END AS [202607], CASE WHEN A.[202608] = 0 OR
  B.[202608] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608]) END AS [202608], CASE WHEN A.[202609] = 0 OR
  B.[202609] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609]) END AS [202609], CASE WHEN A.[202610] = 0 OR
  B.[202610] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610]) END AS [202610], CASE WHEN A.[202611] = 0 OR
  B.[202611] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611]) END AS [202611], CASE WHEN A.[202612] = 0 OR
  B.[202612] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]+ A.[202612]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611] + B.[202612]) END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
    FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
    WHERE est.indicador = 'Grado de Cumplimiento de Horas Programadas' AND est.periodo = @Periodo
) AS D ON CEN.codcentro = D.codcentro

/*CE_Recetas - Promedio de Recetas por Consultas */

DECLARE @Periodo CHAR(6) = '202608';          -- <-- único punto que cambias
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);

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
WHERE     variable IN ('Consulta Externa - Horas Médicas Programadas'))
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 

    -- Total dinámico: suma solo los meses 1..@Mes
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
    CASE WHEN A.[202601] = 0 OR B.[202601] = 0 THEN 0 ELSE (A.[202601] * 1.00) / B.[202601] END AS [202601], CASE WHEN A.[202602] = 0 OR
  B.[202602] = 0 THEN 0 ELSE ((A.[202601] + A.[202602]) * 1.00) / (B.[202601] + B.[202602]) END AS [202602], CASE WHEN A.[202603] = 0 OR
  B.[202603] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603]) * 1.00) / (B.[202601] + B.[202602] + B.[202603]) END AS [202603], CASE WHEN A.[202604] = 0 OR
  B.[202604] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604]) END AS [202604], CASE WHEN A.[202605] = 0 OR
  B.[202605] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605]) END AS [202605], CASE WHEN A.[202606] = 0 OR
  B.[202606] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606]) END AS [202606], CASE WHEN A.[202607] = 0 OR
  B.[202607] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607]) END AS [202607], CASE WHEN A.[202608] = 0 OR
  B.[202608] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608]) END AS [202608], CASE WHEN A.[202609] = 0 OR
  B.[202609] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609]) END AS [202609], CASE WHEN A.[202610] = 0 OR
  B.[202610] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610]) END AS [202610], CASE WHEN A.[202611] = 0 OR
  B.[202611] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611]) END AS [202611], CASE WHEN A.[202612] = 0 OR
  B.[202612] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]+ A.[202612]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611] + B.[202612]) END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
    FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
    WHERE est.indicador = 'Promedio de Recetas por Consultas' AND est.periodo = @Periodo
) AS D ON CEN.codcentro = D.codcentro

/* CE_RHrMedico - Rendimiento Hora Medico */

DECLARE @Periodo CHAR(6) = '202608';          -- <-- único punto que cambias
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);

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
WHERE     variable IN ('Consulta Externa - Horas Médicas Programadas'))
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 

    -- Total dinámico: suma solo los meses 1..@Mes
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
    CASE WHEN A.[202601] = 0 OR B.[202601] = 0 THEN 0 ELSE (A.[202601] * 1.00) / B.[202601] END AS [202601], CASE WHEN A.[202602] = 0 OR
  B.[202602] = 0 THEN 0 ELSE ((A.[202601] + A.[202602]) * 1.00) / (B.[202601] + B.[202602]) END AS [202602], CASE WHEN A.[202603] = 0 OR
  B.[202603] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603]) * 1.00) / (B.[202601] + B.[202602] + B.[202603]) END AS [202603], CASE WHEN A.[202604] = 0 OR
  B.[202604] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604]) END AS [202604], CASE WHEN A.[202605] = 0 OR
  B.[202605] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605]) END AS [202605], CASE WHEN A.[202606] = 0 OR
  B.[202606] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606]) END AS [202606], CASE WHEN A.[202607] = 0 OR
  B.[202607] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607]) END AS [202607], CASE WHEN A.[202608] = 0 OR
  B.[202608] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608]) END AS [202608], CASE WHEN A.[202609] = 0 OR
  B.[202609] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609]) END AS [202609], CASE WHEN A.[202610] = 0 OR
  B.[202610] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610]) END AS [202610], CASE WHEN A.[202611] = 0 OR
  B.[202611] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611]) END AS [202611], CASE WHEN A.[202612] = 0 OR
  B.[202612] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]+ A.[202612]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611] + B.[202612]) END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
    FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
    WHERE est.indicador = 'Promedio de Recetas por Consultas' AND est.periodo = @Periodo
) AS D ON CEN.codcentro = D.codcentro



/*CE_RHrMedico - Rendimiento Hora Medico */

DECLARE @Periodo CHAR(6) = '202607';          -- <-- único punto que cambias
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);

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
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 

    -- Total dinámico: suma solo los meses 1..@Mes
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
    WHERE est.indicador = 'Rendimiento Hora Medico' AND est.periodo = @Periodo
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo NOT IN ('CNSR','IPO','INCOR')


/* Em_PrioI_II - % Prioridad I y II con respecto al Total de Emergencias */

DECLARE @Periodo CHAR(6) = '202607';          -- <-- único punto que cambias
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable IN ('Emergencia - Prioridad I', 'Emergencia - Prioridad II')
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
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 

    -- Total dinámico: suma solo los meses 1..@Mes
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
    CASE WHEN X.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) 
                      / X.[202601] ELSE 0 END AS [202601], CASE WHEN X.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / X.[202602] ELSE 0 END AS [202602], 
                      CASE WHEN X.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / X.[202603] ELSE 0 END AS [202603], CASE WHEN X.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) 
                      * 1.00) / X.[202604] ELSE 0 END AS [202604], CASE WHEN X.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / X.[202605] ELSE 0 END AS [202605], 
                      CASE WHEN X.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / X.[202606] ELSE 0 END AS [202606], CASE WHEN X.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) 
                      * 1.00) / X.[202607] ELSE 0 END AS [202607], CASE WHEN X.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / X.[202608] ELSE 0 END AS [202608], 
                      CASE WHEN X.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / X.[202609] ELSE 0 END AS [202609], CASE WHEN X.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) 
                      * 1.00) / X.[202610] ELSE 0 END AS [202610], CASE WHEN X.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / X.[202611] ELSE 0 END AS [202611], 
                      CASE WHEN X.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / X.[202612] ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN X ON CEN.codcentro = X.codcentro
LEFT OUTER JOIN (
    SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
    FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
    WHERE est.indicador = '% Prioridad I y II con respecto al Total de Emergencias' AND est.periodo = @Periodo
) AS D ON CEN.codcentro = D.codcentro

/* Em_PrioIV_V % Prioridad IV y V con respecto al Total de Emergencias -- corroborar*/

DECLARE @Periodo CHAR(6) = '202607';          -- <-- único punto que cambias
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);

WITH A AS (
    SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden,
           [202601],[202602],[202603],[202604],[202605],[202606],
           [202607],[202608],[202609],[202610],[202611],[202612], Variable
    FROM pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
    WHERE Variable IN ('Emergencia - Prioridad IV', 'Emergencia - Prioridad V')
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
WHERE     (Variable IN ('Emergencia - Prioridad IV', 'Emergencia - Prioridad V', 'Emergencia - Total de Atenciones')))
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 

    -- Total dinámico: suma solo los meses 1..@Mes
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
     CASE WHEN X.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) 
     / X.[202601] ELSE 0 END AS [202601], CASE WHEN X.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / X.[202602] ELSE 0 END AS [202602], 
                      CASE WHEN X.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / X.[202603] ELSE 0 END AS [202603], CASE WHEN X.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) 
                      * 1.00) / X.[202604] ELSE 0 END AS [202604], CASE WHEN X.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / X.[202605] ELSE 0 END AS [202605], 
                      CASE WHEN X.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / X.[202606] ELSE 0 END AS [202606], CASE WHEN X.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) 
                      * 1.00) / X.[202607] ELSE 0 END AS [202607], CASE WHEN X.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / X.[202608] ELSE 0 END AS [202608], 
                      CASE WHEN X.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / X.[202609] ELSE 0 END AS [202609], CASE WHEN X.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) 
                      * 1.00) / X.[202610] ELSE 0 END AS [202610], CASE WHEN X.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / X.[202611] ELSE 0 END AS [202611], 
                      CASE WHEN X.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / X.[202612] ELSE 0 END AS [202612]
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN X ON CEN.codcentro = X.codcentro
LEFT OUTER JOIN (
    SElECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept , cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
    FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
    WHERE est.indicador = '% Prioridad IV y V con respecto al Total de Emergencias' AND est.periodo = @Periodo
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo IN ('H.N.', 'H.IV', 'H.III', 'H.II', 'H.I')




/* H_Estancias - Promedio Dia Estancia */


DECLARE @Periodo CHAR(6) = '202607';          -- <-- único punto que cambias
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);

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
WHERE     variable IN ('Hospitalizacion - Egresos'))
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 

    -- Total dinámico: suma solo los meses 1..@Mes
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
    CASE WHEN A.[202601] = 0 OR B.[202601] = 0 THEN 0 ELSE (A.[202601] * 1.00) / B.[202601] END AS [202601], CASE WHEN A.[202602] = 0 OR
  B.[202602] = 0 THEN 0 ELSE ((A.[202601] + A.[202602]) * 1.00) / (B.[202601] + B.[202602]) END AS [202602], CASE WHEN A.[202603] = 0 OR
  B.[202603] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603]) * 1.00) / (B.[202601] + B.[202602] + B.[202603]) END AS [202603], CASE WHEN A.[202604] = 0 OR
  B.[202604] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604]) END AS [202604], CASE WHEN A.[202605] = 0 OR
  B.[202605] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605]) END AS [202605], CASE WHEN A.[202606] = 0 OR
  B.[202606] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606]) END AS [202606], CASE WHEN A.[202607] = 0 OR
  B.[202607] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607]) END AS [202607], CASE WHEN A.[202608] = 0 OR
  B.[202608] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608]) END AS [202608], CASE WHEN A.[202609] = 0 OR
  B.[202609] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609]) END AS [202609], CASE WHEN A.[202610] = 0 OR
  B.[202610] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610]) END AS [202610], CASE WHEN A.[202611] = 0 OR
  B.[202611] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611]) END AS [202611], CASE WHEN A.[202612] = 0 OR
  B.[202612] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]+ A.[202612]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611] + B.[202612]) END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept, cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
    FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
    WHERE est.indicador = 'Promedio Dia Estancia' AND est.periodo = @Periodo
) AS D ON CEN.codcentro = D.codcentro

/* H_ISust - Intervalo de Sustitución */






/* H_OCama - Porcentaje de Ocupación de Cama */

DECLARE @Periodo CHAR(6) = '202608';          -- <-- único punto que cambias
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);

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
WHERE     variable IN ('Hospitalizacion - Días Cama Disponible'))
SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 

    -- Total dinámico: suma solo los meses 1..@Mes
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

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept, cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
    FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
    WHERE est.indicador = 'Porcentaje de Ocupación de Cama' AND est.periodo = @Periodo
) AS D ON CEN.codcentro = D.codcentro


/* H_RCama -  Rendimiento Cama */
DECLARE @Periodo CHAR(6) = '202608';          -- <-- único punto que cambias
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);

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
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.acept AS [% Acept], 

    -- Total dinámico: suma solo los meses 1..@Mes
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
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT cen.id, est.tipo AS tipo_indicador, est.indicador, est.estandar, est.acept, cen.codcentro, cen.centro, cen.nivel, cen.tipo, cen.categoria
    FROM pentahodev_prueba.dbo.tmi_estandar_tipo est
    JOIN pentahodev_prueba.dbo.tmi_centro cen ON est.tipo_centro = cen.tipo AND est.periodo = cen.periodo
    WHERE est.indicador = 'Rendimiento Cama' AND est.periodo = @Periodo
) AS D ON CEN.codcentro = D.codcentro

/* H_TBMHosp - Tasa Neta de Mortalidad Hospitalaria*/


/* O_Concent - */



/* O_GCHOdon -  */












