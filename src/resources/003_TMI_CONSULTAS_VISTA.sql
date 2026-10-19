
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
    D.id AS ORDEN, 
    D.red AS Red, 
    D.codcentro, 
    D.centro AS Centro, 
    D.nivel AS NIVEL, 
    D.categoria AS TIPO, 
    D.estandar AS Estandar, 
    D.estandar * 1.1 AS [% Acept],

    CASE 
        WHEN (
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
        ) > 0
        THEN (
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
        ) * 1.00 / (
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
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_nivel est_nivel
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_nivel.id_estandar 
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_nivel.nivel_centro = cen.nivel
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.exclusion_centro_estandar exc ON exc.id_centro = cen.id
    WHERE est.indicador = 'Concentracion de Consultas' AND est_nivel.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro
ORDER BY ORDEN ASC;

use pentahodev_prueba_01


CREATE TABLE exclusion_centro_estandar (
    id INT IDENTITY(1,1) PRIMARY KEY,
    id_centro INT REFERENCES tmi_centro(id),
    id_estandar INT REFERENCES tmi_estandar(id),
    anio INT,
    excl_01 BIT,
    excl_02 BIT,
    excl_03 BIT,
    excl_04 BIT,
    excl_05 BIT,
    excl_06 BIT,
    excl_07 BIT,
    excl_08 BIT,
    excl_09 BIT,
    excl_10 BIT,
    excl_11 BIT,
    excl_12 BIT
);


INSERT INTO [dbo].[exclusion_centro_estandar]
           (id_centro ,id_estandar ,anio ,excl_01 ,excl_02 ,excl_03 ,excl_04 ,excl_05 ,excl_06 ,excl_07 ,excl_08 ,excl_09 ,excl_10 ,excl_11 ,excl_12)
     VALUES
           (176, 1, 2026, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1), 
           (323, 1, 2026, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1)




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
    CASE WHEN (
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
         ) <> 0
    THEN (
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
         ) * 1.00 / (
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
         )
    ELSE 0 END AS Total,
    CASE WHEN @Mes >= 1  AND (D.excl_01 = 1 OR D.excl_01 IS NULL) THEN ISNULL((ISNULL(A.[202601],0) * 1.00) / NULLIF(ISNULL(B.[202601],0),0),0) ELSE 0 END AS [202601],
    CASE WHEN @Mes >= 2  AND (D.excl_02 = 1 OR D.excl_02 IS NULL) THEN ISNULL((ISNULL(A.[202602],0) * 1.00) / NULLIF(ISNULL(B.[202602],0),0),0) ELSE 0 END AS [202602],
    CASE WHEN @Mes >= 3  AND (D.excl_03 = 1 OR D.excl_03 IS NULL) THEN ISNULL((ISNULL(A.[202603],0) * 1.00) / NULLIF(ISNULL(B.[202603],0),0),0) ELSE 0 END AS [202603],
    CASE WHEN @Mes >= 4  AND (D.excl_04 = 1 OR D.excl_04 IS NULL) THEN ISNULL((ISNULL(A.[202604],0) * 1.00) / NULLIF(ISNULL(B.[202604],0),0),0) ELSE 0 END AS [202604],
    CASE WHEN @Mes >= 5  AND (D.excl_05 = 1 OR D.excl_05 IS NULL) THEN ISNULL((ISNULL(A.[202605],0) * 1.00) / NULLIF(ISNULL(B.[202605],0),0),0) ELSE 0 END AS [202605],
    CASE WHEN @Mes >= 6  AND (D.excl_06 = 1 OR D.excl_06 IS NULL) THEN ISNULL((ISNULL(A.[202606],0) * 1.00) / NULLIF(ISNULL(B.[202606],0),0),0) ELSE 0 END AS [202606],
    CASE WHEN @Mes >= 7  AND (D.excl_07 = 1 OR D.excl_07 IS NULL) THEN ISNULL((ISNULL(A.[202607],0) * 1.00) / NULLIF(ISNULL(B.[202607],0),0),0) ELSE 0 END AS [202607],
    CASE WHEN @Mes >= 8  AND (D.excl_08 = 1 OR D.excl_08 IS NULL) THEN ISNULL((ISNULL(A.[202608],0) * 1.00) / NULLIF(ISNULL(B.[202608],0),0),0) ELSE 0 END AS [202608],
    CASE WHEN @Mes >= 9  AND (D.excl_09 = 1 OR D.excl_09 IS NULL) THEN ISNULL((ISNULL(A.[202609],0) * 1.00) / NULLIF(ISNULL(B.[202609],0),0),0) ELSE 0 END AS [202609],
    CASE WHEN @Mes >= 10 AND (D.excl_10 = 1 OR D.excl_10 IS NULL) THEN ISNULL((ISNULL(A.[202610],0) * 1.00) / NULLIF(ISNULL(B.[202610],0),0),0) ELSE 0 END AS [202610],
    CASE WHEN @Mes >= 11 AND (D.excl_11 = 1 OR D.excl_11 IS NULL) THEN ISNULL((ISNULL(A.[202611],0) * 1.00) / NULLIF(ISNULL(B.[202611],0),0),0) ELSE 0 END AS [202611],
    CASE WHEN @Mes >= 12 AND (D.excl_12 = 1 OR D.excl_12 IS NULL) THEN ISNULL((ISNULL(A.[202612],0) * 1.00) / NULLIF(ISNULL(B.[202612],0),0),0) ELSE 0 END AS [202612]

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
        cen.categoria,
        exc.excl_01, exc.excl_02, exc.excl_03, exc.excl_04,
        exc.excl_05, exc.excl_06, exc.excl_07, exc.excl_08,
        exc.excl_09, exc.excl_10, exc.excl_11, exc.excl_12
    FROM pentahodev_prueba_01.dbo.tmi_estandar_tipo est_tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_estandar est ON est.id = est_tipo.id_estandar 
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.tmi_centro cen ON est_tipo.tipo_centro = cen.tipo
    LEFT OUTER JOIN pentahodev_prueba_01.dbo.exclusion_centro_estandar exc ON exc.id_centro = cen.id
    WHERE est.indicador = 'Promedio de Recetas por Consultas' AND est_tipo.anio = @Anio
) AS D ON CEN.codcentro = D.codcentro

