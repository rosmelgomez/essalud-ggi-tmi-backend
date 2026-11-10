/* Historial de cambios de la configuración del TMI: quién cambió qué y cuándo (fórmula, estándares, % Acept,
   exclusiones, ámbito, variables...).

   Un trigger AFTER INSERT, UPDATE, DELETE por tabla de configuración escribe en dbo.tmi_config_historial (la crea el
   backend desde src/main/model/historialModel.py) una fila por registro que cambió, con la fila antes y después en XML.
   - usuario: el del token, que el backend pone en CONTEXT_INFO al tomar una conexión del pool
     (src/main/db/auditoria.py); si el cambio no vino de la API (SSMS, scripts), el login de SQL Server.
   - No guarda las columnas de auditoría ni formula_sql / formula_plantilla (se derivan de la fórmula), y descarta los UPDATE que no
     cambiaron nada (por ejemplo, al volver a generar formula_sql al iniciar).
   Los triggers se generan desde sys.columns: si se agrega una columna a una tabla, al reiniciar el backend el
   trigger la incluye. Compatible con SQL Server 2008 R2 (FOR XML, sin STRING_AGG ni JSON). */

IF OBJECT_ID('dbo.tmi_config_historial', 'U') IS NULL
    RAISERROR('Falta dbo.tmi_config_historial: la crea el backend al iniciar (historialModel.py).', 16, 1);
GO

DECLARE @tablas TABLE (tabla SYSNAME PRIMARY KEY);
INSERT INTO @tablas (tabla) VALUES
    ('tmi_indicador'), ('tmi_indicador_estandar'), ('tmi_indicador_tolerancia'), ('tmi_indicador_ambito'),
    ('tmi_centro_estandar'), ('tmi_exclusion_centro_indicador'),
    ('tmi_estandar_tipo'), ('tmi_estandar_nivel'), ('tmi_estandar_categoria'), ('tmi_estandar'), ('tmi_tipo_estandar'),
    ('tmi_variable'), ('tmi_variable_logica'), ('tmi_variable_componente'), ('tmi_centro');

/* Plantilla del trigger: {TABLA}, {IND} (columna del indicador) y {COLS} se reemplazan por tabla */
DECLARE @plantilla NVARCHAR(MAX) = N'{ACCION} TRIGGER dbo.[tr_hist_{TABLA}] ON dbo.[{TABLA}]
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;
    IF NOT EXISTS (SELECT 1 FROM inserted) AND NOT EXISTS (SELECT 1 FROM deleted) RETURN;
    DECLARE @usuario VARCHAR(128);
    SET @usuario = NULLIF(LTRIM(RTRIM(REPLACE(CAST(CONTEXT_INFO() AS VARCHAR(128)) COLLATE Latin1_General_BIN, CHAR(0), ''''))), '''');
    INSERT INTO dbo.tmi_config_historial (usuario, tabla, id_registro, id_indicador, accion, antes, despues)
    SELECT ISNULL(@usuario, SUSER_SNAME()), ''{TABLA}'', h.id_registro, h.id_indicador, h.accion, h.antes, h.despues
    FROM  (SELECT COALESCE(i.id, d.id) AS id_registro, {IND} AS id_indicador,
                  CASE WHEN d.id IS NULL THEN ''ALTA'' WHEN i.id IS NULL THEN ''BAJA'' ELSE ''CAMBIO'' END AS accion,
                  CAST((SELECT {COLS} FROM deleted x WHERE x.id = d.id FOR XML RAW(''fila'')) AS NVARCHAR(MAX)) AS antes,
                  CAST((SELECT {COLS} FROM inserted x WHERE x.id = i.id FOR XML RAW(''fila'')) AS NVARCHAR(MAX)) AS despues
           FROM inserted i
           FULL JOIN deleted d ON d.id = i.id) h
    WHERE h.antes IS NULL OR h.despues IS NULL OR h.antes <> h.despues;
END';

DECLARE @tabla SYSNAME, @ind NVARCHAR(200), @cols NVARCHAR(MAX), @sql NVARCHAR(MAX);
DECLARE cur CURSOR LOCAL FAST_FORWARD FOR
    SELECT t.tabla FROM @tablas t
    WHERE OBJECT_ID(N'dbo.' + t.tabla, 'U') IS NOT NULL AND COL_LENGTH(N'dbo.' + t.tabla, 'id') IS NOT NULL;
OPEN cur;
FETCH NEXT FROM cur INTO @tabla;
WHILE @@FETCH_STATUS = 0
BEGIN
    SET @ind = CASE WHEN @tabla = 'tmi_indicador' THEN N'COALESCE(i.id, d.id)'
                    WHEN COL_LENGTH(N'dbo.' + @tabla, 'id_indicador') IS NOT NULL THEN N'COALESCE(i.id_indicador, d.id_indicador)'
                    WHEN COL_LENGTH(N'dbo.' + @tabla, 'id_estandar') IS NOT NULL THEN N'COALESCE(i.id_estandar, d.id_estandar)'
                    ELSE N'CAST(NULL AS INT)' END;
    -- text/ntext/image no se pueden leer en inserted/deleted
    SET @cols = STUFF((SELECT N', x.' + QUOTENAME(c.name)
                       FROM sys.columns c JOIN sys.types ty ON ty.user_type_id = c.user_type_id
                       WHERE c.object_id = OBJECT_ID(N'dbo.' + @tabla)
                         AND ty.name NOT IN ('text', 'ntext', 'image', 'timestamp')
                         AND c.name NOT IN ('usuario_creacion', 'fecha_creacion', 'usuario_modificacion', 'fecha_modificacion', 'formula_sql', 'formula_plantilla')
                       ORDER BY c.column_id
                       FOR XML PATH('')), 1, 2, N'');
    SET @sql = REPLACE(REPLACE(REPLACE(REPLACE(@plantilla,
                   N'{ACCION}', CASE WHEN OBJECT_ID(N'dbo.tr_hist_' + @tabla, 'TR') IS NULL THEN N'CREATE' ELSE N'ALTER' END),
                   N'{TABLA}', @tabla), N'{IND}', @ind), N'{COLS}', @cols);
    EXEC (@sql);
    FETCH NEXT FROM cur INTO @tabla;
END
CLOSE cur;
DEALLOCATE cur;
GO
