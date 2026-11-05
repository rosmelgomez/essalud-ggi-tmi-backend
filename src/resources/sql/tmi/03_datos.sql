/* =====================================================================================================
   TMI DINAMICO - 03 DATOS INICIALES (idempotente: solo inserta lo que falta, no pisa cambios del usuario)
   Origen: Analisis_TMI/TMI (insert_grupo.sql, calculo tmi/02, 03 y 07, equivalencias.txt)
   ===================================================================================================== */

/* ---------- Tipos de cálculo ---------- */
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_tipo_calculo WHERE codigo = 'MENSUAL')
    INSERT INTO dbo.tmi_tipo_calculo (codigo, descripcion) VALUES ('MENSUAL', 'Cada letra toma el valor del mes n');
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_tipo_calculo WHERE codigo = 'ACUMULADO')
    INSERT INTO dbo.tmi_tipo_calculo (codigo, descripcion) VALUES ('ACUMULADO', 'Cada letra toma la suma de enero al mes n');
GO

/* ---------- Secciones del reporte: se leen de DIM_GRUPO (tmi_indicador.grupo = DIM_GRUPO.tipgrupo) ---------- */
-- bases creadas antes: quita la FK de tmi_indicador.grupo hacia tmi_grupo (la tabla ya no se usa)
DECLARE @fk_grupo sysname = (SELECT TOP 1 name FROM sys.foreign_keys
                             WHERE parent_object_id = OBJECT_ID('dbo.tmi_indicador')
                               AND referenced_object_id = OBJECT_ID('dbo.tmi_grupo'));
IF @fk_grupo IS NOT NULL EXEC('ALTER TABLE dbo.tmi_indicador DROP CONSTRAINT ' + @fk_grupo);
GO

/* ---------- Variables y su lógica (grupo / actividad / servicio de TOTALIZADO3) ---------- */
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Consulta Externa - Consultas') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Consulta Externa - Consultas', 'Consulta Externa - Consultas', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Consulta Externa - Consultantes al Establecimiento') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Consulta Externa - Consultantes al Establecimiento', 'Consulta Externa - Consultantes al Establecimiento', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Consulta Externa - Horas Médicas Efectivas') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Consulta Externa - Horas Médicas Efectivas', 'Consulta Externa - Horas Médicas Efectivas', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Consulta Externa - Horas Médicas Programadas') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Consulta Externa - Horas Médicas Programadas', 'Consulta Externa - Horas Médicas Programadas', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Actividades Intermedias - Recetas Despachadas de C. E') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Actividades Intermedias - Recetas Despachadas de C. E', 'Actividades Intermedias - Recetas Despachadas de C. E', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Hospitalizacion - Egresos') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Hospitalizacion - Egresos', 'Hospitalizacion - Egresos', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Hospitalizacion - Estancias') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Hospitalizacion - Estancias', 'Hospitalizacion - Estancias', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Hospitalizacion - Pacientes Días') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Hospitalizacion - Pacientes Días', 'Hospitalizacion - Pacientes Días', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Hospitalizacion - Días Cama Disponible') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Hospitalizacion - Días Cama Disponible', 'Hospitalizacion - Días Cama Disponible', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Hospitalizacion -  Camas Hospitalarias') INSERT INTO dbo.tmi_variable (nombre, descripcion, agregacion, total_anual, activo) VALUES ('Hospitalizacion -  Camas Hospitalarias', 'Hospitalizacion -  Camas Hospitalarias', 'MEDIANA', 'MEDIANA_PERIODO', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Hospitalizacion - Defunciones antes de 48 horas') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Hospitalizacion - Defunciones antes de 48 horas', 'Hospitalizacion - Defunciones antes de 48 horas', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Hospitalizacion - Defunciones después de 48 horas') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Hospitalizacion - Defunciones después de 48 horas', 'Hospitalizacion - Defunciones después de 48 horas', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento', 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Centro Quirúrgico - Cirugías sin clasificación de complejidad') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'Centro Quirúrgico - Cirugías sin clasificación de complejidad', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Centro Quirúrgico - Horas Uso de Sala') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Centro Quirúrgico - Horas Uso de Sala', 'Centro Quirúrgico - Horas Uso de Sala', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Centro Quirúrgico - Horas Programadas Intervenc.Quirurgicas') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Centro Quirúrgico - Horas Programadas Intervenc.Quirurgicas', 'Centro Quirúrgico - Horas Programadas Intervenc.Quirurgicas', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Centro Quirúrgico - Operaciones Suspendidas') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Centro Quirúrgico - Operaciones Suspendidas', 'Centro Quirúrgico - Operaciones Suspendidas', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Centro Quirúrgico - Intervenc.Quirurgicas Programadas') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Centro Quirúrgico - Intervenc.Quirurgicas Programadas', 'Centro Quirúrgico - Intervenc.Quirurgicas Programadas', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Centro Quirúrgico -  Salas Quirúrgicas Funcionales') INSERT INTO dbo.tmi_variable (nombre, descripcion, agregacion, total_anual, activo) VALUES ('Centro Quirúrgico -  Salas Quirúrgicas Funcionales', 'Centro Quirúrgico -  Salas Quirúrgicas Funcionales', 'MEDIANA', 'MEDIANA_PERIODO', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Centro Obstétrico - Cesáreas') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Centro Obstétrico - Cesáreas', 'Centro Obstétrico - Cesáreas', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Centro Obstétrico - Total de Partos') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Centro Obstétrico - Total de Partos', 'Centro Obstétrico - Total de Partos', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Emergencia - Prioridad I') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Emergencia - Prioridad I', 'Emergencia - Prioridad I', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Emergencia - Prioridad II') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Emergencia - Prioridad II', 'Emergencia - Prioridad II', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Emergencia - Prioridad IV') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Emergencia - Prioridad IV', 'Emergencia - Prioridad IV', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Emergencia - Prioridad V') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Emergencia - Prioridad V', 'Emergencia - Prioridad V', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Emergencia - Total de Atenciones') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Emergencia - Total de Atenciones', 'Emergencia - Total de Atenciones', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Odontología - Sesiones Odontológicas') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Odontología - Sesiones Odontológicas', 'Odontología - Sesiones Odontológicas', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Odontología - Consultantes de Odontología') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Odontología - Consultantes de Odontología', 'Odontología - Consultantes de Odontología', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Odontología - Horas Odontológicas Efectivas') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Odontología - Horas Odontológicas Efectivas', 'Odontología - Horas Odontológicas Efectivas', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Odontología - Horas Odontológicas Programadas') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Odontología - Horas Odontológicas Programadas', 'Odontología - Horas Odontológicas Programadas', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Odontología - Trabajos Odontológicos') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Odontología - Trabajos Odontológicos', 'Odontología - Trabajos Odontológicos', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Odontología - Diagnóstico por imágenes') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Odontología - Diagnóstico por imágenes', 'Odontología - Diagnóstico por imágenes', 'SUMA_MESES', 1);
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_variable WHERE nombre = 'Odontología - Procedimientos Especiales') INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo) VALUES ('Odontología - Procedimientos Especiales', 'Odontología - Procedimientos Especiales', 'SUMA_MESES', 1);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 1, 3, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Consulta Externa - Consultas' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 1 AND l.actividad = 3 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 1, 1, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Consulta Externa - Consultantes al Establecimiento' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 1 AND l.actividad = 1 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 1, 6, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Consulta Externa - Horas Médicas Efectivas' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 1 AND l.actividad = 6 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 1, 5, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Consulta Externa - Horas Médicas Programadas' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 1 AND l.actividad = 5 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 9, 9, 14 FROM dbo.tmi_variable v WHERE v.nombre = 'Actividades Intermedias - Recetas Despachadas de C. E' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 9 AND l.actividad = 9 AND l.servicio = 14);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 3, 47, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Hospitalizacion - Egresos' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 3 AND l.actividad = 47 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 3, 48, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Hospitalizacion - Estancias' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 3 AND l.actividad = 48 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 3, 49, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Hospitalizacion - Pacientes Días' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 3 AND l.actividad = 49 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 3, 50, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Hospitalizacion - Días Cama Disponible' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 3 AND l.actividad = 50 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 3, 51, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Hospitalizacion -  Camas Hospitalarias' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 3 AND l.actividad = 51 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 3, 52, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Hospitalizacion - Defunciones antes de 48 horas' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 3 AND l.actividad = 52 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 3, 53, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Hospitalizacion - Defunciones después de 48 horas' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 3 AND l.actividad = 53 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 6, 225, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 6 AND l.actividad = 225 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 6, 226, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 6 AND l.actividad = 226 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 6, 227, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 6 AND l.actividad = 227 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 6, 228, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 6 AND l.actividad = 228 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 6, 229, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 6 AND l.actividad = 229 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 6, 636, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Centro Quirúrgico - Cirugías sin clasificación de complejidad' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 6 AND l.actividad = 636 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 6, 38, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Centro Quirúrgico - Horas Uso de Sala' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 6 AND l.actividad = 38 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 6, 5, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Centro Quirúrgico - Horas Programadas Intervenc.Quirurgicas' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 6 AND l.actividad = 5 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 6, 349, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Centro Quirúrgico - Operaciones Suspendidas' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 6 AND l.actividad = 349 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 6, 430, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Centro Quirúrgico - Intervenc.Quirurgicas Programadas' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 6 AND l.actividad = 430 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 6, 315, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Centro Quirúrgico -  Salas Quirúrgicas Funcionales' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 6 AND l.actividad = 315 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 5, 19, 77 FROM dbo.tmi_variable v WHERE v.nombre = 'Centro Obstétrico - Cesáreas' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 5 AND l.actividad = 19 AND l.servicio = 77);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 5, 18, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Centro Obstétrico - Total de Partos' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 5 AND l.actividad = 18 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 5, 19, 77 FROM dbo.tmi_variable v WHERE v.nombre = 'Centro Obstétrico - Total de Partos' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 5 AND l.actividad = 19 AND l.servicio = 77);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 5, 19, 78 FROM dbo.tmi_variable v WHERE v.nombre = 'Centro Obstétrico - Total de Partos' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 5 AND l.actividad = 19 AND l.servicio = 78);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 8, 44, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Emergencia - Prioridad I' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 8 AND l.actividad = 44 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 8, 42, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Emergencia - Prioridad II' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 8 AND l.actividad = 42 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 8, 235, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Emergencia - Prioridad IV' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 8 AND l.actividad = 235 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 8, 585, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Emergencia - Prioridad V' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 8 AND l.actividad = 585 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 8, 44, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Emergencia - Total de Atenciones' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 8 AND l.actividad = 44 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 8, 42, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Emergencia - Total de Atenciones' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 8 AND l.actividad = 42 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 8, 41, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Emergencia - Total de Atenciones' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 8 AND l.actividad = 41 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 8, 235, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Emergencia - Total de Atenciones' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 8 AND l.actividad = 235 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 8, 585, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Emergencia - Total de Atenciones' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 8 AND l.actividad = 585 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 19, 59, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Odontología - Sesiones Odontológicas' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 19 AND l.actividad = 59 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 19, 2, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Odontología - Consultantes de Odontología' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 19 AND l.actividad = 2 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 19, 6, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Odontología - Horas Odontológicas Efectivas' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 19 AND l.actividad = 6 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 19, 5, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Odontología - Horas Odontológicas Programadas' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 19 AND l.actividad = 5 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 19, 60, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Odontología - Trabajos Odontológicos' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 19 AND l.actividad = 60 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 19, 605, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Odontología - Diagnóstico por imágenes' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 19 AND l.actividad = 605 AND l.servicio IS NULL);
INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio) SELECT v.id, 19, 165, NULL FROM dbo.tmi_variable v WHERE v.nombre = 'Odontología - Procedimientos Especiales' AND NOT EXISTS (SELECT 1 FROM dbo.tmi_variable_logica l WHERE l.id_variable = v.id AND l.tipgrupo = 19 AND l.actividad = 165 AND l.servicio IS NULL);
GO

/* ---------- Indicadores (id = id_estandar de tmi_estandar y de las tablas de estándar) ---------- */
SET IDENTITY_INSERT dbo.tmi_indicador ON;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 1) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (1, 1, 'Concentracion de Consultas', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'CE_Concent', nombre_hoja = 'C.E_Concent.', titulo_hoja = 'CONCENTRACION DE CONSULTAS', orden = 1, tipo_calculo = 'ACUMULADO', sin_datos_anio = 'NA', base_estandar = 'NIVEL', sentido = 'MENOR', tipo_tolerancia = 'REL', tolerancia = 0.1, decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 1 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 2) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (2, 1, 'Rendimiento Hora Medico', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'CE_RHrMedico', nombre_hoja = 'C.E_R.Hr.Medico', titulo_hoja = 'RENDIMIENTO HORA MEDICO', orden = 2, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'NIVEL_TIPO', sentido = 'MAYOR', tipo_tolerancia = 'REL', tolerancia = 0.1, decimales = 2, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 2 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 3) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (3, 1, 'Grado de Cumplimiento de Horas Programadas', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'CE_GCHProg', nombre_hoja = 'C.E_G.C.H.Prog', titulo_hoja = 'GRADO DE CUMPLIMIENTO DE HORAS PROGRAMADAS', orden = 3, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MAYOR', tipo_tolerancia = 'REL', tolerancia = 0.05, decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 3 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 4) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (4, 1, 'Promedio de Recetas por Consultas', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'CE_Recetas', nombre_hoja = 'C.E_Recetas', titulo_hoja = 'PROMEDIO DE RECETAS POR CONSULTAS', orden = 4, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MENOR', tipo_tolerancia = 'REL', tolerancia = 0.1, decimales = 2, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 4 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 5) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (5, 3, 'Promedio Dia Estancia', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'H_Estancias', nombre_hoja = 'H_Estancias', titulo_hoja = 'PROMEDIO DIA ESTANCIA', orden = 5, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MENOR', tipo_tolerancia = 'REL', tolerancia = 0.2, decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 5 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 6) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (6, 3, 'Porcentaje de Ocupación de Cama', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'H_OCama', nombre_hoja = 'H_% O.Cama', titulo_hoja = 'PORCENTAJE DE OCUPACIÓN DE CAMA', orden = 6, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'BANDA', tipo_tolerancia = 'ABS', tolerancia = 0.05, decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 6 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 7) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (7, 3, 'Intervalo de Sustitución', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'H_ISust', nombre_hoja = 'H_I.Sust.', titulo_hoja = 'INTERVALO DE SUSTITUCIÓN', orden = 7, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MENOR', tipo_tolerancia = 'REL', tolerancia = 0.2, decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 7 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 8) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (8, 3, 'Rendimiento Cama', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'H_RCama', nombre_hoja = 'H_R.Cama', titulo_hoja = 'RENDIMIENTO CAMA', orden = 8, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MAYOR', tipo_tolerancia = 'REL', tolerancia = 0.2, decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 8 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 9) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (9, 3, 'Tasa Neta de Mortalidad Hospitalaria', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'H_TBMHosp', nombre_hoja = 'H_T.B.M.Hosp', titulo_hoja = 'TASA NETA DE MORTALIDAD HOSPITALARIA', orden = 9, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MENOR', tipo_tolerancia = 'REL', tolerancia = 0.1, decimales = NULL, cero_es_logro = 1, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 9 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 10) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (10, 6, 'Porcentaje de Intervenciones Menores', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'Qx_IMenor', nombre_hoja = 'Qx_I.Menor', titulo_hoja = 'PORCENTAJE DE INTERVENCIONES MENORES', orden = 10, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MENOR', tipo_tolerancia = 'REL', tolerancia = 0.2, decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 10 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 11) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (11, 6, 'Porcentaje de Intervenciones de Alta Complejidad', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'Qx_IAlta', nombre_hoja = 'Qx_I.Alta', titulo_hoja = 'PORCENTAJE DE INTERVENCIONES DE ALTA COMPLEJIDAD', orden = 11, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MAYOR', tipo_tolerancia = 'REL', tolerancia = 0.2, decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 11 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 12) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (12, 6, 'Porcentaje de Horas Quirúrgicas Efectivas', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'Qx_GCHProg', nombre_hoja = 'Qx_G.C.H.Prog', titulo_hoja = 'PORCENTAJE DE HORAS QUIRÚRGICAS EFECTIVAS', orden = 12, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MAYOR', tipo_tolerancia = 'ABS', tolerancia = 0.1, decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 12 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 13) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (13, 6, 'Rendimiento de Sala de Operaciones', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'Qx_RendSO', nombre_hoja = 'Qx_Rend.SO', titulo_hoja = 'RENDIMIENTO DE SALA DE OPERACIONES', orden = 13, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MAYOR', tipo_tolerancia = 'REL', tolerancia = 0.1, decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 13 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 14) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (14, 6, 'Porcentaje de Operaciones Suspendidas', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'Qx_IntSusp', nombre_hoja = 'Qx.Int.Susp', titulo_hoja = 'PORCENTAJE DE OPERACIONES SUSPENDIDAS', orden = 14, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MENOR', tipo_tolerancia = 'REL', tolerancia = 0.1, decimales = NULL, cero_es_logro = 1, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 14 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 15) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (15, 6, 'Tasa de Cesáreas', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'Qx_HTCesareas', nombre_hoja = 'H_T.Cesareas', titulo_hoja = 'TASA DE CESÁREAS', orden = 15, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MENOR', tipo_tolerancia = 'REL', tolerancia = 0.1, decimales = NULL, cero_es_logro = 1, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 15 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 16) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (16, 8, '% Prioridad IV y V con respecto al Total de Emergencias', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'Em_PrioIV_V', nombre_hoja = 'Em_Prio.IV_V', titulo_hoja = '% PRIORIDAD IV Y V CON RESPECTO AL TOTAL DE EMERGENCIAS', orden = 16, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MENOR', tipo_tolerancia = 'REL', tolerancia = 0.2, decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 16 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 17) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (17, 8, '% Prioridad I y II con respecto al Total de Emergencias', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'Em_PrioI_II', nombre_hoja = 'Em_Prio.I_II', titulo_hoja = '% PRIORIDAD I Y II CON RESPECTO AL TOTAL DE EMERGENCIAS', orden = 17, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MAYOR', tipo_tolerancia = 'REL', tolerancia = 0.1, decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 17 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 18) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (18, 19, 'Concentración de Sesiones Odontológicas', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'O_Concent', nombre_hoja = 'O_Concent.', titulo_hoja = 'CONCENTRACIÓN DE SESIONES ODONTOLÓGICAS', orden = 18, tipo_calculo = 'ACUMULADO', sin_datos_anio = 'NA', base_estandar = 'NIVEL', sentido = 'MENOR', tipo_tolerancia = 'REL', tolerancia = 0.1, decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 18 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 19) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (19, 19, 'Rendimiento Hora Odontológica', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'O_HrOdont', nombre_hoja = 'O_Hr.Odont', titulo_hoja = 'RENDIMIENTO HORA ODONTOLÓGICA', orden = 19, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'NIVEL_TIPO', sentido = 'MAYOR', tipo_tolerancia = 'REL', tolerancia = 0.1, decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 19 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 20) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (20, 19, 'Grado de Cumplimiento de Hora Odontólogo', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'O_GCHOdon', nombre_hoja = 'O_G.C.H.Odon', titulo_hoja = 'GRADO DE CUMPLIMIENTO DE HORA ODONTÓLOGO', orden = 20, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MAYOR', tipo_tolerancia = 'REL', tolerancia = 0.05, decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 20 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 21) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (21, 19, 'Número de trabajos Odontológicos por Sesión', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'O_NTOdontS', nombre_hoja = 'O_N.T.Odont.S', titulo_hoja = 'NÚMERO DE TRABAJOS ODONTOLÓGICOS POR SESIÓN', orden = 21, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MAYOR', tipo_tolerancia = 'REL', tolerancia = 0.1, decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 21 AND codigo IS NULL;
SET IDENTITY_INSERT dbo.tmi_indicador OFF;
GO

/* ---------- Fórmula de cada indicador (términos de TOTALIZADO3, como la columna de fórmulas de TMI_SQL) ----------
   Los términos (tmi_indicador_termino) y formula_sql los genera el backend al iniciar desde esta columna. */
UPDATE dbo.tmi_indicador SET formula = N'[1;3] / [1;1]' WHERE codigo = 'CE_Concent' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'[1;3] / [1;6]' WHERE codigo = 'CE_RHrMedico' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'[1;6] / [1;5]' WHERE codigo = 'CE_GCHProg' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'[9;9#14] / [1;3]' WHERE codigo = 'CE_Recetas' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'[3;48] / [3;47]' WHERE codigo = 'H_Estancias' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'[3;49] / [3;50]' WHERE codigo = 'H_OCama' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'([3;50] - [3;49]) / [3;47]' WHERE codigo = 'H_ISust' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'[3;47] / MEDIANA([3;51])' WHERE codigo = 'H_RCama' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'[3;53] / ([3;47] - [3;52])' WHERE codigo = 'H_TBMHosp' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'([6;228] + [6;229]) / ([6;225] + [6;226] + [6;227] + [6;228] + [6;229] + [6;636])' WHERE codigo = 'Qx_IMenor' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'[6;225] / ([6;225] + [6;226] + [6;227] + [6;228] + [6;229] + [6;636])' WHERE codigo = 'Qx_IAlta' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'[6;38] / [6;5]' WHERE codigo = 'Qx_GCHProg' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'([6;225] + [6;226] + [6;227] + [6;228] + [6;229] + [6;636]) / MEDIANA([6;315])' WHERE codigo = 'Qx_RendSO' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'[6;349] / [6;430]' WHERE codigo = 'Qx_IntSusp' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'[5;19#77] / ([5;18] + [5;19#77] + [5;19#78])' WHERE codigo = 'Qx_HTCesareas' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'([8;235] + [8;585]) / ([8;41] + [8;42] + [8;44] + [8;235] + [8;585])' WHERE codigo = 'Em_PrioIV_V' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'([8;44] + [8;42]) / ([8;41] + [8;42] + [8;44] + [8;235] + [8;585])' WHERE codigo = 'Em_PrioI_II' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'[19;59] / [19;2]' WHERE codigo = 'O_Concent' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'[19;59] / [19;6]' WHERE codigo = 'O_HrOdont' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'[19;6] / [19;5]' WHERE codigo = 'O_GCHOdon' AND formula IS NULL;
UPDATE dbo.tmi_indicador SET formula = N'([19;60] + [19;605] + [19;165]) / [19;59]' WHERE codigo = 'O_NTOdontS' AND formula IS NULL;
GO

/* ---------- Fórmula con letras: una variable por letra ----------
   Solo si el indicador todavía no tiene formula_alias: reemplaza las letras anteriores (varias variables por letra). */
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'CE_Concent' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'CE_Concent';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Consulta Externa - Consultas' WHERE i.codigo = 'CE_Concent';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Consulta Externa - Consultantes al Establecimiento' WHERE i.codigo = 'CE_Concent';
    UPDATE dbo.tmi_indicador SET formula_alias = N'A / B' WHERE codigo = 'CE_Concent';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'CE_RHrMedico' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'CE_RHrMedico';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Consulta Externa - Consultas' WHERE i.codigo = 'CE_RHrMedico';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Consulta Externa - Horas Médicas Efectivas' WHERE i.codigo = 'CE_RHrMedico';
    UPDATE dbo.tmi_indicador SET formula_alias = N'A / B' WHERE codigo = 'CE_RHrMedico';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'CE_GCHProg' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'CE_GCHProg';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Consulta Externa - Horas Médicas Efectivas' WHERE i.codigo = 'CE_GCHProg';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Consulta Externa - Horas Médicas Programadas' WHERE i.codigo = 'CE_GCHProg';
    UPDATE dbo.tmi_indicador SET formula_alias = N'A / B' WHERE codigo = 'CE_GCHProg';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'CE_Recetas' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'CE_Recetas';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Actividades Intermedias - Recetas Despachadas de C. E' WHERE i.codigo = 'CE_Recetas';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Consulta Externa - Consultas' WHERE i.codigo = 'CE_Recetas';
    UPDATE dbo.tmi_indicador SET formula_alias = N'A / B' WHERE codigo = 'CE_Recetas';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'H_Estancias' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'H_Estancias';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Hospitalizacion - Estancias' WHERE i.codigo = 'H_Estancias';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Hospitalizacion - Egresos' WHERE i.codigo = 'H_Estancias';
    UPDATE dbo.tmi_indicador SET formula_alias = N'A / B' WHERE codigo = 'H_Estancias';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'H_OCama' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'H_OCama';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Hospitalizacion - Pacientes Días' WHERE i.codigo = 'H_OCama';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Hospitalizacion - Días Cama Disponible' WHERE i.codigo = 'H_OCama';
    UPDATE dbo.tmi_indicador SET formula_alias = N'A / B' WHERE codigo = 'H_OCama';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'H_ISust' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'H_ISust';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Hospitalizacion - Días Cama Disponible' WHERE i.codigo = 'H_ISust';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Hospitalizacion - Pacientes Días' WHERE i.codigo = 'H_ISust';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'C', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Hospitalizacion - Egresos' WHERE i.codigo = 'H_ISust';
    UPDATE dbo.tmi_indicador SET formula_alias = N'(A - B) / C' WHERE codigo = 'H_ISust';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'H_RCama' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'H_RCama';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Hospitalizacion - Egresos' WHERE i.codigo = 'H_RCama';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Hospitalizacion -  Camas Hospitalarias' WHERE i.codigo = 'H_RCama';
    UPDATE dbo.tmi_indicador SET formula_alias = N'A / B' WHERE codigo = 'H_RCama';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'H_TBMHosp' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'H_TBMHosp';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Hospitalizacion - Defunciones después de 48 horas' WHERE i.codigo = 'H_TBMHosp';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Hospitalizacion - Egresos' WHERE i.codigo = 'H_TBMHosp';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'C', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Hospitalizacion - Defunciones antes de 48 horas' WHERE i.codigo = 'H_TBMHosp';
    UPDATE dbo.tmi_indicador SET formula_alias = N'A / (B - C)' WHERE codigo = 'H_TBMHosp';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'Qx_IMenor' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'Qx_IMenor';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento' WHERE i.codigo = 'Qx_IMenor';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento' WHERE i.codigo = 'Qx_IMenor';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'C', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad' WHERE i.codigo = 'Qx_IMenor';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'D', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad' WHERE i.codigo = 'Qx_IMenor';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'E', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad' WHERE i.codigo = 'Qx_IMenor';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'F', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - Cirugías sin clasificación de complejidad' WHERE i.codigo = 'Qx_IMenor';
    UPDATE dbo.tmi_indicador SET formula_alias = N'(A + B) / (C + D + E + A + B + F)' WHERE codigo = 'Qx_IMenor';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'Qx_IAlta' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'Qx_IAlta';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad' WHERE i.codigo = 'Qx_IAlta';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad' WHERE i.codigo = 'Qx_IAlta';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'C', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad' WHERE i.codigo = 'Qx_IAlta';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'D', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento' WHERE i.codigo = 'Qx_IAlta';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'E', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento' WHERE i.codigo = 'Qx_IAlta';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'F', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - Cirugías sin clasificación de complejidad' WHERE i.codigo = 'Qx_IAlta';
    UPDATE dbo.tmi_indicador SET formula_alias = N'A / (A + B + C + D + E + F)' WHERE codigo = 'Qx_IAlta';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'Qx_GCHProg' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'Qx_GCHProg';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - Horas Uso de Sala' WHERE i.codigo = 'Qx_GCHProg';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - Horas Programadas Intervenc.Quirurgicas' WHERE i.codigo = 'Qx_GCHProg';
    UPDATE dbo.tmi_indicador SET formula_alias = N'A / B' WHERE codigo = 'Qx_GCHProg';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'Qx_RendSO' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'Qx_RendSO';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad' WHERE i.codigo = 'Qx_RendSO';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad' WHERE i.codigo = 'Qx_RendSO';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'C', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad' WHERE i.codigo = 'Qx_RendSO';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'D', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento' WHERE i.codigo = 'Qx_RendSO';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'E', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento' WHERE i.codigo = 'Qx_RendSO';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'F', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - Cirugías sin clasificación de complejidad' WHERE i.codigo = 'Qx_RendSO';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'G', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico -  Salas Quirúrgicas Funcionales' WHERE i.codigo = 'Qx_RendSO';
    UPDATE dbo.tmi_indicador SET formula_alias = N'(A + B + C + D + E + F) / G' WHERE codigo = 'Qx_RendSO';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'Qx_IntSusp' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'Qx_IntSusp';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - Operaciones Suspendidas' WHERE i.codigo = 'Qx_IntSusp';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Quirúrgico - Intervenc.Quirurgicas Programadas' WHERE i.codigo = 'Qx_IntSusp';
    UPDATE dbo.tmi_indicador SET formula_alias = N'A / B' WHERE codigo = 'Qx_IntSusp';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'Qx_HTCesareas' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'Qx_HTCesareas';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Obstétrico - Cesáreas' WHERE i.codigo = 'Qx_HTCesareas';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Centro Obstétrico - Total de Partos' WHERE i.codigo = 'Qx_HTCesareas';
    UPDATE dbo.tmi_indicador SET formula_alias = N'A / B' WHERE codigo = 'Qx_HTCesareas';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'Em_PrioIV_V' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'Em_PrioIV_V';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Emergencia - Prioridad IV' WHERE i.codigo = 'Em_PrioIV_V';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Emergencia - Prioridad V' WHERE i.codigo = 'Em_PrioIV_V';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'C', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Emergencia - Total de Atenciones' WHERE i.codigo = 'Em_PrioIV_V';
    UPDATE dbo.tmi_indicador SET formula_alias = N'(A + B) / C' WHERE codigo = 'Em_PrioIV_V';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'Em_PrioI_II' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'Em_PrioI_II';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Emergencia - Prioridad I' WHERE i.codigo = 'Em_PrioI_II';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Emergencia - Prioridad II' WHERE i.codigo = 'Em_PrioI_II';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'C', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Emergencia - Total de Atenciones' WHERE i.codigo = 'Em_PrioI_II';
    UPDATE dbo.tmi_indicador SET formula_alias = N'(A + B) / C' WHERE codigo = 'Em_PrioI_II';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'O_Concent' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'O_Concent';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Odontología - Sesiones Odontológicas' WHERE i.codigo = 'O_Concent';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Odontología - Consultantes de Odontología' WHERE i.codigo = 'O_Concent';
    UPDATE dbo.tmi_indicador SET formula_alias = N'A / B' WHERE codigo = 'O_Concent';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'O_HrOdont' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'O_HrOdont';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Odontología - Sesiones Odontológicas' WHERE i.codigo = 'O_HrOdont';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Odontología - Horas Odontológicas Efectivas' WHERE i.codigo = 'O_HrOdont';
    UPDATE dbo.tmi_indicador SET formula_alias = N'A / B' WHERE codigo = 'O_HrOdont';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'O_GCHOdon' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'O_GCHOdon';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Odontología - Horas Odontológicas Efectivas' WHERE i.codigo = 'O_GCHOdon';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Odontología - Horas Odontológicas Programadas' WHERE i.codigo = 'O_GCHOdon';
    UPDATE dbo.tmi_indicador SET formula_alias = N'A / B' WHERE codigo = 'O_GCHOdon';
END
IF EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE codigo = 'O_NTOdontS' AND formula_alias IS NULL)
BEGIN
    DELETE iv FROM dbo.tmi_indicador_variable iv JOIN dbo.tmi_indicador i ON i.id = iv.id_indicador WHERE i.codigo = 'O_NTOdontS';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'A', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Odontología - Trabajos Odontológicos' WHERE i.codigo = 'O_NTOdontS';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'B', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Odontología - Diagnóstico por imágenes' WHERE i.codigo = 'O_NTOdontS';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'C', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Odontología - Procedimientos Especiales' WHERE i.codigo = 'O_NTOdontS';
    INSERT INTO dbo.tmi_indicador_variable (id_indicador, letra, id_variable) SELECT i.id, 'D', v.id FROM dbo.tmi_indicador i JOIN dbo.tmi_variable v ON v.nombre = N'Odontología - Sesiones Odontológicas' WHERE i.codigo = 'O_NTOdontS';
    UPDATE dbo.tmi_indicador SET formula_alias = N'(A + B + C) / D' WHERE codigo = 'O_NTOdontS';
END
GO

/* ---------- Estándares específicos de centro (notas de la hoja Estándares del Excel y cartas o directivas) ---------- */
-- La columna del indicador se llama id_indicador (indicador_estandar.sql / centros_tmi.sql) o id_estandar (tablas antiguas)
DECLARE @col SYSNAME = CASE WHEN COL_LENGTH('dbo.tmi_centro_estandar', 'id_indicador') IS NOT NULL THEN 'id_indicador' ELSE 'id_estandar' END,
        @s NVARCHAR(MAX);
SET @s = REPLACE(N'IF NOT EXISTS (SELECT 1 FROM dbo.tmi_centro_estandar WHERE codcentro = ''19'' AND #COL# = 4 AND anio = 2026) INSERT INTO dbo.tmi_centro_estandar (id_centro, codcentro, #COL#, anio, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, aplica, acept, sustento) SELECT (SELECT MIN(id_centro) FROM dbo.vw_tmi_centro_base WHERE codcentro = 19), ''19'', 4, 2026, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 1, 2.5, ''Nota hoja Estándares: Pol. Ancije 2.5'';', '#COL#', @col); EXEC sp_executesql @s;
SET @s = REPLACE(N'IF NOT EXISTS (SELECT 1 FROM dbo.tmi_centro_estandar WHERE codcentro = ''701'' AND #COL# = 4 AND anio = 2026) INSERT INTO dbo.tmi_centro_estandar (id_centro, codcentro, #COL#, anio, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, aplica, acept, sustento) SELECT (SELECT MIN(id_centro) FROM dbo.vw_tmi_centro_base WHERE codcentro = 701), ''701'', 4, 2026, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, NULL, ''Carta N° 2223-OCPD-EsSalud-2008 (nota hoja Estándares)'';', '#COL#', @col); EXEC sp_executesql @s;
SET @s = REPLACE(N'IF NOT EXISTS (SELECT 1 FROM dbo.tmi_centro_estandar WHERE codcentro = ''507'' AND #COL# = 5 AND anio = 2026) INSERT INTO dbo.tmi_centro_estandar (id_centro, codcentro, #COL#, anio, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, aplica, acept, sustento) SELECT (SELECT MIN(id_centro) FROM dbo.vw_tmi_centro_base WHERE codcentro = 507), ''507'', 5, 2026, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 1, 19.4, ''Nota hoja Estándares: estancia 16.2'';', '#COL#', @col); EXEC sp_executesql @s;
SET @s = REPLACE(N'IF NOT EXISTS (SELECT 1 FROM dbo.tmi_centro_estandar WHERE codcentro = ''507'' AND #COL# = 8 AND anio = 2026) INSERT INTO dbo.tmi_centro_estandar (id_centro, codcentro, #COL#, anio, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, aplica, acept, sustento) SELECT (SELECT MIN(id_centro) FROM dbo.vw_tmi_centro_base WHERE codcentro = 507), ''507'', 8, 2026, 1.74, 1.74, 1.74, 1.74, 1.74, 1.74, 1.74, 1.74, 1.74, 1.74, 1.74, 1.74, 1, 1.39, ''Carta N° 3002-OCPD-EsSalud-2009'';', '#COL#', @col); EXEC sp_executesql @s;
SET @s = REPLACE(N'IF NOT EXISTS (SELECT 1 FROM dbo.tmi_centro_estandar WHERE codcentro = ''507'' AND #COL# = 9 AND anio = 2026) INSERT INTO dbo.tmi_centro_estandar (id_centro, codcentro, #COL#, anio, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, aplica, acept, sustento) SELECT (SELECT MIN(id_centro) FROM dbo.vw_tmi_centro_base WHERE codcentro = 507), ''507'', 9, 2026, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 1, 0.2, ''Nota hoja Estándares: mortalidad 20%'';', '#COL#', @col); EXEC sp_executesql @s;
SET @s = REPLACE(N'IF NOT EXISTS (SELECT 1 FROM dbo.tmi_centro_estandar WHERE codcentro = ''701'' AND #COL# = 2 AND anio = 2026) INSERT INTO dbo.tmi_centro_estandar (id_centro, codcentro, #COL#, anio, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, aplica, acept, sustento) SELECT (SELECT MIN(id_centro) FROM dbo.vw_tmi_centro_base WHERE codcentro = 701), ''701'', 2, 2026, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, NULL, ''CNSR - Directiva N° 06-GCOP-ESSALUD-2016'';', '#COL#', @col); EXEC sp_executesql @s;
SET @s = REPLACE(N'IF NOT EXISTS (SELECT 1 FROM dbo.tmi_centro_estandar WHERE codcentro = ''700'' AND #COL# = 2 AND anio = 2026) INSERT INTO dbo.tmi_centro_estandar (id_centro, codcentro, #COL#, anio, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, aplica, acept, sustento) SELECT (SELECT MIN(id_centro) FROM dbo.vw_tmi_centro_base WHERE codcentro = 700), ''700'', 2, 2026, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, NULL, ''INCOR - Nota N° 000675-DIR-INCOR-ESSALUD-2025'';', '#COL#', @col); EXEC sp_executesql @s;
SET @s = REPLACE(N'IF NOT EXISTS (SELECT 1 FROM dbo.tmi_centro_estandar WHERE codcentro = ''702'' AND #COL# = 2 AND anio = 2026) INSERT INTO dbo.tmi_centro_estandar (id_centro, codcentro, #COL#, anio, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, aplica, acept, sustento) SELECT (SELECT MIN(id_centro) FROM dbo.vw_tmi_centro_base WHERE codcentro = 702), ''702'', 2, 2026, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, NULL, ''IPO - TMI_ESTANDARES_D.csv'';', '#COL#', @col); EXEC sp_executesql @s;
-- Un centro sin estándar ya queda en NA (SIN_ESTANDAR): las filas "No aplica" de TMI_ESTANDARES_D.csv no hacen falta
DELETE FROM dbo.tmi_centro_estandar WHERE aplica = 0 AND sustento LIKE 'TMI_ESTANDARES_D.csv%';
GO


/* ---------- Tablas maestras de estándares: tipos y claves (solo agrega lo que falta) ---------- */
INSERT INTO dbo.tmi_tipo_estandar (codigo, descripcion, orden)
SELECT v.codigo, v.descripcion, v.orden
FROM (VALUES ('NIVEL', 'Nivel', 1), ('NIVEL_TIPO', 'Nivel y Tipo', 2), ('TIPO', 'Tipo', 3), ('CATEGORIA', 'Categoría', 4)) v(codigo, descripcion, orden)
WHERE NOT EXISTS (SELECT 1 FROM dbo.tmi_tipo_estandar t WHERE t.codigo = v.codigo);

INSERT INTO dbo.tmi_estandar (tipo_estandar, orden, fuente, clave, descripcion, prioridad)
SELECT v.tipo_estandar, v.orden, v.fuente, v.clave, v.descripcion, v.prioridad
FROM (VALUES
    ('NIVEL', 1, 'NIVEL', 'I', 'I', 1),
    ('NIVEL', 2, 'NIVEL', 'II', 'II', 1),
    ('NIVEL', 3, 'NIVEL', 'III', 'III', 1),
    ('NIVEL_TIPO', 1, 'NIVEL', 'I', 'I', 1),
    ('NIVEL_TIPO', 2, 'NIVEL', 'II', 'II', 1),
    ('NIVEL_TIPO', 3, 'NIVEL', 'III', 'III', 1),
    ('NIVEL_TIPO', 4, 'TIPO', 'CNSR', 'CNSR', 2),
    ('NIVEL_TIPO', 5, 'TIPO', 'IPO', 'IPO', 2),
    ('NIVEL_TIPO', 6, 'TIPO', 'INCOR', 'INCOR', 2),
    ('TIPO', 1, 'TIPO', 'H.N.', 'H.N.', 1),
    ('TIPO', 2, 'TIPO', 'H.IV', 'H.IV', 1),
    ('TIPO', 3, 'TIPO', 'H.III', 'H.III', 1),
    ('TIPO', 4, 'TIPO', 'H.II', 'H.II', 1),
    ('TIPO', 5, 'TIPO', 'H.I', 'H.I', 1),
    ('TIPO', 6, 'TIPO', 'POL.', 'POL.', 1),
    ('TIPO', 7, 'TIPO', 'C.M.', 'C.M.', 1),
    ('TIPO', 8, 'TIPO', 'P.M.', 'P.M.', 1),
    ('TIPO', 9, 'TIPO', 'CNSR', 'CNSR', 1),
    ('TIPO', 10, 'TIPO', 'IPO', 'IPO', 1),
    ('TIPO', 11, 'TIPO', 'INCOR', 'INCOR', 1),
    ('CATEGORIA', 1, 'CATEGORIA', 'H.N.', 'H.N.', 1),
    ('CATEGORIA', 2, 'CATEGORIA', 'H.IV', 'H.IV', 1),
    ('CATEGORIA', 3, 'CATEGORIA', 'H.III', 'H.III', 1),
    ('CATEGORIA', 4, 'CATEGORIA', 'H.II', 'H.II', 1),
    ('CATEGORIA', 5, 'CATEGORIA', 'H.I', 'H.I', 1),
    ('CATEGORIA', 6, 'CATEGORIA', 'POL.', 'POL.', 1),
    ('CATEGORIA', 7, 'CATEGORIA', 'C.A.P.III', 'C.A.P.III', 1),
    ('CATEGORIA', 8, 'CATEGORIA', 'C.A.P.II', 'C.A.P.II', 1),
    ('CATEGORIA', 9, 'CATEGORIA', 'C.A.P.I', 'C.A.P.I', 1),
    ('CATEGORIA', 10, 'CATEGORIA', 'C.M.', 'C.M.', 1),
    ('CATEGORIA', 11, 'CATEGORIA', 'P.M.', 'P.M.', 1),
    ('CATEGORIA', 12, 'CATEGORIA', 'CNSR', 'CNSR', 1),
    ('CATEGORIA', 13, 'CATEGORIA', 'IPO', 'IPO', 1),
    ('CATEGORIA', 14, 'CATEGORIA', 'INCOR', 'INCOR', 1)
) v(tipo_estandar, orden, fuente, clave, descripcion, prioridad)
WHERE NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar e
                  WHERE e.tipo_estandar = v.tipo_estandar AND e.fuente = v.fuente AND e.clave = v.clave);
GO

-- Los niveles se muestran como I, II y III (la carga anterior los llamaba N1, N2 y N3)
UPDATE dbo.tmi_estandar SET descripcion = clave
WHERE fuente = 'NIVEL' AND descripcion IN ('N1', 'N2', 'N3') AND clave IN ('I', 'II', 'III');
GO

-- base_estandar del indicador -> tmi_tipo_estandar.codigo. Se crea cuando todos los indicadores usan un tipo del
-- catálogo (si no, usp_tmi_validar_config lo informa).
IF OBJECT_ID('dbo.FK_tmi_indicador_base_estandar') IS NULL
   AND NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador i
                   WHERE i.base_estandar IS NOT NULL
                     AND NOT EXISTS (SELECT 1 FROM dbo.tmi_tipo_estandar t WHERE t.codigo = i.base_estandar))
    EXEC (N'ALTER TABLE dbo.tmi_indicador ADD CONSTRAINT FK_tmi_indicador_base_estandar
            FOREIGN KEY (base_estandar) REFERENCES dbo.tmi_tipo_estandar (codigo)');
GO

/* ---------- Estándares de cada indicador por Nivel / Categoría / Tipo y por Periodo (inicializados desde vw_tmi_std) ---------- */
IF OBJECT_ID('dbo.tmi_indicador_estandar') IS NOT NULL
   AND NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador_estandar)
BEGIN
    INSERT INTO dbo.tmi_indicador_estandar (id_indicador, nivel, categoria, tipo, periodo_desde, periodo_hasta, estandar, activo)
    SELECT s.id_estandar,
           CASE WHEN s.fuente = 'NIVEL'     THEN s.clave END AS nivel,
           CASE WHEN s.fuente = 'CATEGORIA' THEN s.clave END AS categoria,
           CASE WHEN s.fuente = 'TIPO'      THEN s.clave END AS tipo,
           ISNULL(s.anio, 2026) * 100 + 1 AS periodo_desde,
           ISNULL(s.anio, 2026) * 100 + 12 AS periodo_hasta,
           COALESCE(s.m08, s.m01, s.m07, s.m06) AS estandar,
           1
    FROM dbo.vw_tmi_std s
    JOIN dbo.tmi_indicador i ON i.id = s.id_estandar
    WHERE COALESCE(s.m08, s.m01, s.m07, s.m06, 0) > 0
      AND ((s.fuente = 'NIVEL'     AND i.base_estandar LIKE '%NIVEL%')
        OR (s.fuente = 'TIPO'      AND i.base_estandar LIKE '%TIPO%')
        OR (s.fuente = 'CATEGORIA' AND i.base_estandar LIKE '%CATEGORIA%'));
END
GO


/* ---------- Catálogos de centro: nivel_centro, tipo_centro y categoria_centro (solo agrega lo que falta) ----------
   codigo = valor que se guarda en tmi_centro (nivel, tipo, categoria); orden = orden en filtros y listas. */
INSERT INTO dbo.nivel_centro (codigo, descripcion, orden)
SELECT v.codigo, v.descripcion, v.orden
FROM (VALUES
    ('I',   'Primer nivel',  1),
    ('II',  'Segundo nivel', 2),
    ('III', 'Tercer nivel',  3)) v(codigo, descripcion, orden)
WHERE NOT EXISTS (SELECT 1 FROM dbo.nivel_centro n WHERE n.codigo = v.codigo);

INSERT INTO dbo.tipo_centro (codigo, descripcion, orden)
SELECT v.codigo, v.descripcion, v.orden
FROM (VALUES
    ('CNSR',  'Centro Nacional de Salud Renal',    1),
    ('IPO',   'IPO',                               2),
    ('INCOR', 'Instituto Nacional Cardiovascular', 3),
    ('H.N.',  'Hospital Nacional',                 4),
    ('H.IV',  'Hospital IV',                       5),
    ('H.III', 'Hospital III',                      6),
    ('H.II',  'Hospital II',                       7),
    ('H.I',   'Hospital I',                        8),
    ('POL.',  'Policlínico',                       9),
    ('C.M.',  'Centro Médico',                     10),
    ('P.M.',  'Posta Médica',                      11)) v(codigo, descripcion, orden)
WHERE NOT EXISTS (SELECT 1 FROM dbo.tipo_centro t WHERE t.codigo = v.codigo);


