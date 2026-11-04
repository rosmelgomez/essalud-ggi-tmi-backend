/* =====================================================================================================
   Limpieza de estándares que el cálculo no usa
   -----------------------------------------------------------------------------------------------------
   Cada indicador se evalúa con su base_estandar (tmi_indicador.base_estandar) y el cálculo solo lee las
   claves de esa base (tmi_estandar: tipo_estandar + fuente + clave, activo = 1). Por ejemplo, Concentración
   de Consultas se evalúa por NIVEL: sus filas en tmi_estandar_tipo nunca se leen.

   Este script:
     1. Lista las filas de tmi_estandar_tipo / _nivel / _categoria que no son clave de la base de su indicador.
     2. Lista las reglas activas de tmi_indicador_estandar (cuarta fuente: el cálculo la usa cuando la tabla
        maestra tiene 0 o no tiene la clave, así un 0 no queda "sin estándar").
     3. Con @aplicar = 1: copia las filas a dbo.tmi_estandar_sin_uso_respaldo y las borra. Con
        @desactivar_reglas = 1 también pone activo = 0 en las reglas (no se borran). Todo en una transacción.
        Ojo con las reglas: si una clave usada tiene 0 en la tabla maestra, el cálculo toma la regla; al
        desactivarla, ese caso queda sin estándar. Revise la columna est_fijo antes.

   Uso: ejecutar primero con @aplicar = 0 (solo muestra), revisar y luego con @aplicar = 1.
   Se puede volver a ejecutar: si no hay nada sin uso, no hace nada.
   Sin funciones de SQL Server 2012 (CONCAT, IIF, CHOOSE, THROW): el servidor tiene compatibilidad anterior.
   ===================================================================================================== */
SET NOCOUNT ON;

DECLARE @aplicar BIT = 0;            -- 0 = solo muestra lo que se quitaría | 1 = respalda y quita
DECLARE @desactivar_reglas BIT = 0;  -- 1 = además desactiva las reglas de tmi_indicador_estandar (con @aplicar = 1)

IF OBJECT_ID('tempdb..#sin_uso') IS NOT NULL DROP TABLE #sin_uso;
CREATE TABLE #sin_uso (
    tabla        VARCHAR(40)  NOT NULL,
    id           INT          NOT NULL,
    id_indicador INT          NULL,
    indicador    VARCHAR(300) NULL,
    base         VARCHAR(50)  NULL,
    clave        VARCHAR(50)  NULL,
    anio         INT          NULL,
    est_fijo     FLOAT        NULL,
    motivo       NVARCHAR(300) NOT NULL
);

/* ---------- 1. Filas de las tablas maestras que no son clave de la base de su indicador ---------- */
INSERT INTO #sin_uso (tabla, id, id_indicador, indicador, base, clave, anio, est_fijo, motivo)
SELECT 'tmi_estandar_tipo', t.id, t.id_indicador, i.indicador, i.base_estandar, LTRIM(RTRIM(t.tipo_centro)), t.anio, t.est_fijo,
       CASE WHEN i.id IS NULL THEN N'El indicador no existe'
            WHEN NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar e
                             WHERE e.tipo_estandar = i.base_estandar AND e.activo = 1 AND e.fuente = 'TIPO')
                 THEN N'Se evalúa por ' + ISNULL(i.base_estandar, '(sin base)') + N': no usa tipo'
            ELSE N'El tipo ' + LTRIM(RTRIM(t.tipo_centro)) + N' no es clave de ' + i.base_estandar END
FROM dbo.tmi_estandar_tipo t
LEFT JOIN dbo.tmi_indicador i ON i.id = t.id_indicador
WHERE NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar e
                  WHERE e.tipo_estandar = i.base_estandar AND e.activo = 1 AND e.fuente = 'TIPO'
                    AND LTRIM(RTRIM(e.clave)) = LTRIM(RTRIM(t.tipo_centro)));

INSERT INTO #sin_uso (tabla, id, id_indicador, indicador, base, clave, anio, est_fijo, motivo)
SELECT 'tmi_estandar_nivel', t.id, t.id_indicador, i.indicador, i.base_estandar, LTRIM(RTRIM(t.nivel_centro)), t.anio, t.est_fijo,
       CASE WHEN i.id IS NULL THEN N'El indicador no existe'
            WHEN NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar e
                             WHERE e.tipo_estandar = i.base_estandar AND e.activo = 1 AND e.fuente = 'NIVEL')
                 THEN N'Se evalúa por ' + ISNULL(i.base_estandar, '(sin base)') + N': no usa nivel'
            ELSE N'El nivel ' + LTRIM(RTRIM(t.nivel_centro)) + N' no es clave de ' + i.base_estandar END
FROM dbo.tmi_estandar_nivel t
LEFT JOIN dbo.tmi_indicador i ON i.id = t.id_indicador
WHERE NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar e
                  WHERE e.tipo_estandar = i.base_estandar AND e.activo = 1 AND e.fuente = 'NIVEL'
                    AND LTRIM(RTRIM(e.clave)) = LTRIM(RTRIM(t.nivel_centro)));

IF OBJECT_ID('dbo.tmi_estandar_categoria') IS NOT NULL
    INSERT INTO #sin_uso (tabla, id, id_indicador, indicador, base, clave, anio, est_fijo, motivo)
    SELECT 'tmi_estandar_categoria', t.id, t.id_indicador, i.indicador, i.base_estandar, LTRIM(RTRIM(t.categoria_centro)), t.anio, t.est_fijo,
           CASE WHEN i.id IS NULL THEN N'El indicador no existe'
                WHEN NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar e
                                 WHERE e.tipo_estandar = i.base_estandar AND e.activo = 1 AND e.fuente = 'CATEGORIA')
                     THEN N'Se evalúa por ' + ISNULL(i.base_estandar, '(sin base)') + N': no usa categoría'
                ELSE N'La categoría ' + LTRIM(RTRIM(t.categoria_centro)) + N' no es clave de ' + i.base_estandar END
    FROM dbo.tmi_estandar_categoria t
    LEFT JOIN dbo.tmi_indicador i ON i.id = t.id_indicador
    WHERE NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar e
                      WHERE e.tipo_estandar = i.base_estandar AND e.activo = 1 AND e.fuente = 'CATEGORIA'
                        AND LTRIM(RTRIM(e.clave)) = LTRIM(RTRIM(t.categoria_centro)));

/* ---------- 2. Reglas activas de tmi_indicador_estandar (cuarta fuente del estándar) ---------- */
IF OBJECT_ID('dbo.tmi_indicador_estandar') IS NOT NULL
    INSERT INTO #sin_uso (tabla, id, id_indicador, indicador, base, clave, anio, est_fijo, motivo)
    SELECT 'tmi_indicador_estandar', r.id, r.id_indicador, i.indicador, i.base_estandar,
           COALESCE(r.nivel, r.tipo, r.categoria, '(todos)'), r.periodo_desde / 100, r.estandar,
           N'Regla del panel: repite el estándar de las tablas maestras (se desactiva con @desactivar_reglas = 1, no se borra)'
    FROM dbo.tmi_indicador_estandar r
    LEFT JOIN dbo.tmi_indicador i ON i.id = r.id_indicador
    WHERE r.activo = 1;

/* ---------- Resumen y detalle ---------- */
SELECT tabla, motivo, COUNT(*) AS filas
FROM #sin_uso
GROUP BY tabla, motivo
ORDER BY tabla, motivo;

SELECT tabla, id, id_indicador, indicador, base, clave, anio, est_fijo, motivo
FROM #sin_uso
ORDER BY tabla, id_indicador, clave;

IF @aplicar = 0
BEGIN
    PRINT 'Modo revisión (@aplicar = 0): no se cambió nada. Revise las filas y vuelva a ejecutar con @aplicar = 1.';
    RETURN;
END;

IF @desactivar_reglas = 0 DELETE FROM #sin_uso WHERE tabla = 'tmi_indicador_estandar';

IF NOT EXISTS (SELECT 1 FROM #sin_uso)
BEGIN
    PRINT 'No hay estándares sin uso.';
    RETURN;
END;

/* ---------- 3. Respaldo y limpieza ---------- */
IF OBJECT_ID('dbo.tmi_estandar_sin_uso_respaldo') IS NULL
    CREATE TABLE dbo.tmi_estandar_sin_uso_respaldo (
        id_respaldo    INT IDENTITY(1,1) PRIMARY KEY,
        tabla          VARCHAR(40)  NOT NULL,
        id             INT          NOT NULL,
        id_indicador   INT          NULL,
        clave          VARCHAR(50)  NULL,
        anio           INT          NULL,
        est_fijo       FLOAT        NULL,
        est_01 FLOAT, est_02 FLOAT, est_03 FLOAT, est_04 FLOAT, est_05 FLOAT, est_06 FLOAT,
        est_07 FLOAT, est_08 FLOAT, est_09 FLOAT, est_10 FLOAT, est_11 FLOAT, est_12 FLOAT,
        motivo         NVARCHAR(300) NOT NULL,
        fecha_respaldo DATETIME     NOT NULL DEFAULT GETDATE()
    );

DECLARE @tipo INT, @nivel INT, @categoria INT, @reglas INT;

BEGIN TRY
    BEGIN TRANSACTION;

    INSERT INTO dbo.tmi_estandar_sin_uso_respaldo (tabla, id, id_indicador, clave, anio, est_fijo,
           est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, motivo)
    SELECT s.tabla, t.id, t.id_indicador, s.clave, t.anio, t.est_fijo,
           t.est_01, t.est_02, t.est_03, t.est_04, t.est_05, t.est_06, t.est_07, t.est_08, t.est_09, t.est_10, t.est_11, t.est_12, s.motivo
    FROM #sin_uso s JOIN dbo.tmi_estandar_tipo t ON t.id = s.id
    WHERE s.tabla = 'tmi_estandar_tipo';
    DELETE t FROM dbo.tmi_estandar_tipo t JOIN #sin_uso s ON s.tabla = 'tmi_estandar_tipo' AND s.id = t.id;
    SET @tipo = @@ROWCOUNT;

    INSERT INTO dbo.tmi_estandar_sin_uso_respaldo (tabla, id, id_indicador, clave, anio, est_fijo,
           est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, motivo)
    SELECT s.tabla, t.id, t.id_indicador, s.clave, t.anio, t.est_fijo,
           t.est_01, t.est_02, t.est_03, t.est_04, t.est_05, t.est_06, t.est_07, t.est_08, t.est_09, t.est_10, t.est_11, t.est_12, s.motivo
    FROM #sin_uso s JOIN dbo.tmi_estandar_nivel t ON t.id = s.id
    WHERE s.tabla = 'tmi_estandar_nivel';
    DELETE t FROM dbo.tmi_estandar_nivel t JOIN #sin_uso s ON s.tabla = 'tmi_estandar_nivel' AND s.id = t.id;
    SET @nivel = @@ROWCOUNT;

    SET @categoria = 0;
    IF OBJECT_ID('dbo.tmi_estandar_categoria') IS NOT NULL
    BEGIN
        INSERT INTO dbo.tmi_estandar_sin_uso_respaldo (tabla, id, id_indicador, clave, anio, est_fijo,
               est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, motivo)
        SELECT s.tabla, t.id, t.id_indicador, s.clave, t.anio, t.est_fijo,
               t.est_01, t.est_02, t.est_03, t.est_04, t.est_05, t.est_06, t.est_07, t.est_08, t.est_09, t.est_10, t.est_11, t.est_12, s.motivo
        FROM #sin_uso s JOIN dbo.tmi_estandar_categoria t ON t.id = s.id
        WHERE s.tabla = 'tmi_estandar_categoria';
        DELETE t FROM dbo.tmi_estandar_categoria t JOIN #sin_uso s ON s.tabla = 'tmi_estandar_categoria' AND s.id = t.id;
        SET @categoria = @@ROWCOUNT;
    END;

    SET @reglas = 0;
    IF OBJECT_ID('dbo.tmi_indicador_estandar') IS NOT NULL
    BEGIN
        UPDATE r SET activo = 0
        FROM dbo.tmi_indicador_estandar r JOIN #sin_uso s ON s.tabla = 'tmi_indicador_estandar' AND s.id = r.id;
        SET @reglas = @@ROWCOUNT;
    END;

    COMMIT TRANSACTION;

    PRINT 'Respaldo en dbo.tmi_estandar_sin_uso_respaldo.';
    PRINT 'Borradas: tmi_estandar_tipo ' + CAST(@tipo AS VARCHAR(10)) + ', tmi_estandar_nivel ' + CAST(@nivel AS VARCHAR(10))
        + ', tmi_estandar_categoria ' + CAST(@categoria AS VARCHAR(10)) + '.';
    PRINT 'Reglas de tmi_indicador_estandar desactivadas: ' + CAST(@reglas AS VARCHAR(10)) + '.';
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
    DECLARE @msg NVARCHAR(2048);
    SET @msg = N'No se aplicó la limpieza: ' + ERROR_MESSAGE();
    RAISERROR(@msg, 16, 1);
END CATCH;

/* ---------- Para deshacer (si hiciera falta) ----------
-- Volver a activar las reglas:
--   UPDATE dbo.tmi_indicador_estandar SET activo = 1 WHERE id IN (SELECT id FROM dbo.tmi_estandar_sin_uso_respaldo ...);
--   (las reglas no se copian al respaldo: basta con volver a poner activo = 1)
-- Devolver filas borradas, por ejemplo de tipo:
--   INSERT INTO dbo.tmi_estandar_tipo (id_indicador, tipo_centro, anio, est_fijo, est_01, ..., est_12)
--   SELECT id_indicador, clave, anio, est_fijo, est_01, ..., est_12
--   FROM dbo.tmi_estandar_sin_uso_respaldo WHERE tabla = 'tmi_estandar_tipo';
*/
