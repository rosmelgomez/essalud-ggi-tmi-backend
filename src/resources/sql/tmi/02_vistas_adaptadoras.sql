/* =====================================================================================================
   TMI DINAMICO - 02 VISTAS ADAPTADORAS
   Las tablas existentes no tienen las mismas columnas en todas las bases:
     - estándares: est_01..12  o  estandar_01..12 ; id_estandar  o  id_indicador
                   o formato largo (indicador por nombre, mes, estandar)
     - tmi_centro: flag (un solo valor)  o  anio + flag_01..12
     - exclusiones: excl_01..12  o  estandar_01..12 ; id_centro y/o codcentro
   Estas vistas se arman con las columnas que existan, y el cálculo (04_procedimientos.sql) lee solo de ellas.
   Compatible con SQL Server 2008 R2+.
   ===================================================================================================== */

/* ---------- Sinónimo con el nombre anterior de tmi_exclusion_centro_indicador ----------
   Para las consultas existentes (002/003_TMI_CONSULTAS_VISTA.sql, Pentaho...). La tabla la crea src/main/model. */
IF OBJECT_ID('dbo.tmi_exclusion_centro_estandar') IS NULL
    EXEC (N'CREATE SYNONYM dbo.tmi_exclusion_centro_estandar FOR dbo.tmi_exclusion_centro_indicador');
GO

/* ---------- tmi_centro con la estructura anterior (sin nivel_estandar) ----------
   Antes: tipo = NIVEL_ESTANDAR del Excel (H.I, C.M., POL. ...) y categoria = TIPO del Excel (C.A.P.II, P.M. ...).
   Ahora: nivel_estandar = NIVEL_ESTANDAR, tipo = TIPO y categoria queda libre; nivel (I, II, III) ya no se usa.
   Solo se ejecuta una vez: cuando la tabla todavía no tiene nivel_estandar. */
IF OBJECT_ID('dbo.tmi_centro') IS NOT NULL AND COL_LENGTH('dbo.tmi_centro', 'nivel_estandar') IS NULL
BEGIN
    ALTER TABLE dbo.tmi_centro ADD nivel_estandar VARCHAR(50) NULL;
    EXEC (N'UPDATE dbo.tmi_centro SET nivel_estandar = tipo, tipo = categoria, categoria = NULL');
END
GO

/* ---------- vw_tmi_std: estándar por TIPO / NIVEL / CATEGORIA en formato común ---------- */
DECLARE @sql NVARCHAR(MAX) = N'', @t SYSNAME, @fuente VARCHAR(10), @clave SYSNAME, @pre SYSNAME, @id SYSNAME, @cols NVARCHAR(MAX);
DECLARE @tablas TABLE (tabla SYSNAME, fuente VARCHAR(10), clave SYSNAME);
INSERT INTO @tablas VALUES ('tmi_estandar_tipo', 'TIPO', 'tipo_centro'),
                           ('tmi_estandar_nivel', 'NIVEL', 'nivel_centro'),
                           ('tmi_estandar_categoria', 'CATEGORIA', 'categoria_centro');
DECLARE c CURSOR LOCAL FAST_FORWARD FOR SELECT tabla, fuente, clave FROM @tablas;
OPEN c; FETCH NEXT FROM c INTO @t, @fuente, @clave;
WHILE @@FETCH_STATUS = 0
BEGIN
    IF OBJECT_ID('dbo.' + @t) IS NOT NULL AND COL_LENGTH('dbo.' + @t, 'mes') IS NOT NULL AND COL_LENGTH('dbo.' + @t, 'estandar') IS NOT NULL
    BEGIN
        /* formato largo: una fila por mes (mes, estandar) y el indicador por nombre;
           si solo hay un mes cargado en el año, se usa ese estándar para los demás meses */
        SELECT @cols = STUFF((
            SELECT ', COALESCE(MAX(CASE WHEN s.mes = ' + CAST(n AS VARCHAR) + ' THEN CASE WHEN ISNUMERIC(s.estandar) = 1 THEN CAST(s.estandar AS FLOAT) END END), MAX(CASE WHEN ISNUMERIC(s.estandar) = 1 THEN CAST(s.estandar AS FLOAT) END)) AS m'
                   + RIGHT('0' + CAST(n AS VARCHAR), 2)
            FROM (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) x(n)
            ORDER BY n
            FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, '');
        SET @sql += CASE WHEN @sql = N'' THEN N'' ELSE N' UNION ALL ' END
                 + N'SELECT i.id AS id_estandar, ''' + @fuente + N''' AS fuente, LTRIM(RTRIM(s.' + QUOTENAME(@clave) + N')) AS clave, s.anio, '
                 + @cols + N', CAST(NULL AS FLOAT) AS m00 FROM dbo.' + QUOTENAME(@t) + N' s'
                 + N' JOIN dbo.tmi_indicador i ON REPLACE(LTRIM(RTRIM(i.indicador)), '' de '', '' '') = REPLACE(LTRIM(RTRIM(s.indicador)), '' de '', '' '')'
                 + N' GROUP BY i.id, LTRIM(RTRIM(s.' + QUOTENAME(@clave) + N')), s.anio';
    END
    ELSE IF OBJECT_ID('dbo.' + @t) IS NOT NULL
    BEGIN
        SET @pre = CASE WHEN COL_LENGTH('dbo.' + @t, 'est_01') IS NOT NULL THEN 'est_' ELSE 'estandar_' END;
        SET @id  = CASE WHEN COL_LENGTH('dbo.' + @t, 'id_estandar') IS NOT NULL THEN 'id_estandar' ELSE 'id_indicador' END;
        SELECT @cols = STUFF((
            SELECT ', ' + CASE WHEN COL_LENGTH('dbo.' + @t, 'est_fijo') IS NOT NULL
                               -- un mes sin valor (aún no cerrado) queda vacío: el cierre del mes le copia est_fijo
                               THEN 'CASE WHEN ' + QUOTENAME(@pre + RIGHT('0' + CAST(n AS VARCHAR), 2)) + ' IS NOT NULL THEN COALESCE(NULLIF(CAST('
                                    + QUOTENAME(@pre + RIGHT('0' + CAST(n AS VARCHAR), 2)) + ' AS FLOAT), 0), CAST([est_fijo] AS FLOAT)) END'
                               ELSE 'CAST(' + QUOTENAME(@pre + RIGHT('0' + CAST(n AS VARCHAR), 2)) + ' AS FLOAT)' END
                   + ' AS m' + RIGHT('0' + CAST(n AS VARCHAR), 2)
            FROM (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) x(n)
            ORDER BY n
            FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, '');
        SET @sql += CASE WHEN @sql = N'' THEN N'' ELSE N' UNION ALL ' END
                 + N'SELECT ' + QUOTENAME(@id) + N' AS id_estandar, ''' + @fuente + N''' AS fuente, '
                 + N'LTRIM(RTRIM(' + QUOTENAME(@clave) + N')) AS clave, anio, ' + @cols
                 /* m00 = fijo del año: el cálculo lo usa en un mes aún no cerrado (vacío); m01..m12 no cambian */
                 + CASE WHEN COL_LENGTH('dbo.' + @t, 'est_fijo') IS NOT NULL THEN N', CAST([est_fijo] AS FLOAT) AS m00' ELSE N', CAST(NULL AS FLOAT) AS m00' END
                 + N' FROM dbo.' + QUOTENAME(@t);
    END
    FETCH NEXT FROM c INTO @t, @fuente, @clave;
END
CLOSE c; DEALLOCATE c;
IF @sql = N''
    SET @sql = N'SELECT CAST(NULL AS INT) AS id_estandar, CAST(NULL AS VARCHAR(10)) AS fuente, CAST(NULL AS VARCHAR(50)) AS clave, CAST(NULL AS INT) AS anio, '
             + N'CAST(NULL AS FLOAT) m01, CAST(NULL AS FLOAT) m02, CAST(NULL AS FLOAT) m03, CAST(NULL AS FLOAT) m04, CAST(NULL AS FLOAT) m05, CAST(NULL AS FLOAT) m06, '
             + N'CAST(NULL AS FLOAT) m07, CAST(NULL AS FLOAT) m08, CAST(NULL AS FLOAT) m09, CAST(NULL AS FLOAT) m10, CAST(NULL AS FLOAT) m11, CAST(NULL AS FLOAT) m12, CAST(NULL AS FLOAT) m00 WHERE 1 = 0';
/* ALTER en lugar de DROP + CREATE: la vista nunca deja de existir (las consultas en curso no fallan) */
IF OBJECT_ID('dbo.vw_tmi_std', 'V') IS NULL EXEC(N'CREATE VIEW dbo.vw_tmi_std AS SELECT 1 AS x');
SET @sql = N'ALTER VIEW dbo.vw_tmi_std AS ' + @sql;
EXEC sp_executesql @sql;
GO

/* ---------- vw_tmi_centro_base: centro con visibilidad por mes (f01..f12) ---------- */
DECLARE @sql NVARCHAR(MAX), @flags NVARCHAR(MAX), @anio NVARCHAR(100), @nivel_est NVARCHAR(200), @codred NVARCHAR(200), @orden NVARCHAR(400), @orden_tipo NVARCHAR(400);
IF COL_LENGTH('dbo.tmi_centro', 'flag_01') IS NOT NULL
    SELECT @flags = STUFF((
        SELECT ', CAST(ISNULL(flag_' + RIGHT('0' + CAST(n AS VARCHAR), 2) + ', 1) AS BIT) AS f' + RIGHT('0' + CAST(n AS VARCHAR), 2)
        FROM (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) x(n)
        ORDER BY n
        FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, '');
ELSE IF COL_LENGTH('dbo.tmi_centro', 'flag') IS NOT NULL
    SELECT @flags = STUFF((
        SELECT ', CAST(ISNULL(flag, 1) AS BIT) AS f' + RIGHT('0' + CAST(n AS VARCHAR), 2)
        FROM (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) x(n)
        ORDER BY n
        FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, '');
ELSE
    SELECT @flags = STUFF((
        SELECT ', CAST(1 AS BIT) AS f' + RIGHT('0' + CAST(n AS VARCHAR), 2)
        FROM (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) x(n)
        ORDER BY n
        FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, '');
SET @anio = CASE WHEN COL_LENGTH('dbo.tmi_centro', 'anio') IS NOT NULL THEN N'anio' ELSE N'CAST(NULL AS INT)' END;
-- nivel_estandar reemplaza a nivel en la unión con los estándares (fuente NIVEL); si la tabla aún no la tiene, se usa nivel
SET @nivel_est = CASE WHEN COL_LENGTH('dbo.tmi_centro', 'nivel_estandar') IS NOT NULL THEN N'LTRIM(RTRIM(nivel_estandar))' ELSE N'LTRIM(RTRIM(nivel))' END;
SET @codred = CASE WHEN COL_LENGTH('dbo.tmi_centro', 'codred') IS NOT NULL THEN N'LTRIM(RTRIM(codred))' ELSE N'CAST(NULL AS VARCHAR(50))' END;
SET @orden = CASE WHEN COL_LENGTH('dbo.tmi_centro', 'orden') IS NOT NULL
                  THEN N'CASE WHEN LTRIM(RTRIM(CAST(orden AS VARCHAR(50)))) NOT LIKE ''%[^0-9]%'' AND LEN(LTRIM(RTRIM(CAST(orden AS VARCHAR(50))))) BETWEEN 1 AND 9 THEN CAST(LTRIM(RTRIM(CAST(orden AS VARCHAR(50)))) AS INT) END'
                  ELSE N'CAST(NULL AS INT)' END;
SET @orden_tipo = CASE WHEN COL_LENGTH('dbo.tmi_centro', 'orden_tipo') IS NOT NULL
                  THEN N'CASE WHEN LTRIM(RTRIM(CAST(orden_tipo AS VARCHAR(50)))) NOT LIKE ''%[^0-9]%'' AND LEN(LTRIM(RTRIM(CAST(orden_tipo AS VARCHAR(50))))) BETWEEN 1 AND 9 THEN CAST(LTRIM(RTRIM(CAST(orden_tipo AS VARCHAR(50)))) AS INT) END'
                  ELSE N'CAST(NULL AS INT)' END;
/* ALTER en lugar de DROP + CREATE: la vista nunca deja de existir (las consultas en curso no fallan) */
IF OBJECT_ID('dbo.vw_tmi_centro_base', 'V') IS NULL EXEC(N'CREATE VIEW dbo.vw_tmi_centro_base AS SELECT 1 AS x');
SET @sql = N'ALTER VIEW dbo.vw_tmi_centro_base AS
SELECT id AS id_centro,
       CASE WHEN LTRIM(RTRIM(codcentro)) NOT LIKE ''%[^0-9]%'' AND LEN(LTRIM(RTRIM(codcentro))) BETWEEN 1 AND 9 THEN CAST(LTRIM(RTRIM(codcentro)) AS INT) END AS codcentro,
       ' + @codred + N' AS codred, LTRIM(RTRIM(red)) AS red,
       ' + @orden + N' AS orden,
       ' + @orden_tipo + N' AS orden_tipo,
       LTRIM(RTRIM(centro)) AS centro,
       LTRIM(RTRIM(categoria)) AS categoria, LTRIM(RTRIM(nivel)) AS nivel, ' + @nivel_est + N' AS nivel_estandar, LTRIM(RTRIM(tipo)) AS tipo,
       ' + @anio + N' AS anio, ' + @flags + N'
FROM dbo.tmi_centro
WHERE LTRIM(RTRIM(codcentro)) NOT LIKE ''%[^0-9]%'' AND LEN(LTRIM(RTRIM(codcentro))) BETWEEN 1 AND 9';
EXEC sp_executesql @sql;
GO

/* ---------- vw_tmi_exclusion: exclusión por centro, indicador (NULL = todos) y mes ---------- */
DECLARE @sql NVARCHAR(MAX), @pre SYSNAME, @cols NVARCHAR(MAX), @cod NVARCHAR(400), @motivo NVARCHAR(100), @resultado NVARCHAR(100);
SET @pre = CASE WHEN COL_LENGTH('dbo.tmi_exclusion_centro_indicador', 'excl_01') IS NOT NULL THEN 'excl_' ELSE 'estandar_' END;
SELECT @cols = STUFF((
    SELECT ', CAST(ISNULL(e.' + QUOTENAME(@pre + RIGHT('0' + CAST(n AS VARCHAR), 2)) + ', 0) AS BIT) AS x'
           + RIGHT('0' + CAST(n AS VARCHAR), 2)
    FROM (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) x(n)
    ORDER BY n
    FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, '');
SET @cod = CASE WHEN COL_LENGTH('dbo.tmi_exclusion_centro_indicador', 'codcentro') IS NOT NULL
                THEN N'COALESCE(CASE WHEN LTRIM(RTRIM(e.codcentro)) NOT LIKE ''%[^0-9]%'' AND LEN(LTRIM(RTRIM(e.codcentro))) BETWEEN 1 AND 9 THEN CAST(LTRIM(RTRIM(e.codcentro)) AS INT) END, c.codcentro)' ELSE N'c.codcentro' END;
SET @motivo = CASE WHEN COL_LENGTH('dbo.tmi_exclusion_centro_indicador', 'motivo') IS NOT NULL THEN N'e.motivo' ELSE N'CAST(NULL AS VARCHAR(300))' END;
-- resultado del mes excluido: '0' (por defecto) o 'NA'
SET @resultado = CASE WHEN COL_LENGTH('dbo.tmi_exclusion_centro_indicador', 'resultado') IS NOT NULL
                      THEN N'CAST(ISNULL(e.resultado, ''0'') AS VARCHAR(2))' ELSE N'CAST(''0'' AS VARCHAR(2))' END;
/* ALTER en lugar de DROP + CREATE: la vista nunca deja de existir (las consultas en curso no fallan) */
IF OBJECT_ID('dbo.vw_tmi_exclusion', 'V') IS NULL EXEC(N'CREATE VIEW dbo.vw_tmi_exclusion AS SELECT 1 AS x');
SET @sql = N'ALTER VIEW dbo.vw_tmi_exclusion AS
SELECT ' + @cod + N' AS codcentro, e.' + CASE WHEN COL_LENGTH('dbo.tmi_exclusion_centro_indicador', 'id_estandar') IS NOT NULL
                                              THEN N'id_estandar' ELSE N'id_indicador' END + N' AS id_estandar,
       e.anio, ' + @cols + N', ' + @motivo + N' AS motivo, ' + @resultado + N' AS resultado
FROM dbo.tmi_exclusion_centro_indicador e
LEFT JOIN dbo.vw_tmi_centro_base c ON c.id_centro = e.id_centro';
EXEC sp_executesql @sql;
GO

/* ---------- vw_tmi_centro_estandar: estándar específico de centro ---------- */
DECLARE @sql NVARCHAR(MAX), @pre SYSNAME, @cols NVARCHAR(MAX), @cod NVARCHAR(400);
SET @pre = CASE WHEN COL_LENGTH('dbo.tmi_centro_estandar', 'est_01') IS NOT NULL THEN 'est_' ELSE 'estandar_' END;
SELECT @cols = STUFF((
    SELECT ', CAST(ce.' + QUOTENAME(@pre + RIGHT('0' + CAST(n AS VARCHAR), 2)) + ' AS FLOAT) AS m'
           + RIGHT('0' + CAST(n AS VARCHAR), 2)
    FROM (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) x(n)
    ORDER BY n
    FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, '');
SET @cod = N'COALESCE(CASE WHEN LTRIM(RTRIM(ce.codcentro)) NOT LIKE ''%[^0-9]%'' AND LEN(LTRIM(RTRIM(ce.codcentro))) BETWEEN 1 AND 9 THEN CAST(LTRIM(RTRIM(ce.codcentro)) AS INT) END, c.codcentro)';
/* ALTER en lugar de DROP + CREATE: la vista nunca deja de existir (las consultas en curso no fallan) */
IF OBJECT_ID('dbo.vw_tmi_centro_estandar', 'V') IS NULL EXEC(N'CREATE VIEW dbo.vw_tmi_centro_estandar AS SELECT 1 AS x');
SET @sql = N'ALTER VIEW dbo.vw_tmi_centro_estandar AS
SELECT ' + @cod + N' AS codcentro, ce.' + CASE WHEN COL_LENGTH('dbo.tmi_centro_estandar', 'id_estandar') IS NOT NULL
                                               THEN N'id_estandar' ELSE N'id_indicador' END + N' AS id_estandar,
       ce.anio, ' + @cols + N', ce.aplica, ce.acept, ce.sustento
FROM dbo.tmi_centro_estandar ce
LEFT JOIN dbo.vw_tmi_centro_base c ON c.id_centro = ce.id_centro';
EXEC sp_executesql @sql;
GO
