
SET NOCOUNT ON;

IF OBJECT_ID('tempdb..#est') IS NOT NULL DROP TABLE #est;
CREATE TABLE #est (id_indicador INT NOT NULL, tipo_centro VARCHAR(50) NOT NULL, anio INT NOT NULL,
                   est_fijo FLOAT NULL, est_01 FLOAT NULL, est_02 FLOAT NULL, est_03 FLOAT NULL, est_04 FLOAT NULL, est_05 FLOAT NULL, est_06 FLOAT NULL, est_07 FLOAT NULL, est_08 FLOAT NULL, est_09 FLOAT NULL, est_10 FLOAT NULL, est_11 FLOAT NULL, est_12 FLOAT NULL);

INSERT INTO #est (id_indicador, tipo_centro, anio, est_fijo, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12) VALUES

    (2, 'H.N.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (2, 'H.IV', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (2, 'H.III', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (2, 'H.II', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,NULL, NULL, NULL),
    (2, 'H.I', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (2, 'POL.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (2, 'C.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (2, 'P.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (2, 'CNSR', 2026, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, NULL, NULL, NULL),
    (2, 'IPO', 2026, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, NULL, NULL, NULL),
    (2, 'INCOR', 2026, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, NULL, NULL, NULL),

    (3, 'H.N.', 2026, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, NULL, NULL, NULL),
    (3, 'H.IV', 2026, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, NULL, NULL, NULL),
    (3, 'H.III', 2026, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, NULL, NULL, NULL),
    (3, 'H.II', 2026, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, NULL, NULL, NULL),
    (3, 'H.I', 2026, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, NULL, NULL, NULL),
    (3, 'POL.', 2026, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, NULL, NULL, NULL),
    (3, 'C.M.', 2026, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, NULL, NULL, NULL),
    (3, 'P.M.', 2026, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, NULL, NULL, NULL),
    (3, 'CNSR', 2026, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, NULL, NULL, NULL),
    (3, 'IPO', 2026, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, NULL, NULL, NULL),
    (3, 'INCOR', 2026, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98, NULL, NULL, NULL),

    (4, 'H.N.', 2026, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, NULL, NULL, NULL),
    (4, 'H.IV', 2026, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, NULL, NULL, NULL),
    (4, 'H.III', 2026, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, NULL, NULL, NULL),
    (4, 'H.II', 2026, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, NULL, NULL, NULL),
    (4, 'H.I', 2026, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, NULL, NULL, NULL),
    (4, 'POL.', 2026, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, NULL, NULL, NULL),
    (4, 'C.M.', 2026, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, NULL, NULL, NULL),
    (4, 'P.M.', 2026, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, NULL, NULL, NULL),
    (4, 'CNSR', 2026, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, NULL, NULL, NULL),
    (4, 'IPO', 2026, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, NULL, NULL, NULL),
    (4, 'INCOR', 2026, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5, NULL, NULL, NULL),

    (5, 'H.N.', 2026, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, NULL, NULL, NULL),
    (5, 'H.IV', 2026, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, NULL, NULL, NULL),
    (5, 'H.III', 2026, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, NULL, NULL, NULL),
    (5, 'H.II', 2026, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, NULL, NULL, NULL),
    (5, 'H.I', 2026, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, NULL, NULL, NULL),
    (5, 'POL.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (5, 'C.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (5, 'P.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (5, 'CNSR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (5, 'IPO', 2026, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, NULL, NULL, NULL),
    (5, 'INCOR', 2026, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, NULL, NULL, NULL),

    (6, 'H.N.', 2026, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, NULL, NULL, NULL),
    (6, 'H.IV', 2026, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, NULL, NULL, NULL),
    (6, 'H.III', 2026, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, NULL, NULL, NULL),
    (6, 'H.II', 2026, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, NULL, NULL, NULL),
    (6, 'H.I', 2026, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, NULL, NULL, NULL),
    (6, 'POL.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (6, 'C.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (6, 'P.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (6, 'CNSR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (6, 'IPO', 2026, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, NULL, NULL, NULL),
    (6, 'INCOR', 2026, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, NULL, NULL, NULL),

    (7, 'H.N.', 2026, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, NULL, NULL, NULL),
    (7, 'H.IV', 2026, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, NULL, NULL, NULL),
    (7, 'H.III', 2026, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, NULL, NULL, NULL),
    (7, 'H.II', 2026, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, NULL, NULL, NULL),
    (7, 'H.I', 2026, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, NULL, NULL, NULL),
    (7, 'POL.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (7, 'C.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (7, 'P.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (7, 'CNSR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (7, 'IPO', 2026, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, NULL, NULL, NULL),
    (7, 'INCOR', 2026, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, NULL, NULL, NULL),

    (8, 'H.N.', 2026, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, NULL, NULL, NULL),
    (8, 'H.IV', 2026, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, NULL, NULL, NULL),
    (8, 'H.III', 2026, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5, NULL, NULL, NULL),
    (8, 'H.II', 2026, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, NULL, NULL, NULL),
    (8, 'H.I', 2026, 6.7, 6.7, 6.7, 6.7, 6.7, 6.7, 6.7, 6.7, 6.7, 6.7, NULL, NULL, NULL),
    (8, 'POL.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL , NULL),
    (8, 'C.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (8, 'P.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (8, 'CNSR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (8, 'IPO', 2026, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, NULL, NULL, NULL),
    (8, 'INCOR', 2026, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, NULL, NULL, NULL),

    (9, 'H.N.', 2026, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, NULL, NULL, NULL),
    (9, 'H.IV', 2026, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, NULL, NULL, NULL),
    (9, 'H.III', 2026, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, NULL, NULL, NULL),
    (9, 'H.II', 2026, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, NULL, NULL, NULL),
    (9, 'H.I', 2026, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, NULL, NULL, NULL),
    (9, 'POL.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (9, 'C.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (9, 'P.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (9, 'CNSR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,NULL, NULL, NULL),
    (9, 'IPO', 2026, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, NULL, NULL, NULL),
    (9, 'INCOR', 2026, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, NULL, NULL, NULL),

    (10, 'H.N.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (10, 'H.IV', 2026, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, NULL, NULL, NULL),
    (10, 'H.III', 2026, 0.15, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.15, NULL, NULL, NULL),
    (10, 'H.II', 2026, 0.5, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.5, NULL, NULL, NULL),
    (10, 'H.I', 2026, 0.5, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, NULL, NULL, NULL),
    (10, 'POL.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (10, 'C.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (10, 'P.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (10, 'CNSR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (10, 'IPO', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (10, 'INCOR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),

    (11, 'H.N.', 2026, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0, 0, 0),
    (11, 'H.IV', 2026, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, NULL, NULL, NULL),
    (11, 'H.III', 2026, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, NULL, NULL, NULL),
    (11, 'H.II', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (11, 'H.I', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (11, 'POL.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (11, 'C.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (11, 'P.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (11, 'CNSR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (11, 'IPO', 2026, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, NULL, NULL, NULL),
    (11, 'INCOR', 2026, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, NULL, NULL, NULL),

    (12, 'H.N.', 2026, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, NULL, NULL, NULL),
    (12, 'H.IV', 2026, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, NULL, NULL, NULL),
    (12, 'H.III', 2026, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, NULL, NULL, NULL),
    (12, 'H.II', 2026, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, NULL, NULL, NULL),
    (12, 'H.I', 2026, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, NULL, NULL, NULL),
    (12, 'POL.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (12, 'C.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (12, 'P.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (12, 'CNSR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (12, 'IPO', 2026, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, NULL, NULL, NULL),
    (12, 'INCOR', 2026, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, NULL, NULL, NULL),

    (13, 'H.N.', 2026, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, NULL, NULL, NULL),
    (13, 'H.IV', 2026, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, NULL, NULL, NULL),
    (13, 'H.III', 2026, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, NULL, NULL, NULL),
    (13, 'H.II', 2026, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85, NULL, NULL, NULL),
    (13, 'H.I', 2026, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, NULL, NULL, NULL),
    (13, 'POL.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (13, 'C.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (13, 'P.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (13, 'CNSR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (13, 'IPO', 2026, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, NULL, NULL, NULL),
    (13, 'INCOR', 2026, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, NULL, NULL, NULL),

    (14, 'H.N.', 2026, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, NULL, NULL, NULL),
    (14, 'H.IV', 2026, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, NULL, NULL, NULL),
    (14, 'H.III', 2026, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, NULL, NULL, NULL),
    (14, 'H.II', 2026, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, NULL, NULL, NULL),
    (14, 'H.I', 2026, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, NULL, NULL, NULL),
    (14, 'POL.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (14, 'C.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (14, 'P.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (14, 'CNSR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (14, 'IPO', 2026, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, NULL, NULL, NULL),
    (14, 'INCOR', 2026, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, NULL, NULL, NULL),

    (15, 'H.N.', 2026, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45, NULL, NULL, NULL),
    (15, 'H.IV', 2026, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, NULL, NULL, NULL),
    (15, 'H.III', 2026, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, NULL, NULL, NULL),
    (15, 'H.II', 2026, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, NULL, NULL, NULL),
    (15, 'H.I', 2026, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, NULL, NULL, NULL),
    (15, 'POL.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (15, 'C.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (15, 'P.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (15, 'CNSR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (15, 'IPO', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (15, 'INCOR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),

    (16, 'H.N.', 2026, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, NULL, NULL, NULL),
    (16, 'H.IV', 2026, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, NULL, NULL, NULL),
    (16, 'H.III', 2026, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, NULL, NULL, NULL),
    (16, 'H.II', 2026, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, NULL, NULL, NULL),
    (16, 'H.I', 2026, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, NULL, NULL, NULL),
    (16, 'POL.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (16, 'C.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (16, 'P.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (16, 'CNSR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (16, 'IPO', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (16, 'INCOR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),

    (17, 'H.N.', 2026, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, NULL, NULL, NULL),
    (17, 'H.IV', 2026, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, NULL, NULL, NULL),
    (17, 'H.III', 2026, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, NULL, NULL, NULL),
    (17, 'H.II', 2026, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, NULL, NULL, NULL),
    (17, 'H.I', 2026, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, NULL, NULL, NULL),
    (17, 'POL.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (17, 'C.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (17, 'P.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,NULL, NULL, NULL),
    (17, 'CNSR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (17, 'IPO', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (17, 'INCOR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),

    (19, 'H.N.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (19, 'H.IV', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (19, 'H.III', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (19, 'H.II', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (19, 'H.I', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (19, 'POL.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (19, 'C.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (19, 'P.M.', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (19, 'CNSR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (19, 'IPO', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (19, 'INCOR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),

    (20, 'H.N.', 2026, 0.98, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.98, NULL, NULL, NULL),
    (20, 'H.IV', 2026, 0.98, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.98, NULL, NULL, NULL),
    (20, 'H.III', 2026, 0.98, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.98, 0, 0, 0),
    (20, 'H.II', 2026, 0.98, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.98, 0, 0, 0),
    (20, 'H.I', 2026, 0.98, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.98, 0, 0, 0),
    (20, 'POL.', 2026, 0.98, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.98, 0, 0, 0),
    (20, 'C.M.', 2026, 0.98, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.98, 0, 0, 0),
    (20, 'P.M.', 2026, 0.98, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.98, 0, 0, 0),
    (20, 'CNSR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (20, 'IPO', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (20, 'INCOR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),

    (21, 'H.N.', 2026, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, NULL, NULL, NULL),
    (21, 'H.IV', 2026, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, NULL, NULL, NULL),
    (21, 'H.III', 2026, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, NULL, NULL, NULL),
    (21, 'H.II', 2026, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, NULL, NULL, NULL),
    (21, 'H.I', 2026, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, NULL, NULL, NULL),
    (21, 'POL.', 2026, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, NULL, NULL, NULL),
    (21, 'C.M.', 2026, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, NULL, NULL, NULL),
    (21, 'P.M.', 2026, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, NULL, NULL, NULL),
    (21, 'CNSR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (21, 'IPO', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    (21, 'INCOR', 2026, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- Validación: no puede repetirse indicador + tipo_centro + año
IF EXISTS (SELECT 1 FROM #est GROUP BY id_indicador, tipo_centro, anio HAVING COUNT(*) > 1)
BEGIN
    SELECT id_indicador, tipo_centro, anio, COUNT(*) AS veces
    FROM #est GROUP BY id_indicador, tipo_centro, anio HAVING COUNT(*) > 1;
    RAISERROR('Hay estándares repetidos (indicador + tipo_centro + año). No se cargó nada.', 16, 1);
    RETURN;
END;

-- Validación: el indicador debe existir
IF EXISTS (SELECT 1 FROM #est s WHERE NOT EXISTS (SELECT 1 FROM tmi_indicador i WHERE i.id = s.id_indicador))
BEGIN
    SELECT DISTINCT s.id_indicador FROM #est s
    WHERE NOT EXISTS (SELECT 1 FROM tmi_indicador i WHERE i.id = s.id_indicador);
    RAISERROR('Hay id_indicador que no existen en tmi_indicador. No se cargó nada.', 16, 1);
    RETURN;
END;

-- Solo se cargan las claves que usa el cálculo: las de la base_estandar del indicador (tmi_estandar).
-- Las demás (por ejemplo un tipo para un indicador que se evalúa por otra base) se informan y se omiten.
IF OBJECT_ID('tempdb..#omitidas') IS NOT NULL DROP TABLE #omitidas;
SELECT s.id_indicador, i.base_estandar, s.tipo_centro, s.anio
INTO #omitidas
FROM #est s
JOIN tmi_indicador i ON i.id = s.id_indicador
WHERE NOT EXISTS (SELECT 1 FROM tmi_estandar e
                  WHERE e.tipo_estandar = i.base_estandar AND e.activo = 1 AND e.fuente = 'TIPO'
                    AND LTRIM(RTRIM(e.clave)) = LTRIM(RTRIM(s.tipo_centro)));
IF EXISTS (SELECT 1 FROM #omitidas)
BEGIN
    SELECT 'Omitida: no es clave de la base del indicador' AS aviso, * FROM #omitidas ORDER BY id_indicador, tipo_centro;
    DELETE s FROM #est s JOIN #omitidas o ON o.id_indicador = s.id_indicador AND o.tipo_centro = s.tipo_centro AND o.anio = s.anio;
    PRINT 'Filas omitidas (no son clave de la base del indicador): ' + CAST(@@ROWCOUNT AS VARCHAR(10));
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
FROM tmi_estandar_tipo t
JOIN #est s ON s.id_indicador = t.id_indicador AND s.tipo_centro = t.tipo_centro AND s.anio = t.anio;
PRINT 'tmi_estandar_tipo actualizados: ' + CAST(@@ROWCOUNT AS VARCHAR(10));

INSERT INTO tmi_estandar_tipo (id_indicador, tipo_centro, anio, est_fijo, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12)
SELECT s.id_indicador, s.tipo_centro, s.anio, s.est_fijo, s.est_01, s.est_02, s.est_03, s.est_04, s.est_05, s.est_06, s.est_07, s.est_08, s.est_09, s.est_10, s.est_11, s.est_12
FROM #est s
WHERE NOT EXISTS (SELECT 1 FROM tmi_estandar_tipo t
                  WHERE t.id_indicador = s.id_indicador AND t.tipo_centro = s.tipo_centro AND t.anio = s.anio);
PRINT 'tmi_estandar_tipo insertados: ' + CAST(@@ROWCOUNT AS VARCHAR(10));

COMMIT TRANSACTION;

DROP TABLE #est;
