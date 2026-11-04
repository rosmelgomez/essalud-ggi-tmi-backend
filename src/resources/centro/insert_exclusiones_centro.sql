/* =====================================================================================================
   Exclusiones de centro por indicador (tmi_exclusion_centro_indicador) - año 2026
   Origen: UPDATE ... SET <indicador>='NA' de 01_TMI_PROCESAMIENTO_GENERAL_2025.sql (periodos 202601-202612)
           + hoja Exclusiones_centro de Analisis_TMI/Nuevas_Versiones.xlsx
   excl_MM = 1 -> el indicador queda excluido ese mes. id_indicador NULL = todos los indicadores del centro.
   resultado: 'NA' (por defecto) o '0' (el mes excluido sale con 0).
   id_indicador: 1-4 CE1-CE4 | 5-9 H1-H5 | 10-15 Q1-Q6 | 16-17 EM1-EM2 | 18-21 O_1-O_4
   No se cargan:
     - 194 CHOTA (O_1-O_4): en el script original los UPDATE están comentados en todos los meses.
   Validación: un centro no puede tener dos filas con el mismo indicador en el mismo año
               (centro + indicador + año). Si se repite en esta lista, no se carga nada.
   Se puede volver a ejecutar: no duplica lo que ya está en la tabla.
   ===================================================================================================== */
SET NOCOUNT ON;

IF OBJECT_ID('tempdb..#excl') IS NOT NULL DROP TABLE #excl;
CREATE TABLE #excl (codcentro VARCHAR(50) NOT NULL, id_indicador INT NULL,
                    e01 BIT, e02 BIT, e03 BIT, e04 BIT, e05 BIT, e06 BIT,
                    e07 BIT, e08 BIT, e09 BIT, e10 BIT, e11 BIT, e12 BIT,
                    motivo VARCHAR(300) NULL, resultado VARCHAR(2) NOT NULL);

INSERT INTO #excl (codcentro, id_indicador, e01, e02, e03, e04, e05, e06, e07, e08, e09, e10, e11, e12, motivo, resultado)
VALUES
    -- 824 SAN NICOLÁS: cierre de IPRESS, todos los indicadores, todo el año
    ('824', NULL, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'Cierre de IPRESS San Nicolás (TMI Octubre figura con puntaje 0)', 'NA'),
    -- 498: CE4 Promedio de recetas por consulta, todo el año
    ('498', 4,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'Exclusión de CE4 (Promedio de recetas por consultas)', 'NA'),
    -- 230 QUIRUVILCA: odontología, todo el año salvo febrero y marzo
    ('230', 18,   1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'MODIFICAR QUIRUVILCA', 'NA'),
    ('230', 19,   1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'MODIFICAR QUIRUVILCA', 'NA'),
    ('230', 20,   1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'MODIFICAR QUIRUVILCA', 'NA'),
    ('230', 21,   1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'MODIFICAR QUIRUVILCA', 'NA'),
    -- 219, 225, 228, 835, 236, 237: odontología, solo junio
    ('219', 18,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('219', 19,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('219', 20,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('219', 21,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('225', 18,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('225', 19,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('225', 20,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('225', 21,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('228', 18,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('228', 19,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('228', 20,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('228', 21,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('835', 18,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('835', 19,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('835', 20,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('835', 21,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('236', 18,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('236', 19,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('236', 20,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('236', 21,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('237', 18,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('237', 19,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('237', 20,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    ('237', 21,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio', 'NA'),
    -- 224 HUAMACHUCO: odontología, solo diciembre
    ('224', 18,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 'MODIFICAR HUAMACHUCO', 'NA'),
    ('224', 19,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 'MODIFICAR HUAMACHUCO', 'NA'),
    ('224', 20,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 'MODIFICAR HUAMACHUCO', 'NA'),
    ('224', 21,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 'MODIFICAR HUAMACHUCO', 'NA'),
    -- Nuevas_Versiones.xlsx (hoja Exclusiones_centro): un mes, resultado 0
    ('323', 1,    0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, NULL, '0'),
    ('286', 1,    0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, NULL, '0'),
    ('323', 2,    0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, NULL, '0'),
    ('286', 2,    0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, NULL, '0'),
    ('286', 3,    0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, NULL, '0'),
    ('827', 1,    0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, NULL, '0'),
    ('824', 4,    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, NULL, '0'),
    ('498', 1,    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, NULL, '0'),
    ('498', 7,    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, NULL, '0'),
    ('498', 12,   0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, NULL, '0'),
    ('498', 20,   0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, NULL, '0'),
    ('272', 1,    0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, NULL, '0');

-- Validación 1: centro + indicador repetido en esta lista (mismo año)
IF EXISTS (SELECT 1 FROM #excl GROUP BY codcentro, ISNULL(id_indicador, -1) HAVING COUNT(*) > 1)
BEGIN
    SELECT codcentro, id_indicador, 2026 AS anio, COUNT(*) AS veces
    FROM #excl GROUP BY codcentro, id_indicador HAVING COUNT(*) > 1;
    RAISERROR('Centro con el mismo indicador repetido en el año 2026. No se cargó nada.', 16, 1);
    RETURN;
END;

-- Validación 2: el centro debe existir en tmi_centro
IF EXISTS (SELECT 1 FROM #excl x
           WHERE NOT EXISTS (SELECT 1 FROM tmi_centro c WHERE LTRIM(RTRIM(c.codcentro)) = x.codcentro))
BEGIN
    SELECT x.codcentro, x.id_indicador FROM #excl x
    WHERE NOT EXISTS (SELECT 1 FROM tmi_centro c WHERE LTRIM(RTRIM(c.codcentro)) = x.codcentro);
    RAISERROR('Hay codcentro que no existen en tmi_centro. No se cargó nada.', 16, 1);
    RETURN;
END;

-- Validación 3: la tabla ya tiene centro + indicador + año repetidos (cargas anteriores)
IF EXISTS (SELECT 1 FROM tmi_exclusion_centro_indicador
           GROUP BY id_centro, ISNULL(id_indicador, -1), anio HAVING COUNT(*) > 1)
BEGIN
    SELECT id_centro, id_indicador, anio, COUNT(*) AS veces
    FROM tmi_exclusion_centro_indicador
    GROUP BY id_centro, id_indicador, anio HAVING COUNT(*) > 1;
    RAISERROR('tmi_exclusion_centro_indicador ya tiene centro + indicador + año repetidos. Corregir antes de cargar.', 16, 1);
    RETURN;
END;

INSERT INTO tmi_exclusion_centro_indicador (id_centro, codcentro, id_indicador, anio,
       excl_01, excl_02, excl_03, excl_04, excl_05, excl_06, excl_07, excl_08, excl_09, excl_10, excl_11, excl_12,
       motivo, resultado)
SELECT c.id, v.codcentro, v.id_indicador, 2026,
       v.e01, v.e02, v.e03, v.e04, v.e05, v.e06, v.e07, v.e08, v.e09, v.e10, v.e11, v.e12,
       v.motivo, v.resultado
FROM #excl v
JOIN (SELECT LTRIM(RTRIM(codcentro)) AS codcentro, MIN(id) AS id FROM tmi_centro GROUP BY LTRIM(RTRIM(codcentro))) c
  ON c.codcentro = v.codcentro
WHERE NOT EXISTS (SELECT 1 FROM tmi_exclusion_centro_indicador e
                  WHERE e.id_centro = c.id AND e.anio = 2026
                    AND (e.id_indicador = v.id_indicador OR (e.id_indicador IS NULL AND v.id_indicador IS NULL)));
PRINT 'tmi_exclusion_centro_indicador insertados: ' + CAST(@@ROWCOUNT AS VARCHAR(10));

-- Regla en la tabla: un solo registro por centro + indicador + año (NULL = todos cuenta como un valor)
IF NOT EXISTS (SELECT 1 FROM sys.indexes
               WHERE name = 'UX_tmi_exclusion_centro_indicador'
                 AND object_id = OBJECT_ID('dbo.tmi_exclusion_centro_indicador'))
    CREATE UNIQUE INDEX UX_tmi_exclusion_centro_indicador
        ON dbo.tmi_exclusion_centro_indicador (id_centro, id_indicador, anio);

DROP TABLE #excl;
