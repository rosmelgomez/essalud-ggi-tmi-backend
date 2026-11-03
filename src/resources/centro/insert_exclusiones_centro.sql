/* =====================================================================================================
   Exclusiones de centro por indicador (tmi_exclusion_centro_indicador) - año 2026
   Origen: UPDATE ... SET <indicador>='NA' de 01_TMI_PROCESAMIENTO_GENERAL_2025.sql (periodos 202601-202612)
   excl_MM = 1 -> el indicador queda NA ese mes. id_indicador NULL = todos los indicadores del centro.
   id_indicador: 1-4 CE1-CE4 | 5-9 H1-H5 | 10-15 Q1-Q6 | 16-17 EM1-EM2 | 18-21 O_1-O_4
   No se cargan:
     - 194 CHOTA (O_1-O_4): en el script original los UPDATE están comentados en todos los meses.
   Se puede volver a ejecutar: no duplica (centro + indicador + año).
   ===================================================================================================== */
INSERT INTO tmi_exclusion_centro_indicador (id_centro, codcentro, id_indicador, anio,
       excl_01, excl_02, excl_03, excl_04, excl_05, excl_06, excl_07, excl_08, excl_09, excl_10, excl_11, excl_12,
       motivo, resultado)
SELECT c.id, v.codcentro, v.id_indicador, 2026,
       v.e01, v.e02, v.e03, v.e04, v.e05, v.e06, v.e07, v.e08, v.e09, v.e10, v.e11, v.e12,
       v.motivo, 'NA'
FROM (VALUES
    -- 824 SAN NICOLÁS: cierre de IPRESS, todos los indicadores, todo el año
    ('824', NULL, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'Cierre de IPRESS San Nicolás (TMI Octubre figura con puntaje 0)'),
    -- 498: CE4 Promedio de recetas por consulta, todo el año
    ('498', 4,    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'Exclusión de CE4 (Promedio de recetas por consultas)'),
    -- 230 QUIRUVILCA: odontología, todo el año salvo febrero y marzo
    ('230', 18,   1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'MODIFICAR QUIRUVILCA'),
    ('230', 19,   1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'MODIFICAR QUIRUVILCA'),
    ('230', 20,   1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'MODIFICAR QUIRUVILCA'),
    ('230', 21,   1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'MODIFICAR QUIRUVILCA'),
    -- 219, 225, 228, 835, 236, 237: odontología, solo junio
    ('219', 18,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('219', 19,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('219', 20,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('219', 21,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('225', 18,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('225', 19,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('225', 20,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('225', 21,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('228', 18,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('228', 19,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('228', 20,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('228', 21,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('835', 18,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('835', 19,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('835', 20,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('835', 21,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('236', 18,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('236', 19,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('236', 20,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('236', 21,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('237', 18,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('237', 19,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('237', 20,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    ('237', 21,   0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'Exclusión de odontología - junio'),
    -- 224 HUAMACHUCO: odontología, solo diciembre
    ('224', 18,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 'MODIFICAR HUAMACHUCO'),
    ('224', 19,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 'MODIFICAR HUAMACHUCO'),
    ('224', 20,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 'MODIFICAR HUAMACHUCO'),
    ('224', 21,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 'MODIFICAR HUAMACHUCO')
) v (codcentro, id_indicador, e01, e02, e03, e04, e05, e06, e07, e08, e09, e10, e11, e12, motivo)
JOIN (SELECT LTRIM(RTRIM(codcentro)) AS codcentro, MIN(id) AS id FROM tmi_centro GROUP BY LTRIM(RTRIM(codcentro))) c
  ON c.codcentro = v.codcentro
WHERE NOT EXISTS (SELECT 1 FROM tmi_exclusion_centro_indicador e
                  WHERE e.id_centro = c.id AND e.anio = 2026
                    AND (e.id_indicador = v.id_indicador OR (e.id_indicador IS NULL AND v.id_indicador IS NULL)));
