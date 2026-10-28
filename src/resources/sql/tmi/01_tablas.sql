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
    total_anual          VARCHAR(15)  NOT NULL DEFAULT 'SUMA_MESES',   -- SUMA_MESES | MEDIANA_PERIODO
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
    agregacion     VARCHAR(10) NOT NULL DEFAULT 'SUMA',   -- SUMA | MEDIANA
    periodo_desde  INT NOT NULL DEFAULT 200001,
    periodo_hasta  INT NOT NULL DEFAULT 999912,
    activo         BIT NOT NULL DEFAULT 1
);
GO
IF COL_LENGTH('dbo.tmi_variable_logica', 'agregacion') IS NULL
    ALTER TABLE dbo.tmi_variable_logica ADD
        condicion_hoja VARCHAR(20) NULL,
        agregacion     VARCHAR(10) NOT NULL CONSTRAINT DF_tmi_vl_agregacion DEFAULT 'SUMA',
        periodo_desde  INT NOT NULL CONSTRAINT DF_tmi_vl_desde DEFAULT 200001,
        periodo_hasta  INT NOT NULL CONSTRAINT DF_tmi_vl_hasta DEFAULT 999912,
        activo         BIT NOT NULL CONSTRAINT DF_tmi_vl_activo DEFAULT 1;
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
        expr_numerador      VARCHAR(200) NULL,      -- letras A..Z, números, + - * . ( )
        expr_denominador    VARCHAR(200) NULL,
        tipo_calculo        VARCHAR(20)  NULL,      -- tmi_tipo_calculo: MENSUAL | ACUMULADO
        factor              FLOAT        NOT NULL CONSTRAINT DF_tmi_ind_factor DEFAULT 1,
        den_cero            VARCHAR(4)   NOT NULL CONSTRAINT DF_tmi_ind_dencero DEFAULT 'CERO',     -- CERO | NA
        cero_si_letra_mes_0 BIT          NOT NULL CONSTRAINT DF_tmi_ind_letra0 DEFAULT 0,
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

-- 1 = numerador 0 -> NA (el Excel actual pone NA a los centros con partos y 0 cesáreas)
IF COL_LENGTH('dbo.tmi_indicador', 'num_cero_na') IS NULL
    ALTER TABLE dbo.tmi_indicador ADD num_cero_na BIT NOT NULL CONSTRAINT DF_tmi_ind_numcero DEFAULT 0;
GO
-- Ampliar base_estandar para permitir combinaciones: TIPO, NIVEL, CATEGORIA, TIPO_NIVEL, TIPO_CATEGORIA, NIVEL_CATEGORIA, TIPO_NIVEL_CATEGORIA
IF COL_LENGTH('dbo.tmi_indicador', 'base_estandar') IS NOT NULL AND COL_LENGTH('dbo.tmi_indicador', 'base_estandar') < 30
    ALTER TABLE dbo.tmi_indicador ALTER COLUMN base_estandar VARCHAR(30) NULL;
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
    acept         FLOAT NULL,
    acept_mas     FLOAT NULL,
    activo        BIT NOT NULL DEFAULT 1
);
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
    ALTER TABLE dbo.tmi_centro_estandar ADD acept FLOAT NULL;                                            -- Rojo propio
IF COL_LENGTH('dbo.tmi_centro_estandar', 'sustento') IS NULL
    ALTER TABLE dbo.tmi_centro_estandar ADD sustento VARCHAR(300) NULL;
GO

-- Aceptación por mes cuando no sirve la tolerancia del indicador (condicion: ACEPT = Rojo | MAS = Rojo +)
IF OBJECT_ID('dbo.tmi_estandar_acept') IS NULL
CREATE TABLE dbo.tmi_estandar_acept (
    id INT IDENTITY(1,1) PRIMARY KEY, id_indicador INT NOT NULL REFERENCES dbo.tmi_indicador(id),
    tipo VARCHAR(50), condicion VARCHAR(50) NOT NULL DEFAULT 'ACEPT', anio INT NOT NULL,
    acept_01 FLOAT, acept_02 FLOAT, acept_03 FLOAT, acept_04 FLOAT, acept_05 FLOAT, acept_06 FLOAT,
    acept_07 FLOAT, acept_08 FLOAT, acept_09 FLOAT, acept_10 FLOAT, acept_11 FLOAT, acept_12 FLOAT
);
GO

-- Exclusión por periodo: excl_MM = 1 -> NA ese mes. id_indicador NULL = todos los indicadores del centro.
IF OBJECT_ID('dbo.tmi_exclusion_centro_estandar') IS NULL
CREATE TABLE dbo.tmi_exclusion_centro_estandar (
    id INT IDENTITY(1,1) PRIMARY KEY, id_centro INT NULL, codcentro VARCHAR(50) NULL,
    id_indicador INT NULL REFERENCES dbo.tmi_indicador(id), anio INT NOT NULL,
    excl_01 BIT, excl_02 BIT, excl_03 BIT, excl_04 BIT, excl_05 BIT, excl_06 BIT,
    excl_07 BIT, excl_08 BIT, excl_09 BIT, excl_10 BIT, excl_11 BIT, excl_12 BIT
);
GO
IF COL_LENGTH('dbo.tmi_exclusion_centro_estandar', 'codcentro') IS NULL
    ALTER TABLE dbo.tmi_exclusion_centro_estandar ADD codcentro VARCHAR(50) NULL;
IF COL_LENGTH('dbo.tmi_exclusion_centro_estandar', 'motivo') IS NULL
    ALTER TABLE dbo.tmi_exclusion_centro_estandar ADD motivo VARCHAR(300) NULL;
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
    rojo          FLOAT NULL,
    rojo_mas      FLOAT NULL,
    puntaje       VARCHAR(2) NOT NULL,       -- 5 | 3 | 1 | 0 | NA
    motivo_na     VARCHAR(30) NULL,
    visible       BIT NOT NULL DEFAULT 1,
    fecha_calculo DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_tmi_resultado PRIMARY KEY (periodo_corte, id_indicador, codcentro, mes)
);
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
    acept         FLOAT NULL,                -- Rojo (Rojo - en BANDA)
    acept_mas     FLOAT NULL,                -- Rojo + (solo BANDA)
    total         FLOAT NULL,
    puntaje       VARCHAR(2) NOT NULL,
    motivo_na     VARCHAR(30) NULL,
    visible       BIT NOT NULL DEFAULT 1,
    periodo_01 FLOAT, periodo_02 FLOAT, periodo_03 FLOAT, periodo_04 FLOAT, periodo_05 FLOAT, periodo_06 FLOAT, periodo_07 FLOAT, periodo_08 FLOAT, periodo_09 FLOAT, periodo_10 FLOAT, periodo_11 FLOAT, periodo_12 FLOAT,
    fecha_calculo DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_tmi_resultado_indicador PRIMARY KEY (periodo, id_indicador, codcentro)
);
GO
