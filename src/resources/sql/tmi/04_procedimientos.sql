/* =====================================================================================================
   TMI DINAMICO - 04 PROCEDIMIENTOS
     EXEC dbo.usp_tmi_validar_config;          -- 0 filas = configuración correcta
     EXEC dbo.usp_tmi_generar_pivot 202608;    -- variables usadas por indicadores activos -> tmi_variable_pivot
     EXEC dbo.usp_tmi_calcular      202608;    -- indicadores, estándar, puntaje -> tmi_resultado y tmi_resultado_indicador
   Compatible con SQL Server 2008 R2+.
   ===================================================================================================== */

/* -----------------------------------------------------------------------------------------------------
   0. VALIDACION DE LA CONFIGURACION
   ----------------------------------------------------------------------------------------------------- */
IF OBJECT_ID('dbo.usp_tmi_validar_config', 'P') IS NOT NULL DROP PROCEDURE dbo.usp_tmi_validar_config;
GO
CREATE PROCEDURE dbo.usp_tmi_validar_config
AS
BEGIN
    SET NOCOUNT ON;
    -- Las DIM pueden estar en otro servidor (servidor vinculado): se copian una vez y se consultan localmente
    SELECT DISTINCT tipgrupo INTO #dim_grupo FROM {{DIM}}.DIM_GRUPO;
    SELECT DISTINCT actividad INTO #dim_actividad FROM {{DIM}}.DIM_ACTIVIDAD;
    SELECT i.id AS id_indicador, i.codigo AS elemento, 'Fórmula con caracteres no permitidos (solo A-Z, números, espacios, + - * / . y paréntesis)' AS problema
    FROM dbo.tmi_indicador i
    WHERE i.activo = 1
      AND (PATINDEX('%[^A-Z0-9 ().+*/-]%', ISNULL(i.expr_numerador, '') COLLATE Latin1_General_BIN) > 0
        OR PATINDEX('%[^A-Z0-9 ().+*/-]%', ISNULL(i.expr_denominador, '') COLLATE Latin1_General_BIN) > 0)
    UNION ALL
    SELECT i.id, i.codigo, 'Falta numerador, denominador, nombre de hoja, tipo de cálculo, sentido o base de estándar'
    FROM dbo.tmi_indicador i
    WHERE i.activo = 1
      AND (NULLIF(LTRIM(i.expr_numerador), '') IS NULL OR NULLIF(LTRIM(i.expr_denominador), '') IS NULL
        OR i.nombre_hoja IS NULL OR i.tipo_calculo IS NULL OR i.sentido IS NULL OR i.base_estandar IS NULL)
    UNION ALL
    SELECT i.id, i.codigo, 'Tipo de estándar no existe en tmi_tipo_estandar: ' + i.base_estandar
    FROM dbo.tmi_indicador i
    WHERE i.activo = 1 AND i.base_estandar IS NOT NULL
      AND NOT EXISTS (SELECT 1 FROM dbo.tmi_tipo_estandar t WHERE t.codigo = i.base_estandar)
    UNION ALL
    SELECT i.id, i.codigo, 'Tipo de estándar ' + i.base_estandar + ' sin claves activas en tmi_estandar'
    FROM dbo.tmi_indicador i
    WHERE i.activo = 1 AND EXISTS (SELECT 1 FROM dbo.tmi_tipo_estandar t WHERE t.codigo = i.base_estandar)
      AND NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar e WHERE e.tipo_estandar = i.base_estandar AND e.activo = 1)
    UNION ALL
    SELECT i.id, i.codigo, 'Tipo de cálculo no existe en tmi_tipo_calculo: ' + i.tipo_calculo
    FROM dbo.tmi_indicador i
    WHERE i.activo = 1 AND i.tipo_calculo IS NOT NULL
      AND NOT EXISTS (SELECT 1 FROM dbo.tmi_tipo_calculo t WHERE t.codigo = i.tipo_calculo)
    UNION ALL
    SELECT i.id, i.codigo, 'Nombre de hoja repetido: ' + i.nombre_hoja
    FROM dbo.tmi_indicador i
    WHERE i.activo = 1 AND EXISTS (SELECT 1 FROM dbo.tmi_indicador j WHERE j.activo = 1 AND j.id <> i.id AND j.nombre_hoja = i.nombre_hoja)
    UNION ALL
    SELECT i.id, i.codigo, 'Letra ' + l.letra + ' usada en la fórmula sin variable en tmi_indicador_variable'
    FROM dbo.tmi_indicador i
    CROSS APPLY (SELECT CHAR(n) AS letra FROM (VALUES (65),(66),(67),(68),(69),(70),(71),(72),(73),(74),(75),(76),(77),
                                                      (78),(79),(80),(81),(82),(83),(84),(85),(86),(87),(88),(89),(90)) x(n)) l
    WHERE i.activo = 1
      AND CHARINDEX(l.letra COLLATE Latin1_General_BIN,
                    (ISNULL(i.expr_numerador, '') + ' ' + ISNULL(i.expr_denominador, '')) COLLATE Latin1_General_BIN) > 0
      AND NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador_variable iv WHERE iv.id_indicador = i.id AND iv.letra = l.letra)
    UNION ALL
    SELECT i.id, v.nombre, 'Variable sin filas activas en tmi_variable_logica'
    FROM dbo.tmi_indicador i
    JOIN dbo.tmi_indicador_variable iv ON iv.id_indicador = i.id
    JOIN dbo.tmi_variable v ON v.id = iv.id_variable
    WHERE i.activo = 1
      AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.activo = 1)
    UNION ALL
    SELECT NULL, v.nombre, 'Grupo/actividad repetido en la variable (tipgrupo ' + CAST(l.tipgrupo AS VARCHAR(10))
                           + ', actividad ' + CAST(l.actividad AS VARCHAR(10)) + '): se contaría dos veces'
    FROM dbo.tmi_variable_logica l
    JOIN dbo.tmi_variable v ON v.id = l.id_variable
    JOIN dbo.tmi_variable_logica l2 ON l2.id_variable = l.id_variable AND l2.id > l.id AND l2.activo = 1
     AND l2.tipgrupo = l.tipgrupo AND l2.actividad = l.actividad
     AND (l2.servicio IS NULL OR l.servicio IS NULL OR l2.servicio = l.servicio)
     AND l2.periodo_desde <= l.periodo_hasta AND l.periodo_desde <= l2.periodo_hasta
    WHERE l.activo = 1
    UNION ALL
    SELECT NULL, v.nombre, 'tipgrupo ' + CAST(l.tipgrupo AS VARCHAR(10)) + ' no existe en DIM_GRUPO'
    FROM dbo.tmi_variable_logica l JOIN dbo.tmi_variable v ON v.id = l.id_variable
    WHERE l.activo = 1 AND NOT EXISTS (SELECT 1 FROM #dim_grupo g WHERE g.tipgrupo = l.tipgrupo)
    UNION ALL
    SELECT NULL, v.nombre, 'actividad ' + CAST(l.actividad AS VARCHAR(10)) + ' no existe en DIM_ACTIVIDAD'
    FROM dbo.tmi_variable_logica l JOIN dbo.tmi_variable v ON v.id = l.id_variable
    WHERE l.activo = 1 AND NOT EXISTS (SELECT 1 FROM #dim_actividad a WHERE a.actividad = l.actividad);
END
GO

/* -----------------------------------------------------------------------------------------------------
   1. PIVOT DE VARIABLES (solo las que usan los indicadores activos)
      Valor de la variable = suma de sus filas de tmi_variable_logica; cada fila con su agregación:
        SUMA    : suma de cantidad
        MEDIANA : mediana de cada servicio en el mes, redondeada, y suma de servicios (como CONSO4 / CONSO5)
   ----------------------------------------------------------------------------------------------------- */
IF OBJECT_ID('dbo.usp_tmi_generar_pivot', 'P') IS NOT NULL DROP PROCEDURE dbo.usp_tmi_generar_pivot;
GO
CREATE PROCEDURE dbo.usp_tmi_generar_pivot
    @PERIODO INT
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @anio INT = @PERIODO / 100;
    IF @PERIODO % 100 NOT BETWEEN 1 AND 12
    BEGIN
        RAISERROR('El periodo debe tener formato AAAAMM.', 16, 1);
        RETURN;
    END

    SELECT DISTINCT iv.id_variable
    INTO   #vars
    FROM   dbo.tmi_indicador_variable iv
    JOIN   dbo.tmi_indicador i ON i.id = iv.id_indicador AND i.activo = 1
    JOIN   dbo.tmi_variable  v ON v.id = iv.id_variable  AND v.activo = 1;

    /* TOTALIZADO3 y DIM_HOJA pueden estar en otro servidor (servidor vinculado, nombre de 4 partes en el .env).
       Una sola lectura de TOTALIZADO3: se copian solo las filas del año y de los grupos que usan las variables, con un
       filtro sobre una sola tabla y valores literales, para que se resuelva en el servidor remoto y viaje solo lo necesario.
       El cruce con tmi_variable_logica se hace después, contra la copia local. */
    DECLARE @grupos NVARCHAR(MAX), @sql NVARCHAR(MAX);
    SELECT @grupos = STUFF((
        SELECT N',' + CAST(g.tipgrupo AS NVARCHAR(20))
        FROM (SELECT DISTINCT L.tipgrupo FROM dbo.tmi_variable_logica L JOIN #vars V ON V.id_variable = L.id_variable
              WHERE L.activo = 1) g
        ORDER BY g.tipgrupo
        FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, N'');

    SELECT TOP 0 T.periodo, T.codcentro_ses, T.servicio, T.tipgrupo, T.actividad, T.tipohoja, T.cantidad
    INTO   #t3
    FROM   {{TOTALIZADO3}} T;
    IF @grupos IS NOT NULL
    BEGIN
        SET @sql = N'INSERT INTO #t3 (periodo, codcentro_ses, servicio, tipgrupo, actividad, tipohoja, cantidad)
                     SELECT T.periodo, T.codcentro_ses, T.servicio, T.tipgrupo, T.actividad, T.tipohoja, T.cantidad
                     FROM {{TOTALIZADO3}} T
                     WHERE T.periodo BETWEEN ' + CAST(@anio * 100 + 1 AS NVARCHAR(10)) + N' AND ' + CAST(@PERIODO AS NVARCHAR(10)) + N'
                       AND T.tipgrupo IN (' + @grupos + N');';
        EXEC sp_executesql @sql;
    END
    SELECT tipohoja, condicion INTO #dim_hoja FROM {{DIM}}.DIM_HOJA;

    SELECT T.periodo % 100 AS mes, T.codcentro_ses AS codcentro, T.servicio,
           L.id AS id_logica, L.id_variable, L.agregacion, CAST(T.cantidad AS FLOAT) AS cantidad
    INTO   #base
    FROM   #t3 T
    JOIN   dbo.tmi_variable_logica L
           ON  L.activo = 1
           AND L.tipgrupo = T.tipgrupo AND L.actividad = T.actividad
           AND (L.servicio IS NULL OR L.servicio = T.servicio)
           AND T.periodo BETWEEN L.periodo_desde AND L.periodo_hasta
    JOIN   #vars V ON V.id_variable = L.id_variable
    LEFT JOIN #dim_hoja H ON H.tipohoja = T.tipohoja
    WHERE  T.periodo BETWEEN @anio * 100 + 1 AND @PERIODO
      AND  (L.condicion_hoja IS NULL OR UPPER(H.condicion) = UPPER(L.condicion_hoja));

    SELECT mes, codcentro, id_variable, SUM(v) AS valor
    INTO   #mes
    FROM (
        SELECT mes, codcentro, id_variable, id_logica, SUM(cantidad) AS v
        FROM   #base WHERE agregacion = 'SUMA'
        GROUP BY mes, codcentro, id_variable, id_logica
        UNION ALL
        SELECT mes, codcentro, id_variable, id_logica, SUM(ROUND(med, 0))
        FROM (SELECT mes, codcentro, id_variable, id_logica, servicio, AVG(cantidad) AS med
              FROM (SELECT mes, codcentro, id_variable, id_logica, servicio, cantidad,
                           ROW_NUMBER() OVER (PARTITION BY mes, codcentro, id_logica, servicio ORDER BY cantidad) AS rn,
                           COUNT(*) OVER (PARTITION BY mes, codcentro, id_logica, servicio) AS cnt
                    FROM #base WHERE agregacion = 'MEDIANA') r
              WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
              GROUP BY mes, codcentro, id_variable, id_logica, servicio) m
        GROUP BY mes, codcentro, id_variable, id_logica
    ) x
    GROUP BY mes, codcentro, id_variable;

    -- Total anual MEDIANA_PERIODO: mediana de todo el periodo por servicio y suma (como #TEMPO2 de los CONSO)
    SELECT codcentro, id_variable, SUM(ROUND(med, 0)) AS total
    INTO   #total_mediana
    FROM (SELECT codcentro, id_variable, id_logica, servicio, AVG(cantidad) AS med
          FROM (SELECT codcentro, id_variable, id_logica, servicio, cantidad,
                       ROW_NUMBER() OVER (PARTITION BY codcentro, id_logica, servicio ORDER BY cantidad) AS rn,
                       COUNT(*) OVER (PARTITION BY codcentro, id_logica, servicio) AS cnt
                FROM #base WHERE agregacion = 'MEDIANA') r
          WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
          GROUP BY codcentro, id_variable, id_logica, servicio) m
    GROUP BY codcentro, id_variable;

    BEGIN TRAN;
    DELETE dbo.tmi_variable_pivot WHERE anio = @anio AND id_variable IN (SELECT id_variable FROM #vars);

    INSERT INTO dbo.tmi_variable_pivot (anio, codcentro, id_variable, total, m01, m02, m03, m04, m05, m06, m07, m08, m09, m10, m11, m12)
    SELECT @anio, m.codcentro, m.id_variable,
           CASE WHEN v.total_anual = 'MEDIANA_PERIODO' THEN MAX(t.total) ELSE SUM(m.valor) END,
           SUM(CASE WHEN m.mes =  1 THEN m.valor END), SUM(CASE WHEN m.mes =  2 THEN m.valor END),
           SUM(CASE WHEN m.mes =  3 THEN m.valor END), SUM(CASE WHEN m.mes =  4 THEN m.valor END),
           SUM(CASE WHEN m.mes =  5 THEN m.valor END), SUM(CASE WHEN m.mes =  6 THEN m.valor END),
           SUM(CASE WHEN m.mes =  7 THEN m.valor END), SUM(CASE WHEN m.mes =  8 THEN m.valor END),
           SUM(CASE WHEN m.mes =  9 THEN m.valor END), SUM(CASE WHEN m.mes = 10 THEN m.valor END),
           SUM(CASE WHEN m.mes = 11 THEN m.valor END), SUM(CASE WHEN m.mes = 12 THEN m.valor END)
    FROM   #mes m
    JOIN   dbo.tmi_variable v ON v.id = m.id_variable
    LEFT JOIN #total_mediana t ON t.codcentro = m.codcentro AND t.id_variable = m.id_variable
    GROUP BY m.codcentro, m.id_variable, v.total_anual;
    COMMIT;
END
GO

/* -----------------------------------------------------------------------------------------------------
   2. CALCULO DE INDICADORES
   ----------------------------------------------------------------------------------------------------- */
IF OBJECT_ID('dbo.usp_tmi_calcular', 'P') IS NOT NULL DROP PROCEDURE dbo.usp_tmi_calcular;
GO
CREATE PROCEDURE dbo.usp_tmi_calcular
    @PERIODO INT
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @anio INT = @PERIODO / 100, @mes INT = @PERIODO % 100;
    IF @mes NOT BETWEEN 1 AND 12
    BEGIN
        RAISERROR('El periodo debe tener formato AAAAMM.', 16, 1);
        RETURN;
    END

    /* 2.1 Valor de cada letra por centro y mes (varias variables con la misma letra se suman) */
    SELECT iv.id_indicador, p.codcentro, u.mes, iv.letra, SUM(u.valor) AS valor_mes
    INTO   #letra_mes
    FROM   dbo.tmi_indicador_variable iv
    JOIN   dbo.tmi_indicador i ON i.id = iv.id_indicador AND i.activo = 1
    JOIN   dbo.tmi_variable_pivot p ON p.id_variable = iv.id_variable AND p.anio = @anio
    CROSS APPLY (VALUES (1,p.m01),(2,p.m02),(3,p.m03),(4,p.m04),(5,p.m05),(6,p.m06),
                        (7,p.m07),(8,p.m08),(9,p.m09),(10,p.m10),(11,p.m11),(12,p.m12)) u(mes, valor)
    WHERE  u.mes <= @mes
    GROUP BY iv.id_indicador, p.codcentro, u.mes, iv.letra;

    /* 2.2 Centros del reporte y situación de cada mes (exclusión por periodo)
           - Filas = centros de tmi_centro del año (o sin año) visibles en el mes de corte (flag del mes).
           - Cada mes: si el flag del mes es 0 -> NA ese mes (NO_VIGENTE_MES).
           - vw_tmi_exclusion: excl del mes = 1 -> NA ese mes, para un indicador o todos (id_estandar NULL). */
    SELECT c.codcentro, MIN(c.id_centro) AS id_centro, MAX(c.red) AS red, MIN(c.orden) AS orden, MIN(c.orden_tipo) AS orden_tipo,
           MAX(c.centro) AS centro, MAX(c.categoria) AS categoria, MAX(c.nivel) AS nivel, MAX(c.tipo) AS tipo,
           MAX(CAST(c.f01 AS INT)) f01, MAX(CAST(c.f02 AS INT)) f02, MAX(CAST(c.f03 AS INT)) f03, MAX(CAST(c.f04 AS INT)) f04,
           MAX(CAST(c.f05 AS INT)) f05, MAX(CAST(c.f06 AS INT)) f06, MAX(CAST(c.f07 AS INT)) f07, MAX(CAST(c.f08 AS INT)) f08,
           MAX(CAST(c.f09 AS INT)) f09, MAX(CAST(c.f10 AS INT)) f10, MAX(CAST(c.f11 AS INT)) f11, MAX(CAST(c.f12 AS INT)) f12
    INTO   #centro
    FROM   dbo.vw_tmi_centro_base c
    WHERE  c.anio = @anio
       OR (c.anio IS NULL AND NOT EXISTS (SELECT 1 FROM dbo.vw_tmi_centro_base x WHERE x.anio = @anio))
    GROUP BY c.codcentro;

    DELETE #centro
    WHERE (CASE @mes WHEN 1 THEN f01 WHEN 2 THEN f02 WHEN 3 THEN f03 WHEN 4 THEN f04 WHEN 5 THEN f05 WHEN 6 THEN f06
                     WHEN 7 THEN f07 WHEN 8 THEN f08 WHEN 9 THEN f09 WHEN 10 THEN f10 WHEN 11 THEN f11 WHEN 12 THEN f12 END) = 0;

    SELECT i.id AS id_indicador, c.codcentro, c.red, c.orden, c.orden_tipo, c.id_centro, c.categoria, c.nivel, c.tipo, m.mes,
           CASE WHEN (CASE m.mes WHEN 1 THEN c.f01 WHEN 2 THEN c.f02 WHEN 3 THEN c.f03 WHEN 4 THEN c.f04 WHEN 5 THEN c.f05 WHEN 6 THEN c.f06
                                 WHEN 7 THEN c.f07 WHEN 8 THEN c.f08 WHEN 9 THEN c.f09 WHEN 10 THEN c.f10 WHEN 11 THEN c.f11 WHEN 12 THEN c.f12 END) = 0
                THEN 'NO_VIGENTE_MES' END AS motivo_centro,
           ISNULL(x.excluido, 0) AS excluido
    INTO   #centro_ind_mes
    FROM   #centro c
    CROSS JOIN dbo.tmi_indicador i
    CROSS JOIN (SELECT v AS mes FROM (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) z(v) WHERE v <= @mes) m
    OUTER APPLY (SELECT MAX(q.v) AS excluido
                 FROM (SELECT CAST(CASE m.mes WHEN 1 THEN e.x01 WHEN 2 THEN e.x02 WHEN 3 THEN e.x03 WHEN 4 THEN e.x04 WHEN 5 THEN e.x05 WHEN 6 THEN e.x06
                                              WHEN 7 THEN e.x07 WHEN 8 THEN e.x08 WHEN 9 THEN e.x09 WHEN 10 THEN e.x10 WHEN 11 THEN e.x11 WHEN 12 THEN e.x12 END AS INT) AS v
                       FROM dbo.vw_tmi_exclusion e
                       WHERE e.codcentro = c.codcentro AND e.anio = @anio
                         AND (e.id_estandar = i.id OR e.id_estandar IS NULL)) q) x
    WHERE  i.activo = 1;

    /* 2.3 MENSUAL = valor del mes ; ACUMULADO = enero..mes, sin los meses excluidos / no vigentes */
    SELECT l.id_indicador, l.codcentro, l.mes, l.letra, l.valor_mes,
           CASE WHEN i.tipo_calculo = 'ACUMULADO' THEN ISNULL(ac.valor_acum, 0) ELSE l.valor_mes END AS valor
    INTO   #letra
    FROM   #letra_mes l
    JOIN   dbo.tmi_indicador i ON i.id = l.id_indicador
    OUTER APPLY (
        SELECT SUM(CASE WHEN n2.excluido = 1 OR n2.motivo_centro IS NOT NULL THEN 0 ELSE ISNULL(l2.valor_mes, 0) END) AS valor_acum
        FROM #letra_mes l2
        LEFT JOIN #centro_ind_mes n2 ON n2.id_indicador = l2.id_indicador AND n2.codcentro = l2.codcentro AND n2.mes = l2.mes
        WHERE l2.id_indicador = l.id_indicador AND l2.codcentro = l.codcentro AND l2.letra = l.letra AND l2.mes <= l.mes
    ) ac;

    /* 2.4 Letras como columnas: #letra_piv se crea aquí y se le agregan las letras con SQL dinámico */
    CREATE TABLE #letra_piv (id_indicador INT, codcentro INT, mes INT, letra_mes_cero BIT);
    CREATE TABLE #num_den   (id_indicador INT, codcentro INT, mes INT, num FLOAT, den FLOAT, letra_mes_cero BIT);

    DECLARE @letras NVARCHAR(MAX), @add NVARCHAR(MAX), @sql NVARCHAR(MAX);
    SELECT @letras = STUFF((SELECT ',' + QUOTENAME(letra) FROM (SELECT DISTINCT letra FROM #letra) d ORDER BY letra FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, ''),
           @add    = STUFF((SELECT ',' + QUOTENAME(letra) + ' FLOAT' FROM (SELECT DISTINCT letra FROM #letra) d ORDER BY letra FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, '');

    IF @letras IS NOT NULL
    BEGIN
        SET @sql = N'ALTER TABLE #letra_piv ADD ' + @add + N';';
        EXEC sp_executesql @sql;
        SET @sql = N'INSERT INTO #letra_piv (id_indicador, codcentro, mes, letra_mes_cero, ' + @letras + N')
                     SELECT b.id_indicador, b.codcentro, b.mes, b.letra_mes_cero, ' + @letras + N'
                     FROM (SELECT id_indicador, codcentro, mes,
                                  CASE WHEN MIN(ISNULL(valor_mes, 0)) = 0 THEN 1 ELSE 0 END AS letra_mes_cero
                           FROM #letra GROUP BY id_indicador, codcentro, mes) b
                     JOIN (SELECT * FROM (SELECT id_indicador, codcentro, mes, letra, valor FROM #letra) s
                           PIVOT (SUM(valor) FOR letra IN (' + @letras + N')) x) p
                       ON p.id_indicador = b.id_indicador AND p.codcentro = b.codcentro AND p.mes = b.mes;';
        EXEC sp_executesql @sql;

        /* 2.5 Fórmula de cada indicador: cada letra -> ISNULL(p.[letra],0) (traducción carácter por carácter) */
        DECLARE @id INT, @num VARCHAR(200), @den VARCHAR(200), @e_num NVARCHAR(MAX), @e_den NVARCHAR(MAX), @k INT, @c CHAR(1), @div BIT;
        DECLARE cur CURSOR LOCAL FAST_FORWARD FOR
            SELECT i.id, i.expr_numerador, i.expr_denominador FROM dbo.tmi_indicador i
            WHERE i.activo = 1 AND EXISTS (SELECT 1 FROM #letra_piv p WHERE p.id_indicador = i.id);
        OPEN cur; FETCH NEXT FROM cur INTO @id, @num, @den;
        WHILE @@FETCH_STATUS = 0
        BEGIN
            /* letra que sigue a "/" -> NULLIF(...,0): una división entre cero da NULL (NA ese mes) en vez de detener el
               cálculo. Tras "/" con paréntesis queda la división simple (los bloques no generan paréntesis). */
            SELECT @e_num = N'', @e_den = N'', @k = 1, @div = 0;
            WHILE @k <= LEN(@num)
            BEGIN
                SET @c = SUBSTRING(@num, @k, 1);
                SET @e_num += CASE WHEN @c COLLATE Latin1_General_BIN LIKE '[A-Z]' AND @div = 1 THEN N'NULLIF(ISNULL(p.[' + @c + N'],0),0)'
                                   WHEN @c COLLATE Latin1_General_BIN LIKE '[A-Z]' THEN N'ISNULL(p.[' + @c + N'],0)' ELSE @c END;
                SET @div = CASE WHEN @c = '/' THEN 1 WHEN @c = ' ' THEN @div ELSE 0 END;
                SET @k += 1;
            END
            SELECT @k = 1, @div = 0;
            WHILE @k <= LEN(@den)
            BEGIN
                SET @c = SUBSTRING(@den, @k, 1);
                SET @e_den += CASE WHEN @c COLLATE Latin1_General_BIN LIKE '[A-Z]' AND @div = 1 THEN N'NULLIF(ISNULL(p.[' + @c + N'],0),0)'
                                   WHEN @c COLLATE Latin1_General_BIN LIKE '[A-Z]' THEN N'ISNULL(p.[' + @c + N'],0)' ELSE @c END;
                SET @div = CASE WHEN @c = '/' THEN 1 WHEN @c = ' ' THEN @div ELSE 0 END;
                SET @k += 1;
            END
            SET @sql = N'INSERT INTO #num_den SELECT p.id_indicador, p.codcentro, p.mes, ' + @e_num + N', ' + @e_den +
                       N', p.letra_mes_cero FROM #letra_piv p WHERE p.id_indicador = @id;';
            EXEC sp_executesql @sql, N'@id INT', @id = @id;
            FETCH NEXT FROM cur INTO @id, @num, @den;
        END
        CLOSE cur; DEALLOCATE cur;
    END

    /* 2.6 Estándar, reglas de ceros, puntaje -> tmi_resultado */
    BEGIN TRAN;
    DELETE dbo.tmi_resultado WHERE periodo_corte = @PERIODO;

    WITH malla AS (
        SELECT c.codcentro, c.red, c.tipo, c.nivel, c.categoria, c.motivo_centro, c.excluido, c.mes,
               i.id, i.factor, i.den_cero, i.num_cero_na, i.cero_si_letra_mes_0, i.sin_datos_anio, i.base_estandar, i.sentido,
               /* qué centros entran al indicador lo decide el estándar: el centro se une a la tabla de su tipo de estándar
                  (nivel, tipo o categoría); sin estándar (o 0) queda NA "Sin estándar" */
               i.tipo_tolerancia, i.tolerancia, ISNULL(i.tolerancia_menos, i.tolerancia) AS tolerancia_menos,
               i.decimales, i.cero_es_logro, i.mostrar_no_aplica
        FROM #centro_ind_mes c
        JOIN dbo.tmi_indicador i ON i.id = c.id_indicador
    ),
    est AS (
        SELECT g.*, d.num, d.den, ISNULL(d.letra_mes_cero, 1) AS letra_mes_cero,
               -- datos del indicador en el año (enero..corte): 0 = el centro no reportó ninguna de sus variables
               SUM(ABS(ISNULL(d.num, 0)) + ABS(ISNULL(d.den, 0))) OVER (PARTITION BY g.id, g.codcentro) AS datos_anio,
               NULLIF(CASE g.mes WHEN 1 THEN ce.m01 WHEN 2 THEN ce.m02 WHEN 3 THEN ce.m03 WHEN 4 THEN ce.m04 WHEN 5 THEN ce.m05 WHEN 6 THEN ce.m06
                                 WHEN 7 THEN ce.m07 WHEN 8 THEN ce.m08 WHEN 9 THEN ce.m09 WHEN 10 THEN ce.m10 WHEN 11 THEN ce.m11 WHEN 12 THEN ce.m12 END, 0) AS est_centro,
               ce.aplica AS aplica_centro, ce.acept AS acept_centro, eb.est AS est_base,
               NULLIF(ie.estandar, 0) AS est_combinado, ie.acept AS acept_combinado, ie.aceptmenos AS aceptmenos_combinado,
               NULLIF(CASE g.mes WHEN 1 THEN st.m01 WHEN 2 THEN st.m02 WHEN 3 THEN st.m03 WHEN 4 THEN st.m04 WHEN 5 THEN st.m05 WHEN 6 THEN st.m06
                                 WHEN 7 THEN st.m07 WHEN 8 THEN st.m08 WHEN 9 THEN st.m09 WHEN 10 THEN st.m10 WHEN 11 THEN st.m11 WHEN 12 THEN st.m12 END, 0) AS est_tipo,
               NULLIF(CASE g.mes WHEN 1 THEN sn.m01 WHEN 2 THEN sn.m02 WHEN 3 THEN sn.m03 WHEN 4 THEN sn.m04 WHEN 5 THEN sn.m05 WHEN 6 THEN sn.m06
                                 WHEN 7 THEN sn.m07 WHEN 8 THEN sn.m08 WHEN 9 THEN sn.m09 WHEN 10 THEN sn.m10 WHEN 11 THEN sn.m11 WHEN 12 THEN sn.m12 END, 0) AS est_nivel,
               NULLIF(CASE g.mes WHEN 1 THEN sc.m01 WHEN 2 THEN sc.m02 WHEN 3 THEN sc.m03 WHEN 4 THEN sc.m04 WHEN 5 THEN sc.m05 WHEN 6 THEN sc.m06
                                 WHEN 7 THEN sc.m07 WHEN 8 THEN sc.m08 WHEN 9 THEN sc.m09 WHEN 10 THEN sc.m10 WHEN 11 THEN sc.m11 WHEN 12 THEN sc.m12 END, 0) AS est_categoria
        FROM malla g
        LEFT JOIN #num_den d ON d.id_indicador = g.id AND d.codcentro = g.codcentro AND d.mes = g.mes
        OUTER APPLY (SELECT TOP 1 * FROM dbo.vw_tmi_centro_estandar x
                     WHERE x.id_estandar = g.id AND x.codcentro = g.codcentro AND x.anio = @anio) ce
        OUTER APPLY (SELECT TOP 1 x.estandar, x.acept, x.aceptmenos
                     FROM dbo.tmi_indicador_estandar x
                     WHERE x.id_indicador = g.id AND x.activo = 1
                       AND (@anio * 100 + g.mes) BETWEEN x.periodo_desde AND x.periodo_hasta
                       AND (x.nivel IS NULL OR x.nivel = g.nivel)
                       AND (x.categoria IS NULL OR x.categoria = g.categoria)
                       AND (x.tipo IS NULL OR x.tipo = g.tipo)
                       AND (x.nivel IS NOT NULL OR x.categoria IS NOT NULL OR x.tipo IS NOT NULL)
                     ORDER BY (CASE WHEN x.tipo IS NOT NULL THEN 4 ELSE 0 END
                             + CASE WHEN x.categoria IS NOT NULL THEN 2 ELSE 0 END
                             + CASE WHEN x.nivel IS NOT NULL THEN 1 ELSE 0 END) DESC,
                              (x.periodo_hasta - x.periodo_desde) ASC,
                              x.id DESC) ie
        /* Estándar según el tipo del indicador (tmi_tipo_estandar / tmi_estandar): de las claves que coinciden con el
           centro (nivel, tipo o categoría según la fuente), la de mayor prioridad que tenga valor en su tabla. */
        OUTER APPLY (SELECT TOP 1 v.est, k.fuente, k.clave
                     FROM dbo.tmi_estandar k
                     JOIN dbo.vw_tmi_std x ON x.id_estandar = g.id AND x.anio = @anio AND x.fuente = k.fuente AND x.clave = k.clave
                     /* CASE en lugar de CHOOSE: el servidor no lo reconoce (compatibilidad anterior a SQL Server 2012) */
                     CROSS APPLY (SELECT NULLIF(CASE g.mes WHEN 1 THEN x.m01 WHEN 2 THEN x.m02 WHEN 3 THEN x.m03
                                                       WHEN 4 THEN x.m04 WHEN 5 THEN x.m05 WHEN 6 THEN x.m06
                                                       WHEN 7 THEN x.m07 WHEN 8 THEN x.m08 WHEN 9 THEN x.m09
                                                       WHEN 10 THEN x.m10 WHEN 11 THEN x.m11 WHEN 12 THEN x.m12 END, 0) AS est) v
                     WHERE k.tipo_estandar = g.base_estandar AND k.activo = 1 AND v.est IS NOT NULL
                       AND k.clave = CASE k.fuente WHEN 'NIVEL' THEN g.nivel WHEN 'TIPO' THEN g.tipo ELSE g.categoria END
                     ORDER BY k.prioridad DESC, k.orden) eb
        OUTER APPLY (SELECT TOP 1 * FROM dbo.vw_tmi_std x WHERE x.id_estandar = g.id AND x.anio = @anio
                       AND x.fuente = 'TIPO' AND x.clave = g.tipo) st
        OUTER APPLY (SELECT TOP 1 * FROM dbo.vw_tmi_std x WHERE x.id_estandar = g.id AND x.anio = @anio
                       AND x.fuente = 'NIVEL' AND x.clave = g.nivel) sn
        OUTER APPLY (SELECT TOP 1 * FROM dbo.vw_tmi_std x WHERE x.id_estandar = g.id AND x.anio = @anio
                       AND x.fuente = 'CATEGORIA' AND x.clave = g.categoria) sc
    ),
    val AS (
        SELECT e.*,
               /* orden: estándar del centro > tipo de estándar del indicador (tablas maestras) > reglas del panel
                  (tmi_indicador_estandar) > combinaciones anteriores de base_estandar que no estén en el catálogo */
               CASE WHEN e.aplica_centro = 0 THEN NULL
                    ELSE COALESCE(e.est_centro, e.est_base, e.est_combinado,
                                  CASE e.base_estandar
                                      WHEN 'TIPO_NIVEL'           THEN COALESCE(e.est_tipo, e.est_nivel)
                                      WHEN 'TIPO_CATEGORIA'       THEN COALESCE(e.est_tipo, e.est_categoria)
                                      WHEN 'NIVEL_CATEGORIA'      THEN COALESCE(e.est_nivel, e.est_categoria)
                                      WHEN 'TIPO_NIVEL_CATEGORIA' THEN COALESCE(e.est_tipo, e.est_categoria, e.est_nivel)
                                  END) END                                       AS estandar,
               CASE WHEN ISNULL(e.den, 0) = 0
                         THEN CASE WHEN e.den_cero = 'NA' THEN NULL ELSE 0 END
                    WHEN e.num_cero_na = 1 AND ISNULL(e.num, 0) = 0 THEN NULL
                    WHEN e.cero_si_letra_mes_0 = 1 AND e.letra_mes_cero = 1 THEN 0
                    ELSE e.num / e.den * e.factor END                            AS valor
        FROM est e
    ),
    lim AS (
        SELECT v.*,
               v.estandar AS verde,
               /* % Acept: límite para el puntaje 3 (en banda, el de arriba) = estándar ± el porcentaje del indicador.
                  El % Acept propio del centro (tmi_centro_estandar.acept) gana. */
               COALESCE(v.acept_centro,
                        CASE WHEN v.est_centro IS NULL AND v.est_base IS NULL THEN v.acept_combinado END,
                        CASE WHEN v.sentido IN ('MENOR', 'BANDA')
                             THEN CASE v.tipo_tolerancia WHEN 'ABS' THEN v.estandar + v.tolerancia ELSE v.estandar * (1 + v.tolerancia) END
                             ELSE CASE v.tipo_tolerancia WHEN 'ABS' THEN v.estandar - v.tolerancia ELSE v.estandar * (1 - v.tolerancia) END
                        END) AS acept,
               /* % Aceptmenos: solo banda, el límite de abajo */
               CASE WHEN v.sentido = 'BANDA'
                    THEN COALESCE(CASE WHEN v.est_centro IS NULL AND v.est_base IS NULL THEN v.aceptmenos_combinado END,
                                  CASE v.tipo_tolerancia WHEN 'ABS' THEN v.estandar - v.tolerancia_menos
                                                         ELSE v.estandar * (1 - v.tolerancia_menos) END) END AS aceptmenos,
               ROUND(v.valor, ISNULL(v.decimales, 15)) AS valor_eval,
               CASE WHEN v.motivo_centro IS NOT NULL                         THEN v.motivo_centro
                    WHEN v.excluido = 1                                      THEN 'EXCLUIDO'
                    WHEN v.estandar IS NULL                                  THEN 'SIN_ESTANDAR'
                    WHEN v.datos_anio = 0 AND v.sin_datos_anio <> 'MOSTRAR'  THEN 'SIN_DATOS_ANIO'
                    WHEN v.valor IS NULL                                     THEN 'SIN_DATO' END AS motivo_na
        FROM val v
    )
    INSERT INTO dbo.tmi_resultado (periodo_corte, id_indicador, codcentro, mes, numerador, denominador, valor,
                                   estandar, verde, acept, aceptmenos, puntaje, motivo_na, visible)
    SELECT @PERIODO, l.id, l.codcentro, l.mes, l.num, l.den, l.valor, l.estandar, l.verde, l.acept, l.aceptmenos,
           CASE WHEN l.motivo_na IS NOT NULL                   THEN 'NA'
                WHEN l.valor_eval = 0 AND l.cero_es_logro = 0  THEN '0'
                WHEN l.sentido = 'BANDA' THEN
                     CASE WHEN l.valor_eval BETWEEN (l.verde + l.aceptmenos) / 2 AND (l.verde + l.acept) / 2 THEN '5'
                          WHEN l.valor_eval BETWEEN l.aceptmenos AND l.acept                                 THEN '3'
                          ELSE '1' END
                WHEN l.sentido = 'MAYOR' THEN CASE WHEN l.valor_eval >= l.verde THEN '5' WHEN l.valor_eval >= l.acept THEN '3' ELSE '1' END
                ELSE                          CASE WHEN l.valor_eval <= l.verde THEN '5' WHEN l.valor_eval <= l.acept THEN '3' ELSE '1' END
           END,
           l.motivo_na,
           -- visible = 0: el centro no se lista en la hoja del indicador (por defecto los NA sí se listan)
           CASE WHEN l.motivo_na = 'SIN_DATOS_ANIO' AND l.sin_datos_anio = 'OCULTAR'                  THEN 0
                WHEN l.motivo_na IN ('SIN_ESTANDAR', 'FUERA_DE_AMBITO') AND l.mostrar_no_aplica = 0  THEN 0
                ELSE 1 END
    FROM lim l;

    /* 2.7 Resultado final por indicador (filas del Excel) -> tmi_resultado_indicador */
    DELETE dbo.tmi_resultado_indicador WHERE periodo = @PERIODO;
    INSERT INTO dbo.tmi_resultado_indicador (periodo, anio, id_indicador, orden, orden_red, red, codcentro, centro, nivel, tipo,
                                             categoria, estandar, acept, aceptmenos, total, puntaje, motivo_na, visible,
                                             periodo_01, periodo_02, periodo_03, periodo_04, periodo_05, periodo_06, periodo_07, periodo_08, periodo_09, periodo_10, periodo_11, periodo_12)
    SELECT @PERIODO, @anio, r.id_indicador, MIN(c.id_centro), MIN(c.orden), MAX(c.red), r.codcentro, MAX(c.centro), MAX(c.nivel), MAX(c.tipo),
           MAX(c.categoria),
           MAX(CASE WHEN r.mes = @mes THEN r.estandar END),
           MAX(CASE WHEN r.mes = @mes THEN r.acept END),
           MAX(CASE WHEN r.mes = @mes THEN r.aceptmenos END),
           MAX(CASE WHEN r.mes = @mes THEN CASE WHEN r.puntaje = 'NA' THEN r.valor ELSE ISNULL(r.valor, 0) END END),
           MAX(CASE WHEN r.mes = @mes THEN r.puntaje END),
           MAX(CASE WHEN r.mes = @mes THEN r.motivo_na END),
           CAST(MAX(CASE WHEN r.mes = @mes THEN CAST(r.visible AS INT) END) AS BIT),
           CASE WHEN 1 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 1 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END,
           CASE WHEN 2 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 2 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END,
           CASE WHEN 3 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 3 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END,
           CASE WHEN 4 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 4 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END,
           CASE WHEN 5 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 5 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END,
           CASE WHEN 6 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 6 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END,
           CASE WHEN 7 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 7 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END,
           CASE WHEN 8 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 8 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END,
           CASE WHEN 9 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 9 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END,
           CASE WHEN 10 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 10 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END,
           CASE WHEN 11 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 11 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END,
           CASE WHEN 12 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 12 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END
    FROM dbo.tmi_resultado r
    JOIN #centro c ON c.codcentro = r.codcentro
    WHERE r.periodo_corte = @PERIODO
    GROUP BY r.id_indicador, r.codcentro
    HAVING MAX(CASE WHEN r.mes = @mes THEN 1 END) = 1;
    COMMIT;
END
GO
