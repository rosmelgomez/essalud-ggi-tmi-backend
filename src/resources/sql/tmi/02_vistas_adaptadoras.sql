/* =====================================================================================================
   TMI DINAMICO - 02 VISTAS
   Vistas que lee el cálculo (04_procedimientos.sql) y el SQL descargable de cada indicador. Las tablas las crea
   src/main/model. Compatible con SQL Server 2008 R2+.
   Cada vista se crea vacía si no existe y luego se cambia con ALTER: nunca deja de existir, así las consultas en curso
   no fallan.
   ===================================================================================================== */

/* ---------- Sinónimo con el nombre anterior de tmi_exclusion_centro_indicador ----------
   Para las consultas externas que aún lo usan (002/003_TMI_CONSULTAS_VISTA.sql, Pentaho...). */
IF OBJECT_ID('dbo.tmi_exclusion_centro_estandar') IS NULL
    EXEC (N'CREATE SYNONYM dbo.tmi_exclusion_centro_estandar FOR dbo.tmi_exclusion_centro_indicador');
GO

/* ---------- vw_tmi_std: estándar por TIPO / NIVEL / CATEGORIA en un solo formato ----------
   m01..m12: el estándar del mes; un mes sin valor (aún no cerrado) queda vacío y el cierre le copia est_fijo.
   m00: el fijo del año, el que usa el cálculo en un mes aún no cerrado. */
IF OBJECT_ID('dbo.vw_tmi_std', 'V') IS NULL EXEC (N'CREATE VIEW dbo.vw_tmi_std AS SELECT 1 AS x');
GO
ALTER VIEW dbo.vw_tmi_std AS
SELECT id_indicador AS id_estandar, 'TIPO' AS fuente, LTRIM(RTRIM(tipo_centro)) AS clave, anio,
       est_01 AS m01, est_02 AS m02,
       est_03 AS m03, est_04 AS m04,
       est_05 AS m05, est_06 AS m06,
       est_07 AS m07, est_08 AS m08,
       est_09 AS m09, est_10 AS m10,
       est_11 AS m11, est_12 AS m12,
       est_fijo AS m00
FROM dbo.tmi_estandar_tipo
UNION ALL
SELECT id_indicador AS id_estandar, 'NIVEL' AS fuente, LTRIM(RTRIM(nivel_centro)) AS clave, anio,
       est_01 AS m01, est_02 AS m02,
       est_03 AS m03, est_04 AS m04,
       est_05 AS m05, est_06 AS m06,
       est_07 AS m07, est_08 AS m08,
       est_09 AS m09, est_10 AS m10,
       est_11 AS m11, est_12 AS m12,
       est_fijo AS m00
FROM dbo.tmi_estandar_nivel
UNION ALL
SELECT id_indicador AS id_estandar, 'CATEGORIA' AS fuente, LTRIM(RTRIM(categoria_centro)) AS clave, anio,
       est_01 AS m01, est_02 AS m02,
       est_03 AS m03, est_04 AS m04,
       est_05 AS m05, est_06 AS m06,
       est_07 AS m07, est_08 AS m08,
       est_09 AS m09, est_10 AS m10,
       est_11 AS m11, est_12 AS m12,
       est_fijo AS m00
FROM dbo.tmi_estandar_categoria;
GO

/* ---------- vw_tmi_centro_base: centros con código numérico ----------
   flag: el centro se lista y se calcula (todo el año); un cierre a mitad de año se maneja con exclusiones. */
IF OBJECT_ID('dbo.vw_tmi_centro_base', 'V') IS NULL EXEC (N'CREATE VIEW dbo.vw_tmi_centro_base AS SELECT 1 AS x');
GO
ALTER VIEW dbo.vw_tmi_centro_base AS
SELECT id AS id_centro, CASE WHEN LTRIM(RTRIM(codcentro)) NOT LIKE '%[^0-9]%' AND LEN(LTRIM(RTRIM(codcentro))) BETWEEN 1 AND 9 THEN CAST(LTRIM(RTRIM(codcentro)) AS INT) END AS codcentro,
       LTRIM(RTRIM(codred)) AS codred, LTRIM(RTRIM(red)) AS red,
       LTRIM(RTRIM(centro)) AS centro, LTRIM(RTRIM(categoria)) AS categoria, LTRIM(RTRIM(nivel)) AS nivel,
       LTRIM(RTRIM(nivel_estandar)) AS nivel_estandar, LTRIM(RTRIM(tipo)) AS tipo,
       CAST(ISNULL(flag, 1) AS BIT) AS flag
FROM dbo.tmi_centro
WHERE LTRIM(RTRIM(codcentro)) NOT LIKE '%[^0-9]%' AND LEN(LTRIM(RTRIM(codcentro))) BETWEEN 1 AND 9;
GO

/* ---------- vw_tmi_exclusion: exclusión por centro, indicador (NULL = todos) y mes ----------
   x01..x12: el mes está excluido. resultado: 'NA' (por defecto) o '0'.
   r01..r12: resultado de cada mes, el propio del mes (res_MM) o, si no tiene, el de la fila. */
IF OBJECT_ID('dbo.vw_tmi_exclusion', 'V') IS NULL EXEC (N'CREATE VIEW dbo.vw_tmi_exclusion AS SELECT 1 AS x');
GO
ALTER VIEW dbo.vw_tmi_exclusion AS
SELECT COALESCE(CASE WHEN LTRIM(RTRIM(e.codcentro)) NOT LIKE '%[^0-9]%' AND LEN(LTRIM(RTRIM(e.codcentro))) BETWEEN 1 AND 9 THEN CAST(LTRIM(RTRIM(e.codcentro)) AS INT) END, c.codcentro) AS codcentro,
       e.id_indicador AS id_estandar, e.anio,
       CAST(ISNULL(e.excl_01, 0) AS BIT) AS x01, CAST(ISNULL(e.excl_02, 0) AS BIT) AS x02, CAST(ISNULL(e.excl_03, 0) AS BIT) AS x03, CAST(ISNULL(e.excl_04, 0) AS BIT) AS x04,
       CAST(ISNULL(e.excl_05, 0) AS BIT) AS x05, CAST(ISNULL(e.excl_06, 0) AS BIT) AS x06, CAST(ISNULL(e.excl_07, 0) AS BIT) AS x07, CAST(ISNULL(e.excl_08, 0) AS BIT) AS x08,
       CAST(ISNULL(e.excl_09, 0) AS BIT) AS x09, CAST(ISNULL(e.excl_10, 0) AS BIT) AS x10, CAST(ISNULL(e.excl_11, 0) AS BIT) AS x11, CAST(ISNULL(e.excl_12, 0) AS BIT) AS x12,
       e.motivo, CAST(ISNULL(e.resultado, 'NA') AS VARCHAR(2)) AS resultado,
       CAST(COALESCE(e.res_01, e.resultado, 'NA') AS VARCHAR(2)) AS r01, CAST(COALESCE(e.res_02, e.resultado, 'NA') AS VARCHAR(2)) AS r02, CAST(COALESCE(e.res_03, e.resultado, 'NA') AS VARCHAR(2)) AS r03,
       CAST(COALESCE(e.res_04, e.resultado, 'NA') AS VARCHAR(2)) AS r04, CAST(COALESCE(e.res_05, e.resultado, 'NA') AS VARCHAR(2)) AS r05, CAST(COALESCE(e.res_06, e.resultado, 'NA') AS VARCHAR(2)) AS r06,
       CAST(COALESCE(e.res_07, e.resultado, 'NA') AS VARCHAR(2)) AS r07, CAST(COALESCE(e.res_08, e.resultado, 'NA') AS VARCHAR(2)) AS r08, CAST(COALESCE(e.res_09, e.resultado, 'NA') AS VARCHAR(2)) AS r09,
       CAST(COALESCE(e.res_10, e.resultado, 'NA') AS VARCHAR(2)) AS r10, CAST(COALESCE(e.res_11, e.resultado, 'NA') AS VARCHAR(2)) AS r11, CAST(COALESCE(e.res_12, e.resultado, 'NA') AS VARCHAR(2)) AS r12
FROM dbo.tmi_exclusion_centro_indicador e
LEFT JOIN dbo.vw_tmi_centro_base c ON c.id_centro = e.id_centro;
GO

/* ---------- vw_tmi_estandar_centro: estándar propio de cada centro ---------- */
IF OBJECT_ID('dbo.vw_tmi_estandar_centro', 'V') IS NULL EXEC (N'CREATE VIEW dbo.vw_tmi_estandar_centro AS SELECT 1 AS x');
GO
ALTER VIEW dbo.vw_tmi_estandar_centro AS
SELECT COALESCE(CASE WHEN LTRIM(RTRIM(ce.codcentro)) NOT LIKE '%[^0-9]%' AND LEN(LTRIM(RTRIM(ce.codcentro))) BETWEEN 1 AND 9 THEN CAST(LTRIM(RTRIM(ce.codcentro)) AS INT) END, c.codcentro) AS codcentro,
       ce.id_indicador AS id_estandar, ce.anio,
       ce.est_01 AS m01, ce.est_02 AS m02, ce.est_03 AS m03, ce.est_04 AS m04, ce.est_05 AS m05, ce.est_06 AS m06,
       ce.est_07 AS m07, ce.est_08 AS m08, ce.est_09 AS m09, ce.est_10 AS m10, ce.est_11 AS m11, ce.est_12 AS m12,
       ce.aplica, ce.sustento
FROM dbo.tmi_estandar_centro ce
LEFT JOIN dbo.vw_tmi_centro_base c ON c.id_centro = ce.id_centro;
GO
