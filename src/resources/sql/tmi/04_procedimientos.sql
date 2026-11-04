/* =====================================================================================================
   TMI DINAMICO - 04 PROCEDIMIENTOS
     EXEC dbo.usp_tmi_validar_config;          -- 0 filas = configuración correcta
     EXEC dbo.usp_tmi_generar_pivot 202608;    -- valores de las variables -> tmi_variable_pivot (consulta, no lo usa el cálculo)
     EXEC dbo.usp_tmi_calcular      202608;    -- fórmula de cada indicador sobre TOTALIZADO3, estándar, puntaje
                                               -- -> tmi_resultado y tmi_resultado_indicador
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
    /* Conjuntos de cada variable, incluidos los de sus componentes (variables compuestas, hasta 10 niveles) */
    ;WITH arbol AS (
        SELECT v.id AS raiz, v.id AS id_var, 0 AS nivel, CAST('/' + CAST(v.id AS VARCHAR(10)) + '/' AS VARCHAR(400)) AS camino
        FROM dbo.tmi_variable v
        UNION ALL
        SELECT a.raiz, c.id_variable_componente, a.nivel + 1, CAST(a.camino + CAST(c.id_variable_componente AS VARCHAR(10)) + '/' AS VARCHAR(400))
        FROM arbol a
        JOIN dbo.tmi_variable_componente c ON c.id_variable = a.id_var AND c.activo = 1
        WHERE a.nivel < 10 AND a.camino NOT LIKE '%/' + CAST(c.id_variable_componente AS VARCHAR(10)) + '/%'
    )
    SELECT raiz, id_var, nivel INTO #arbol FROM arbol OPTION (MAXRECURSION 20);
    -- ciclo: una variable que se contiene a sí misma a través de sus componentes
    SELECT DISTINCT c.id_variable AS raiz
    INTO   #ciclo
    FROM   #arbol a JOIN dbo.tmi_variable_componente c ON c.id_variable = a.id_var AND c.activo = 1
    WHERE  c.id_variable_componente = a.raiz;
    SELECT a.raiz, a.id_var, l.id, l.tipgrupo, l.actividad, l.servicio, l.periodo_desde, l.periodo_hasta
    INTO   #conjuntos
    FROM   #arbol a JOIN dbo.tmi_variable_logica l ON l.id_variable = a.id_var AND l.activo = 1;

    SELECT i.id AS id_indicador, i.codigo AS elemento, 'Indicador activo sin fórmula (o la fórmula no se pudo analizar)' AS problema
    FROM dbo.tmi_indicador i
    WHERE i.activo = 1
      AND (NULLIF(LTRIM(i.formula), '') IS NULL OR i.formula_sql IS NULL
        OR NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador_termino t WHERE t.id_indicador = i.id))
    UNION ALL
    SELECT i.id, i.codigo, 'Falta nombre de hoja, tipo de cálculo, sentido o base de estándar'
    FROM dbo.tmi_indicador i
    WHERE i.activo = 1
      AND (i.nombre_hoja IS NULL OR i.tipo_calculo IS NULL OR i.sentido IS NULL OR i.base_estandar IS NULL)
    UNION ALL
    SELECT DISTINCT i.id, i.codigo, 'Término ' + t.texto + ': tipgrupo ' + CAST(t.tipgrupo AS VARCHAR(10)) + ' no existe en DIM_GRUPO'
    FROM dbo.tmi_indicador i JOIN dbo.tmi_indicador_termino t ON t.id_indicador = i.id
    WHERE i.activo = 1 AND NOT EXISTS (SELECT 1 FROM #dim_grupo g WHERE g.tipgrupo = t.tipgrupo)
    UNION ALL
    SELECT DISTINCT i.id, i.codigo, 'Término ' + t.texto + ': actividad ' + CAST(t.actividad AS VARCHAR(10)) + ' no existe en DIM_ACTIVIDAD'
    FROM dbo.tmi_indicador i JOIN dbo.tmi_indicador_termino t ON t.id_indicador = i.id
    WHERE i.activo = 1 AND NOT EXISTS (SELECT 1 FROM #dim_actividad a WHERE a.actividad = t.actividad)
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
    SELECT NULL, v.nombre, 'La variable se contiene a sí misma a través de sus componentes (ciclo)'
    FROM #ciclo c JOIN dbo.tmi_variable v ON v.id = c.raiz
    UNION ALL
    /* Los conjuntos de una misma variable son un OR: si se pisan, el registro cuenta una vez. Pero dos variables que suma
       una compuesta se suman (A + B): el mismo grupo/actividad en las dos se contaría dos veces */
    SELECT DISTINCT NULL, v.nombre, 'Grupo/actividad repetido en dos variables que suma (tipgrupo ' + CAST(l.tipgrupo AS VARCHAR(10))
                           + ', actividad ' + CAST(l.actividad AS VARCHAR(10)) + '): se contaría dos veces'
    FROM #conjuntos l
    JOIN dbo.tmi_variable v ON v.id = l.raiz
    JOIN #conjuntos l2 ON l2.raiz = l.raiz AND l2.id > l.id AND l2.id_var <> l.id_var
     AND l2.tipgrupo = l.tipgrupo AND l2.actividad = l.actividad
     AND (l2.servicio IS NULL OR l.servicio IS NULL OR l2.servicio = l.servicio)
     AND l2.periodo_desde <= l.periodo_hasta AND l.periodo_desde <= l2.periodo_hasta
    UNION ALL
    -- la misma fila de lógica alcanzada por dos caminos (dos componentes que comparten un componente)
    SELECT DISTINCT NULL, v.nombre, 'Un conjunto entra dos veces por sus componentes: se contaría dos veces'
    FROM (SELECT raiz, id FROM #conjuntos GROUP BY raiz, id HAVING COUNT(*) > 1) d
    JOIN dbo.tmi_variable v ON v.id = d.raiz
    UNION ALL
    -- una compuesta no puede sumar una variable SUMA con una MEDIANA (son unidades distintas: atenciones y recursos)
    SELECT NULL, v.nombre, 'La variable suma variables con distinto cálculo (SUMA y MEDIANA)'
    FROM (SELECT c.raiz FROM (SELECT DISTINCT raiz, id_var FROM #conjuntos) c JOIN dbo.tmi_variable d ON d.id = c.id_var
          GROUP BY c.raiz HAVING COUNT(DISTINCT d.agregacion) > 1) x
    JOIN dbo.tmi_variable v ON v.id = x.raiz
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
      El cálculo es de la variable (tmi_variable.agregacion), como en Generar_pivot.sql:
        SUMA    : suma de cantidad de los registros que cumplen cualquiera de sus conjuntos (WHERE c1 OR c2 ...)
        MEDIANA : con esos registros, mediana de cada servicio en el mes, redondeada, y suma de servicios (como CONSO4 / CONSO5)
      Una variable compuesta suma el valor de sus componentes (tmi_variable_componente), cada uno con su propio cálculo.
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

    /* Conjuntos de cada variable: sus filas de lógica y las de sus componentes (variables compuestas, recursivo).
       dueno = la variable a la que pertenece la fila (la misma o un componente): de ella salen el cálculo y el total anual. */
    ;WITH arbol AS (
        SELECT V.id_variable AS raiz, V.id_variable AS id_var, 0 AS nivel,
               CAST('/' + CAST(V.id_variable AS VARCHAR(10)) + '/' AS VARCHAR(400)) AS camino
        FROM #vars V
        UNION ALL
        SELECT a.raiz, c.id_variable_componente, a.nivel + 1,
               CAST(a.camino + CAST(c.id_variable_componente AS VARCHAR(10)) + '/' AS VARCHAR(400))
        FROM arbol a
        JOIN dbo.tmi_variable_componente c ON c.id_variable = a.id_var AND c.activo = 1
        WHERE a.nivel < 10 AND a.camino NOT LIKE '%/' + CAST(c.id_variable_componente AS VARCHAR(10)) + '/%'
    )
    SELECT DISTINCT L.id AS id_logica, a.raiz AS id_variable, a.id_var AS dueno, D.agregacion, D.total_anual,
           L.tipgrupo, L.actividad, L.servicio, L.condicion_hoja, L.periodo_desde, L.periodo_hasta
    INTO   #logica
    FROM   arbol a
    JOIN   dbo.tmi_variable_logica L ON L.id_variable = a.id_var AND L.activo = 1
    JOIN   dbo.tmi_variable D ON D.id = a.id_var
    OPTION (MAXRECURSION 20);

    /* TOTALIZADO3 y DIM_HOJA pueden estar en otro servidor (servidor vinculado, nombre de 4 partes en el .env).
       Una sola lectura de TOTALIZADO3: se copian solo las filas del año y de los grupos que usan las variables, con un
       filtro sobre una sola tabla y valores literales, para que se resuelva en el servidor remoto y viaje solo lo necesario.
       El cruce con los conjuntos (#logica) se hace después, contra la copia local. */
    DECLARE @grupos NVARCHAR(MAX), @sql NVARCHAR(MAX);
    SELECT @grupos = STUFF((
        SELECT N',' + CAST(g.tipgrupo AS NVARCHAR(20))
        FROM (SELECT DISTINCT L.tipgrupo FROM #logica L) g
        ORDER BY g.tipgrupo
        FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, N'');

    SELECT TOP 0 T.periodo, T.codcentro_ses, T.servicio, T.tipgrupo, T.actividad, T.tipohoja, T.cantidad
    INTO   #t3
    FROM   {{TOTALIZADO3}} T;
    ALTER TABLE #t3 ADD fila INT IDENTITY(1,1);   -- identifica cada registro para contarlo una sola vez (OR)
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

    /* Varios conjuntos de una variable son un OR (WHERE c1 OR c2 de Generar_pivot.sql): un registro que cumple dos
       conjuntos de la misma variable cuenta una sola vez (DISTINCT por fila y dueño). */
    SELECT DISTINCT T.fila, T.periodo % 100 AS mes, T.codcentro_ses AS codcentro, T.servicio,
           L.id_variable, L.dueno, L.agregacion, L.total_anual, CAST(T.cantidad AS FLOAT) AS cantidad
    INTO   #base
    FROM   #t3 T
    JOIN   #logica L
           ON  L.tipgrupo = T.tipgrupo AND L.actividad = T.actividad
           AND (L.servicio IS NULL OR L.servicio = T.servicio)
           AND T.periodo BETWEEN L.periodo_desde AND L.periodo_hasta
    LEFT JOIN #dim_hoja H ON H.tipohoja = T.tipohoja
    WHERE  T.periodo BETWEEN @anio * 100 + 1 AND @PERIODO
      AND  (L.condicion_hoja IS NULL OR UPPER(H.condicion) = UPPER(L.condicion_hoja));

    -- Valor de cada mes por dueño, con el cálculo del dueño
    SELECT mes, codcentro, id_variable, dueno, SUM(cantidad) AS valor
    INTO   #mes
    FROM   #base WHERE agregacion = 'SUMA'
    GROUP BY mes, codcentro, id_variable, dueno
    UNION ALL
    SELECT mes, codcentro, id_variable, dueno, SUM(ROUND(med, 0))
    FROM (SELECT mes, codcentro, id_variable, dueno, servicio, AVG(cantidad) AS med
          FROM (SELECT mes, codcentro, id_variable, dueno, servicio, cantidad,
                       ROW_NUMBER() OVER (PARTITION BY mes, codcentro, id_variable, dueno, servicio ORDER BY cantidad) AS rn,
                       COUNT(*) OVER (PARTITION BY mes, codcentro, id_variable, dueno, servicio) AS cnt
                FROM #base WHERE agregacion = 'MEDIANA') r
          WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
          GROUP BY mes, codcentro, id_variable, dueno, servicio) m
    GROUP BY mes, codcentro, id_variable, dueno;

    -- Total anual MEDIANA_PERIODO: mediana de todo el periodo por servicio y suma (como #TEMPO2 de los CONSO)
    SELECT codcentro, id_variable, dueno, SUM(ROUND(med, 0)) AS total
    INTO   #total_mediana
    FROM (SELECT codcentro, id_variable, dueno, servicio, AVG(cantidad) AS med
          FROM (SELECT codcentro, id_variable, dueno, servicio, cantidad,
                       ROW_NUMBER() OVER (PARTITION BY codcentro, id_variable, dueno, servicio ORDER BY cantidad) AS rn,
                       COUNT(*) OVER (PARTITION BY codcentro, id_variable, dueno, servicio) AS cnt
                FROM #base WHERE agregacion = 'MEDIANA' AND total_anual = 'MEDIANA_PERIODO') r
          WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
          GROUP BY codcentro, id_variable, dueno, servicio) m
    GROUP BY codcentro, id_variable, dueno;

    -- Total anual de la variable: suma del total de cada dueño (suma de sus meses, o su mediana del periodo)
    SELECT d.codcentro, d.id_variable, SUM(COALESCE(t.total, d.suma)) AS total
    INTO   #total
    FROM  (SELECT codcentro, id_variable, dueno, SUM(valor) AS suma FROM #mes GROUP BY codcentro, id_variable, dueno) d
    LEFT JOIN #total_mediana t ON t.codcentro = d.codcentro AND t.id_variable = d.id_variable AND t.dueno = d.dueno
    GROUP BY d.codcentro, d.id_variable;

    BEGIN TRAN;
    DELETE dbo.tmi_variable_pivot WHERE anio = @anio AND id_variable IN (SELECT id_variable FROM #vars);

    INSERT INTO dbo.tmi_variable_pivot (anio, codcentro, id_variable, total, m01, m02, m03, m04, m05, m06, m07, m08, m09, m10, m11, m12)
    SELECT @anio, m.codcentro, m.id_variable, MAX(t.total),
           SUM(CASE WHEN m.mes =  1 THEN m.valor END), SUM(CASE WHEN m.mes =  2 THEN m.valor END),
           SUM(CASE WHEN m.mes =  3 THEN m.valor END), SUM(CASE WHEN m.mes =  4 THEN m.valor END),
           SUM(CASE WHEN m.mes =  5 THEN m.valor END), SUM(CASE WHEN m.mes =  6 THEN m.valor END),
           SUM(CASE WHEN m.mes =  7 THEN m.valor END), SUM(CASE WHEN m.mes =  8 THEN m.valor END),
           SUM(CASE WHEN m.mes =  9 THEN m.valor END), SUM(CASE WHEN m.mes = 10 THEN m.valor END),
           SUM(CASE WHEN m.mes = 11 THEN m.valor END), SUM(CASE WHEN m.mes = 12 THEN m.valor END)
    FROM   #mes m
    JOIN   #total t ON t.codcentro = m.codcentro AND t.id_variable = m.id_variable
    GROUP BY m.codcentro, m.id_variable;
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

    /* 2.1 Valor de cada término de la fórmula (tmi_indicador_termino: T1, T2...) por centro y mes, directo de TOTALIZADO3.
           Término [g;a#s]: suma de cantidad del grupo, actividad y servicios. MEDIANA([..]): mediana de cada servicio en
           el mes, redondeada, y suma de servicios (recursos, como CONSO4 / CONSO5 de Generar_pivot.sql). */
    SELECT t.id_indicador, t.codigo, t.tipgrupo, t.actividad, t.servicio, t.mediana
    INTO   #termino
    FROM   dbo.tmi_indicador_termino t
    JOIN   dbo.tmi_indicador i ON i.id = t.id_indicador AND i.activo = 1 AND i.formula_sql IS NOT NULL;

    /* TOTALIZADO3 puede estar en otro servidor: una sola lectura con filtro literal (año y grupos), como el pivot */
    DECLARE @grupos NVARCHAR(MAX), @sql NVARCHAR(MAX);
    SELECT @grupos = STUFF((SELECT N',' + CAST(g.tipgrupo AS NVARCHAR(20))
                            FROM (SELECT DISTINCT tipgrupo FROM #termino) g ORDER BY g.tipgrupo
                            FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, N'');
    SELECT TOP 0 T.periodo, T.codcentro_ses, T.servicio, T.tipgrupo, T.actividad, T.cantidad
    INTO   #t3
    FROM   {{TOTALIZADO3}} T;
    IF @grupos IS NOT NULL
    BEGIN
        SET @sql = N'INSERT INTO #t3 (periodo, codcentro_ses, servicio, tipgrupo, actividad, cantidad)
                     SELECT T.periodo, T.codcentro_ses, T.servicio, T.tipgrupo, T.actividad, T.cantidad
                     FROM {{TOTALIZADO3}} T
                     WHERE T.periodo BETWEEN ' + CAST(@anio * 100 + 1 AS NVARCHAR(10)) + N' AND ' + CAST(@PERIODO AS NVARCHAR(10)) + N'
                       AND T.tipgrupo IN (' + @grupos + N');';
        EXEC sp_executesql @sql;
    END

    -- un registro entra una vez por término: los servicios de un término son filas distintas
    SELECT k.id_indicador, k.codigo, k.mediana, T.codcentro_ses AS codcentro, T.periodo % 100 AS mes, T.servicio,
           CAST(T.cantidad AS FLOAT) AS cantidad
    INTO   #base
    FROM   #t3 T
    JOIN   #termino k ON k.tipgrupo = T.tipgrupo AND k.actividad = T.actividad
                     AND (k.servicio IS NULL OR k.servicio = T.servicio);

    SELECT id_indicador, codcentro, mes, CAST(codigo AS VARCHAR(5)) AS letra, SUM(cantidad) AS valor_mes
    INTO   #letra_mes
    FROM   #base WHERE mediana = 0
    GROUP BY id_indicador, codcentro, mes, codigo;

    INSERT INTO #letra_mes (id_indicador, codcentro, mes, letra, valor_mes)
    SELECT id_indicador, codcentro, mes, codigo, SUM(ROUND(med, 0))
    FROM  (SELECT id_indicador, codigo, codcentro, mes, servicio, AVG(cantidad) AS med
           FROM  (SELECT id_indicador, codigo, codcentro, mes, servicio, cantidad,
                         ROW_NUMBER() OVER (PARTITION BY id_indicador, codigo, codcentro, mes, servicio ORDER BY cantidad) AS rn,
                         COUNT(*) OVER (PARTITION BY id_indicador, codigo, codcentro, mes, servicio) AS cnt
                  FROM #base WHERE mediana = 1) r
           WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
           GROUP BY id_indicador, codigo, codcentro, mes, servicio) m
    GROUP BY id_indicador, codcentro, mes, codigo;
    CREATE CLUSTERED INDEX ix_letra_mes ON #letra_mes (id_indicador, codcentro, letra, mes);

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

    /* Las vistas de exclusión y estándares (UNION y cruces con vw_tmi_centro_base) se consultan por cada centro,
       indicador y mes: se copian una sola vez, solo del año, a tablas temporales con índice */
    SELECT * INTO #excl FROM dbo.vw_tmi_exclusion WHERE anio = @anio;
    CREATE CLUSTERED INDEX ix_excl ON #excl (codcentro, id_estandar);
    SELECT * INTO #std FROM dbo.vw_tmi_std WHERE anio = @anio;
    CREATE CLUSTERED INDEX ix_std ON #std (id_estandar, fuente);
    SELECT * INTO #cest FROM dbo.vw_tmi_centro_estandar WHERE anio = @anio;
    CREATE CLUSTERED INDEX ix_cest ON #cest (id_estandar, codcentro);

    SELECT i.id AS id_indicador, c.codcentro, c.red, c.orden, c.orden_tipo, c.id_centro, c.categoria, c.nivel, c.tipo, m.mes,
           CASE WHEN (CASE m.mes WHEN 1 THEN c.f01 WHEN 2 THEN c.f02 WHEN 3 THEN c.f03 WHEN 4 THEN c.f04 WHEN 5 THEN c.f05 WHEN 6 THEN c.f06
                                 WHEN 7 THEN c.f07 WHEN 8 THEN c.f08 WHEN 9 THEN c.f09 WHEN 10 THEN c.f10 WHEN 11 THEN c.f11 WHEN 12 THEN c.f12 END) = 0
                THEN 'NO_VIGENTE_MES'
                /* Centros del indicador (tmi_indicador_ambito, vigente en el mes): con filas incluir = 1, solo los centros
                   que coinciden con alguna; una fila incluir = 0 que coincide lo deja fuera. Sin filas = todos los centros. */
                WHEN (amb.lista_blanca = 1 AND amb.incluido = 0) OR amb.excluido = 1
                THEN 'FUERA_DE_AMBITO' END AS motivo_centro,
           ISNULL(x.excluido, 0) AS excluido,
           ISNULL(x.resultado, 'NA') AS excl_resultado
    INTO   #centro_ind_mes
    FROM   #centro c
    CROSS JOIN dbo.tmi_indicador i
    CROSS JOIN (SELECT v AS mes FROM (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) z(v) WHERE v <= @mes) m
    /* resultado del mes excluido ('NA' o '0'): manda la exclusión del indicador sobre la de "todos los indicadores" */
    OUTER APPLY (SELECT TOP 1 q.v AS excluido, q.resultado
                 FROM (SELECT CAST(CASE m.mes WHEN 1 THEN e.x01 WHEN 2 THEN e.x02 WHEN 3 THEN e.x03 WHEN 4 THEN e.x04 WHEN 5 THEN e.x05 WHEN 6 THEN e.x06
                                              WHEN 7 THEN e.x07 WHEN 8 THEN e.x08 WHEN 9 THEN e.x09 WHEN 10 THEN e.x10 WHEN 11 THEN e.x11 WHEN 12 THEN e.x12 END AS INT) AS v,
                              e.resultado, e.id_estandar
                       FROM #excl e
                       WHERE e.codcentro = c.codcentro
                         AND (e.id_estandar = i.id OR e.id_estandar IS NULL)) q
                 WHERE q.v = 1
                 ORDER BY CASE WHEN q.id_estandar IS NULL THEN 1 ELSE 0 END,
                          CASE WHEN q.resultado = 'NA' THEN 0 ELSE 1 END) x
    OUTER APPLY (SELECT MAX(CASE WHEN a.incluir = 1 THEN 1 ELSE 0 END)                AS lista_blanca,
                        MAX(CASE WHEN a.incluir = 1 AND k.coincide = 1 THEN 1 ELSE 0 END) AS incluido,
                        MAX(CASE WHEN a.incluir = 0 AND k.coincide = 1 THEN 1 ELSE 0 END) AS excluido
                 FROM dbo.tmi_indicador_ambito a
                 CROSS APPLY (SELECT CASE WHEN (a.red IS NULL OR a.red = c.red) AND (a.nivel IS NULL OR a.nivel = c.nivel)
                                           AND (a.categoria IS NULL OR a.categoria = c.categoria)
                                           AND (a.tipo IS NULL OR a.tipo = c.tipo)
                                           AND (a.codcentro IS NULL OR a.codcentro = c.codcentro) THEN 1 ELSE 0 END AS coincide) k
                 WHERE a.id_indicador = i.id
                   AND @anio * 100 + m.mes BETWEEN a.periodo_desde AND a.periodo_hasta) amb
    WHERE  i.activo = 1;
    CREATE CLUSTERED INDEX ix_centro_ind_mes ON #centro_ind_mes (id_indicador, codcentro, mes);

    /* 2.3 MENSUAL = valor del mes ; ACUMULADO = enero..mes, sin los meses excluidos / no vigentes
           Cada término del centro tiene todos los meses hasta el corte (un mes sin registros queda en NULL). */
    SELECT l.id_indicador, l.codcentro, l.mes, l.letra, lm.valor_mes,
           CASE WHEN i.tipo_calculo = 'ACUMULADO' THEN ISNULL(ac.valor_acum, 0) ELSE lm.valor_mes END AS valor
    INTO   #letra
    FROM  (SELECT g.id_indicador, g.codcentro, g.letra, m.mes
           FROM (SELECT DISTINCT id_indicador, codcentro, letra FROM #letra_mes) g
           CROSS JOIN (SELECT v AS mes FROM (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) z(v) WHERE v <= @mes) m) l
    LEFT JOIN #letra_mes lm ON lm.id_indicador = l.id_indicador AND lm.codcentro = l.codcentro AND lm.letra = l.letra AND lm.mes = l.mes
    JOIN   dbo.tmi_indicador i ON i.id = l.id_indicador
    OUTER APPLY (
        SELECT SUM(CASE WHEN n2.excluido = 1 OR n2.motivo_centro IS NOT NULL THEN 0 ELSE ISNULL(l2.valor_mes, 0) END) AS valor_acum
        FROM #letra_mes l2
        LEFT JOIN #centro_ind_mes n2 ON n2.id_indicador = l2.id_indicador AND n2.codcentro = l2.codcentro AND n2.mes = l2.mes
        WHERE l2.id_indicador = l.id_indicador AND l2.codcentro = l.codcentro AND l2.letra = l.letra AND l2.mes <= l.mes
    ) ac;

    /* 2.4 Términos como columnas (T1, T2...): #letra_piv se crea aquí y se le agregan con SQL dinámico. Se crean todas
           las columnas de los términos, aunque un término no tenga datos, para que la fórmula siempre las encuentre.
           datos = suma de los valores del mes (0 = el centro no reportó ninguno de los términos). */
    CREATE TABLE #letra_piv (id_indicador INT, codcentro INT, mes INT, datos FLOAT);
    CREATE TABLE #num_den   (id_indicador INT, codcentro INT, mes INT, valor FLOAT, datos FLOAT);

    DECLARE @letras NVARCHAR(MAX), @add NVARCHAR(MAX);
    SELECT @letras = STUFF((SELECT ',' + QUOTENAME(codigo) FROM (SELECT DISTINCT codigo FROM #termino) d ORDER BY codigo FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, ''),
           @add    = STUFF((SELECT ',' + QUOTENAME(codigo) + ' FLOAT' FROM (SELECT DISTINCT codigo FROM #termino) d ORDER BY codigo FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, '');

    IF @letras IS NOT NULL
    BEGIN
        SET @sql = N'ALTER TABLE #letra_piv ADD ' + @add + N';';
        EXEC sp_executesql @sql;
        SET @sql = N'INSERT INTO #letra_piv (id_indicador, codcentro, mes, datos, ' + @letras + N')
                     SELECT b.id_indicador, b.codcentro, b.mes, b.datos, ' + @letras + N'
                     FROM (SELECT l.id_indicador, l.codcentro, l.mes, SUM(ABS(ISNULL(l.valor_mes, 0))) AS datos
                           FROM #letra l GROUP BY l.id_indicador, l.codcentro, l.mes) b
                     JOIN (SELECT * FROM (SELECT id_indicador, codcentro, mes, letra, valor FROM #letra) s
                           PIVOT (SUM(valor) FOR letra IN (' + @letras + N')) x) p
                       ON p.id_indicador = b.id_indicador AND p.codcentro = b.codcentro AND p.mes = b.mes;';
        EXEC sp_executesql @sql;

        /* 2.5 Fórmula de cada indicador (formula_sql, generada por el backend desde tmi_indicador.formula): solo
               ISNULL(p.[Tn],0), NULLIF(..,0) en los divisores, números y + - * / ( ). Una división entre 0 da NULL (NA
               ese mes). Por seguridad se comprueba que no tenga otra cosa antes de ejecutarla. */
        DECLARE @id INT, @f NVARCHAR(MAX), @resto NVARCHAR(MAX);
        DECLARE cur CURSOR LOCAL FAST_FORWARD FOR
            SELECT i.id, i.formula_sql FROM dbo.tmi_indicador i
            WHERE i.activo = 1 AND i.formula_sql IS NOT NULL AND EXISTS (SELECT 1 FROM #letra_piv p WHERE p.id_indicador = i.id);
        OPEN cur; FETCH NEXT FROM cur INTO @id, @f;
        WHILE @@FETCH_STATUS = 0
        BEGIN
            SET @resto = REPLACE(REPLACE(REPLACE(REPLACE(@f, N'ISNULL(', N''), N'NULLIF(', N''), N'p.[T', N''), N']', N'');
            IF PATINDEX(N'%[^-0-9 .,()+*/]%', @resto COLLATE Latin1_General_BIN) = 0
               AND CHARINDEX(N'--', @resto) = 0 AND CHARINDEX(N'/*', @resto) = 0
            BEGIN
                SET @sql = N'INSERT INTO #num_den SELECT p.id_indicador, p.codcentro, p.mes, ' + @f +
                           N', p.datos FROM #letra_piv p WHERE p.id_indicador = @id;';
                EXEC sp_executesql @sql, N'@id INT', @id = @id;
            END
            FETCH NEXT FROM cur INTO @id, @f;
        END
        CLOSE cur; DEALLOCATE cur;
    END
    CREATE CLUSTERED INDEX ix_num_den ON #num_den (id_indicador, codcentro, mes);

    /* 2.6 Estándar y puntaje -> tmi_resultado (el valor es el de la fórmula, sin reglas de ceros) */
    BEGIN TRAN;
    DELETE dbo.tmi_resultado WHERE periodo_corte = @PERIODO;

    WITH malla AS (
        SELECT c.codcentro, c.red, c.tipo, c.nivel, c.categoria, c.motivo_centro, c.excluido, c.excl_resultado, c.mes,
               i.id, i.sin_datos_anio, i.base_estandar, i.sentido,
               /* qué centros entran al indicador lo decide el estándar: el centro se une a la tabla de su tipo de estándar
                  (nivel, tipo o categoría); sin estándar (o 0) queda NA "Sin estándar" */
               COALESCE(tol.tipo_tolerancia, fijo.tipo_tolerancia, i.tipo_tolerancia) AS tipo_tolerancia,
               COALESCE(tol.tolerancia, fijo.tolerancia, i.tolerancia) AS tolerancia,
               CASE WHEN tol.id IS NOT NULL THEN ISNULL(tol.tolerancia_menos, tol.tolerancia)
                    WHEN fijo.id IS NOT NULL THEN ISNULL(fijo.tolerancia_menos, fijo.tolerancia)
                    ELSE ISNULL(i.tolerancia_menos, i.tolerancia) END AS tolerancia_menos,
               i.decimales, i.cero_es_logro, i.mostrar_no_aplica
        FROM #centro_ind_mes c
        JOIN dbo.tmi_indicador i ON i.id = c.id_indicador
        LEFT JOIN dbo.tmi_indicador_tolerancia tol ON tol.id_indicador = i.id AND tol.anio = @anio AND tol.mes = c.mes
        LEFT JOIN dbo.tmi_indicador_tolerancia fijo ON fijo.id_indicador = i.id AND fijo.anio = @anio AND fijo.mes = 0
    ),
    est AS (
        SELECT g.*, d.valor,
               -- datos del indicador en el año (enero..corte): 0 = el centro no reportó ninguno de los términos
               SUM(ISNULL(d.datos, 0)) OVER (PARTITION BY g.id, g.codcentro) AS datos_anio,
               NULLIF(CASE g.mes WHEN 1 THEN ce.m01 WHEN 2 THEN ce.m02 WHEN 3 THEN ce.m03 WHEN 4 THEN ce.m04 WHEN 5 THEN ce.m05 WHEN 6 THEN ce.m06
                                 WHEN 7 THEN ce.m07 WHEN 8 THEN ce.m08 WHEN 9 THEN ce.m09 WHEN 10 THEN ce.m10 WHEN 11 THEN ce.m11 WHEN 12 THEN ce.m12 END, 0) AS est_centro,
               ce.aplica AS aplica_centro, ce.acept AS acept_centro, eb.est AS est_base, kc.clave AS clave_base,
               NULLIF(ie.estandar, 0) AS est_combinado, ie.acept AS acept_combinado, ie.aceptmenos AS aceptmenos_combinado,
               NULLIF(CASE g.mes WHEN 1 THEN st.m01 WHEN 2 THEN st.m02 WHEN 3 THEN st.m03 WHEN 4 THEN st.m04 WHEN 5 THEN st.m05 WHEN 6 THEN st.m06
                                 WHEN 7 THEN st.m07 WHEN 8 THEN st.m08 WHEN 9 THEN st.m09 WHEN 10 THEN st.m10 WHEN 11 THEN st.m11 WHEN 12 THEN st.m12 END, 0) AS est_tipo,
               NULLIF(CASE g.mes WHEN 1 THEN sn.m01 WHEN 2 THEN sn.m02 WHEN 3 THEN sn.m03 WHEN 4 THEN sn.m04 WHEN 5 THEN sn.m05 WHEN 6 THEN sn.m06
                                 WHEN 7 THEN sn.m07 WHEN 8 THEN sn.m08 WHEN 9 THEN sn.m09 WHEN 10 THEN sn.m10 WHEN 11 THEN sn.m11 WHEN 12 THEN sn.m12 END, 0) AS est_nivel,
               NULLIF(CASE g.mes WHEN 1 THEN sc.m01 WHEN 2 THEN sc.m02 WHEN 3 THEN sc.m03 WHEN 4 THEN sc.m04 WHEN 5 THEN sc.m05 WHEN 6 THEN sc.m06
                                 WHEN 7 THEN sc.m07 WHEN 8 THEN sc.m08 WHEN 9 THEN sc.m09 WHEN 10 THEN sc.m10 WHEN 11 THEN sc.m11 WHEN 12 THEN sc.m12 END, 0) AS est_categoria
        FROM malla g
        LEFT JOIN #num_den d ON d.id_indicador = g.id AND d.codcentro = g.codcentro AND d.mes = g.mes
        OUTER APPLY (SELECT TOP 1 * FROM #cest x
                     WHERE x.id_estandar = g.id AND x.codcentro = g.codcentro) ce
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
        /* Estándar según el tipo del indicador (tmi_tipo_estandar / tmi_estandar). Cada centro calza con UNA sola clave
           de la base, por exclusión (como 002_TMI_CONSULTAS_VISTA: nivel "WHERE tipo NOT IN (CNSR, IPO, INCOR)" UNION
           ALL tipo): si el tipo del centro es clave de la base, usa su tipo; si no, su categoría; si no, su nivel. La
           lista de tipos sale del catálogo, no está escrita aquí. No hay respaldo cruzado: si la clave del centro no
           tiene valor (o es 0), el centro queda sin estándar; no toma el de su nivel. No usa tmi_estandar.prioridad. */
        OUTER APPLY (SELECT TOP 1 k.fuente, k.clave
                     FROM dbo.tmi_estandar k
                     WHERE k.tipo_estandar = g.base_estandar AND k.activo = 1
                       AND k.clave = CASE k.fuente WHEN 'NIVEL' THEN g.nivel WHEN 'TIPO' THEN g.tipo ELSE g.categoria END
                     ORDER BY CASE k.fuente WHEN 'TIPO' THEN 1 WHEN 'CATEGORIA' THEN 2 ELSE 3 END) kc
        /* Valor del mes; si el mes aún no cerró (vacío) toma el fijo del año (m00), lo mismo que le copiará el cierre.
           0 = sin estándar. CASE en lugar de CHOOSE: el servidor no lo reconoce (compatibilidad anterior a SQL Server 2012) */
        OUTER APPLY (SELECT TOP 1 NULLIF(COALESCE(CASE g.mes WHEN 1 THEN x.m01 WHEN 2 THEN x.m02 WHEN 3 THEN x.m03
                                                    WHEN 4 THEN x.m04 WHEN 5 THEN x.m05 WHEN 6 THEN x.m06
                                                    WHEN 7 THEN x.m07 WHEN 8 THEN x.m08 WHEN 9 THEN x.m09
                                                    WHEN 10 THEN x.m10 WHEN 11 THEN x.m11 WHEN 12 THEN x.m12 END, x.m00), 0) AS est
                     FROM #std x
                     WHERE x.id_estandar = g.id AND x.fuente = kc.fuente AND x.clave = kc.clave) eb
        OUTER APPLY (SELECT TOP 1 * FROM #std x WHERE x.id_estandar = g.id
                       AND x.fuente = 'TIPO' AND x.clave = g.tipo) st
        OUTER APPLY (SELECT TOP 1 * FROM #std x WHERE x.id_estandar = g.id
                       AND x.fuente = 'NIVEL' AND x.clave = g.nivel) sn
        OUTER APPLY (SELECT TOP 1 * FROM #std x WHERE x.id_estandar = g.id
                       AND x.fuente = 'CATEGORIA' AND x.clave = g.categoria) sc
    ),
    val AS (
        SELECT e.*,
               /* orden: estándar del centro > tipo de estándar del indicador (tablas maestras) > reglas del panel
                  (tmi_indicador_estandar) > combinaciones anteriores de base_estandar que no estén en el catálogo.
                  Las reglas del panel y las combinaciones anteriores solo se usan si el centro no calza con ninguna clave
                  del catálogo (clave_base NULL): si calza y su clave no tiene valor, queda sin estándar (sin respaldo). */
               CASE WHEN e.aplica_centro = 0 THEN NULL
                    ELSE COALESCE(e.est_centro, e.est_base,
                                  CASE WHEN e.clave_base IS NULL THEN COALESCE(e.est_combinado,
                                  CASE e.base_estandar
                                      WHEN 'TIPO_NIVEL'           THEN COALESCE(e.est_tipo, e.est_nivel)
                                      WHEN 'TIPO_CATEGORIA'       THEN COALESCE(e.est_tipo, e.est_categoria)
                                      WHEN 'NIVEL_CATEGORIA'      THEN COALESCE(e.est_nivel, e.est_categoria)
                                      WHEN 'TIPO_NIVEL_CATEGORIA' THEN COALESCE(e.est_tipo, e.est_categoria, e.est_nivel)
                                  END) END) END                                  AS estandar
        FROM est e
    ),
    lim AS (
        SELECT v.*,
               v.estandar AS verde,
               /* % Acept: límite para el puntaje 3 (en banda, el de arriba) = estándar ± el porcentaje del indicador.
                  El % Acept propio del centro (tmi_centro_estandar.acept) gana. */
               COALESCE(v.acept_centro,
                        CASE WHEN v.est_centro IS NULL AND v.est_base IS NULL AND v.clave_base IS NULL THEN v.acept_combinado END,
                        CASE WHEN v.sentido IN ('MENOR', 'BANDA')
                             THEN CASE v.tipo_tolerancia WHEN 'ABS' THEN v.estandar + v.tolerancia ELSE v.estandar * (1 + v.tolerancia) END
                             ELSE CASE v.tipo_tolerancia WHEN 'ABS' THEN v.estandar - v.tolerancia ELSE v.estandar * (1 - v.tolerancia) END
                        END) AS acept,
               /* % Aceptmenos: solo banda, el límite de abajo */
               CASE WHEN v.sentido = 'BANDA'
                    THEN COALESCE(CASE WHEN v.est_centro IS NULL AND v.est_base IS NULL AND v.clave_base IS NULL THEN v.aceptmenos_combinado END,
                                  CASE v.tipo_tolerancia WHEN 'ABS' THEN v.estandar - v.tolerancia_menos
                                                         ELSE v.estandar * (1 - v.tolerancia_menos) END) END AS aceptmenos,
               ROUND(v.valor, ISNULL(v.decimales, 15)) AS valor_eval,
               CASE WHEN v.motivo_centro IS NOT NULL                         THEN v.motivo_centro
                    -- el usuario elige en la exclusión si el mes queda NA o con puntaje 0 (EXCLUIDO_CERO)
                    WHEN v.excluido = 1 AND v.excl_resultado = '0'           THEN 'EXCLUIDO_CERO'
                    WHEN v.excluido = 1                                      THEN 'EXCLUIDO'
                    WHEN v.estandar IS NULL                                  THEN 'SIN_ESTANDAR'
                    WHEN v.datos_anio = 0 AND v.sin_datos_anio <> 'MOSTRAR'  THEN 'SIN_DATOS_ANIO'
                    WHEN v.valor IS NULL                                     THEN 'SIN_DATO' END AS motivo_na
        FROM val v
    )
    INSERT INTO dbo.tmi_resultado (periodo_corte, id_indicador, codcentro, mes, numerador, denominador, valor,
                                   estandar, verde, acept, aceptmenos, puntaje, motivo_na, visible)
    SELECT @PERIODO, l.id, l.codcentro, l.mes, NULL, NULL,
           CASE WHEN l.motivo_na = 'EXCLUIDO_CERO' THEN 0 ELSE l.valor END, l.estandar, l.verde, l.acept, l.aceptmenos,
           CASE WHEN l.motivo_na = 'EXCLUIDO_CERO'             THEN '0'
                WHEN l.motivo_na IS NOT NULL                   THEN 'NA'
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
