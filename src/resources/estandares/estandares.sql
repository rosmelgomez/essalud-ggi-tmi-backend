
CREATE TABLE tmi_estandar_tipo (
    id INT IDENTITY(1,1) PRIMARY KEY,
    tipo VARCHAR(200),
    indicador VARCHAR(200),
    tipo_centro VARCHAR(50),
    anio INT,
    mes INT,
    periodo VARCHAR(50),
   estandar FLOAT,
   acept FLOAT,
   aceptmenos FLOAT
);

CREATE TABLE tmi_estandar_nivel (
    id INT IDENTITY(1,1) PRIMARY KEY,
    tipo VARCHAR(200),
    indicador VARCHAR(200),
    nivel_centro VARCHAR(50),
    anio INT,
    mes INT,
    periodo VARCHAR(50),
    estandar FLOAT,
    acept FLOAT,
    aceptmenos FLOAT
);

CREATE TABLE tmi_estandar_categoria (
    id INT IDENTITY(1,1) PRIMARY KEY,
    tipo VARCHAR(200),
    indicador VARCHAR(200),
    categoria_centro VARCHAR(50),
    anio INT,
    mes INT,
    periodo VARCHAR(50),
    estandar FLOAT,
    acept FLOAT,
    aceptmenos FLOAT
);

