

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

-- (repite el mismo bloque de Total dinámico en el segundo SELECT del UNION ALL,
--  cambiando CEN_TIPO, tmi_estandar_tipo/tipo_centro y WHERE D.tipo IN (...))

ORDER BY ORDEN;