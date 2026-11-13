/* =====================================================================================================
   TMI DINAMICO - 04 PROCEDIMIENTOS
     EXEC dbo.usp_tmi_validar_config;          -- 0 filas = configuración correcta
     EXEC dbo.usp_tmi_calcular      202608;    -- fórmula de cada indicador sobre TOTALIZADO3, estándar, puntaje
                                               -- en tiempo real: devuelve el resultado, no guarda nada
   Compatible con SQL Server 2008 R2+.
   ===================================================================================================== */

/* -----------------------------------------------------------------------------------------------------
   0. VALIDACION DE LA CONFIGURACION
   ----------------------------------------------------------------------------------------------------- */
IF OBJECT_ID('dbo.usp_tmi_validar_config', 'P') IS NULL EXEC(N'CREATE PROCEDURE dbo.usp_tmi_validar_config AS RETURN 0');   -- luego ALTER: no deja de existir
GO
ALTER PROCEDURE dbo.usp_tmi_validar_config
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
   1. PIVOT DE VARIABLES: ya no existe. El cálculo lee TOTALIZADO3 con los términos de cada fórmula, solo del
      periodo que se calcula (y de enero al corte para los acumulados); la tabla tmi_variable_pivot la borra el backend.
   ----------------------------------------------------------------------------------------------------- */
IF OBJECT_ID('dbo.usp_tmi_generar_pivot', 'P') IS NOT NULL DROP PROCEDURE dbo.usp_tmi_generar_pivot;
GO

/* -----------------------------------------------------------------------------------------------------
   1b. REGLA UNICA DE EXCLUSIONES Y ESTANDAR
       La usan usp_tmi_calcular (Calcular y el cierre) y el SQL descargable de cada indicador (backend,
       tmiFormula.consulta_sql): si se cambia la regla, se cambia solo aquí.
         SELECT * FROM dbo.fn_tmi_exclusion(202609) WHERE id_indicador = 1;
         SELECT * FROM dbo.fn_tmi_estandar(202609)  WHERE id_indicador = 1;
   ----------------------------------------------------------------------------------------------------- */

/* Meses excluidos (enero..mes del periodo) por indicador y centro. Manda la exclusión del indicador sobre la de
   "todos los indicadores" (id_estandar NULL); entre iguales, la que deja el mes en NA.
   resultado: 'NA' (el mes queda NA) o '0' (el mes queda con valor y puntaje 0); cada mes puede tener el suyo
   (res_MM de la tabla) o tomar el de la fila. */
IF OBJECT_ID('dbo.fn_tmi_exclusion') IS NULL
    EXEC(N'CREATE FUNCTION dbo.fn_tmi_exclusion (@PERIODO INT) RETURNS TABLE AS RETURN SELECT 1 AS x');   -- luego ALTER
GO
ALTER FUNCTION dbo.fn_tmi_exclusion (@PERIODO INT)
RETURNS TABLE
AS
RETURN
SELECT z.id_indicador, z.codcentro, z.mes, ISNULL(z.resultado, 'NA') AS resultado, z.motivo
FROM  (SELECT i.id AS id_indicador, e.codcentro, m.mes, r.resultado, e.motivo,
              ROW_NUMBER() OVER (PARTITION BY i.id, e.codcentro, m.mes
                                 ORDER BY CASE WHEN e.id_estandar IS NULL THEN 1 ELSE 0 END,
                                          CASE WHEN r.resultado = 'NA' THEN 0 ELSE 1 END) AS rn
       FROM   dbo.vw_tmi_exclusion e
       JOIN   dbo.tmi_indicador i ON i.id = e.id_estandar OR e.id_estandar IS NULL
       CROSS JOIN (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) m (mes)
       /* resultado del mes: el propio del mes (r01..r12) o el de la fila */
       CROSS APPLY (SELECT CASE m.mes WHEN 1 THEN e.r01 WHEN 2 THEN e.r02 WHEN 3 THEN e.r03 WHEN 4 THEN e.r04
                                      WHEN 5 THEN e.r05 WHEN 6 THEN e.r06 WHEN 7 THEN e.r07 WHEN 8 THEN e.r08
                                      WHEN 9 THEN e.r09 WHEN 10 THEN e.r10 WHEN 11 THEN e.r11 WHEN 12 THEN e.r12
                                      END AS resultado) r
       WHERE  e.anio = @PERIODO / 100 AND m.mes <= @PERIODO % 100 AND e.codcentro IS NOT NULL
         AND  CAST(CASE m.mes WHEN 1 THEN e.x01 WHEN 2 THEN e.x02 WHEN 3 THEN e.x03 WHEN 4 THEN e.x04 WHEN 5 THEN e.x05
                              WHEN 6 THEN e.x06 WHEN 7 THEN e.x07 WHEN 8 THEN e.x08 WHEN 9 THEN e.x09 WHEN 10 THEN e.x10
                              WHEN 11 THEN e.x11 WHEN 12 THEN e.x12 END AS INT) = 1) z
WHERE  z.rn = 1;
GO

/* Estándar, % Acept y % Aceptmenos del mes del periodo, por indicador y centro del año (tmi_centro del año o, si el
   año no tiene centros, los sin año).
   Estándar: "no aplica" del centro (NULL) > estándar del centro > tipo de estándar del indicador (tablas maestras;
   mes vacío = fijo del año m00) > reglas del panel (tmi_indicador_estandar) > combinaciones anteriores de
   base_estandar. Las reglas del panel y las combinaciones solo se usan si el centro no calza con ninguna clave del
   catálogo: si calza y su clave no tiene valor, queda sin estándar (sin respaldo).
   % Acept: el del centro > el de la regla del panel > estándar ± tolerancia (del mes > fija del año > del indicador). */
IF OBJECT_ID('dbo.fn_tmi_estandar') IS NULL
    EXEC(N'CREATE FUNCTION dbo.fn_tmi_estandar (@PERIODO INT) RETURNS TABLE AS RETURN SELECT 1 AS x');   -- luego ALTER
GO
ALTER FUNCTION dbo.fn_tmi_estandar (@PERIODO INT)
RETURNS TABLE
AS
RETURN
WITH centro AS (
    SELECT c.codcentro, MAX(c.nivel) AS nivel, MAX(c.nivel_estandar) AS nivel_estandar, MAX(c.categoria) AS categoria
    FROM   dbo.vw_tmi_centro_base c
    WHERE  c.anio = @PERIODO / 100
       OR (c.anio IS NULL AND NOT EXISTS (SELECT 1 FROM dbo.vw_tmi_centro_base x WHERE x.anio = @PERIODO / 100))
    GROUP BY c.codcentro
),
ind AS (   -- % Acept del mes: el del mes > el fijo del año (mes 0) > el del indicador
    SELECT i.id, i.base_estandar, i.sentido,
           COALESCE(tol.tipo_tolerancia, fijo.tipo_tolerancia, i.tipo_tolerancia) AS tipo_tolerancia,
           COALESCE(tol.tolerancia, fijo.tolerancia, i.tolerancia) AS tolerancia,
           CASE WHEN tol.id IS NOT NULL THEN ISNULL(tol.tolerancia_menos, tol.tolerancia)
                WHEN fijo.id IS NOT NULL THEN ISNULL(fijo.tolerancia_menos, fijo.tolerancia)
                ELSE ISNULL(i.tolerancia_menos, i.tolerancia) END AS tolerancia_menos
    FROM   dbo.tmi_indicador i
    LEFT JOIN dbo.tmi_indicador_tolerancia tol  ON tol.id_indicador = i.id AND tol.anio = @PERIODO / 100 AND tol.mes = @PERIODO % 100
    LEFT JOIN dbo.tmi_indicador_tolerancia fijo ON fijo.id_indicador = i.id AND fijo.anio = @PERIODO / 100 AND fijo.mes = 0
),
est AS (
    SELECT g.id AS id_indicador, c.codcentro, g.base_estandar, g.sentido, g.tipo_tolerancia, g.tolerancia, g.tolerancia_menos,
           NULLIF(CASE @PERIODO % 100 WHEN 1 THEN ce.m01 WHEN 2 THEN ce.m02 WHEN 3 THEN ce.m03 WHEN 4 THEN ce.m04 WHEN 5 THEN ce.m05 WHEN 6 THEN ce.m06
                             WHEN 7 THEN ce.m07 WHEN 8 THEN ce.m08 WHEN 9 THEN ce.m09 WHEN 10 THEN ce.m10 WHEN 11 THEN ce.m11 WHEN 12 THEN ce.m12 END, 0) AS est_centro,
           ce.aplica AS aplica_centro, ce.acept AS acept_centro, kc.fuente AS fuente_base, kc.clave AS clave_base, eb.est AS est_base,
           NULLIF(ie.estandar, 0) AS est_combinado, ie.acept AS acept_combinado, ie.aceptmenos AS aceptmenos_combinado,
           NULLIF(CASE @PERIODO % 100 WHEN 1 THEN st.m01 WHEN 2 THEN st.m02 WHEN 3 THEN st.m03 WHEN 4 THEN st.m04 WHEN 5 THEN st.m05 WHEN 6 THEN st.m06
                             WHEN 7 THEN st.m07 WHEN 8 THEN st.m08 WHEN 9 THEN st.m09 WHEN 10 THEN st.m10 WHEN 11 THEN st.m11 WHEN 12 THEN st.m12 END, 0) AS est_tipo,
           NULLIF(CASE @PERIODO % 100 WHEN 1 THEN sn.m01 WHEN 2 THEN sn.m02 WHEN 3 THEN sn.m03 WHEN 4 THEN sn.m04 WHEN 5 THEN sn.m05 WHEN 6 THEN sn.m06
                             WHEN 7 THEN sn.m07 WHEN 8 THEN sn.m08 WHEN 9 THEN sn.m09 WHEN 10 THEN sn.m10 WHEN 11 THEN sn.m11 WHEN 12 THEN sn.m12 END, 0) AS est_nivel,
           NULLIF(CASE @PERIODO % 100 WHEN 1 THEN sc.m01 WHEN 2 THEN sc.m02 WHEN 3 THEN sc.m03 WHEN 4 THEN sc.m04 WHEN 5 THEN sc.m05 WHEN 6 THEN sc.m06
                             WHEN 7 THEN sc.m07 WHEN 8 THEN sc.m08 WHEN 9 THEN sc.m09 WHEN 10 THEN sc.m10 WHEN 11 THEN sc.m11 WHEN 12 THEN sc.m12 END, 0) AS est_categoria
    FROM   ind g
    CROSS JOIN centro c
    OUTER APPLY (SELECT TOP 1 * FROM dbo.vw_tmi_centro_estandar x
                 WHERE x.id_estandar = g.id AND x.codcentro = c.codcentro AND x.anio = @PERIODO / 100) ce
    OUTER APPLY (SELECT TOP 1 x.estandar, x.acept, x.aceptmenos
                 FROM dbo.tmi_indicador_estandar x
                 WHERE x.id_indicador = g.id AND x.activo = 1
                   AND @PERIODO BETWEEN x.periodo_desde AND x.periodo_hasta
                   AND (x.nivel IS NULL OR x.nivel IN (c.nivel, c.nivel_estandar))
                   AND (x.categoria IS NULL OR x.categoria = c.categoria)
                   AND (x.tipo IS NULL OR x.tipo = c.nivel_estandar)
                   AND (x.nivel IS NOT NULL OR x.categoria IS NOT NULL OR x.tipo IS NOT NULL)
                 ORDER BY (CASE WHEN x.tipo IS NOT NULL THEN 4 ELSE 0 END
                         + CASE WHEN x.categoria IS NOT NULL THEN 2 ELSE 0 END
                         + CASE WHEN x.nivel IS NOT NULL THEN 1 ELSE 0 END) DESC,
                          (x.periodo_hasta - x.periodo_desde) ASC,
                          x.id DESC) ie
    /* clave del catálogo: si el tipo del centro es clave de la base, su tipo; si no, su categoría; si no, su nivel */
    OUTER APPLY (SELECT TOP 1 k.fuente, k.clave
                 FROM dbo.tmi_estandar k
                 WHERE k.tipo_estandar = g.base_estandar AND k.activo = 1
                   AND k.clave = CASE k.fuente WHEN 'NIVEL' THEN c.nivel WHEN 'TIPO' THEN c.nivel_estandar ELSE c.categoria END
                 ORDER BY CASE k.fuente WHEN 'TIPO' THEN 1 WHEN 'CATEGORIA' THEN 2 ELSE 3 END) kc
    /* valor del mes; si el mes aún no cerró (vacío) el fijo del año (m00). 0 = sin estándar */
    OUTER APPLY (SELECT TOP 1 NULLIF(COALESCE(CASE @PERIODO % 100 WHEN 1 THEN x.m01 WHEN 2 THEN x.m02 WHEN 3 THEN x.m03
                                                WHEN 4 THEN x.m04 WHEN 5 THEN x.m05 WHEN 6 THEN x.m06
                                                WHEN 7 THEN x.m07 WHEN 8 THEN x.m08 WHEN 9 THEN x.m09
                                                WHEN 10 THEN x.m10 WHEN 11 THEN x.m11 WHEN 12 THEN x.m12 END, x.m00), 0) AS est
                 FROM dbo.vw_tmi_std x
                 WHERE x.id_estandar = g.id AND x.anio = @PERIODO / 100 AND x.fuente = kc.fuente AND x.clave = kc.clave) eb
    OUTER APPLY (SELECT TOP 1 * FROM dbo.vw_tmi_std x WHERE x.id_estandar = g.id AND x.anio = @PERIODO / 100
                   AND x.fuente = 'TIPO' AND x.clave = c.nivel_estandar) st
    OUTER APPLY (SELECT TOP 1 * FROM dbo.vw_tmi_std x WHERE x.id_estandar = g.id AND x.anio = @PERIODO / 100
                   AND x.fuente = 'NIVEL' AND x.clave = c.nivel) sn
    OUTER APPLY (SELECT TOP 1 * FROM dbo.vw_tmi_std x WHERE x.id_estandar = g.id AND x.anio = @PERIODO / 100
                   AND x.fuente = 'CATEGORIA' AND x.clave = c.categoria) sc
),
val AS (
    SELECT e.*,
           CASE WHEN e.aplica_centro = 0 THEN NULL
                ELSE COALESCE(e.est_centro, e.est_base,
                              CASE WHEN e.clave_base IS NULL THEN COALESCE(e.est_combinado,
                              CASE e.base_estandar
                                  WHEN 'TIPO_NIVEL'           THEN COALESCE(e.est_tipo, e.est_nivel)
                                  WHEN 'TIPO_CATEGORIA'       THEN COALESCE(e.est_tipo, e.est_categoria)
                                  WHEN 'NIVEL_CATEGORIA'      THEN COALESCE(e.est_nivel, e.est_categoria)
                                  WHEN 'TIPO_NIVEL_CATEGORIA' THEN COALESCE(e.est_tipo, e.est_categoria, e.est_nivel)
                              END) END) END AS estandar
    FROM   est e
)
SELECT v.id_indicador, v.codcentro, v.estandar,
       /* % Acept: límite del puntaje 3 (en banda, el de arriba). El del centro gana. */
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
       v.est_centro, v.aplica_centro,
       CASE WHEN v.aplica_centro = 0         THEN 'NO APLICA (estándar del centro)'
            WHEN v.est_centro IS NOT NULL    THEN 'ESTÁNDAR DEL CENTRO'
            WHEN v.est_base IS NOT NULL      THEN v.fuente_base + ' ' + v.clave_base
            WHEN v.clave_base IS NOT NULL    THEN 'SIN ESTÁNDAR (' + v.fuente_base + ' ' + v.clave_base + ' sin valor)'
            WHEN v.est_combinado IS NOT NULL THEN 'REGLA DEL PANEL'
            WHEN v.estandar IS NOT NULL      THEN 'COMBINACIÓN ' + v.base_estandar
            ELSE 'SIN ESTÁNDAR' END AS origen_estandar
FROM   val v;
GO

/* -----------------------------------------------------------------------------------------------------
   1.9 VERSIONES DE TOTALIZADO3 Y RESULTADO OFICIAL
   ----------------------------------------------------------------------------------------------------- */
/* usp_tmi_backup_totalizado3 @PERIODO: copia TOTALIZADO3 de enero a @PERIODO de ese año en TOTALIZADO3_BACKUP con
   periodo_backup = @PERIODO (la misma estructura más las columnas de la copia). TOTALIZADO3 solo se lee. Si la copia
   del periodo ya existe no se toca, salvo @REEMPLAZAR = 1. Devuelve copiado (1 = se copió ahora) y filas. */
IF OBJECT_ID('dbo.usp_tmi_backup_totalizado3', 'P') IS NULL
    EXEC(N'CREATE PROCEDURE dbo.usp_tmi_backup_totalizado3 AS RETURN 0');   -- luego ALTER
GO
ALTER PROCEDURE dbo.usp_tmi_backup_totalizado3
    @PERIODO    INT,
    @USUARIO    NVARCHAR(50) = NULL,
    @REEMPLAZAR BIT = 0
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    DECLARE @anio INT = @PERIODO / 100, @mes INT = @PERIODO % 100, @sql NVARCHAR(MAX);
    IF @mes NOT BETWEEN 1 AND 12
    BEGIN
        RAISERROR('El periodo debe tener formato AAAAMM.', 16, 1);
        RETURN;
    END
    IF ISNULL(@REEMPLAZAR, 0) = 0 AND EXISTS (SELECT 1 FROM dbo.TOTALIZADO3_BACKUP WHERE periodo_backup = @PERIODO)
    BEGIN
        SELECT CAST(0 AS BIT) AS copiado, COUNT(*) AS filas FROM dbo.TOTALIZADO3_BACKUP WHERE periodo_backup = @PERIODO;
        RETURN;
    END

    /* primero se lee TOTALIZADO3 (puede estar en otro servidor) a una tabla temporal, fuera de la transacción */
    SELECT TOP 0 CAST(T.ID AS BIGINT) AS ID, T.periodo, T.codred_ses, T.red_ses, T.codcentro_ses, T.desccentro_ses, T.codredsgh, T.redsgh, T.codcentrosgh, T.descripcionsgh, T.nivel, T.tipgrupo, T.desctipgrupo, T.actividad, T.descactividad, T.servicio, T.descservicio, T.cantidad, T.usuariocrea, T.fechacrea, T.usuariomod, T.fechamod, T.tiponivel, T.descnivel, T.tipohoja   -- CAST: sin la propiedad IDENTITY
    INTO   #copia
    FROM   {{TOTALIZADO3}} T;
    SET @sql = N'INSERT INTO #copia (ID, periodo, codred_ses, red_ses, codcentro_ses, desccentro_ses, codredsgh, redsgh, codcentrosgh, descripcionsgh, nivel, tipgrupo, desctipgrupo, actividad, descactividad, servicio, descservicio, cantidad, usuariocrea, fechacrea, usuariomod, fechamod, tiponivel, descnivel, tipohoja)
                 SELECT T.ID, T.periodo, T.codred_ses, T.red_ses, T.codcentro_ses, T.desccentro_ses, T.codredsgh, T.redsgh, T.codcentrosgh, T.descripcionsgh, T.nivel, T.tipgrupo, T.desctipgrupo, T.actividad, T.descactividad, T.servicio, T.descservicio, T.cantidad, T.usuariocrea, T.fechacrea, T.usuariomod, T.fechamod, T.tiponivel, T.descnivel, T.tipohoja
                 FROM {{TOTALIZADO3}} T
                 WHERE T.periodo BETWEEN ' + CAST(@anio * 100 + 1 AS NVARCHAR(10)) + N' AND ' + CAST(@PERIODO AS NVARCHAR(10)) + N';';
    EXEC sp_executesql @sql;
    IF NOT EXISTS (SELECT 1 FROM #copia WHERE periodo = @PERIODO)
    BEGIN
        RAISERROR('TOTALIZADO3 no tiene datos del periodo %d: no se copia.', 16, 1, @PERIODO);
        RETURN;
    END

    BEGIN TRAN;
    DELETE dbo.TOTALIZADO3_BACKUP WHERE periodo_backup = @PERIODO;
    INSERT INTO dbo.TOTALIZADO3_BACKUP (ID, periodo, codred_ses, red_ses, codcentro_ses, desccentro_ses, codredsgh, redsgh, codcentrosgh, descripcionsgh, nivel, tipgrupo, desctipgrupo, actividad, descactividad, servicio, descservicio, cantidad, usuariocrea, fechacrea, usuariomod, fechamod, tiponivel, descnivel, tipohoja, periodo_backup, fecha_backup, usuario_backup)
    SELECT ID, periodo, codred_ses, red_ses, codcentro_ses, desccentro_ses, codredsgh, redsgh, codcentrosgh, descripcionsgh, nivel, tipgrupo, desctipgrupo, actividad, descactividad, servicio, descservicio, cantidad, usuariocrea, fechacrea, usuariomod, fechamod, tiponivel, descnivel, tipohoja, @PERIODO, GETDATE(), @USUARIO
    FROM   #copia;
    COMMIT;
    SELECT CAST(1 AS BIT) AS copiado, COUNT(*) AS filas FROM dbo.TOTALIZADO3_BACKUP WHERE periodo_backup = @PERIODO;
END
GO

/* El resultado ya no se guarda (se calcula en tiempo real): se quitan la función y las vistas del resultado guardado. */
IF OBJECT_ID('dbo.vw_tmi_resultado_indicador', 'V') IS NOT NULL DROP VIEW dbo.vw_tmi_resultado_indicador;
IF OBJECT_ID('dbo.vw_tmi_resultado', 'V') IS NOT NULL DROP VIEW dbo.vw_tmi_resultado;
IF OBJECT_ID('dbo.fn_tmi_resultado') IS NOT NULL DROP FUNCTION dbo.fn_tmi_resultado;
GO

/* fn_tmi_num: número en texto para el desarrollo de la fórmula (hasta 4 decimales, sin ceros a la derecha) */
IF OBJECT_ID('dbo.fn_tmi_num') IS NULL
    EXEC(N'CREATE FUNCTION dbo.fn_tmi_num (@v FLOAT) RETURNS VARCHAR(50) AS BEGIN RETURN NULL END');   -- luego ALTER
GO
ALTER FUNCTION dbo.fn_tmi_num (@v FLOAT)
RETURNS VARCHAR(50)
AS
BEGIN
    IF @v IS NULL OR ABS(@v) >= 1e20 RETURN CONVERT(VARCHAR(50), @v);
    DECLARE @s VARCHAR(50) = CONVERT(VARCHAR(50), CAST(ROUND(@v, 4) AS DECIMAL(28, 4)));
    WHILE RIGHT(@s, 1) = '0' SET @s = LEFT(@s, LEN(@s) - 1);
    IF RIGHT(@s, 1) = '.' SET @s = LEFT(@s, LEN(@s) - 1);
    IF @s = '-0' SET @s = '0';
    RETURN @s;
END
GO

/* -----------------------------------------------------------------------------------------------------
   2. CALCULO DE INDICADORES
   ----------------------------------------------------------------------------------------------------- */
IF OBJECT_ID('dbo.usp_tmi_calcular', 'P') IS NULL EXEC(N'CREATE PROCEDURE dbo.usp_tmi_calcular AS RETURN 0');   -- luego ALTER: no deja de existir
GO
ALTER PROCEDURE dbo.usp_tmi_calcular
    @PERIODO INT,
    @ORIGEN  VARCHAR(10) = 'ACTUAL',   -- ACTUAL: TOTALIZADO3 de hoy | BACKUP: la copia del cierre del periodo (TOTALIZADO3_BACKUP)
    @USUARIO NVARCHAR(50) = NULL,
    /* Siempre en tiempo real: no escribe nada. Calcula cada mes de enero al corte con la misma regla (como si cada
       mes fuera el corte) y devuelve 4 resultados: final por centro, resultado del mes de corte, términos y valor y
       puntaje de cada mes. @GUARDAR queda por compatibilidad: solo acepta 0 (el resultado ya no se guarda). */
    @GUARDAR BIT = 0
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    DECLARE @anio INT = @PERIODO / 100, @mes INT = @PERIODO % 100;
    IF @mes NOT BETWEEN 1 AND 12
    BEGIN
        RAISERROR('El periodo debe tener formato AAAAMM.', 16, 1);
        RETURN;
    END

    SET @ORIGEN = UPPER(ISNULL(@ORIGEN, 'ACTUAL'));
    IF @ORIGEN NOT IN ('ACTUAL', 'BACKUP')
    BEGIN
        RAISERROR('El origen de los datos debe ser ACTUAL o BACKUP.', 16, 1);
        RETURN;
    END
    IF ISNULL(@GUARDAR, 0) = 1
    BEGIN
        RAISERROR('El resultado del TMI ya no se guarda: se calcula en tiempo real.', 16, 1);
        RETURN;
    END

    /* Sin datos del periodo (aún no se cargó el mes, o no hay copia del cierre) no se calcula */
    DECLARE @hay INT = 0, @sql_hay NVARCHAR(MAX);
    IF @ORIGEN = 'BACKUP'
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM dbo.TOTALIZADO3_BACKUP WHERE periodo_backup = @PERIODO)
        BEGIN
            RAISERROR('No hay copia de TOTALIZADO3 del periodo %d en TOTALIZADO3_BACKUP: se guarda al cerrar el periodo.', 16, 1, @PERIODO);
            RETURN;
        END
        IF EXISTS (SELECT 1 FROM dbo.TOTALIZADO3_BACKUP WHERE periodo_backup = @PERIODO AND periodo = @PERIODO) SET @hay = 1;
    END
    ELSE
    BEGIN
        SET @sql_hay = N'SELECT @hay = CASE WHEN EXISTS (SELECT 1 FROM {{TOTALIZADO3}} T WHERE T.periodo = '
                     + CAST(@PERIODO AS NVARCHAR(10)) + N') THEN 1 ELSE 0 END;';
        EXEC sp_executesql @sql_hay, N'@hay INT OUTPUT', @hay = @hay OUTPUT;
    END
    IF @hay = 0
    BEGIN
        RAISERROR('TOTALIZADO3 no tiene datos del periodo %d: no se calcula.', 16, 1, @PERIODO);
        RETURN;
    END

    BEGIN TRY
    /* 2.1 Valor de cada término de la fórmula (tmi_indicador_termino: T1, T2...) por centro y mes, directo de TOTALIZADO3.
           Término [g;a#s]: suma de cantidad del grupo, actividad y servicios. MEDIANA([..]): mediana de cada servicio en
           el mes, redondeada, y suma de servicios (recursos, como CONSO4 / CONSO5 de Generar_pivot.sql). */
    SELECT t.id_indicador, t.codigo, t.tipgrupo, t.actividad, t.servicio, t.mediana
    INTO   #termino
    FROM   dbo.tmi_indicador_termino t
    JOIN   dbo.tmi_indicador i ON i.id = t.id_indicador AND i.activo = 1 AND i.formula_sql IS NOT NULL;

    /* TOTALIZADO3 puede estar en otro servidor: una sola lectura con filtro literal (enero..corte y grupos) */
    DECLARE @grupos NVARCHAR(MAX), @sql NVARCHAR(MAX);
    SELECT @grupos = STUFF((SELECT N',' + CAST(g.tipgrupo AS NVARCHAR(20))
                            FROM (SELECT DISTINCT tipgrupo FROM #termino) g ORDER BY g.tipgrupo
                            FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, N'');
    SELECT TOP 0 T.periodo, T.codcentro_ses, T.servicio, T.tipgrupo, T.actividad, T.cantidad
    INTO   #t3
    FROM   {{TOTALIZADO3}} T;
    -- origen de los datos: TOTALIZADO3 de hoy o la copia del cierre del periodo
    DECLARE @fuente NVARCHAR(500) = CASE WHEN @ORIGEN = 'BACKUP'
        THEN N'dbo.TOTALIZADO3_BACKUP T WHERE T.periodo_backup = ' + CAST(@PERIODO AS NVARCHAR(10)) + N' AND'
        ELSE N'{{TOTALIZADO3}} T WHERE' END;
    IF @grupos IS NOT NULL
    BEGIN
        SET @sql = N'INSERT INTO #t3 (periodo, codcentro_ses, servicio, tipgrupo, actividad, cantidad)
                     SELECT T.periodo, T.codcentro_ses, T.servicio, T.tipgrupo, T.actividad, T.cantidad
                     FROM ' + @fuente + N' T.periodo BETWEEN ' + CAST(@anio * 100 + 1 AS NVARCHAR(10)) + N' AND ' + CAST(@PERIODO AS NVARCHAR(10)) + N'
                       AND T.tipgrupo IN (' + @grupos + N');';
        EXEC sp_executesql @sql;
    END

    -- un registro entra una vez por término: los servicios de un término son filas distintas
    SELECT k.id_indicador, k.codigo, k.mediana, T.codcentro_ses AS codcentro, T.periodo % 100 AS mes, T.servicio,
           CAST(T.cantidad AS FLOAT) AS cantidad, k.tipgrupo, k.actividad, k.servicio AS servicio_def
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

    /* Justificación: lo mismo por cada parte del término (grupo, actividad y servicio de tmi_indicador_termino), con
       las filas de TOTALIZADO3 que se sumaron (términos del resultado) */
    SELECT id_indicador, codigo, tipgrupo, actividad, servicio_def, codcentro, mes,
           SUM(cantidad) AS valor_mes, COUNT(*) AS filas
    INTO   #det_mes
    FROM   #base WHERE mediana = 0
    GROUP BY id_indicador, codigo, tipgrupo, actividad, servicio_def, codcentro, mes;

    INSERT INTO #det_mes (id_indicador, codigo, tipgrupo, actividad, servicio_def, codcentro, mes, valor_mes, filas)
    SELECT id_indicador, codigo, tipgrupo, actividad, servicio_def, codcentro, mes, SUM(ROUND(med, 0)), SUM(cnt)
    FROM  (SELECT id_indicador, codigo, tipgrupo, actividad, servicio_def, codcentro, mes, servicio,
                  AVG(cantidad) AS med, MAX(cnt) AS cnt
           FROM  (SELECT id_indicador, codigo, tipgrupo, actividad, servicio_def, codcentro, mes, servicio, cantidad,
                         ROW_NUMBER() OVER (PARTITION BY id_indicador, codigo, tipgrupo, actividad, servicio_def, codcentro, mes, servicio
                                            ORDER BY cantidad) AS rn,
                         COUNT(*) OVER (PARTITION BY id_indicador, codigo, tipgrupo, actividad, servicio_def, codcentro, mes, servicio) AS cnt
                  FROM #base WHERE mediana = 1) r
           WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
           GROUP BY id_indicador, codigo, tipgrupo, actividad, servicio_def, codcentro, mes, servicio) m
    GROUP BY id_indicador, codigo, tipgrupo, actividad, servicio_def, codcentro, mes;
    CREATE CLUSTERED INDEX ix_det_mes ON #det_mes (id_indicador, codcentro, codigo, mes);

    /* Meses que se calculan (#meses): cada mes de enero al corte, cada uno como si fuera el corte (sus centros vigentes, exclusiones, estándar y acumulado). Todos van en una sola pasada:
       las tablas llevan la columna mes (el mes que se calcula) en lugar de repetir el cálculo una vez por mes.
       @mes y @PERIODO siguen siendo los del mes de corte. */
    CREATE TABLE #meses (mes INT PRIMARY KEY);
    INSERT INTO #meses (mes)
    SELECT v FROM (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) z(v)
    WHERE  v <= @mes;

    /* 2.2 Centros del reporte y situación de cada mes (exclusión por periodo)
           - Centros de tmi_centro del año (o sin año) -> #centro_anio; los de cada mes calculado son los visibles en ese
             mes (flag del mes distinto de 0, #centro_vig). #centro = los del mes de corte (filas del resultado final).
           - Cada mes: si el flag del mes es 0 -> NA ese mes (NO_VIGENTE_MES).
           - vw_tmi_exclusion: excl del mes = 1 -> NA ese mes, para un indicador o todos (id_estandar NULL). */
    SELECT c.codcentro, MIN(c.id_centro) AS id_centro, MAX(c.red) AS red, MIN(c.orden) AS orden, MIN(c.orden_tipo) AS orden_tipo,
           MAX(c.centro) AS centro, MAX(c.categoria) AS categoria, MAX(c.nivel) AS nivel, MAX(c.nivel_estandar) AS nivel_estandar, MAX(c.tipo) AS tipo,
           MAX(CAST(c.f01 AS INT)) f01, MAX(CAST(c.f02 AS INT)) f02, MAX(CAST(c.f03 AS INT)) f03, MAX(CAST(c.f04 AS INT)) f04,
           MAX(CAST(c.f05 AS INT)) f05, MAX(CAST(c.f06 AS INT)) f06, MAX(CAST(c.f07 AS INT)) f07, MAX(CAST(c.f08 AS INT)) f08,
           MAX(CAST(c.f09 AS INT)) f09, MAX(CAST(c.f10 AS INT)) f10, MAX(CAST(c.f11 AS INT)) f11, MAX(CAST(c.f12 AS INT)) f12
    INTO   #centro_anio
    FROM   dbo.vw_tmi_centro_base c
    WHERE  c.anio = @anio
       OR (c.anio IS NULL AND NOT EXISTS (SELECT 1 FROM dbo.vw_tmi_centro_base x WHERE x.anio = @anio))
    GROUP BY c.codcentro;

    -- flag de cada centro en cada mes de enero al corte (0 = no se lista ese mes)
    SELECT c.codcentro, m.v AS mes,
           CASE m.v WHEN 1 THEN c.f01 WHEN 2 THEN c.f02 WHEN 3 THEN c.f03 WHEN 4 THEN c.f04 WHEN 5 THEN c.f05 WHEN 6 THEN c.f06
                    WHEN 7 THEN c.f07 WHEN 8 THEN c.f08 WHEN 9 THEN c.f09 WHEN 10 THEN c.f10 WHEN 11 THEN c.f11 WHEN 12 THEN c.f12 END AS flag
    INTO   #centro_vig
    FROM   #centro_anio c
    CROSS JOIN (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) m(v)
    WHERE  m.v <= @mes;
    CREATE CLUSTERED INDEX ix_centro_vig ON #centro_vig (codcentro, mes);

    SELECT c.* INTO #centro FROM #centro_anio c
    JOIN   #centro_vig v ON v.codcentro = c.codcentro AND v.mes = @mes
    WHERE  ISNULL(v.flag, 1) <> 0;

    /* Exclusiones y estándar con la regla única (fn_tmi_exclusion, fn_tmi_estandar: la misma que el SQL descargable
       del indicador). Se copian a tablas temporales con índice. Las exclusiones del corte traen enero..corte (cada mes
       con la suya); el estándar y el % Acept son los de cada mes calculado. */
    SELECT * INTO #excl_mes FROM dbo.fn_tmi_exclusion(@PERIODO);
    CREATE CLUSTERED INDEX ix_excl_mes ON #excl_mes (id_indicador, codcentro, mes);
    SELECT CAST(@mes AS INT) AS mes, e.* INTO #est_ind FROM dbo.fn_tmi_estandar(@PERIODO) e WHERE 1 = 0;
    DECLARE @k INT;
    DECLARE cmes CURSOR LOCAL FAST_FORWARD FOR SELECT mes FROM #meses ORDER BY mes;
    OPEN cmes; FETCH NEXT FROM cmes INTO @k;
    WHILE @@FETCH_STATUS = 0
    BEGIN
        INSERT INTO #est_ind SELECT @k, e.* FROM dbo.fn_tmi_estandar(@anio * 100 + @k) e;
        FETCH NEXT FROM cmes INTO @k;
    END
    CLOSE cmes; DEALLOCATE cmes;
    CREATE CLUSTERED INDEX ix_est_ind ON #est_ind (id_indicador, codcentro, mes);

    SELECT i.id AS id_indicador, c.codcentro, c.red, c.orden, c.orden_tipo, c.id_centro, c.categoria, c.nivel, c.nivel_estandar, c.tipo, m.mes,
           CASE WHEN (CASE m.mes WHEN 1 THEN c.f01 WHEN 2 THEN c.f02 WHEN 3 THEN c.f03 WHEN 4 THEN c.f04 WHEN 5 THEN c.f05 WHEN 6 THEN c.f06
                                 WHEN 7 THEN c.f07 WHEN 8 THEN c.f08 WHEN 9 THEN c.f09 WHEN 10 THEN c.f10 WHEN 11 THEN c.f11 WHEN 12 THEN c.f12 END) = 0
                THEN 'NO_VIGENTE_MES'
                /* Centros del indicador (tmi_indicador_ambito, vigente en el mes): con filas incluir = 1, solo los centros
                   que coinciden con alguna; una fila incluir = 0 que coincide lo deja fuera. Sin filas = todos los centros. */
                WHEN (amb.lista_blanca = 1 AND amb.incluido = 0) OR amb.excluido = 1
                THEN 'FUERA_DE_AMBITO' END AS motivo_centro,
           CASE WHEN x.id_indicador IS NOT NULL THEN 1 ELSE 0 END AS excluido,
           ISNULL(x.resultado, 'NA') AS excl_resultado
    INTO   #centro_ind_mes
    FROM   #centro_anio c
    CROSS JOIN dbo.tmi_indicador i
    CROSS JOIN (SELECT v AS mes FROM (VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)) z(v) WHERE v <= @mes) m
    /* mes excluido ('NA' o '0'), regla de fn_tmi_exclusion */
    LEFT JOIN #excl_mes x ON x.id_indicador = i.id AND x.codcentro = c.codcentro AND x.mes = m.mes
    OUTER APPLY (SELECT MAX(CASE WHEN a.incluir = 1 THEN 1 ELSE 0 END)                AS lista_blanca,
                        MAX(CASE WHEN a.incluir = 1 AND k.coincide = 1 THEN 1 ELSE 0 END) AS incluido,
                        MAX(CASE WHEN a.incluir = 0 AND k.coincide = 1 THEN 1 ELSE 0 END) AS excluido
                 FROM dbo.tmi_indicador_ambito a
                 CROSS APPLY (SELECT CASE WHEN (a.red IS NULL OR a.red = c.red) AND (a.nivel IS NULL OR a.nivel IN (c.nivel, c.nivel_estandar))
                                           AND (a.categoria IS NULL OR a.categoria = c.categoria)
                                           AND (a.tipo IS NULL OR a.tipo = c.nivel_estandar)
                                           AND (a.codcentro IS NULL OR a.codcentro = c.codcentro) THEN 1 ELSE 0 END AS coincide) k
                 WHERE a.id_indicador = i.id
                   AND @anio * 100 + m.mes BETWEEN a.periodo_desde AND a.periodo_hasta) amb
    WHERE  i.activo = 1;
    CREATE CLUSTERED INDEX ix_centro_ind_mes ON #centro_ind_mes (id_indicador, codcentro, mes);

    /* 2.3 Valor de cada término en cada mes calculado: MENSUAL = valor del mes; ACUMULADO = enero..mes, sin los meses
           excluidos / no vigentes / fuera del ámbito (su aporte es 0). Cada centro lleva todos los términos que tuvo en
           el año (enero..corte), aunque ese mes no tenga dato. */
    SELECT l.id_indicador, l.codcentro, l.letra, l.mes, l.valor_mes,
           CASE WHEN n.excluido = 1 OR n.motivo_centro IS NOT NULL THEN 0 ELSE ISNULL(l.valor_mes, 0) END AS aporte
    INTO   #letra_aporte
    FROM   #letra_mes l
    LEFT JOIN #centro_ind_mes n ON n.id_indicador = l.id_indicador AND n.codcentro = l.codcentro AND n.mes = l.mes;
    CREATE CLUSTERED INDEX ix_letra_aporte ON #letra_aporte (id_indicador, codcentro, letra, mes);

    SELECT x.id_indicador, x.codcentro, x.mes, x.letra, x.valor_mes,
           CASE WHEN i.tipo_calculo = 'ACUMULADO' THEN ISNULL(x.acumulado, 0) ELSE x.valor_mes END AS valor
    INTO   #letra
    FROM  (SELECT g.id_indicador, g.codcentro, k.mes, g.letra,
                  MAX(CASE WHEN a.mes = k.mes THEN a.valor_mes END) AS valor_mes,
                  SUM(a.aporte) AS acumulado
           FROM  (SELECT DISTINCT id_indicador, codcentro, letra FROM #letra_mes) g
           CROSS JOIN #meses k
           LEFT JOIN #letra_aporte a ON a.id_indicador = g.id_indicador AND a.codcentro = g.codcentro AND a.letra = g.letra
                                    AND a.mes <= k.mes
           GROUP BY g.id_indicador, g.codcentro, k.mes, g.letra) x
    JOIN   dbo.tmi_indicador i ON i.id = x.id_indicador;
    CREATE CLUSTERED INDEX ix_letra ON #letra (id_indicador, codcentro, letra, mes);

    -- datos del indicador en el año (enero..mes): 0 = el centro no reportó ninguno de los términos (SIN_DATOS_ANIO)
    SELECT d.id_indicador, d.codcentro, k.mes, SUM(d.datos) AS datos_anio
    INTO   #datos_anio
    FROM  (SELECT id_indicador, codcentro, mes, SUM(ABS(ISNULL(valor_mes, 0))) AS datos
           FROM #letra_mes GROUP BY id_indicador, codcentro, mes) d
    JOIN   #meses k ON d.mes <= k.mes
    GROUP BY d.id_indicador, d.codcentro, k.mes;
    CREATE CLUSTERED INDEX ix_datos_anio ON #datos_anio (id_indicador, codcentro, mes);

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
               ese mes). Por seguridad se comprueba que no tenga otra cosa antes de ejecutarla. Una sola vez por
               indicador: #letra_piv trae todos los meses calculados. */
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

    /* 2.6 Estándar y puntaje de cada mes calculado -> #res_all (el valor es el de la fórmula, sin reglas de ceros);
           #res = el mes de corte: una fila por periodo de corte, indicador y centro. Cada mes lleva
           los centros visibles en ese mes. */
    CREATE TABLE #res_all (id_indicador INT, codcentro INT, mes INT, valor FLOAT, estandar FLOAT, verde FLOAT,
                           acept FLOAT, aceptmenos FLOAT, puntaje VARCHAR(2), motivo_na VARCHAR(30), visible INT);
    WITH malla AS (
        SELECT c.codcentro, c.red, c.tipo, c.nivel, c.nivel_estandar, c.categoria, c.motivo_centro, c.excluido, c.excl_resultado, c.mes,
               i.id, i.sin_datos_anio, i.sentido,
               i.decimales, i.cero_es_logro, i.mostrar_no_aplica
        FROM #centro_ind_mes c
        JOIN #meses k ON k.mes = c.mes
        JOIN #centro_vig cv ON cv.codcentro = c.codcentro AND cv.mes = c.mes AND ISNULL(cv.flag, 1) <> 0
        JOIN dbo.tmi_indicador i ON i.id = c.id_indicador
    ),
    est AS (
        SELECT g.*,
               /* centro sin ningún dato del indicador en el año: con sin_datos_anio = MOSTRAR se reporta 0 (no queda en
                  #num_den porque no tiene términos; sin esto caía en SIN_DATO = NA) */
               CASE WHEN d.valor IS NULL AND ISNULL(da.datos_anio, 0) = 0 AND g.sin_datos_anio = 'MOSTRAR'
                    THEN 0 ELSE d.valor END AS valor,
               -- datos del indicador en el año (enero..mes): 0 = el centro no reportó ninguno de los términos
               ISNULL(da.datos_anio, 0) AS datos_anio,
               -- estándar y % Acept del mes: regla única de fn_tmi_estandar (copiada en #est_ind)
               s.estandar, s.acept, s.aceptmenos
        FROM malla g
        LEFT JOIN #num_den d ON d.id_indicador = g.id AND d.codcentro = g.codcentro AND d.mes = g.mes
        LEFT JOIN #datos_anio da ON da.id_indicador = g.id AND da.codcentro = g.codcentro AND da.mes = g.mes
        LEFT JOIN #est_ind s ON s.id_indicador = g.id AND s.codcentro = g.codcentro AND s.mes = g.mes
    ),
    lim AS (
        SELECT v.*,
               v.estandar AS verde,
               ROUND(v.valor, ISNULL(v.decimales, 15)) AS valor_eval,
               CASE WHEN v.motivo_centro IS NOT NULL                         THEN v.motivo_centro
                    -- el usuario elige en la exclusión si el mes queda NA o con puntaje 0 (EXCLUIDO_CERO)
                    WHEN v.excluido = 1 AND v.excl_resultado = '0'           THEN 'EXCLUIDO_CERO'
                    WHEN v.excluido = 1                                      THEN 'EXCLUIDO'
                    WHEN v.estandar IS NULL                                  THEN 'SIN_ESTANDAR'
                    WHEN v.datos_anio = 0 AND v.sin_datos_anio <> 'MOSTRAR'  THEN 'SIN_DATOS_ANIO'
                    WHEN v.valor IS NULL                                     THEN 'SIN_DATO' END AS motivo_na
        FROM est v
    )
    INSERT INTO #res_all (id_indicador, codcentro, mes, valor, estandar, verde, acept, aceptmenos, puntaje, motivo_na, visible)
    SELECT l.id AS id_indicador, l.codcentro, l.mes,
           CASE WHEN l.motivo_na = 'EXCLUIDO_CERO' THEN 0 ELSE l.valor END AS valor, l.estandar, l.verde, l.acept, l.aceptmenos,
           CASE WHEN l.motivo_na = 'EXCLUIDO_CERO'             THEN '0'
                WHEN l.motivo_na IS NOT NULL                   THEN 'NA'
                WHEN l.valor_eval = 0 AND l.cero_es_logro = 0  THEN '0'
                WHEN l.sentido = 'BANDA' THEN
                     CASE WHEN l.valor_eval BETWEEN (l.verde + l.aceptmenos) / 2 AND (l.verde + l.acept) / 2 THEN '5'
                          WHEN l.valor_eval BETWEEN l.aceptmenos AND l.acept                                 THEN '3'
                          ELSE '1' END
                WHEN l.sentido = 'MAYOR' THEN CASE WHEN l.valor_eval >= l.verde THEN '5' WHEN l.valor_eval >= l.acept THEN '3' ELSE '1' END
                ELSE                          CASE WHEN l.valor_eval <= l.verde THEN '5' WHEN l.valor_eval <= l.acept THEN '3' ELSE '1' END
           END AS puntaje,
           l.motivo_na,
           -- visible = 0: el centro no se lista en la hoja del indicador (por defecto los NA sí se listan)
           CASE WHEN l.motivo_na = 'SIN_DATOS_ANIO' AND l.sin_datos_anio = 'OCULTAR'                  THEN 0
                WHEN l.motivo_na IN ('SIN_ESTANDAR', 'FUERA_DE_AMBITO') AND l.mostrar_no_aplica = 0  THEN 0
                ELSE 1 END AS visible
    FROM lim l;

    SELECT * INTO #res FROM #res_all WHERE mes = @mes;
    CREATE CLUSTERED INDEX ix_res ON #res (id_indicador, codcentro, mes);

    /* Resultado del mes: una fila por periodo de corte, indicador y centro (codcentro = código del centro, no el id de
       tmi_centro), con el valor y el puntaje de ese periodo. Cada periodo calculado guarda sus filas: al cerrar el año
       hay 12 periodos, y el valor de cada mes se lee de la fila de su periodo. */
    /* Desarrollo de la fórmula: la plantilla ([T1] - [T2]) / [T3] con el valor de cada término que entró en la
       fórmula, y el resultado: (135 - 20) / 160 = 0.7188. Solo donde la fórmula se calculó. */
    SELECT r.id_indicador, r.codcentro, CAST(i.formula_plantilla AS NVARCHAR(4000)) AS txt, i.si_variable_nula, n.valor
    INTO   #des
    FROM   #res r
    JOIN   dbo.tmi_indicador i ON i.id = r.id_indicador
    JOIN   #num_den n ON n.id_indicador = r.id_indicador AND n.codcentro = r.codcentro AND n.mes = @mes
    WHERE  i.formula_plantilla IS NOT NULL;
    DECLARE @cod VARCHAR(5);
    DECLARE cdes CURSOR LOCAL FAST_FORWARD FOR SELECT DISTINCT codigo FROM #termino;
    OPEN cdes; FETCH NEXT FROM cdes INTO @cod;
    WHILE @@FETCH_STATUS = 0
    BEGIN
        UPDATE x
        SET    x.txt = REPLACE(x.txt, '[' + @cod + ']',
                               COALESCE(dbo.fn_tmi_num(l.valor), CASE WHEN x.si_variable_nula = 'NA' THEN 'sin dato' ELSE '0' END))
        FROM   #des x
        LEFT JOIN #letra l ON l.id_indicador = x.id_indicador AND l.codcentro = x.codcentro AND l.letra = @cod AND l.mes = @mes
        WHERE  CHARINDEX('[' + @cod + ']', x.txt) > 0;
        FETCH NEXT FROM cdes INTO @cod;
    END
    CLOSE cdes; DEALLOCATE cdes;

    /* Resultados en tablas temporales: se guardan (BACKUP) o se devuelven (tiempo real) al final */
    SELECT @PERIODO AS periodo_corte, CAST(@ORIGEN AS VARCHAR(10)) AS origen_datos, r.id_indicador, r.codcentro, r.valor,
           r.estandar, r.verde, r.acept, r.aceptmenos, r.puntaje, r.motivo_na, CAST(r.visible AS BIT) AS visible,
           CASE WHEN @ORIGEN = 'BACKUP' THEN @PERIODO END AS periodo_backup, i.tipo_calculo, i.formula_alias, i.formula,
           CAST(LEFT(x.txt + N' = ' + ISNULL(dbo.fn_tmi_num(x.valor), N'NA'), 4000) AS NVARCHAR(4000)) AS formula_desarrollo,
           @USUARIO AS usuario_calculo, GETDATE() AS fecha_calculo
    INTO #out_res
    FROM #res r
    JOIN dbo.tmi_indicador i ON i.id = r.id_indicador
    LEFT JOIN #des x ON x.id_indicador = r.id_indicador AND x.codcentro = r.codcentro;

    /* Valor de cada término (grupo, actividad y servicio) con el que se calculó: donde la fórmula se calculó */
    SELECT @PERIODO AS periodo_corte, CAST(@ORIGEN AS VARCHAR(10)) AS origen_datos, r.id_indicador, r.codcentro, t.codigo,
           t.tipgrupo, t.actividad, t.servicio, t.mediana, t.texto,
           dm.valor_mes,
           CASE WHEN i.tipo_calculo = 'ACUMULADO' THEN ac.valor ELSE dm.valor_mes END AS valor,
           dm.filas AS filas_mes,
           CASE WHEN i.tipo_calculo = 'ACUMULADO' THEN ac.filas ELSE dm.filas END AS filas
    INTO   #out_term
    FROM   #res r
    JOIN   #num_den n ON n.id_indicador = r.id_indicador AND n.codcentro = r.codcentro AND n.mes = @mes
    JOIN   dbo.tmi_indicador i ON i.id = r.id_indicador
    JOIN   dbo.tmi_indicador_termino t ON t.id_indicador = r.id_indicador
    LEFT JOIN #det_mes dm ON dm.id_indicador = r.id_indicador AND dm.codcentro = r.codcentro AND dm.codigo = t.codigo
                         AND dm.tipgrupo = t.tipgrupo AND dm.actividad = t.actividad AND dm.mes = @mes
                         AND (dm.servicio_def = t.servicio OR (dm.servicio_def IS NULL AND t.servicio IS NULL))
    -- acumulado enero..corte de cada parte del término (sin los meses excluidos / no vigentes / fuera del ámbito)
    LEFT JOIN (
        SELECT d2.id_indicador, d2.codcentro, d2.codigo, d2.tipgrupo, d2.actividad, d2.servicio_def,
               SUM(CASE WHEN n2.excluido = 1 OR n2.motivo_centro IS NOT NULL THEN 0 ELSE d2.valor_mes END) AS valor,
               SUM(CASE WHEN n2.excluido = 1 OR n2.motivo_centro IS NOT NULL THEN 0 ELSE d2.filas END) AS filas
        FROM #det_mes d2
        LEFT JOIN #centro_ind_mes n2 ON n2.id_indicador = d2.id_indicador AND n2.codcentro = d2.codcentro AND n2.mes = d2.mes
        WHERE d2.mes <= @mes
        GROUP BY d2.id_indicador, d2.codcentro, d2.codigo, d2.tipgrupo, d2.actividad, d2.servicio_def
    ) ac ON ac.id_indicador = r.id_indicador AND ac.codcentro = r.codcentro AND ac.codigo = t.codigo
        AND ac.tipgrupo = t.tipgrupo AND ac.actividad = t.actividad
        AND (ac.servicio_def = t.servicio OR (ac.servicio_def IS NULL AND t.servicio IS NULL));

    /* Valores de los meses del año para periodo_01..periodo_12: todos del cálculo de ahora (#res_all). */
    CREATE TABLE #hist (id_indicador INT, codcentro INT, mes INT, valor FLOAT, estandar FLOAT, acept FLOAT,
                        aceptmenos FLOAT, puntaje VARCHAR(2), motivo_na VARCHAR(30), visible INT);
    INSERT INTO #hist (id_indicador, codcentro, mes, valor, estandar, acept, aceptmenos, puntaje, motivo_na, visible)
    SELECT id_indicador, codcentro, mes, valor, estandar, acept, aceptmenos, puntaje, motivo_na, visible FROM #res_all;
    CREATE CLUSTERED INDEX ix_hist ON #hist (id_indicador, codcentro, mes);

    /* 2.7 Resultado final por indicador (filas del Excel), del origen de los datos pedido. */
    SELECT @PERIODO AS periodo, @anio AS anio, r.id_indicador, MIN(c.id_centro) AS orden, MIN(c.orden) AS orden_red,
           MAX(c.red) AS red, r.codcentro, MAX(c.centro) AS centro, MAX(c.nivel) AS nivel,
           MAX(c.nivel_estandar) AS nivel_estandar, MAX(c.tipo) AS tipo, MAX(c.categoria) AS categoria,
           MAX(CASE WHEN r.mes = @mes THEN r.estandar END) AS estandar,
           MAX(CASE WHEN r.mes = @mes THEN r.acept END) AS acept,
           MAX(CASE WHEN r.mes = @mes THEN r.aceptmenos END) AS aceptmenos,
           MAX(CASE WHEN r.mes = @mes THEN CASE WHEN r.puntaje = 'NA' THEN r.valor ELSE ISNULL(r.valor, 0) END END) AS total,
           MAX(CASE WHEN r.mes = @mes THEN r.puntaje END) AS puntaje,
           MAX(CASE WHEN r.mes = @mes THEN r.motivo_na END) AS motivo_na,
           CAST(MAX(CASE WHEN r.mes = @mes THEN CAST(r.visible AS INT) END) AS BIT) AS visible,
           CAST(@ORIGEN AS VARCHAR(10)) AS origen_datos, CASE WHEN @ORIGEN = 'BACKUP' THEN @PERIODO END AS periodo_backup,
           CASE WHEN 1 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 1 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END AS periodo_01,
           CASE WHEN 2 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 2 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END AS periodo_02,
           CASE WHEN 3 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 3 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END AS periodo_03,
           CASE WHEN 4 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 4 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END AS periodo_04,
           CASE WHEN 5 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 5 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END AS periodo_05,
           CASE WHEN 6 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 6 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END AS periodo_06,
           CASE WHEN 7 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 7 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END AS periodo_07,
           CASE WHEN 8 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 8 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END AS periodo_08,
           CASE WHEN 9 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 9 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END AS periodo_09,
           CASE WHEN 10 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 10 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END AS periodo_10,
           CASE WHEN 11 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 11 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END AS periodo_11,
           CASE WHEN 12 > @mes THEN 0 ELSE MAX(CASE WHEN r.mes = 12 THEN CASE WHEN r.motivo_na IN ('EXCLUIDO', 'NO_VIGENTE_MES', 'FUERA_DE_AMBITO') THEN NULL ELSE ISNULL(r.valor, 0) END END) END AS periodo_12,
           GETDATE() AS fecha_calculo
    INTO #out_final
    FROM #hist r
    JOIN #centro c ON c.codcentro = r.codcentro
    GROUP BY r.id_indicador, r.codcentro
    HAVING MAX(CASE WHEN r.mes = @mes THEN 1 END) = 1;

    BEGIN
        -- 1) final por centro  2) resultado del mes de corte  3) términos  4) valor y puntaje de cada mes
        SELECT * FROM #out_final;
        SELECT * FROM #out_res;
        SELECT * FROM #out_term;
        SELECT @anio * 100 + mes AS periodo_corte, id_indicador, codcentro, mes, valor, estandar, acept, aceptmenos,
               puntaje, motivo_na, visible
        FROM #res_all;
    END
    END TRY
    BEGIN CATCH
        DECLARE @error NVARCHAR(4000) = ERROR_MESSAGE(), @num INT = ERROR_NUMBER(), @linea INT = ERROR_LINE();
        IF @@TRANCOUNT > 0 ROLLBACK;
        -- RAISERROR y no THROW (compatibilidad con servidores anteriores a 2012). Los mensajes propios (50000) pasan
        -- igual; los de SQL Server van marcados [TMI-INTERNO]: el backend los deja en el log y no los muestra.
        IF @num = 50000
            RAISERROR('%s', 16, 1, @error);
        ELSE
            RAISERROR('[TMI-INTERNO] Error %d en la línea %d de usp_tmi_calcular: %s', 16, 1, @num, @linea, @error);
    END CATCH
END
GO



/* =====================================================================================================================
   usp_tmi_avisos_config @PERIODO: avisos (no bloquean el cálculo) de configuración incompleta para el mes de corte,
   por indicador activo. Cuenta los centros que Calcular dejaría en NA por falta de configuración:
     - sin estándar (SIN_ESTANDAR): centro vigente en el mes, dentro del ámbito, no excluido y sin estándar en
       fn_tmi_estandar (no cuenta los que tienen "no aplica" en su estándar específico);
     - con estándar pero sin % Acept (sin puntaje 3).
   Misma regla de centros, ámbito y exclusiones que usp_tmi_calcular para el mes de corte.
   ===================================================================================================================== */
IF OBJECT_ID('dbo.usp_tmi_avisos_config', 'P') IS NULL
    EXEC(N'CREATE PROCEDURE dbo.usp_tmi_avisos_config AS RETURN 0');   -- luego ALTER
GO
ALTER PROCEDURE dbo.usp_tmi_avisos_config @PERIODO INT
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @anio INT, @mes INT;
    SET @anio = @PERIODO / 100;
    SET @mes = @PERIODO % 100;

    SELECT c.codcentro, MAX(c.red) AS red, MAX(c.categoria) AS categoria, MAX(c.nivel) AS nivel,
           MAX(c.nivel_estandar) AS nivel_estandar,
           MAX(CAST(CASE @mes WHEN 1 THEN c.f01 WHEN 2 THEN c.f02 WHEN 3 THEN c.f03 WHEN 4 THEN c.f04 WHEN 5 THEN c.f05
                              WHEN 6 THEN c.f06 WHEN 7 THEN c.f07 WHEN 8 THEN c.f08 WHEN 9 THEN c.f09 WHEN 10 THEN c.f10
                              WHEN 11 THEN c.f11 WHEN 12 THEN c.f12 END AS INT)) AS vigente
    INTO   #centro
    FROM   dbo.vw_tmi_centro_base c
    WHERE  c.anio = @anio
       OR (c.anio IS NULL AND NOT EXISTS (SELECT 1 FROM dbo.vw_tmi_centro_base x WHERE x.anio = @anio))
    GROUP BY c.codcentro;

    SELECT * INTO #est FROM dbo.fn_tmi_estandar(@PERIODO);
    SELECT * INTO #excl FROM dbo.fn_tmi_exclusion(@PERIODO) WHERE mes = @mes;

    SELECT i.id AS id_indicador, i.codigo, i.indicador, i.mostrar_no_aplica,
           SUM(CASE WHEN s.estandar IS NULL AND ISNULL(s.aplica_centro, 1) <> 0 THEN 1 ELSE 0 END) AS sin_estandar,
           SUM(CASE WHEN s.estandar IS NOT NULL AND s.acept IS NULL THEN 1 ELSE 0 END) AS sin_acept
    INTO   #conteo
    FROM   dbo.tmi_indicador i
    JOIN   #centro c ON c.vigente = 1
    LEFT JOIN #est s ON s.id_indicador = i.id AND s.codcentro = c.codcentro
    OUTER APPLY (SELECT MAX(CASE WHEN a.incluir = 1 THEN 1 ELSE 0 END)                AS lista_blanca,
                        MAX(CASE WHEN a.incluir = 1 AND k.coincide = 1 THEN 1 ELSE 0 END) AS incluido,
                        MAX(CASE WHEN a.incluir = 0 AND k.coincide = 1 THEN 1 ELSE 0 END) AS excluido
                 FROM dbo.tmi_indicador_ambito a
                 CROSS APPLY (SELECT CASE WHEN (a.red IS NULL OR a.red = c.red) AND (a.nivel IS NULL OR a.nivel IN (c.nivel, c.nivel_estandar))
                                           AND (a.categoria IS NULL OR a.categoria = c.categoria)
                                           AND (a.tipo IS NULL OR a.tipo = c.nivel_estandar)
                                           AND (a.codcentro IS NULL OR a.codcentro = c.codcentro) THEN 1 ELSE 0 END AS coincide) k
                 WHERE a.id_indicador = i.id AND @PERIODO BETWEEN a.periodo_desde AND a.periodo_hasta) amb
    WHERE  i.activo = 1
      -- sin filas de ámbito, el MAX da NULL: todos los centros (ISNULL, como el CASE de usp_tmi_calcular)
      AND  NOT ((ISNULL(amb.lista_blanca, 0) = 1 AND ISNULL(amb.incluido, 0) = 0) OR ISNULL(amb.excluido, 0) = 1)
      AND  NOT EXISTS (SELECT 1 FROM #excl x WHERE x.id_indicador = i.id AND x.codcentro = c.codcentro)
    GROUP BY i.id, i.codigo, i.indicador, i.mostrar_no_aplica;

    SELECT id_indicador, codigo AS elemento, indicador, sin_estandar AS centros,
           CAST(sin_estandar AS VARCHAR(10)) + ' centro(s) sin estándar: quedan NA'
           + CASE WHEN mostrar_no_aplica = 0 THEN ' y no se listan en el Excel' ELSE '' END AS aviso
    FROM   #conteo WHERE sin_estandar > 0
    UNION ALL
    SELECT id_indicador, codigo, indicador, sin_acept,
           CAST(sin_acept AS VARCHAR(10)) + ' centro(s) con estándar pero sin % Acept: no pueden obtener puntaje 3'
    FROM   #conteo WHERE sin_acept > 0
    ORDER BY id_indicador, centros DESC;
END
GO
