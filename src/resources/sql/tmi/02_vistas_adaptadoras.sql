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
                 + @cols + N' FROM dbo.' + QUOTENAME(@t) + N' s'
                 + N' JOIN dbo.tmi_indicador i ON REPLACE(LTRIM(RTRIM(i.indicador)), '' de '', '' '') = REPLACE(LTRIM(RTRIM(s.indicador)), '' de '', '' '')'
                 + N' GROUP BY i.id, LTRIM(RTRIM(s.' + QUOTENAME(@clave) + N')), s.anio';
    END
    ELSE IF OBJECT_ID('dbo.' + @t) IS NOT NULL
    BEGIN
        SET @pre = CASE WHEN COL_LENGTH('dbo.' + @t, 'est_01') IS NOT NULL THEN 'est_' ELSE 'estandar_' END;
        SET @id  = CASE WHEN COL_LENGTH('dbo.' + @t, 'id_estandar') IS NOT NULL THEN 'id_estandar' ELSE 'id_indicador' END;
        SELECT @cols = STUFF((
            SELECT ', CAST(' + QUOTENAME(@pre + RIGHT('0' + CAST(n AS VARCHAR), 2)) + ' AS FLOAT) AS m'
                   + RIGHT('0' + CAST(n AS VARCHAR), 2)
            FROM (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) x(n)
            ORDER BY n
            FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, '');
        SET @sql += CASE WHEN @sql = N'' THEN N'' ELSE N' UNION ALL ' END
                 + N'SELECT ' + QUOTENAME(@id) + N' AS id_estandar, ''' + @fuente + N''' AS fuente, '
                 + N'LTRIM(RTRIM(' + QUOTENAME(@clave) + N')) AS clave, anio, ' + @cols + N' FROM dbo.' + QUOTENAME(@t);
    END
    FETCH NEXT FROM c INTO @t, @fuente, @clave;
END
CLOSE c; DEALLOCATE c;
IF @sql = N''
    SET @sql = N'SELECT CAST(NULL AS INT) AS id_estandar, CAST(NULL AS VARCHAR(10)) AS fuente, CAST(NULL AS VARCHAR(50)) AS clave, CAST(NULL AS INT) AS anio, '
             + N'CAST(NULL AS FLOAT) m01, CAST(NULL AS FLOAT) m02, CAST(NULL AS FLOAT) m03, CAST(NULL AS FLOAT) m04, CAST(NULL AS FLOAT) m05, CAST(NULL AS FLOAT) m06, '
             + N'CAST(NULL AS FLOAT) m07, CAST(NULL AS FLOAT) m08, CAST(NULL AS FLOAT) m09, CAST(NULL AS FLOAT) m10, CAST(NULL AS FLOAT) m11, CAST(NULL AS FLOAT) m12 WHERE 1 = 0';
IF OBJECT_ID('dbo.vw_tmi_std', 'V') IS NOT NULL DROP VIEW dbo.vw_tmi_std;
SET @sql = N'CREATE VIEW dbo.vw_tmi_std AS ' + @sql;
EXEC sp_executesql @sql;
GO

/* ---------- vw_tmi_centro_base: centro con visibilidad por mes (f01..f12) ---------- */
DECLARE @sql NVARCHAR(MAX), @flags NVARCHAR(MAX), @anio NVARCHAR(100);
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
IF OBJECT_ID('dbo.vw_tmi_centro_base', 'V') IS NOT NULL DROP VIEW dbo.vw_tmi_centro_base;
SET @sql = N'CREATE VIEW dbo.vw_tmi_centro_base AS
SELECT id AS id_centro,
       CASE WHEN LTRIM(RTRIM(codcentro)) NOT LIKE ''%[^0-9]%'' AND LEN(LTRIM(RTRIM(codcentro))) BETWEEN 1 AND 9 THEN CAST(LTRIM(RTRIM(codcentro)) AS INT) END AS codcentro,
       LTRIM(RTRIM(red)) AS red,
       CASE WHEN LTRIM(RTRIM(CAST(orden AS VARCHAR(50)))) NOT LIKE ''%[^0-9]%'' AND LEN(LTRIM(RTRIM(CAST(orden AS VARCHAR(50))))) BETWEEN 1 AND 9 THEN CAST(LTRIM(RTRIM(CAST(orden AS VARCHAR(50)))) AS INT) END AS orden,
       CASE WHEN LTRIM(RTRIM(CAST(orden_tipo AS VARCHAR(50)))) NOT LIKE ''%[^0-9]%'' AND LEN(LTRIM(RTRIM(CAST(orden_tipo AS VARCHAR(50))))) BETWEEN 1 AND 9 THEN CAST(LTRIM(RTRIM(CAST(orden_tipo AS VARCHAR(50)))) AS INT) END AS orden_tipo,
       LTRIM(RTRIM(centro)) AS centro,
       LTRIM(RTRIM(categoria)) AS categoria, LTRIM(RTRIM(nivel)) AS nivel, LTRIM(RTRIM(tipo)) AS tipo,
       ' + @anio + N' AS anio, ' + @flags + N'
FROM dbo.tmi_centro
WHERE LTRIM(RTRIM(codcentro)) NOT LIKE ''%[^0-9]%'' AND LEN(LTRIM(RTRIM(codcentro))) BETWEEN 1 AND 9';
EXEC sp_executesql @sql;
GO

/* ---------- vw_tmi_exclusion: exclusión por centro, indicador (NULL = todos) y mes ---------- */
DECLARE @sql NVARCHAR(MAX), @pre SYSNAME, @cols NVARCHAR(MAX), @cod NVARCHAR(400), @motivo NVARCHAR(100);
SET @pre = CASE WHEN COL_LENGTH('dbo.tmi_exclusion_centro_estandar', 'excl_01') IS NOT NULL THEN 'excl_' ELSE 'estandar_' END;
SELECT @cols = STUFF((
    SELECT ', CAST(ISNULL(e.' + QUOTENAME(@pre + RIGHT('0' + CAST(n AS VARCHAR), 2)) + ', 0) AS BIT) AS x'
           + RIGHT('0' + CAST(n AS VARCHAR), 2)
    FROM (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) x(n)
    ORDER BY n
    FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 2, '');
SET @cod = CASE WHEN COL_LENGTH('dbo.tmi_exclusion_centro_estandar', 'codcentro') IS NOT NULL
                THEN N'COALESCE(CASE WHEN LTRIM(RTRIM(e.codcentro)) NOT LIKE ''%[^0-9]%'' AND LEN(LTRIM(RTRIM(e.codcentro))) BETWEEN 1 AND 9 THEN CAST(LTRIM(RTRIM(e.codcentro)) AS INT) END, c.codcentro)' ELSE N'c.codcentro' END;
SET @motivo = CASE WHEN COL_LENGTH('dbo.tmi_exclusion_centro_estandar', 'motivo') IS NOT NULL THEN N'e.motivo' ELSE N'CAST(NULL AS VARCHAR(300))' END;
IF OBJECT_ID('dbo.vw_tmi_exclusion', 'V') IS NOT NULL DROP VIEW dbo.vw_tmi_exclusion;
SET @sql = N'CREATE VIEW dbo.vw_tmi_exclusion AS
SELECT ' + @cod + N' AS codcentro, e.' + CASE WHEN COL_LENGTH('dbo.tmi_exclusion_centro_estandar', 'id_estandar') IS NOT NULL
                                              THEN N'id_estandar' ELSE N'id_indicador' END + N' AS id_estandar,
       e.anio, ' + @cols + N', ' + @motivo + N' AS motivo
FROM dbo.tmi_exclusion_centro_estandar e
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
IF OBJECT_ID('dbo.vw_tmi_centro_estandar', 'V') IS NOT NULL DROP VIEW dbo.vw_tmi_centro_estandar;
SET @sql = N'CREATE VIEW dbo.vw_tmi_centro_estandar AS
SELECT ' + @cod + N' AS codcentro, ce.' + CASE WHEN COL_LENGTH('dbo.tmi_centro_estandar', 'id_estandar') IS NOT NULL
                                               THEN N'id_estandar' ELSE N'id_indicador' END + N' AS id_estandar,
       ce.anio, ' + @cols + N', ce.aplica, ce.acept, ce.sustento
FROM dbo.tmi_centro_estandar ce
LEFT JOIN dbo.vw_tmi_centro_base c ON c.id_centro = ce.id_centro';
EXEC sp_executesql @sql;
GO
