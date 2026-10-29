/* =====================================================================================================
   TMI - INDICADORES Y ESTÁNDARES
   Orden de ejecución: 1) este archivo  2) TMI/centro/centros_tmi.sql (tmi_centro, exclusiones y
   estándar por centro referencian a tmi_indicador).
   Correcciones:
     - se quitó la coma final antes de ")" (SQL Server no la acepta)
     - tmi_estandar_acept: acept_02 estaba repetido y faltaba acept_03
     - tmi_grupo.orden y las columnas de cálculo de tmi_indicador (las usa usp_tmi_calcular)
     - UNIQUE por indicador + clave + año: evita dos estándares para la misma combinación
   ===================================================================================================== */

-- Sección del reporte (Consulta Externa, Hospitalización ...). Los id son los de DIM_GRUPO:
-- al insertar usar SET IDENTITY_INSERT tmi_grupo ON (ver insert_grupo.sql).
CREATE TABLE tmi_grupo (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    descripcion VARCHAR(200),
    visible     BIT,
    orden       INT NULL                     -- orden de las secciones en la hoja Puntajes
);


CREATE TABLE tmi_indicador (
    id                   INT IDENTITY(1,1) PRIMARY KEY,
    grupo                INT REFERENCES tmi_grupo(id),
    indicador            VARCHAR(200),
    -- hoja del Excel
    codigo               VARCHAR(20)  NULL,  -- CE_Concent
    nombre_hoja          VARCHAR(31)  NULL,  -- máx. 31 caracteres, sin [ ] : * ? / \
    titulo_hoja          VARCHAR(200) NULL,
    orden                INT          NULL,
    -- fórmula: letras A..Z (tmi_indicador_variable), números, + - * . ( )
    expr_numerador       VARCHAR(200) NULL,  -- 'A - B'
    expr_denominador     VARCHAR(200) NULL,  -- 'X'
    tipo_calculo         VARCHAR(20)  NULL,  -- MENSUAL | ACUMULADO (tmi_tipo_calculo)
    factor               FLOAT        NOT NULL DEFAULT 1,
    -- reglas de cero
    den_cero             VARCHAR(4)   NOT NULL DEFAULT 'CERO',     -- denominador 0: CERO | NA
    num_cero_na          BIT          NOT NULL DEFAULT 0,          -- 1 = numerador 0 -> NA
    cero_si_letra_mes_0  BIT          NOT NULL DEFAULT 0,          -- 1 = alguna letra del mes en 0 -> 0
    sin_datos_anio       VARCHAR(7)   NOT NULL DEFAULT 'NA',       -- centro sin datos en el año: MOSTRAR | NA | OCULTAR
    -- estándar y puntaje
    base_estandar        VARCHAR(30)  NULL,  -- TIPO | NIVEL | CATEGORIA | TIPO_NIVEL | TIPO_CATEGORIA | NIVEL_CATEGORIA | TIPO_NIVEL_CATEGORIA
    sentido              VARCHAR(5)   NULL,  -- MENOR | MAYOR | BANDA
    tipo_tolerancia      VARCHAR(3)   NULL,  -- REL | ABS
    tolerancia           FLOAT        NULL,
    decimales            INT          NULL,
    cero_es_logro        BIT          NOT NULL DEFAULT 0,
    mostrar_no_aplica    BIT          NOT NULL DEFAULT 1,
    activo               BIT          NOT NULL DEFAULT 1,
    -- auditoría
    usuario_creacion     VARCHAR(200),
    usuario_modificacion VARCHAR(200),
    fecha_creacion       DATE,
    fecha_modificacion   DATE
);


CREATE TABLE tmi_estandar_tipo (
    id           INT IDENTITY(1,1) PRIMARY KEY,
    id_indicador INT NOT NULL REFERENCES tmi_indicador(id),
    tipo_centro  VARCHAR(50) NOT NULL,
    anio         INT NOT NULL,
    est_fijo     FLOAT,
    est_01 FLOAT,
    est_02 FLOAT,
    est_03 FLOAT,
    est_04 FLOAT,
    est_05 FLOAT,
    est_06 FLOAT,
    est_07 FLOAT,
    est_08 FLOAT,
    est_09 FLOAT,
    est_10 FLOAT,
    est_11 FLOAT,
    est_12 FLOAT,
    CONSTRAINT UX_tmi_estandar_tipo UNIQUE (id_indicador, tipo_centro, anio)
);


CREATE TABLE tmi_estandar_nivel (
    id           INT IDENTITY(1,1) PRIMARY KEY,
    id_indicador INT NOT NULL REFERENCES tmi_indicador(id),
    nivel_centro VARCHAR(50) NOT NULL,
    anio         INT NOT NULL,
    est_fijo     FLOAT,
    est_01 FLOAT,
    est_02 FLOAT,
    est_03 FLOAT,
    est_04 FLOAT,
    est_05 FLOAT,
    est_06 FLOAT,
    est_07 FLOAT,
    est_08 FLOAT,
    est_09 FLOAT,
    est_10 FLOAT,
    est_11 FLOAT,
    est_12 FLOAT,
    CONSTRAINT UX_tmi_estandar_nivel UNIQUE (id_indicador, nivel_centro, anio)
);


CREATE TABLE tmi_estandar_categoria (
    id               INT IDENTITY(1,1) PRIMARY KEY,
    id_indicador     INT NOT NULL REFERENCES tmi_indicador(id),
    categoria_centro VARCHAR(50) NOT NULL,
    anio             INT NOT NULL,
    est_fijo         FLOAT,
    est_01 FLOAT,
    est_02 FLOAT,
    est_03 FLOAT,
    est_04 FLOAT,
    est_05 FLOAT,
    est_06 FLOAT,
    est_07 FLOAT,
    est_08 FLOAT,
    est_09 FLOAT,
    est_10 FLOAT,
    est_11 FLOAT,
    est_12 FLOAT,
    CONSTRAINT UX_tmi_estandar_categoria UNIQUE (id_indicador, categoria_centro, anio)
);



-- % Acept: no tiene tabla. Se calcula con el porcentaje del indicador (tmi_indicador.tolerancia /
-- tolerancia_menos), en la pestaña "% Acept".
