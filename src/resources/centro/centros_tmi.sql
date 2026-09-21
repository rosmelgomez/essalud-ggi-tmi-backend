CREATE TABLE tmi_centro (
    id INT IDENTITY(1,1) PRIMARY KEY,
    red VARCHAR(100),
    codred VARCHAR(50),
    orden VARCHAR(50),
    orden_tipo VARCHAR(50),
    codcentro VARCHAR(50),
    categoria VARCHAR(50),
    nivel VARCHAR(50),
    tipo VARCHAR(50),
    centro VARCHAR(100),
    estado VARCHAR(50),
    anio INT,
    mes INT,
    periodo VARCHAR(50)
);
