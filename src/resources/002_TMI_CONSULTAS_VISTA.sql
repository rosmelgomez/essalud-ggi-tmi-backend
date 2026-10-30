/*  CE_Concent - Concentracion de Consultas*/

DECLARE @Periodo CHAR(6) = '202608';         
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
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
        ) <> 0
        THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
        ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
        )
        ELSE 0 
    END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN A.[202601] = 0 OR B.[202601] = 0 THEN 0 ELSE (A.[202601] * 1.00) / B.[202601] END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN A.[202602] = 0 OR B.[202602] = 0 THEN 0 ELSE ((A.[202601] + A.[202602]) * 1.00) / (B.[202601] + B.[202602]) END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN A.[202603] = 0 OR B.[202603] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603]) * 1.00) / (B.[202601] + B.[202602] + B.[202603]) END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN A.[202604] = 0 OR B.[202604] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604]) END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN A.[202605] = 0 OR B.[202605] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605]) END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN A.[202606] = 0 OR B.[202606] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606]) END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN A.[202607] = 0 OR B.[202607] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607]) END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN A.[202608] = 0 OR B.[202608] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608]) END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN A.[202609] = 0 OR B.[202609] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609]) END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN A.[202610] = 0 OR B.[202610] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610]) END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN A.[202611] = 0 OR B.[202611] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611]) END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN A.[202612] = 0 OR B.[202612] = 0 THEN 0 ELSE ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611] + A.[202612]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611] + B.[202612]) END ELSE 0 END AS [202612]
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (        
SELECT cen.id,
       g.descripcion AS tipo_indicador,
       est.indicador,
       CASE @Mes
         WHEN 1  THEN en.est_01
         WHEN 2  THEN en.est_02
         WHEN 3  THEN en.est_03
         WHEN 4  THEN en.est_04
         WHEN 5  THEN en.est_05
         WHEN 6  THEN en.est_06
         WHEN 7  THEN en.est_07
         WHEN 8  THEN en.est_08
         WHEN 9  THEN en.est_09
         WHEN 10 THEN en.est_10
         WHEN 11 THEN en.est_11
         WHEN 12 THEN en.est_12 
        END AS estandar,
       cen.codcentro, cen.centro, cen.red, cen.nivel, cen.tipo, cen.categoria,
       exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04, exc.excl_05, exc.excl_06,
       exc.excl_07, exc.excl_08, exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
FROM pentahodev_prueba.dbo.tmi_estandar_nivel en
JOIN pentahodev_prueba.dbo.tmi_indicador est ON est.id = en.id_indicador
LEFT JOIN pentahodev_prueba.dbo.tmi_grupo g  ON g.id = est.grupo
JOIN pentahodev_prueba.dbo.tmi_centro cen    ON cen.nivel = en.nivel_centro
LEFT JOIN pentahodev_prueba.dbo.tmi_exclusion_centro_estandar exc
       ON exc.id_centro = cen.id AND exc.anio = @Anio
      AND (exc.id_indicador = est.id OR exc.id_indicador IS NULL)
WHERE en.id_indicador = 1 AND en.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
ORDER BY ORDEN asc;


/* CE_GCHProg - Grado de Cumplimiento de Horas Programadas*/
DECLARE @PERIODOI INT = 202601;
DECLARE @PERIODOf INT = 202608;
DECLARE @RED INT=0;
DECLARE @CENTRO INT=0;

DECLARE @Periodo CHAR(6) = '202608';         
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
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.95 AS [% Acept],
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
        SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar 
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Grado de Cumplimiento de Horas Programadas' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;


/*CE_Recetas - Promedio de Recetas por Consultas */

DECLARE @Periodo CHAR(6) = '202609';         
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
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 1.1 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL((ISNULL(A.[202601],0) * 1.00) / NULLIF(ISNULL(B.[202601],0),0),0) ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL((ISNULL(A.[202602],0) * 1.00) / NULLIF(ISNULL(B.[202602],0),0),0) ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL((ISNULL(A.[202603],0) * 1.00) / NULLIF(ISNULL(B.[202603],0),0),0) ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL((ISNULL(A.[202604],0) * 1.00) / NULLIF(ISNULL(B.[202604],0),0),0) ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL((ISNULL(A.[202605],0) * 1.00) / NULLIF(ISNULL(B.[202605],0),0),0) ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL((ISNULL(A.[202606],0) * 1.00) / NULLIF(ISNULL(B.[202606],0),0),0) ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL((ISNULL(A.[202607],0) * 1.00) / NULLIF(ISNULL(B.[202607],0),0),0) ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL((ISNULL(A.[202608],0) * 1.00) / NULLIF(ISNULL(B.[202608],0),0),0) ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL((ISNULL(A.[202609],0) * 1.00) / NULLIF(ISNULL(B.[202609],0),0),0) ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL((ISNULL(A.[202610],0) * 1.00) / NULLIF(ISNULL(B.[202610],0),0),0) ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL((ISNULL(A.[202611],0) * 1.00) / NULLIF(ISNULL(B.[202611],0),0),0) ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL((ISNULL(A.[202612],0) * 1.00) / NULLIF(ISNULL(B.[202612],0),0),0) ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar 
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Promedio de Recetas por Consultas' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;


/*CE_RHrMedico - Rendimiento Hora Medico */

DECLARE @Periodo CHAR(6) = '202608';         
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
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.9  AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN_NIVEL AS CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_nivel.est_01
            WHEN 2  THEN est_nivel.est_02
            WHEN 3  THEN est_nivel.est_03
            WHEN 4  THEN est_nivel.est_04
            WHEN 5  THEN est_nivel.est_05
            WHEN 6  THEN est_nivel.est_06
            WHEN 7  THEN est_nivel.est_07
            WHEN 8  THEN est_nivel.est_08
            WHEN 9  THEN est_nivel.est_09
            WHEN 10 THEN est_nivel.est_10
            WHEN 11 THEN est_nivel.est_11
            WHEN 12 THEN est_nivel.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_nivel est_nivel
    JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_nivel.id_estandar
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_nivel.nivel_centro = cen.nivel
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Rendimiento Hora Medico' AND est_nivel.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo NOT IN ('CNSR','IPO','INCOR')

UNION ALL

SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar *0.9 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / 
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
        
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

    FROM CEN_TIPO AS CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Rendimiento Hora Medico' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo IN ('CNSR','IPO','INCOR')
ORDER BY ORDEN;


/* Em_PrioI_II - % Prioridad I y II con respecto al Total de Emergencias */

DECLARE @Periodo CHAR(6) = '202609';         
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
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(X.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(X.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN X.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / X.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN X.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / X.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN X.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / X.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN X.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / X.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN X.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / X.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN X.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / X.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN X.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / X.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN X.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / X.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN X.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / X.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN X.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / X.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN X.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / X.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN X.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / X.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN X ON CEN.codcentro = X.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = '% Prioridad I y II con respecto al Total de Emergencias' AND est_tipo.anio = @Anio
 ) AS D ON CEN.codcentro = D.codcentro;


/* Em_PrioIV_V - % Prioridad IV y V con respecto al Total de Emergencias */

DECLARE @Periodo CHAR(6) = '202609';         
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
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar* 1.2 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(X.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(X.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN X.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / X.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN X.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / X.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN X.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / X.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN X.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / X.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN X.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / X.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN X.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / X.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN X.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / X.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN X.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / X.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN X.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / X.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN X.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / X.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN X.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / X.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN X.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / X.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN X ON CEN.codcentro = X.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar
    JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = '% Prioridad IV y V con respecto al Total de Emergencias' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo IN ('H.N.', 'H.IV', 'H.III', 'H.II', 'H.I');

/* H_Estancias - Promedio Dia Estancia */

DECLARE @Periodo CHAR(6) = '202609';         
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
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Promedio Dia Estancia' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;

/* H_ISust - Intervalo de Sustitución */

DECLARE @Periodo CHAR(6) = '202609';         
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
            CASE WHEN @Mes>=1  AND (D.excl_01 = 1 OR D.excl_01 IS NULL) THEN ISNULL(x.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 1 OR D.excl_02 IS NULL) THEN ISNULL(x.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 1 OR D.excl_03 IS NULL) THEN ISNULL(x.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 1 OR D.excl_04 IS NULL) THEN ISNULL(x.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 1 OR D.excl_05 IS NULL) THEN ISNULL(x.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 1 OR D.excl_06 IS NULL) THEN ISNULL(x.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 1 OR D.excl_07 IS NULL) THEN ISNULL(x.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 1 OR D.excl_08 IS NULL) THEN ISNULL(x.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 1 OR D.excl_09 IS NULL) THEN ISNULL(x.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 1 OR D.excl_10 IS NULL) THEN ISNULL(x.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 1 OR D.excl_11 IS NULL) THEN ISNULL(x.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 1 OR D.excl_12 IS NULL) THEN ISNULL(x.[202612],0) ELSE 0 END
         ) <> 0
    THEN ((
            CASE WHEN @Mes>=1  AND (D.excl_01 = 1 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 1 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 1 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 1 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 1 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 1 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 1 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 1 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 1 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 1 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 1 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 1 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) - (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 1 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 1 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 1 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 1 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 1 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 1 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 1 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 1 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 1 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 1 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 1 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 1 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 1 OR D.excl_01 IS NULL) THEN ISNULL(x.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 1 OR D.excl_02 IS NULL) THEN ISNULL(x.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 1 OR D.excl_03 IS NULL) THEN ISNULL(x.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 1 OR D.excl_04 IS NULL) THEN ISNULL(x.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 1 OR D.excl_05 IS NULL) THEN ISNULL(x.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 1 OR D.excl_06 IS NULL) THEN ISNULL(x.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 1 OR D.excl_07 IS NULL) THEN ISNULL(x.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 1 OR D.excl_08 IS NULL) THEN ISNULL(x.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 1 OR D.excl_09 IS NULL) THEN ISNULL(x.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 1 OR D.excl_10 IS NULL) THEN ISNULL(x.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 1 OR D.excl_11 IS NULL) THEN ISNULL(x.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 1 OR D.excl_12 IS NULL) THEN ISNULL(x.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 1 OR D.excl_01 IS NULL) THEN CASE WHEN x.[202601] <> 0 THEN ((isnull(A.[202601], 0) - isnull(B.[202601], 0)) * 1.00) / x.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 1 OR D.excl_02 IS NULL) THEN CASE WHEN x.[202602] <> 0 THEN ((isnull(A.[202602], 0) - isnull(B.[202602], 0)) * 1.00) / x.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 1 OR D.excl_03 IS NULL) THEN CASE WHEN x.[202603] <> 0 THEN ((isnull(A.[202603], 0) - isnull(B.[202603], 0)) * 1.00) / x.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 1 OR D.excl_04 IS NULL) THEN CASE WHEN x.[202604] <> 0 THEN ((isnull(A.[202604], 0) - isnull(B.[202604], 0)) * 1.00) / x.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 1 OR D.excl_05 IS NULL) THEN CASE WHEN x.[202605] <> 0 THEN ((isnull(A.[202605], 0) - isnull(B.[202605], 0)) * 1.00) / x.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 1 OR D.excl_06 IS NULL) THEN CASE WHEN x.[202606] <> 0 THEN ((isnull(A.[202606], 0) - isnull(B.[202606], 0)) * 1.00) / x.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 1 OR D.excl_07 IS NULL) THEN CASE WHEN x.[202607] <> 0 THEN ((isnull(A.[202607], 0) - isnull(B.[202607], 0)) * 1.00) / x.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 1 OR D.excl_08 IS NULL) THEN CASE WHEN x.[202608] <> 0 THEN ((isnull(A.[202608], 0) - isnull(B.[202608], 0)) * 1.00) / x.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 1 OR D.excl_09 IS NULL) THEN CASE WHEN x.[202609] <> 0 THEN ((isnull(A.[202609], 0) - isnull(B.[202609], 0)) * 1.00) / x.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 1 OR D.excl_10 IS NULL) THEN CASE WHEN x.[202610] <> 0 THEN ((isnull(A.[202610], 0) - isnull(B.[202610], 0)) * 1.00) / x.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 1 OR D.excl_11 IS NULL) THEN CASE WHEN x.[202611] <> 0 THEN ((isnull(A.[202611], 0) - isnull(B.[202611], 0)) * 1.00) / x.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 1 OR D.excl_12 IS NULL) THEN CASE WHEN x.[202612] <> 0 THEN ((isnull(A.[202612], 0) - isnull(B.[202612], 0)) * 1.00) / x.[202612] ELSE 0 END ELSE 0 END AS [202612]

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
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Intervalo de Sustitución' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;

/* H_OCama - Porcentaje de Ocupación de Cama */

DECLARE @Periodo CHAR(6) = '202609';         
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
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.tipo AS TIPO, D.estandar AS Estandar,  D.estandar + 0.05 AS [% Acept], D.estandar - 0.05 AS [% Aceptmenos],
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Porcentaje de Ocupación de Cama' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;

/* H_RCama -  Rendimiento Cama */

DECLARE @Periodo CHAR(6) = '202609';         
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
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00  / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Rendimiento Cama' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;

/* H_TBMHosp - Tasa Neta de Mortalidad Hospitalaria*/

DECLARE @Periodo CHAR(6) = '202609';         
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
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) - (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(x.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(x.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(x.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(x.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(x.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(x.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(x.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(x.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(x.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(x.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(x.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(x.[202612],0) ELSE 0 END
         )
         <> 0
    THEN ((
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN (ISNULL(A.[202601],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN (ISNULL(A.[202602],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN (ISNULL(A.[202603],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN (ISNULL(A.[202604],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN (ISNULL(A.[202605],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN (ISNULL(A.[202606],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN (ISNULL(A.[202607],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN (ISNULL(A.[202608],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN (ISNULL(A.[202609],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN (ISNULL(A.[202610],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN (ISNULL(A.[202611],0))* 1.00 ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN (ISNULL(A.[202612],0))* 1.00 ELSE 0 END
         ) / ((
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) - (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(x.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(x.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(x.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(x.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(x.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(x.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(x.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(x.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(x.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(x.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(x.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(x.[202612],0) ELSE 0 END
         )))
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL)THEN CASE WHEN (isnull(B.[202601], 0) - isnull(x.[202601], 0)) <> 0 THEN ((isnull(A.[202601], 0)) * 1.00) / (isnull(B.[202601], 0) - isnull(x.[202601], 0)) ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL)THEN CASE WHEN (isnull(B.[202602], 0) - isnull(x.[202602], 0)) <> 0 THEN ((isnull(A.[202602], 0)) * 1.00) / (isnull(B.[202602], 0) - isnull(x.[202602], 0)) ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL)THEN CASE WHEN (isnull(B.[202603], 0) - isnull(x.[202603], 0)) <> 0 THEN ((isnull(A.[202603], 0)) * 1.00) / (isnull(B.[202603], 0) - isnull(x.[202603], 0)) ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL)THEN CASE WHEN (isnull(B.[202604], 0) - isnull(x.[202604], 0)) <> 0 THEN ((isnull(A.[202604], 0)) * 1.00) / (isnull(B.[202604], 0) - isnull(x.[202604], 0)) ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL)THEN CASE WHEN (isnull(B.[202605], 0) - isnull(x.[202605], 0)) <> 0 THEN ((isnull(A.[202605], 0)) * 1.00) / (isnull(B.[202605], 0) - isnull(x.[202605], 0)) ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL)THEN CASE WHEN (isnull(B.[202606], 0) - isnull(x.[202606], 0)) <> 0 THEN ((isnull(A.[202606], 0)) * 1.00) / (isnull(B.[202606], 0) - isnull(x.[202606], 0)) ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL)THEN CASE WHEN (isnull(B.[202607], 0) - isnull(x.[202607], 0)) <> 0 THEN ((isnull(A.[202607], 0)) * 1.00) / (isnull(B.[202607], 0) - isnull(x.[202607], 0)) ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL)THEN CASE WHEN (isnull(B.[202608], 0) - isnull(x.[202608], 0)) <> 0 THEN ((isnull(A.[202608], 0)) * 1.00) / (isnull(B.[202608], 0) - isnull(x.[202608], 0)) ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL)THEN CASE WHEN (isnull(B.[202609], 0) - isnull(x.[202609], 0)) <> 0 THEN ((isnull(A.[202609], 0)) * 1.00) / (isnull(B.[202609], 0) - isnull(x.[202609], 0)) ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL)THEN CASE WHEN (isnull(B.[202610], 0) - isnull(x.[202610], 0)) <> 0 THEN ((isnull(A.[202610], 0)) * 1.00) / (isnull(B.[202610], 0) - isnull(x.[202610], 0)) ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL)THEN CASE WHEN (isnull(B.[202611], 0) - isnull(x.[202611], 0)) <> 0 THEN ((isnull(A.[202611], 0)) * 1.00) / (isnull(B.[202611], 0) - isnull(x.[202611], 0)) ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL)THEN CASE WHEN (isnull(B.[202612], 0) - isnull(x.[202612], 0)) <> 0 THEN ((isnull(A.[202612], 0)) * 1.00) / (isnull(B.[202612], 0) - isnull(x.[202612], 0)) ELSE 0 END ELSE 0 END AS [202612]

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
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo 
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Tasa Neta de Mortalidad Hospitalaria' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;

/* O_Concent - Concentración de Sesiones Odontológicas*/

DECLARE @Periodo CHAR(6) = '202609';         
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
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN A.[202601] <> 0 OR B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN A.[202602] <> 0 OR B.[202602] <> 0 THEN ((A.[202601] + A.[202602]) * 1.00) / (B.[202601] + B.[202602]) ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN A.[202603] <> 0 OR B.[202603] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603]) * 1.00) / (B.[202601] + B.[202602] + B.[202603]) ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN A.[202604] <> 0 OR B.[202604] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604]) ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN A.[202605] <> 0 OR B.[202605] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605]) ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN A.[202606] <> 0 OR B.[202606] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606]) ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN A.[202607] <> 0 OR B.[202607] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607]) ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN A.[202608] <> 0 OR B.[202608] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608]) ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN A.[202609] <> 0 OR B.[202609] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609]) ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN A.[202610] <> 0 OR B.[202610] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610]) ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN A.[202611] <> 0 OR B.[202611] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611]) ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN A.[202612] <> 0 OR B.[202612] <> 0 THEN ((A.[202601] + A.[202602] + A.[202603] + A.[202604] + A.[202605] + A.[202606] + A.[202607] + A.[202608] + A.[202609] + A.[202610] + A.[202611] + A.[202612]) * 1.00) / (B.[202601] + B.[202602] + B.[202603] + B.[202604] + B.[202605] + B.[202606] + B.[202607] + B.[202608] + B.[202609] + B.[202610] + B.[202611] + B.[202612]) ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT
       cen.id,
       g.descripcion AS tipo_indicador,
       est.indicador, 
        CASE @Mes
            WHEN 1  THEN en.est_01
            WHEN 2  THEN en.est_02
            WHEN 3  THEN en.est_03
            WHEN 4  THEN en.est_04
            WHEN 5  THEN en.est_05
            WHEN 6  THEN en.est_06
            WHEN 7  THEN en.est_07
            WHEN 8  THEN en.est_08
            WHEN 9  THEN en.est_09
            WHEN 10 THEN en.est_10
            WHEN 11 THEN en.est_11
            WHEN 12 THEN en.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
FROM pentahodev_prueba.dbo.tmi_estandar_nivel en
JOIN pentahodev_prueba.dbo.tmi_indicador est ON est.id = en.id_indicador
LEFT JOIN pentahodev_prueba.dbo.tmi_grupo g  ON g.id = est.grupo
JOIN pentahodev_prueba.dbo.tmi_centro cen    ON cen.nivel = en.nivel_centro
LEFT JOIN pentahodev_prueba.dbo.tmi_exclusion_centro_estandar exc
       ON exc.id_centro = cen.id AND exc.anio = @Anio
      AND (exc.id_indicador = est.id OR exc.id_indicador IS NULL)
WHERE en.id_indicador = 18 AND en.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;


cen.codcentro, cen.centro, cen.red, cen.nivel, cen.tipo, cen.categoria,
       exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04, exc.excl_05, exc.excl_06,
       exc.excl_07, exc.excl_08, exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
FROM pentahodev_prueba.dbo.tmi_estandar_nivel en
JOIN pentahodev_prueba.dbo.tmi_indicador est ON est.id = en.id_indicador
LEFT JOIN pentahodev_prueba.dbo.tmi_grupo g  ON g.id = est.grupo
JOIN pentahodev_prueba.dbo.tmi_centro cen    ON cen.nivel = en.nivel_centro
LEFT JOIN pentahodev_prueba.dbo.tmi_exclusion_centro_estandar exc
       ON exc.id_centro = cen.id AND exc.anio = @Anio
      AND (exc.id_indicador = est.id OR exc.id_indicador IS NULL)
WHERE en.id_indicador = 1 AND en.anio = @Anio

/* O_GCHOdon - Grado de Cumplimiento de Hora Odontólogo */

DECLARE @Periodo CHAR(6) = '202609';         
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
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
            CASE WHEN ( CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END) ELSE 0 END AS [202601],
            CASE WHEN ( CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END) ELSE 0 END AS [202602],
            CASE WHEN ( CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END) ELSE 0 END AS [202603],
            CASE WHEN ( CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END) ELSE 0 END AS [202604],
            CASE WHEN ( CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END) ELSE 0 END AS [202605],
            CASE WHEN ( CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END) ELSE 0 END AS [202606],
            CASE WHEN ( CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END) ELSE 0 END AS [202607],
            CASE WHEN ( CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END) ELSE 0 END AS [202608],
            CASE WHEN ( CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END) ELSE 0 END AS [202609],
            CASE WHEN ( CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL)  THEN ISNULL(B.[202610],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=10  THEN ISNULL(A.[202610],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=10  THEN ISNULL(B.[202610],0) ELSE 0 END) ELSE 0 END AS [202610],
            CASE WHEN ( CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL)  THEN ISNULL(B.[202611],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=11  THEN ISNULL(A.[202611],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=11  THEN ISNULL(B.[202611],0) ELSE 0 END) ELSE 0 END AS [202611],
            CASE WHEN ( CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL)  THEN ISNULL(B.[202612],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=12  THEN ISNULL(A.[202612],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=12  THEN ISNULL(B.[202612],0) ELSE 0 END) ELSE 0 END AS [202612]
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Grado de Cumplimiento de Hora Odontólogo' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;

/* O_HrOdont - Rendimiento de Hora Odontológica */

DECLARE @Periodo CHAR(6) = '202608';         
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
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]
FROM CEN_NIVEL AS CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_nivel.est_01
            WHEN 2  THEN est_nivel.est_02
            WHEN 3  THEN est_nivel.est_03
            WHEN 4  THEN est_nivel.est_04
            WHEN 5  THEN est_nivel.est_05
            WHEN 6  THEN est_nivel.est_06
            WHEN 7  THEN est_nivel.est_07
            WHEN 8  THEN est_nivel.est_08
            WHEN 9  THEN est_nivel.est_09
            WHEN 10 THEN est_nivel.est_10
            WHEN 11 THEN est_nivel.est_11
            WHEN 12 THEN est_nivel.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_nivel est_nivel
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_nivel.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_nivel.nivel_centro = cen.nivel
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Rendimiento Hora Odontológica' AND est_nivel.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo NOT IN ('CNSR','IPO','INCOR')

UNION ALL

SELECT DISTINCT
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar * 0.9 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (A.[202601] * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (A.[202602] * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (A.[202603] * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (A.[202604] * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (A.[202605] * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (A.[202606] * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (A.[202607] * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (A.[202608] * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (A.[202609] * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (A.[202610] * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (A.[202611] * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (A.[202612] * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]
FROM CEN_TIPO AS CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Rendimiento Hora Odontológica' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo IN ('CNSR','IPO','INCOR')
ORDER BY ORDEN;

/* O_NTOdontS - Número de trabajos Odontológicos por Sesión */

DECLARE @Periodo CHAR(6) = '202609';         
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
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
            CASE WHEN ( CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END) ELSE 0 END AS [202601],
            CASE WHEN ( CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END) ELSE 0 END AS [202602],
            CASE WHEN ( CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END) ELSE 0 END AS [202603],
            CASE WHEN ( CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END) ELSE 0 END AS [202604],
            CASE WHEN ( CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END) ELSE 0 END AS [202605],
            CASE WHEN ( CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END) ELSE 0 END AS [202606],
            CASE WHEN ( CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END) ELSE 0 END AS [202607],
            CASE WHEN ( CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END) ELSE 0 END AS [202608],
            CASE WHEN ( CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END) ELSE 0 END AS [202609],
            CASE WHEN ( CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL)  THEN ISNULL(B.[202610],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=10  THEN ISNULL(A.[202610],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=10  THEN ISNULL(B.[202610],0) ELSE 0 END) ELSE 0 END AS [202610],
            CASE WHEN ( CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL)  THEN ISNULL(B.[202611],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=11  THEN ISNULL(A.[202611],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=11  THEN ISNULL(B.[202611],0) ELSE 0 END) ELSE 0 END AS [202611],
            CASE WHEN ( CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL)  THEN ISNULL(B.[202612],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=12  THEN ISNULL(A.[202612],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=12  THEN ISNULL(B.[202612],0) ELSE 0 END) ELSE 0 END AS [202612]
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar =  est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Número de trabajos Odontológicos por Sesión' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE     (A.Total * 1.00 / B.Total IS NOT NULL);

/* Qx_GCHProg - Porcentaje de Horas Quirúrgicas Efectivas*/

DECLARE @Periodo CHAR(6) = '202608';         
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
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar - 0.1 AS [% Acept], 
    CASE WHEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (ISNULL(A.[202601], 0) * 1.00) / B.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (ISNULL(A.[202602], 0) * 1.00) / B.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (ISNULL(A.[202603], 0) * 1.00) / B.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (ISNULL(A.[202604], 0) * 1.00) / B.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (ISNULL(A.[202605], 0) * 1.00) / B.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (ISNULL(A.[202606], 0) * 1.00) / B.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (ISNULL(A.[202607], 0) * 1.00) / B.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (ISNULL(A.[202608], 0) * 1.00) / B.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (ISNULL(A.[202609], 0) * 1.00) / B.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (ISNULL(A.[202610], 0) * 1.00) / B.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (ISNULL(A.[202611], 0) * 1.00) / B.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (ISNULL(A.[202612], 0) * 1.00) / B.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Porcentaje de Horas Quirúrgicas Efectivas' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;

/* Qx_HTCesareas - Tasa de Cesáreas*/

DECLARE @Periodo CHAR(6) = '202609';         
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
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE NULL END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 AND A.[202601] <> 0 THEN (ISNULL(A.[202601], 0) * 1.00) / B.[202601] ELSE NULL END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 AND A.[202602] <> 0 THEN (ISNULL(A.[202602], 0) * 1.00) / B.[202602] ELSE NULL END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 AND A.[202603] <> 0 THEN (ISNULL(A.[202603], 0) * 1.00) / B.[202603] ELSE NULL END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 AND A.[202604] <> 0 THEN (ISNULL(A.[202604], 0) * 1.00) / B.[202604] ELSE NULL END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 AND A.[202605] <> 0 THEN (ISNULL(A.[202605], 0) * 1.00) / B.[202605] ELSE NULL END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 AND A.[202606] <> 0 THEN (ISNULL(A.[202606], 0) * 1.00) / B.[202606] ELSE NULL END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 AND A.[202607] <> 0 THEN (ISNULL(A.[202607], 0) * 1.00) / B.[202607] ELSE NULL END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 AND A.[202608] <> 0 THEN (ISNULL(A.[202608], 0) * 1.00) / B.[202608] ELSE NULL END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 AND A.[202609] <> 0 THEN (ISNULL(A.[202609], 0) * 1.00) / B.[202609] ELSE NULL END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 AND A.[202610] <> 0 THEN (ISNULL(A.[202610], 0) * 1.00) / B.[202610] ELSE NULL END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 AND A.[202611] <> 0 THEN (ISNULL(A.[202611], 0) * 1.00) / B.[202611] ELSE NULL END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 AND A.[202612] <> 0 THEN (ISNULL(A.[202612], 0) * 1.00) / B.[202612] ELSE NULL END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Tasa de Cesáreas' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;

/* Qx_IAlta - Porcentaje de Intervenciones de Alta Complejidad*/

DECLARE @Periodo CHAR(6) = '202609';         
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
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
            CASE WHEN ( CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END) ELSE 0 END AS [202601],
            CASE WHEN ( CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END) ELSE 0 END AS [202602],
            CASE WHEN ( CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END) ELSE 0 END AS [202603],
            CASE WHEN ( CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END) ELSE 0 END AS [202604],
            CASE WHEN ( CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END) ELSE 0 END AS [202605],
            CASE WHEN ( CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END) ELSE 0 END AS [202606],
            CASE WHEN ( CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END) ELSE 0 END AS [202607],
            CASE WHEN ( CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END) ELSE 0 END AS [202608],
            CASE WHEN ( CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END) ELSE 0 END AS [202609],
            CASE WHEN ( CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL)  THEN ISNULL(B.[202610],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=10  THEN ISNULL(A.[202610],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=10  THEN ISNULL(B.[202610],0) ELSE 0 END) ELSE 0 END AS [202610],
            CASE WHEN ( CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL)  THEN ISNULL(B.[202611],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=11  THEN ISNULL(A.[202611],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=11  THEN ISNULL(B.[202611],0) ELSE 0 END) ELSE 0 END AS [202611],
            CASE WHEN ( CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL)  THEN ISNULL(B.[202612],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=12  THEN ISNULL(A.[202612],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=12  THEN ISNULL(B.[202612],0) ELSE 0 END) ELSE 0 END AS [202612]
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Porcentaje de Intervenciones de Alta Complejidad' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE     (A.Red IN ('ANCASH', 'APURIMAC', 'AREQUIPA', 'AYACUCHO', 'CAJAMARCA', 'CUSCO', 'HUANCAVELICA', 'HUANUCO', 'HUARAZ', 'ICA', 'RED JAEN', 'INCOR', 'JULIACA', 
                      'JUNIN', 'LA LIBERTAD', 'LAMBAYEQUE', 'LORETO', 'MADRE DE DIOS', 'MOQUEGUA', 'MOYOBAMBA', 'PASCO', 'PIURA', 'PUNO', 'REBAGLIATI', 'SABOGAL', 'TACNA', 
                      'TARAPOTO', 'TUMBES', 'RED PRESTACIONAL ALMENARA', 'RED PRESTACIONAL REBAGLIATI', 'RED PRESTACIONAL SABOGAL'));

/* Qx_IMenor - Porcentaje de Intervenciones Menores*/

DECLARE @Periodo CHAR(6) = '202608';         
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
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(X.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(X.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(X.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(X.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(X.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(X.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(X.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(X.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(X.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(X.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(X.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(X.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(X.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN X.[202601] <> 0 THEN ((ISNULL(A.[202601], 0)) * 1.00) / X.[202601] ELSE 0 END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN X.[202602] <> 0 THEN ((ISNULL(A.[202602], 0)) * 1.00) / X.[202602] ELSE 0 END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN X.[202603] <> 0 THEN ((ISNULL(A.[202603], 0)) * 1.00) / X.[202603] ELSE 0 END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN X.[202604] <> 0 THEN ((ISNULL(A.[202604], 0)) * 1.00) / X.[202604] ELSE 0 END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN X.[202605] <> 0 THEN ((ISNULL(A.[202605], 0)) * 1.00) / X.[202605] ELSE 0 END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN X.[202606] <> 0 THEN ((ISNULL(A.[202606], 0)) * 1.00) / X.[202606] ELSE 0 END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN X.[202607] <> 0 THEN ((ISNULL(A.[202607], 0)) * 1.00) / X.[202607] ELSE 0 END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN X.[202608] <> 0 THEN ((ISNULL(A.[202608], 0)) * 1.00) / X.[202608] ELSE 0 END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN X.[202609] <> 0 THEN ((ISNULL(A.[202609], 0)) * 1.00) / X.[202609] ELSE 0 END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN X.[202610] <> 0 THEN ((ISNULL(A.[202610], 0)) * 1.00) / X.[202610] ELSE 0 END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN X.[202611] <> 0 THEN ((ISNULL(A.[202611], 0)) * 1.00) / X.[202611] ELSE 0 END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN X.[202612] <> 0 THEN ((ISNULL(A.[202612], 0)) * 1.00) / X.[202612] ELSE 0 END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN X ON CEN.codcentro = X.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Porcentaje de Intervenciones Menores' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;

/* Qx_IntSusp - Porcentaje de Operaciones Suspendidas*/

DECLARE @Periodo CHAR(6) = '202609';         
DECLARE @Mes     INT     = CAST(RIGHT(@Periodo, 2) AS INT);
DECLARE @Anio    INT     = CAST(LEFT(@Periodo, 4) AS INT);

WITH A AS (
      SELECT Red, Centro, nivel, codcentro, Año, Grupo, Actividad, Orden, Total, [202601], [202602], [202603], [202604], [202605], [202606], [202607], [202608], 
      [202609], [202610], [202611], [202612], Variable
      FROM  pentahodev.dbo.CONSOLIDADO_VAR_ESSALUD_CIFRAS_2026
      WHERE Variable IN ('Centro Quirúrgico - Operaciones Suspendidas')
),
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
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00 / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE NULL END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN CASE WHEN B.[202601] <> 0 THEN (ISNULL(A.[202601], 0) * 1.00) / B.[202601] ELSE NULL END ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN CASE WHEN B.[202602] <> 0 THEN (ISNULL(A.[202602], 0) * 1.00) / B.[202602] ELSE NULL END ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN CASE WHEN B.[202603] <> 0 THEN (ISNULL(A.[202603], 0) * 1.00) / B.[202603] ELSE NULL END ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN CASE WHEN B.[202604] <> 0 THEN (ISNULL(A.[202604], 0) * 1.00) / B.[202604] ELSE NULL END ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN CASE WHEN B.[202605] <> 0 THEN (ISNULL(A.[202605], 0) * 1.00) / B.[202605] ELSE NULL END ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN CASE WHEN B.[202606] <> 0 THEN (ISNULL(A.[202606], 0) * 1.00) / B.[202606] ELSE NULL END ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN CASE WHEN B.[202607] <> 0 THEN (ISNULL(A.[202607], 0) * 1.00) / B.[202607] ELSE NULL END ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN CASE WHEN B.[202608] <> 0 THEN (ISNULL(A.[202608], 0) * 1.00) / B.[202608] ELSE NULL END ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN CASE WHEN B.[202609] <> 0 THEN (ISNULL(A.[202609], 0) * 1.00) / B.[202609] ELSE NULL END ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN CASE WHEN B.[202610] <> 0 THEN (ISNULL(A.[202610], 0) * 1.00) / B.[202610] ELSE NULL END ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN CASE WHEN B.[202611] <> 0 THEN (ISNULL(A.[202611], 0) * 1.00) / B.[202611] ELSE NULL END ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN CASE WHEN B.[202612] <> 0 THEN (ISNULL(A.[202612], 0) * 1.00) / B.[202612] ELSE NULL END ELSE 0 END AS [202612]

FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Porcentaje de Operaciones Suspendidas' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;

/* Qx_RendSO - Rendimiento de Sala de Operaciones*/

DECLARE @Periodo CHAR(6) = '202609';         
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
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         ) <> 0
    THEN (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(A.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(A.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(A.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(A.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(A.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(A.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(A.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(A.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(A.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(A.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(A.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(A.[202612],0) ELSE 0 END
         ) * 1.00  / (
            CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END +
            CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END +
            CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END +
            CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END +
            CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END +
            CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END +
            CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END +
            CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END +
            CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END +
            CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END +
            CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END +
            CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END
         )
    ELSE 0 END AS Total,
    CASE WHEN ( CASE WHEN @Mes>=1  AND (D.excl_01 = 0 OR D.excl_01 IS NULL) THEN ISNULL(B.[202601],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=1  THEN ISNULL(A.[202601],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=1  THEN ISNULL(B.[202601],0) ELSE 0 END) ELSE 0 END AS [202601],
    CASE WHEN ( CASE WHEN @Mes>=2  AND (D.excl_02 = 0 OR D.excl_02 IS NULL) THEN ISNULL(B.[202602],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=2  THEN ISNULL(A.[202602],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=2  THEN ISNULL(B.[202602],0) ELSE 0 END) ELSE 0 END AS [202602],
    CASE WHEN ( CASE WHEN @Mes>=3  AND (D.excl_03 = 0 OR D.excl_03 IS NULL) THEN ISNULL(B.[202603],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=3  THEN ISNULL(A.[202603],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=3  THEN ISNULL(B.[202603],0) ELSE 0 END) ELSE 0 END AS [202603],
    CASE WHEN ( CASE WHEN @Mes>=4  AND (D.excl_04 = 0 OR D.excl_04 IS NULL) THEN ISNULL(B.[202604],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=4  THEN ISNULL(A.[202604],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=4  THEN ISNULL(B.[202604],0) ELSE 0 END) ELSE 0 END AS [202604],
    CASE WHEN ( CASE WHEN @Mes>=5  AND (D.excl_05 = 0 OR D.excl_05 IS NULL) THEN ISNULL(B.[202605],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=5  THEN ISNULL(A.[202605],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=5  THEN ISNULL(B.[202605],0) ELSE 0 END) ELSE 0 END AS [202605],
    CASE WHEN ( CASE WHEN @Mes>=6  AND (D.excl_06 = 0 OR D.excl_06 IS NULL) THEN ISNULL(B.[202606],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=6  THEN ISNULL(A.[202606],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=6  THEN ISNULL(B.[202606],0) ELSE 0 END) ELSE 0 END AS [202606],
    CASE WHEN ( CASE WHEN @Mes>=7  AND (D.excl_07 = 0 OR D.excl_07 IS NULL) THEN ISNULL(B.[202607],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=7  THEN ISNULL(A.[202607],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=7  THEN ISNULL(B.[202607],0) ELSE 0 END) ELSE 0 END AS [202607],
    CASE WHEN ( CASE WHEN @Mes>=8  AND (D.excl_08 = 0 OR D.excl_08 IS NULL) THEN ISNULL(B.[202608],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=8  THEN ISNULL(A.[202608],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=8  THEN ISNULL(B.[202608],0) ELSE 0 END) ELSE 0 END AS [202608],
    CASE WHEN ( CASE WHEN @Mes>=9  AND (D.excl_09 = 0 OR D.excl_09 IS NULL) THEN ISNULL(B.[202609],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=9  THEN ISNULL(A.[202609],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=9  THEN ISNULL(B.[202609],0) ELSE 0 END) ELSE 0 END AS [202609],
    CASE WHEN ( CASE WHEN @Mes>=10 AND (D.excl_10 = 0 OR D.excl_10 IS NULL) THEN ISNULL(B.[202610],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=10  THEN ISNULL(A.[202610],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=10  THEN ISNULL(B.[202610],0) ELSE 0 END) ELSE 0 END AS [202610],
    CASE WHEN ( CASE WHEN @Mes>=11 AND (D.excl_11 = 0 OR D.excl_11 IS NULL) THEN ISNULL(B.[202611],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=11  THEN ISNULL(A.[202611],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=11  THEN ISNULL(B.[202611],0) ELSE 0 END) ELSE 0 END AS [202611],
    CASE WHEN ( CASE WHEN @Mes>=12 AND (D.excl_12 = 0 OR D.excl_12 IS NULL) THEN ISNULL(B.[202612],0) ELSE 0 END ) <> 0 THEN (CASE WHEN @Mes>=12  THEN ISNULL(A.[202612],0) ELSE 0 END) * 1.0 / (CASE WHEN @Mes>=12  THEN ISNULL(B.[202612],0) ELSE 0 END) ELSE 0 END AS [202612]
FROM CEN
LEFT OUTER JOIN A ON CEN.codcentro = A.codcentro
LEFT OUTER JOIN B ON CEN.codcentro = B.codcentro
LEFT OUTER JOIN (
    SELECT 
        cen.id, 
        est.tipo AS tipo_indicador, 
        est.indicador, 
        CASE @Mes
            WHEN 1  THEN est_tipo.est_01
            WHEN 2  THEN est_tipo.est_02
            WHEN 3  THEN est_tipo.est_03
            WHEN 4  THEN est_tipo.est_04
            WHEN 5  THEN est_tipo.est_05
            WHEN 6  THEN est_tipo.est_06
            WHEN 7  THEN est_tipo.est_07
            WHEN 8  THEN est_tipo.est_08
            WHEN 9  THEN est_tipo.est_09
            WHEN 10 THEN est_tipo.est_10
            WHEN 11 THEN est_tipo.est_11
            WHEN 12 THEN est_tipo.est_12
        END AS estandar,
        cen.codcentro, 
        cen.centro, 
        cen.red, 
        cen.nivel, 
        cen.tipo, 
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est_tipo.id_estandar = est.id
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_exclusion_centro_estandar exc ON exc.id_centro = cen.id AND exc.id_estandar =est.id
    WHERE est.indicador = 'Rendimiento de Sala de Operaciones' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro;










