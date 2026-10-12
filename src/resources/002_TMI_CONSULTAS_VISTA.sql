

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

    -- Acumulados mensuales protegidos contra NULL y división por cero
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
        -- Extracción real del valor del estándar según el mes seleccionado
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
    WHERE est.indicador = 'Concentracion de Consultas' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
ORDER BY ORDEN asc;


/* CE_GCHProg - Grado de Cumplimiento de Horas Programadas*/

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
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar*0.95 AS [% Acept],

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
    -- meses posteriores a @Periodo en 0
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
        -- Extracción real del valor del estándar según el mes seleccionado
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
    WHERE est.indicador = 'Grado de Cumplimiento de Horas Programadas' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro


/*CE_Recetas - Promedio de Recetas por Consultas */

DECLARE @Periodo CHAR(6) = '202608';         
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
    -- meses posteriores a @Periodo en 0
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
        -- Extracción real del valor del estándar según el mes seleccionado
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
    WHERE est.indicador = 'Promedio de Recetas por Consultas' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro



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
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar *0.9  AS [% Acept], 

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
    -- meses posteriores a @Periodo en 0
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
    WHERE est.indicador = 'Rendimiento Hora Medico' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo NOT IN ('CNSR','IPO','INCOR')

UNION ALL

SELECT DISTINCT 
    D.id AS ORDEN, CEN.Red, CEN.codcentro, CEN.Centro, D.nivel AS NIVEL, D.categoria AS TIPO, D.estandar AS Estandar, D.estandar *0.9 AS [% Acept], 

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
    -- meses posteriores a @Periodo en 0
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
    WHERE est.indicador = 'Rendimiento Hora Medico' AND est.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
WHERE D.tipo IN ('CNSR','IPO','INCOR')
ORDER BY ORDEN;




/* Em_PrioI_II - % Prioridad I y II con respecto al Total de Emergencias */
DECLARE @Periodo CHAR(6) = '202608';         
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
    -- meses posteriores a @Periodo en 0
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
    WHERE est.indicador = '% Prioridad I y II con respecto al Total de Emergencias' AND est.anio = @Anio
 ) AS D ON CEN.codcentro = D.codcentro

