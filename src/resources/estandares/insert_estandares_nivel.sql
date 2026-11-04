/* =====================================================================================================
   Estándares por nivel de centro (tmi_estandar_nivel) - año 2026
   Origen: Analisis_TMI/Nuevas_Versiones.xlsx, hoja NIVEL (63 filas).
   Un mes en NULL o 0 toma est_fijo (vw adaptadora). Se puede volver a ejecutar:
   actualiza la fila si ya existe (id_indicador + nivel_centro + anio) y si no la inserta.
   Omite (e informa) las claves que no son de la base_estandar del indicador: el cálculo no las usa.
   ===================================================================================================== */
SET NOCOUNT ON;

IF OBJECT_ID('tempdb..#est') IS NOT NULL DROP TABLE #est;
CREATE TABLE #est (id_indicador INT NOT NULL, nivel_centro VARCHAR(50) NOT NULL, anio INT NOT NULL,
                   est_fijo FLOAT NULL, est_01 FLOAT NULL, est_02 FLOAT NULL, est_03 FLOAT NULL, est_04 FLOAT NULL, est_05 FLOAT NULL, est_06 FLOAT NULL, est_07 FLOAT NULL, est_08 FLOAT NULL, est_09 FLOAT NULL, est_10 FLOAT NULL, est_11 FLOAT NULL, est_12 FLOAT NULL);

INSERT INTO #est (id_indicador, nivel_centro, anio, est_fijo, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12) VALUES
    (1, 'I', 2026, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, NULL, NULL, NULL),
    (1, 'II', 2026, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, NULL, NULL, NULL),
    (1, 'III', 2026, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, NULL, NULL, NULL),

    (2, 'I', 2026, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, NULL, NULL, NULL),
    (2, 'II', 2026, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, NULL, NULL, NULL),
    (2, 'III', 2026, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, NULL, NULL, NULL),

    (3, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (3, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (3, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),

    (4, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (4, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (4, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),

    (5, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (5, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (5, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),

    (6, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (6, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (6, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),

    (7, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (7, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (7, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),

    (8, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (8, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (8, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),

    (9, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (9, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (9, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),

    (10, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (10, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (10, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),

    (11, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (11, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (11, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),

    (12, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (12, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (12, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),

    (13, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (13, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (13, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),

    (14, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (14, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (14, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),

    (15, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (15, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (15, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),

    (16, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (16, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (16, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),

    (17, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (17, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (17, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),

    (18, 'I', 2026, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, NULL, NULL, NULL),
    (18, 'II', 2026, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, NULL, NULL, NULL),
    (18, 'III', 2026, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, NULL, NULL, NULL),

    (19, 'I', 2026, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, NULL, NULL, NULL),
    (19, 'II', 2026, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, NULL, NULL, NULL),
    (19, 'III', 2026, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, NULL, NULL, NULL),

    (20, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (20, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (20, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),

    (21, 'I', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (21, 'II', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL),
    (21, 'III', 2026, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL);

-- Validación: no puede repetirse indicador + nivel_centro + año
IF EXISTS (SELECT 1 FROM #est GROUP BY id_indicador, nivel_centro, anio HAVING COUNT(*) > 1)
BEGIN
    SELECT id_indicador, nivel_centro, anio, COUNT(*) AS veces
    FROM #est GROUP BY id_indicador, nivel_centro, anio HAVING COUNT(*) > 1;
    THROW 50001, 'Hay estándares repetidos (indicador + nivel_centro + año). No se cargó nada.', 1;
END;

-- Validación: el indicador debe existir
IF EXISTS (SELECT 1 FROM #est s WHERE NOT EXISTS (SELECT 1 FROM tmi_indicador i WHERE i.id = s.id_indicador))
BEGIN
    SELECT DISTINCT s.id_indicador FROM #est s
    WHERE NOT EXISTS (SELECT 1 FROM tmi_indicador i WHERE i.id = s.id_indicador);
    THROW 50002, 'Hay id_indicador que no existen en tmi_indicador. No se cargó nada.', 1;
END;

-- Solo se cargan las claves que usa el cálculo: las de la base_estandar del indicador (tmi_estandar).
-- Las demás (por ejemplo un nivel para un indicador que se evalúa por otra base) se informan y se omiten.
IF OBJECT_ID('tempdb..#omitidas') IS NOT NULL DROP TABLE #omitidas;
SELECT s.id_indicador, i.base_estandar, s.nivel_centro, s.anio
INTO #omitidas
FROM #est s
JOIN tmi_indicador i ON i.id = s.id_indicador
WHERE NOT EXISTS (SELECT 1 FROM tmi_estandar e
                  WHERE e.tipo_estandar = i.base_estandar AND e.activo = 1 AND e.fuente = 'NIVEL'
                    AND LTRIM(RTRIM(e.clave)) = LTRIM(RTRIM(s.nivel_centro)));
IF EXISTS (SELECT 1 FROM #omitidas)
BEGIN
    SELECT 'Omitida: no es clave de la base del indicador' AS aviso, * FROM #omitidas ORDER BY id_indicador, nivel_centro;
    DELETE s FROM #est s JOIN #omitidas o ON o.id_indicador = s.id_indicador AND o.nivel_centro = s.nivel_centro AND o.anio = s.anio;
    PRINT CONCAT('Filas omitidas (no son clave de la base del indicador): ', @@ROWCOUNT);
END;
DROP TABLE #omitidas;

BEGIN TRANSACTION;

UPDATE t SET est_fijo = s.est_fijo,
                   est_01 = s.est_01,
                   est_02 = s.est_02,
                   est_03 = s.est_03,
                   est_04 = s.est_04,
                   est_05 = s.est_05,
                   est_06 = s.est_06,
                   est_07 = s.est_07,
                   est_08 = s.est_08,
                   est_09 = s.est_09,
                   est_10 = s.est_10,
                   est_11 = s.est_11,
                   est_12 = s.est_12
FROM tmi_estandar_nivel t
JOIN #est s ON s.id_indicador = t.id_indicador AND s.nivel_centro = t.nivel_centro AND s.anio = t.anio;
PRINT CONCAT('tmi_estandar_nivel actualizados: ', @@ROWCOUNT);

INSERT INTO tmi_estandar_nivel (id_indicador, nivel_centro, anio, est_fijo, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12)
SELECT s.id_indicador, s.nivel_centro, s.anio, s.est_fijo, s.est_01, s.est_02, s.est_03, s.est_04, s.est_05, s.est_06, s.est_07, s.est_08, s.est_09, s.est_10, s.est_11, s.est_12
FROM #est s
WHERE NOT EXISTS (SELECT 1 FROM tmi_estandar_nivel t
                  WHERE t.id_indicador = s.id_indicador AND t.nivel_centro = s.nivel_centro AND t.anio = s.anio);
PRINT CONCAT('tmi_estandar_nivel insertados: ', @@ROWCOUNT);

COMMIT TRANSACTION;

DROP TABLE #est;
