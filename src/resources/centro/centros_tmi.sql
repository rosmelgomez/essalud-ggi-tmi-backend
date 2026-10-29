/* =====================================================================================================
   TMI - CENTROS, EXCLUSIONES Y ESTÁNDAR POR CENTRO
   Ejecutar DESPUÉS de TMI/estandares/indicador_estandar.sql (las tablas referencian a tmi_indicador).
   Correcciones:
     - se quitó la coma final antes de ")" en tmi_centro (SQL Server no la acepta)
     - tmi_exclusion_centro_estandar: id_indicador NULL = excluye TODOS los indicadores del centro; motivo
     - tmi_centro_estandar: aplica (0 = NA), acept (% Acept propio) y sustento, que usa el cálculo
     - UNIQUE por centro + indicador + año: una sola fila por combinación
   ===================================================================================================== */

CREATE TABLE tmi_centro (
    id         INT IDENTITY(1,1) PRIMARY KEY,
    red        VARCHAR(100),
    orden      VARCHAR(50),
    orden_tipo VARCHAR(50),
    codcentro  VARCHAR(50),
    centro     VARCHAR(100),
    categoria  VARCHAR(50),
    nivel      VARCHAR(50),
    tipo       VARCHAR(50),
    flag       BIT               -- 0 = el centro no se muestra (vw_tmi_centro_base también acepta anio + flag_01..12)
);


-- Exclusión por periodo: excl_MM = 1 -> el centro sale NA ese mes y no se suma en los acumulados.
CREATE TABLE tmi_exclusion_centro_estandar (
    id           INT IDENTITY(1,1) PRIMARY KEY,
    id_centro    INT REFERENCES tmi_centro(id),
    codcentro    VARCHAR(50),
    id_indicador INT NULL REFERENCES tmi_indicador(id),   -- NULL = todos los indicadores del centro
    anio         INT NOT NULL,
    excl_01 BIT NOT NULL DEFAULT 0,
    excl_02 BIT NOT NULL DEFAULT 0,
    excl_03 BIT NOT NULL DEFAULT 0,
    excl_04 BIT NOT NULL DEFAULT 0,
    excl_05 BIT NOT NULL DEFAULT 0,
    excl_06 BIT NOT NULL DEFAULT 0,
    excl_07 BIT NOT NULL DEFAULT 0,
    excl_08 BIT NOT NULL DEFAULT 0,
    excl_09 BIT NOT NULL DEFAULT 0,
    excl_10 BIT NOT NULL DEFAULT 0,
    excl_11 BIT NOT NULL DEFAULT 0,
    excl_12 BIT NOT NULL DEFAULT 0,
    motivo  VARCHAR(300) NULL,                            -- 'Cierre temporal de Centro Quirúrgico ...'
    CONSTRAINT CK_tmi_exclusion_centro CHECK (id_centro IS NOT NULL OR codcentro IS NOT NULL)
);


-- Estándar específico de un centro: gana sobre el estándar por tipo / nivel / categoría.
CREATE TABLE tmi_centro_estandar (
    id           INT IDENTITY(1,1) PRIMARY KEY,
    id_centro    INT REFERENCES tmi_centro(id),
    codcentro    VARCHAR(50) NOT NULL,
    id_indicador INT NOT NULL REFERENCES tmi_indicador(id),
    anio         INT NOT NULL,
    aplica       BIT NOT NULL DEFAULT 1,    -- 0 = el indicador no se evalúa en el centro (NA)
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
    acept        FLOAT NULL,                -- % Acept propio (NULL = tolerancia del indicador)
    sustento     VARCHAR(300) NULL,         -- carta o directiva
    CONSTRAINT UX_tmi_centro_estandar UNIQUE (codcentro, id_indicador, anio)
);
