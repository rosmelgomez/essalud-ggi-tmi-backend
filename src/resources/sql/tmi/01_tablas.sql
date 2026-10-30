/* =====================================================================================================
   TMI DINAMICO - 01 TABLAS
   Se ejecuta en cada arranque (ver src/main/db/sqlRunner.py): todo es idempotente.
   Marcadores que reemplaza el ejecutor: {{TMI_DB}}, {{TOTALIZADO3}}, {{DIM}}
   ===================================================================================================== */

/* ---------- Parte 1. Variables: cómo se construye cada variable desde TOTALIZADO3 ---------- */
IF OBJECT_ID('dbo.tmi_variable') IS NULL
CREATE TABLE dbo.tmi_variable (
    id                   INT IDENTITY(1,1) PRIMARY KEY,
    nombre               VARCHAR(200) NOT NULL UNIQUE,
    descripcion          VARCHAR(200) NULL,
    agregacion           VARCHAR(10)  NOT NULL DEFAULT 'SUMA',         -- SUMA | MEDIANA (cálculo de la variable)
    total_anual          VARCHAR(15)  NOT NULL DEFAULT 'SUMA_MESES',   -- SUMA_MESES | MEDIANA_PERIODO (solo MEDIANA)
    activo               BIT NOT NULL DEFAULT 1,
    usuario_creacion     VARCHAR(200) NULL,
    fecha_creacion       DATETIME NOT NULL DEFAULT GETDATE(),
    usuario_modificacion VARCHAR(200) NULL,
    fecha_modificacion   DATETIME NULL
);
GO
-- Si la tabla ya existía con la versión de variables_calculo.sql (nombre, descripcion), se completan columnas
IF COL_LENGTH('dbo.tmi_variable', 'total_anual') IS NULL
    ALTER TABLE dbo.tmi_variable ADD total_anual VARCHAR(15) NOT NULL CONSTRAINT DF_tmi_variable_total DEFAULT 'SUMA_MESES';
IF COL_LENGTH('dbo.tmi_variable', 'agregacion') IS NULL
    ALTER TABLE dbo.tmi_variable ADD agregacion VARCHAR(10) NOT NULL CONSTRAINT DF_tmi_variable_agregacion DEFAULT 'SUMA';
IF COL_LENGTH('dbo.tmi_variable', 'activo') IS NULL
    ALTER TABLE dbo.tmi_variable ADD activo BIT NOT NULL CONSTRAINT DF_tmi_variable_activo DEFAULT 1;
IF COL_LENGTH('dbo.tmi_variable', 'usuario_creacion') IS NULL
    ALTER TABLE dbo.tmi_variable ADD usuario_creacion VARCHAR(200) NULL, fecha_creacion DATETIME NULL,
                                     usuario_modificacion VARCHAR(200) NULL, fecha_modificacion DATETIME NULL;
GO

IF OBJECT_ID('dbo.tmi_variable_logica') IS NULL
CREATE TABLE dbo.tmi_variable_logica (
    id             INT IDENTITY(1,1) PRIMARY KEY,
    id_variable    INT NOT NULL REFERENCES dbo.tmi_variable(id),
    tipgrupo       INT NOT NULL,                  -- DIM_GRUPO.tipgrupo
    actividad      INT NOT NULL,                  -- DIM_ACTIVIDAD.actividad
    servicio       INT NULL,                      -- TOTALIZADO3.servicio ; NULL = todos
    condicion_hoja VARCHAR(20) NULL,              -- DIM_HOJA.condicion ; NULL = todas
    periodo_desde  INT NOT NULL DEFAULT 200001,
    periodo_hasta  INT NOT NULL DEFAULT 999912,
    activo         BIT NOT NULL DEFAULT 1
);
GO

/* Variables compuestas: la variable suma, además de sus filas de lógica, el valor de otras variables (componentes).
   Ej.: Consolidado de Consultas = Consultas + Teleconsulta + CAI + ... (Generar_pivot.sql lo hacía con un OR).
   El cálculo abre los componentes en sus conjuntos (también los de componentes compuestos). */
IF OBJECT_ID('dbo.tmi_variable_componente') IS NULL
CREATE TABLE dbo.tmi_variable_componente (
    id                     INT IDENTITY(1,1) PRIMARY KEY,
    id_variable            INT NOT NULL CONSTRAINT FK_tmi_var_comp_variable REFERENCES dbo.tmi_variable(id),
    id_variable_componente INT NOT NULL CONSTRAINT FK_tmi_var_comp_componente REFERENCES dbo.tmi_variable(id),
    activo                 BIT NOT NULL DEFAULT 1,
    CONSTRAINT UX_tmi_variable_componente UNIQUE (id_variable, id_variable_componente),
    CONSTRAINT CK_tmi_variable_componente CHECK (id_variable <> id_variable_componente)
);
GO
IF COL_LENGTH('dbo.tmi_variable_logica', 'condicion_hoja') IS NULL
    ALTER TABLE dbo.tmi_variable_logica ADD
        condicion_hoja VARCHAR(20) NULL,
        periodo_desde  INT NOT NULL CONSTRAINT DF_tmi_vl_desde DEFAULT 200001,
        periodo_hasta  INT NOT NULL CONSTRAINT DF_tmi_vl_hasta DEFAULT 999912,
        activo         BIT NOT NULL CONSTRAINT DF_tmi_vl_activo DEFAULT 1;
GO

/* El cálculo (SUMA | MEDIANA) es de la variable y no de cada conjunto, como en Generar_pivot.sql.
   Migración de una sola vez: la variable toma MEDIANA si alguna de sus filas la tenía y se quita la columna de la lógica. */
IF COL_LENGTH('dbo.tmi_variable_logica', 'agregacion') IS NOT NULL
BEGIN
    EXEC('UPDATE v SET agregacion = ''MEDIANA'' FROM dbo.tmi_variable v
          WHERE EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.agregacion = ''MEDIANA'')');
    DECLARE @df SYSNAME = (SELECT d.name FROM sys.default_constraints d
                           JOIN sys.columns c ON c.object_id = d.parent_object_id AND c.column_id = d.parent_column_id
                           WHERE d.parent_object_id = OBJECT_ID('dbo.tmi_variable_logica') AND c.name = 'agregacion');
    IF @df IS NOT NULL EXEC('ALTER TABLE dbo.tmi_variable_logica DROP CONSTRAINT [' + @df + ']');
    EXEC('ALTER TABLE dbo.tmi_variable_logica DROP COLUMN agregacion');
END
GO
-- La mediana del periodo solo tiene sentido en una variable MEDIANA
IF OBJECT_ID('dbo.CK_tmi_variable_calculo') IS NULL
BEGIN
    UPDATE dbo.tmi_variable SET total_anual = 'SUMA_MESES' WHERE agregacion = 'SUMA' AND total_anual <> 'SUMA_MESES';
    ALTER TABLE dbo.tmi_variable ADD CONSTRAINT CK_tmi_variable_calculo
        CHECK (agregacion IN ('SUMA', 'MEDIANA') AND total_anual IN ('SUMA_MESES', 'MEDIANA_PERIODO')
               AND (agregacion = 'MEDIANA' OR total_anual = 'SUMA_MESES'));
END
GO

/* ---------- Parte 2. Indicadores definidos por el usuario ---------- */
IF OBJECT_ID('dbo.tmi_grupo') IS NULL
CREATE TABLE dbo.tmi_grupo (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    descripcion VARCHAR(200),
    visible     BIT,
    orden       INT NULL
);
GO
IF COL_LENGTH('dbo.tmi_grupo', 'orden') IS NULL ALTER TABLE dbo.tmi_grupo ADD orden INT NULL;
GO

IF OBJECT_ID('dbo.tmi_tipo_calculo') IS NULL
CREATE TABLE dbo.tmi_tipo_calculo (
    codigo      VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(200) NOT NULL
);
GO

IF OBJECT_ID('dbo.tmi_indicador') IS NULL
CREATE TABLE dbo.tmi_indicador (
    id                   INT IDENTITY(1,1) PRIMARY KEY,   -- = id_estandar de las tablas de estándar
    grupo                INT NULL REFERENCES dbo.tmi_grupo(id),
    indicador            VARCHAR(200),
    usuario_creacion     VARCHAR(200),
    usuario_modificacion VARCHAR(200),
    fecha_creacion       DATE,
    fecha_modificacion   DATE
);
GO
IF COL_LENGTH('dbo.tmi_indicador', 'codigo') IS NULL
    ALTER TABLE dbo.tmi_indicador ADD
        codigo              VARCHAR(20)  NULL,
        nombre_hoja         VARCHAR(31)  NULL,      -- nombre de la hoja (máx. 31, sin []:*?/\)
        titulo_hoja         VARCHAR(200) NULL,
        orden               INT          NULL,
        tipo_calculo        VARCHAR(20)  NULL,      -- tmi_tipo_calculo: MENSUAL | ACUMULADO
        sin_datos_anio      VARCHAR(7)   NOT NULL CONSTRAINT DF_tmi_ind_sindatos DEFAULT 'NA',      -- centro sin datos del indicador en el año: MOSTRAR (0) | NA | OCULTAR
        base_estandar       VARCHAR(10)  NULL,      -- TIPO | NIVEL | CATEGORIA | TIPO_NIVEL
        sentido             VARCHAR(5)   NULL,      -- MENOR | MAYOR | BANDA
        tipo_tolerancia     VARCHAR(3)   NULL,      -- REL | ABS
        tolerancia          FLOAT        NULL,
        decimales           INT          NULL,
        cero_es_logro       BIT          NOT NULL CONSTRAINT DF_tmi_ind_logro DEFAULT 0,
        mostrar_no_aplica   BIT          NOT NULL CONSTRAINT DF_tmi_ind_mostrar DEFAULT 1,
        activo              BIT          NOT NULL CONSTRAINT DF_tmi_ind_activo DEFAULT 1;
GO

-- % Acept hacia abajo en los indicadores de banda (NULL = el mismo porcentaje que hacia arriba)
IF COL_LENGTH('dbo.tmi_indicador', 'tolerancia_menos') IS NULL
    ALTER TABLE dbo.tmi_indicador ADD tolerancia_menos FLOAT NULL;
GO

/* Fórmula del indicador con términos de TOTALIZADO3, como la columna de fórmulas de TMI_SQL:
     ([3;50#0] - [3;49#0]) / [3;47#0]        [grupo;actividad#servicio], #0 = todos; MEDIANA([..]) para recursos
   El backend la analiza (src/main/core/tmiFormula.py) y guarda sus términos en tmi_indicador_termino (T1, T2...) y la
   expresión SQL sobre esos códigos en formula_sql. Reemplaza al numerador/denominador por letras y a sus reglas. */
IF COL_LENGTH('dbo.tmi_indicador', 'formula') IS NULL
    ALTER TABLE dbo.tmi_indicador ADD formula NVARCHAR(2000) NULL, formula_sql NVARCHAR(MAX) NULL;
GO
/* El usuario escribe la fórmula con letras: formula_alias = (A - B) / C, y la variable de cada letra
   en tmi_indicador_variable (una variable por letra). formula (términos) se genera desde ellas. */
IF COL_LENGTH('dbo.tmi_indicador', 'formula_alias') IS NULL
    ALTER TABLE dbo.tmi_indicador ADD formula_alias NVARCHAR(500) NULL;
GO
DECLARE @col SYSNAME, @df SYSNAME;
DECLARE c CURSOR LOCAL FAST_FORWARD FOR
    SELECT c.name FROM sys.columns c
    WHERE  c.object_id = OBJECT_ID('dbo.tmi_indicador')
      AND  c.name IN ('expr_numerador', 'expr_denominador', 'factor', 'den_cero', 'num_cero_na', 'cero_si_letra_mes_0');
OPEN c;
FETCH NEXT FROM c INTO @col;
WHILE @@FETCH_STATUS = 0
BEGIN
    SET @df = (SELECT d.name FROM sys.default_constraints d
               JOIN sys.columns x ON x.object_id = d.parent_object_id AND x.column_id = d.parent_column_id
               WHERE d.parent_object_id = OBJECT_ID('dbo.tmi_indicador') AND x.name = @col);
    IF @df IS NOT NULL EXEC ('ALTER TABLE dbo.tmi_indicador DROP CONSTRAINT [' + @df + ']');
    EXEC ('ALTER TABLE dbo.tmi_indicador DROP COLUMN [' + @col + ']');
    FETCH NEXT FROM c INTO @col;
END
CLOSE c; DEALLOCATE c;
GO
-- Términos de la fórmula: una fila por término y servicio (servicio NULL = todos los servicios)
IF OBJECT_ID('dbo.tmi_indicador_termino') IS NULL
CREATE TABLE dbo.tmi_indicador_termino (
    id           INT IDENTITY(1,1) PRIMARY KEY,
    id_indicador INT NOT NULL REFERENCES dbo.tmi_indicador(id),
    codigo       VARCHAR(5)  NOT NULL,          -- T1, T2... (columna de la fórmula en formula_sql)
    tipgrupo     INT NOT NULL,
    actividad    INT NOT NULL,
    servicio     INT NULL,
    mediana      BIT NOT NULL DEFAULT 0,        -- 1 = MEDIANA([..]): mediana de cada servicio en el mes, sumada
    texto        VARCHAR(60) NOT NULL           -- [g;a#s] como está en la fórmula
);
GO
-- Ampliar base_estandar para permitir combinaciones: TIPO, NIVEL, CATEGORIA, TIPO_NIVEL, TIPO_CATEGORIA, NIVEL_CATEGORIA, TIPO_NIVEL_CATEGORIA
IF COL_LENGTH('dbo.tmi_indicador', 'base_estandar') IS NOT NULL AND COL_LENGTH('dbo.tmi_indicador', 'base_estandar') < 30
    ALTER TABLE dbo.tmi_indicador ALTER COLUMN base_estandar VARCHAR(30) NULL;
GO

/* ---------- Tablas maestras de estándares ----------
   tmi_tipo_estandar : tipos de estándar (NIVEL, NIVEL_TIPO, TIPO, CATEGORIA). tmi_indicador.base_estandar -> codigo (FK).
   tmi_estandar      : claves de cada tipo; fuente = tabla de valores (tmi_estandar_nivel / _tipo / _categoria) y
                       clave = valor del centro en tmi_centro. Si un centro cumple dos claves del mismo tipo, gana la
                       de mayor prioridad (NIVEL_TIPO: los institutos toman su estándar por tipo y no por nivel).
   Los valores siguen en tmi_estandar_nivel / _tipo / _categoria. La carga inicial está en 03_datos.sql. */
IF OBJECT_ID('dbo.tmi_tipo_estandar') IS NULL
BEGIN
    CREATE TABLE dbo.tmi_tipo_estandar (
        id          INT IDENTITY(1,1) PRIMARY KEY,
        codigo      VARCHAR(30)  NOT NULL CONSTRAINT UX_tmi_tipo_estandar UNIQUE,
        descripcion VARCHAR(100) NOT NULL,
        orden       INT NULL,
        activo      BIT NOT NULL DEFAULT 1
    );
    -- Una sola vez, al crear el catálogo: Rendimiento Hora Médico y Rendimiento Hora Odontológica se evalúan por
    -- nivel, salvo los institutos (CNSR, IPO, INCOR), que van por tipo (002_TMI_CONSULTAS_VISTA.sql).
    EXEC (N'UPDATE dbo.tmi_indicador SET base_estandar = ''NIVEL_TIPO''
            WHERE codigo IN (''CE_RHrMedico'', ''O_HrOdont'') AND base_estandar = ''NIVEL''');
END
GO
IF OBJECT_ID('dbo.tmi_estandar') IS NULL
CREATE TABLE dbo.tmi_estandar (
    id            INT IDENTITY(1,1) PRIMARY KEY,
    tipo_estandar VARCHAR(30)  NOT NULL CONSTRAINT FK_tmi_estandar_tipo REFERENCES dbo.tmi_tipo_estandar (codigo),
    orden         INT NULL,
    fuente        VARCHAR(10)  NOT NULL CONSTRAINT CK_tmi_estandar_fuente CHECK (fuente IN ('NIVEL', 'TIPO', 'CATEGORIA')),
    clave         VARCHAR(50)  NOT NULL,
    descripcion   VARCHAR(100) NULL,
    prioridad     INT NOT NULL DEFAULT 1,
    activo        BIT NOT NULL DEFAULT 1,
    CONSTRAINT UX_tmi_estandar UNIQUE (tipo_estandar, fuente, clave)
);
GO

-- Formato de los valores en el Excel: NUMERO (0.00) o PORCENTAJE (0.00 %). Al agregar la columna se marcan
-- los indicadores porcentuales de la carga inicial (igual que en TMI_PLANTILLA.xlsx).
IF COL_LENGTH('dbo.tmi_indicador', 'formato') IS NULL
BEGIN
    ALTER TABLE dbo.tmi_indicador ADD formato VARCHAR(12) NOT NULL CONSTRAINT DF_tmi_indicador_formato DEFAULT 'NUMERO'
        CONSTRAINT CK_tmi_indicador_formato CHECK (formato IN ('NUMERO', 'PORCENTAJE'));
    EXEC (N'UPDATE dbo.tmi_indicador SET formato = ''PORCENTAJE'' WHERE codigo IN (''CE_GCHProg'', ''H_OCama'', ''H_TBMHosp'', ''Qx_IMenor'', ''Qx_IAlta'', ''Qx_GCHProg'', ''Qx_IntSusp'', ''Qx_HTCesareas'', ''Em_PrioIV_V'', ''Em_PrioI_II'', ''O_GCHOdon'')');
END
GO

IF OBJECT_ID('dbo.tmi_indicador_variable') IS NULL
CREATE TABLE dbo.tmi_indicador_variable (
    id           INT IDENTITY(1,1) PRIMARY KEY,
    id_indicador INT NOT NULL REFERENCES dbo.tmi_indicador(id),
    letra        CHAR(1) NOT NULL CHECK (letra LIKE '[A-Z]'),
    id_variable  INT NOT NULL REFERENCES dbo.tmi_variable(id),
    CONSTRAINT UX_tmi_indicador_variable UNIQUE (id_indicador, letra, id_variable)
);
GO

-- Qué centros entran a un indicador (unión por nivel, categoría, tipo, red, centro o combinación de ellos, y por periodo).
-- Sin filas = todos. incluir = 1 lista blanca, 0 lista negra.
IF OBJECT_ID('dbo.tmi_indicador_ambito') IS NULL
CREATE TABLE dbo.tmi_indicador_ambito (
    id            INT IDENTITY(1,1) PRIMARY KEY,
    id_indicador  INT NOT NULL REFERENCES dbo.tmi_indicador(id),
    red           VARCHAR(100) NULL,
    nivel         VARCHAR(50)  NULL,
    categoria     VARCHAR(50)  NULL,
    tipo          VARCHAR(50)  NULL,
    codcentro     INT          NULL,
    incluir       BIT NOT NULL DEFAULT 1,
    periodo_desde INT NOT NULL DEFAULT 200001,
    periodo_hasta INT NOT NULL DEFAULT 999912
);
GO
IF COL_LENGTH('dbo.tmi_indicador_ambito', 'nivel') IS NULL
    ALTER TABLE dbo.tmi_indicador_ambito ADD nivel VARCHAR(50) NULL;
IF COL_LENGTH('dbo.tmi_indicador_ambito', 'categoria') IS NULL
    ALTER TABLE dbo.tmi_indicador_ambito ADD categoria VARCHAR(50) NULL;
GO

-- Estándares del indicador por unión con centro (nivel, categoría, tipo o combinación de 2 o 3) y por periodo (AAAAMM)
IF OBJECT_ID('dbo.tmi_indicador_estandar') IS NULL
CREATE TABLE dbo.tmi_indicador_estandar (
    id            INT IDENTITY(1,1) PRIMARY KEY,
    id_indicador  INT NOT NULL REFERENCES dbo.tmi_indicador(id),
    nivel         VARCHAR(50) NULL,
    categoria     VARCHAR(50) NULL,
    tipo          VARCHAR(50) NULL,
    periodo_desde INT NOT NULL DEFAULT 200001,
    periodo_hasta INT NOT NULL DEFAULT 999912,
    estandar      FLOAT NOT NULL,
    acept         FLOAT NULL,                -- % Acept (en banda, el de arriba)
    aceptmenos    FLOAT NULL,                -- % Aceptmenos (solo banda, el de abajo)
    activo        BIT NOT NULL DEFAULT 1
);
GO
-- Nombres como en 002_TMI_CONSULTAS_VISTA.sql: acept / aceptmenos (antes acept / acept_mas)
IF COL_LENGTH('dbo.tmi_indicador_estandar', 'acept_mas') IS NOT NULL
BEGIN
    EXEC sp_rename 'dbo.tmi_indicador_estandar.acept_mas', 'aceptmenos', 'COLUMN';
    EXEC (N'UPDATE dbo.tmi_indicador_estandar SET acept = aceptmenos, aceptmenos = acept WHERE aceptmenos IS NOT NULL');
END
GO

/* ---------- Parte 3. Centros y estándares (tablas existentes; se crean solo si faltan, igual que
   Analisis_TMI/TMI/estandares/indicador_estandar.sql y TMI/centro/centros_tmi.sql). Si ya existen con
   id_estandar en vez de id_indicador, las vistas de 02_vistas_adaptadoras.sql leen cualquiera de los dos. ---------- */
IF OBJECT_ID('dbo.tmi_centro') IS NULL
CREATE TABLE dbo.tmi_centro (
    id INT IDENTITY(1,1) PRIMARY KEY, red VARCHAR(100), orden VARCHAR(50), orden_tipo VARCHAR(50),
    codcentro VARCHAR(50), centro VARCHAR(100), categoria VARCHAR(50), nivel VARCHAR(50), tipo VARCHAR(50),
    flag BIT                                   -- 0 = el centro no se muestra
);
GO

IF OBJECT_ID('dbo.tmi_estandar_tipo') IS NULL
CREATE TABLE dbo.tmi_estandar_tipo (
    id INT IDENTITY(1,1) PRIMARY KEY, id_indicador INT NOT NULL REFERENCES dbo.tmi_indicador(id),
    tipo_centro VARCHAR(50) NOT NULL, anio INT NOT NULL, est_fijo FLOAT,
    est_01 FLOAT, est_02 FLOAT, est_03 FLOAT, est_04 FLOAT, est_05 FLOAT, est_06 FLOAT,
    est_07 FLOAT, est_08 FLOAT, est_09 FLOAT, est_10 FLOAT, est_11 FLOAT, est_12 FLOAT,
    CONSTRAINT UX_tmi_estandar_tipo UNIQUE (id_indicador, tipo_centro, anio)
);
GO

IF OBJECT_ID('dbo.tmi_estandar_nivel') IS NULL
CREATE TABLE dbo.tmi_estandar_nivel (
    id INT IDENTITY(1,1) PRIMARY KEY, id_indicador INT NOT NULL REFERENCES dbo.tmi_indicador(id),
    nivel_centro VARCHAR(50) NOT NULL, anio INT NOT NULL, est_fijo FLOAT,
    est_01 FLOAT, est_02 FLOAT, est_03 FLOAT, est_04 FLOAT, est_05 FLOAT, est_06 FLOAT,
    est_07 FLOAT, est_08 FLOAT, est_09 FLOAT, est_10 FLOAT, est_11 FLOAT, est_12 FLOAT,
    CONSTRAINT UX_tmi_estandar_nivel UNIQUE (id_indicador, nivel_centro, anio)
);
GO

IF OBJECT_ID('dbo.tmi_estandar_categoria') IS NULL
CREATE TABLE dbo.tmi_estandar_categoria (
    id INT IDENTITY(1,1) PRIMARY KEY, id_indicador INT NOT NULL REFERENCES dbo.tmi_indicador(id),
    categoria_centro VARCHAR(50) NOT NULL, anio INT NOT NULL, est_fijo FLOAT,
    est_01 FLOAT, est_02 FLOAT, est_03 FLOAT, est_04 FLOAT, est_05 FLOAT, est_06 FLOAT,
    est_07 FLOAT, est_08 FLOAT, est_09 FLOAT, est_10 FLOAT, est_11 FLOAT, est_12 FLOAT
);
GO

-- Estándar específico de un centro (gana sobre tipo / nivel / categoría)
IF OBJECT_ID('dbo.tmi_centro_estandar') IS NULL
CREATE TABLE dbo.tmi_centro_estandar (
    id INT IDENTITY(1,1) PRIMARY KEY, id_centro INT NULL, codcentro VARCHAR(50) NOT NULL,
    id_indicador INT NOT NULL REFERENCES dbo.tmi_indicador(id), anio INT NOT NULL,
    aplica BIT NOT NULL DEFAULT 1, est_fijo FLOAT,
    est_01 FLOAT, est_02 FLOAT, est_03 FLOAT, est_04 FLOAT, est_05 FLOAT, est_06 FLOAT,
    est_07 FLOAT, est_08 FLOAT, est_09 FLOAT, est_10 FLOAT, est_11 FLOAT, est_12 FLOAT
);
GO
IF COL_LENGTH('dbo.tmi_centro_estandar', 'aplica') IS NULL
    ALTER TABLE dbo.tmi_centro_estandar ADD aplica BIT NOT NULL CONSTRAINT DF_tmi_ce_aplica DEFAULT 1;   -- 0 = NA
IF COL_LENGTH('dbo.tmi_centro_estandar', 'acept') IS NULL
    ALTER TABLE dbo.tmi_centro_estandar ADD acept FLOAT NULL;                                            -- % Acept propio
IF COL_LENGTH('dbo.tmi_centro_estandar', 'sustento') IS NULL
    ALTER TABLE dbo.tmi_centro_estandar ADD sustento VARCHAR(300) NULL;
GO

/* ---------- % Acept ----------
   El % Acept se calcula: estándar ± el porcentaje del indicador (tmi_indicador.tipo_tolerancia / tolerancia; en banda,
   tolerancia = hacia arriba y tolerancia_menos = hacia abajo). No se guarda por mes. La tabla tmi_estandar_acept de
   versiones anteriores se elimina si está vacía; si tiene datos se conserva como tmi_estandar_acept_anterior. */
IF OBJECT_ID('dbo.vw_tmi_acept', 'V') IS NOT NULL DROP VIEW dbo.vw_tmi_acept;
IF OBJECT_ID('dbo.tmi_estandar_acept') IS NOT NULL
BEGIN
    DECLARE @cols NVARCHAR(MAX), @sql NVARCHAR(MAX), @con_valores INT = 0;
    SELECT @cols = STUFF((SELECT ', ' + QUOTENAME(name) FROM sys.columns
                          WHERE object_id = OBJECT_ID('dbo.tmi_estandar_acept') AND name LIKE 'acept[_]__'
                          FOR XML PATH('')), 1, 2, '');
    IF @cols IS NOT NULL
    BEGIN
        SET @sql = N'SELECT @n = COUNT(*) FROM dbo.tmi_estandar_acept WHERE COALESCE(' + @cols + N', NULL) IS NOT NULL';
        EXEC sp_executesql @sql, N'@n INT OUTPUT', @n = @con_valores OUTPUT;
    END
    IF @con_valores > 0 AND OBJECT_ID('dbo.tmi_estandar_acept_anterior') IS NULL
        EXEC sp_rename 'dbo.tmi_estandar_acept', 'tmi_estandar_acept_anterior';
    ELSE IF @con_valores = 0
        DROP TABLE dbo.tmi_estandar_acept;
END
GO

-- % Acept por año (mes = 0 es el fijo del año; mes = 1..12 es el valor de cada mes, que toma el fijo en su fecha de cierre).
IF OBJECT_ID('dbo.tmi_indicador_tolerancia') IS NULL
CREATE TABLE dbo.tmi_indicador_tolerancia (
    id                   INT IDENTITY(1,1) PRIMARY KEY,
    id_indicador         INT NOT NULL REFERENCES dbo.tmi_indicador(id),
    anio                 INT NOT NULL,
    mes                  INT NOT NULL CONSTRAINT CK_tmi_indicador_tolerancia_mes CHECK (mes BETWEEN 0 AND 12),
    tipo_tolerancia      VARCHAR(3) NOT NULL DEFAULT 'REL' CHECK (tipo_tolerancia IN ('REL', 'ABS')),
    tolerancia           FLOAT NOT NULL,
    tolerancia_menos     FLOAT NULL,
    usuario_modificacion VARCHAR(200) NULL,
    fecha_modificacion   DATETIME NULL,
    CONSTRAINT UX_tmi_indicador_tolerancia UNIQUE (id_indicador, anio, mes)
);
GO

-- Exclusión por periodo: excl_MM = 1 -> NA ese mes. id_indicador NULL = todos los indicadores del centro.
-- La exclusión es por indicador: tmi_exclusion_centro_estandar pasa a llamarse tmi_exclusion_centro_indicador.
-- Se deja un sinónimo con el nombre anterior para las consultas existentes (002/003_TMI_CONSULTAS_VISTA.sql, Pentaho...).
IF OBJECT_ID('dbo.tmi_exclusion_centro_estandar', 'U') IS NOT NULL AND OBJECT_ID('dbo.tmi_exclusion_centro_indicador') IS NULL
    EXEC sp_rename 'dbo.tmi_exclusion_centro_estandar', 'tmi_exclusion_centro_indicador';
GO
IF OBJECT_ID('dbo.tmi_exclusion_centro_indicador') IS NULL
CREATE TABLE dbo.tmi_exclusion_centro_indicador (
    id INT IDENTITY(1,1) PRIMARY KEY, id_centro INT NULL, codcentro VARCHAR(50) NULL,
    id_indicador INT NULL REFERENCES dbo.tmi_indicador(id), anio INT NOT NULL,
    excl_01 BIT, excl_02 BIT, excl_03 BIT, excl_04 BIT, excl_05 BIT, excl_06 BIT,
    excl_07 BIT, excl_08 BIT, excl_09 BIT, excl_10 BIT, excl_11 BIT, excl_12 BIT
);
GO
IF COL_LENGTH('dbo.tmi_exclusion_centro_indicador', 'codcentro') IS NULL
    ALTER TABLE dbo.tmi_exclusion_centro_indicador ADD codcentro VARCHAR(50) NULL;
IF COL_LENGTH('dbo.tmi_exclusion_centro_indicador', 'motivo') IS NULL
    ALTER TABLE dbo.tmi_exclusion_centro_indicador ADD motivo VARCHAR(300) NULL;
GO
IF OBJECT_ID('dbo.tmi_exclusion_centro_estandar') IS NULL
    EXEC (N'CREATE SYNONYM dbo.tmi_exclusion_centro_estandar FOR dbo.tmi_exclusion_centro_indicador');
GO

/* ---------- Parte 4. Resultados ---------- */
IF OBJECT_ID('dbo.tmi_variable_pivot') IS NULL
CREATE TABLE dbo.tmi_variable_pivot (
    anio          INT NOT NULL,
    codcentro     INT NOT NULL,
    id_variable   INT NOT NULL REFERENCES dbo.tmi_variable(id),
    total         FLOAT NULL,
    m01 FLOAT, m02 FLOAT, m03 FLOAT, m04 FLOAT, m05 FLOAT, m06 FLOAT,
    m07 FLOAT, m08 FLOAT, m09 FLOAT, m10 FLOAT, m11 FLOAT, m12 FLOAT,
    fecha_calculo DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_tmi_variable_pivot PRIMARY KEY (anio, codcentro, id_variable)
);
GO

IF OBJECT_ID('dbo.tmi_resultado') IS NULL
CREATE TABLE dbo.tmi_resultado (
    periodo_corte INT NOT NULL,
    id_indicador  INT NOT NULL,
    codcentro     INT NOT NULL,
    mes           TINYINT NOT NULL,
    numerador     FLOAT NULL,
    denominador   FLOAT NULL,
    valor         FLOAT NULL,
    estandar      FLOAT NULL,
    verde         FLOAT NULL,
    acept         FLOAT NULL,                -- % Acept: límite para el puntaje 3 (en banda, el de arriba)
    aceptmenos    FLOAT NULL,                -- % Aceptmenos: solo banda, el de abajo
    puntaje       VARCHAR(2) NOT NULL,       -- 5 | 3 | 1 | 0 | NA
    motivo_na     VARCHAR(30) NULL,
    visible       BIT NOT NULL DEFAULT 1,
    fecha_calculo DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_tmi_resultado PRIMARY KEY (periodo_corte, id_indicador, codcentro, mes)
);
GO
-- Nombres como en 002_TMI_CONSULTAS_VISTA.sql: acept / aceptmenos (antes rojo / rojo_mas)
IF COL_LENGTH('dbo.tmi_resultado', 'rojo_mas') IS NOT NULL
BEGIN
    EXEC sp_rename 'dbo.tmi_resultado.rojo', 'acept', 'COLUMN';
    EXEC sp_rename 'dbo.tmi_resultado.rojo_mas', 'aceptmenos', 'COLUMN';
    EXEC (N'UPDATE dbo.tmi_resultado SET acept = aceptmenos, aceptmenos = acept WHERE aceptmenos IS NOT NULL');
END
GO

-- Resultado final por indicador (una fila por centro, como la hoja del Excel): lo llena usp_tmi_calcular.
-- periodo = mes en que se calculó (AAAAMM): guarda los valores tal como estaban hasta ese mes. Los periodos
-- cerrados no se recalculan, y el Excel de un periodo se arma con lo guardado aquí.
-- total = valor al mes del periodo; periodo_01..12 = valor de cada mes (0 después del periodo, NULL si el mes es NA).
-- Primera versión (columna periodo_corte, sin orden_red): solo tenía cálculos de prueba, se rehace.
IF COL_LENGTH('dbo.tmi_resultado_indicador', 'periodo_corte') IS NOT NULL
    DROP TABLE dbo.tmi_resultado_indicador;
GO
IF OBJECT_ID('dbo.tmi_resultado_indicador') IS NULL
CREATE TABLE dbo.tmi_resultado_indicador (
    periodo       INT NOT NULL,
    anio          INT NOT NULL,
    id_indicador  INT NOT NULL,
    orden         INT NULL,                  -- id del centro en tmi_centro
    orden_red     INT NULL,                  -- tmi_centro.orden: orden de la red en el reporte
    red           VARCHAR(100) NULL,
    codcentro     INT NOT NULL,
    centro        VARCHAR(200) NULL,
    nivel         VARCHAR(50) NULL,
    tipo          VARCHAR(50) NULL,
    categoria     VARCHAR(50) NULL,
    estandar      FLOAT NULL,
    acept         FLOAT NULL,                -- % Acept (en banda, el de arriba)
    aceptmenos    FLOAT NULL,                -- % Aceptmenos (solo banda, el de abajo)
    total         FLOAT NULL,
    puntaje       VARCHAR(2) NOT NULL,
    motivo_na     VARCHAR(30) NULL,
    visible       BIT NOT NULL DEFAULT 1,
    periodo_01 FLOAT, periodo_02 FLOAT, periodo_03 FLOAT, periodo_04 FLOAT, periodo_05 FLOAT, periodo_06 FLOAT, periodo_07 FLOAT, periodo_08 FLOAT, periodo_09 FLOAT, periodo_10 FLOAT, periodo_11 FLOAT, periodo_12 FLOAT,
    fecha_calculo DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_tmi_resultado_indicador PRIMARY KEY (periodo, id_indicador, codcentro)
);
GO
-- antes acept / acept_mas
IF COL_LENGTH('dbo.tmi_resultado_indicador', 'acept_mas') IS NOT NULL
BEGIN
    EXEC sp_rename 'dbo.tmi_resultado_indicador.acept_mas', 'aceptmenos', 'COLUMN';
    EXEC (N'UPDATE dbo.tmi_resultado_indicador SET acept = aceptmenos, aceptmenos = acept WHERE aceptmenos IS NOT NULL');
END
GO
