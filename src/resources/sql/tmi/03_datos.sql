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
UPDATE dbo.tmi_indicador SET codigo = 'CE_Concent', nombre_hoja = 'C.E_Concent.', titulo_hoja = 'CONCENTRACION DE CONSULTAS', orden = 1, tipo_calculo = 'ACUMULADO', sin_datos_anio = 'NA', base_estandar = 'NIVEL', sentido = 'MENOR', decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 1 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 2) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (2, 1, 'Rendimiento Hora Medico', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'CE_RHrMedico', nombre_hoja = 'C.E_R.Hr.Medico', titulo_hoja = 'RENDIMIENTO HORA MEDICO', orden = 2, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'NIVEL_TIPO', sentido = 'MAYOR', decimales = 2, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 2 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 3) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (3, 1, 'Grado de Cumplimiento de Horas Programadas', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'CE_GCHProg', nombre_hoja = 'C.E_G.C.H.Prog', titulo_hoja = 'GRADO DE CUMPLIMIENTO DE HORAS PROGRAMADAS', orden = 3, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MAYOR', decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 3 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 4) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (4, 1, 'Promedio de Recetas por Consultas', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'CE_Recetas', nombre_hoja = 'C.E_Recetas', titulo_hoja = 'PROMEDIO DE RECETAS POR CONSULTAS', orden = 4, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MENOR', decimales = 2, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 4 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 5) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (5, 3, 'Promedio Dia Estancia', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'H_Estancias', nombre_hoja = 'H_Estancias', titulo_hoja = 'PROMEDIO DIA ESTANCIA', orden = 5, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MENOR', decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 5 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 6) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (6, 3, 'Porcentaje de Ocupación de Cama', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'H_OCama', nombre_hoja = 'H_% O.Cama', titulo_hoja = 'PORCENTAJE DE OCUPACIÓN DE CAMA', orden = 6, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'BANDA', decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 6 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 7) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (7, 3, 'Intervalo de Sustitución', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'H_ISust', nombre_hoja = 'H_I.Sust.', titulo_hoja = 'INTERVALO DE SUSTITUCIÓN', orden = 7, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MENOR', decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 7 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 8) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (8, 3, 'Rendimiento Cama', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'H_RCama', nombre_hoja = 'H_R.Cama', titulo_hoja = 'RENDIMIENTO CAMA', orden = 8, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MAYOR', decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 8 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 9) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (9, 3, 'Tasa Neta de Mortalidad Hospitalaria', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'H_TBMHosp', nombre_hoja = 'H_T.B.M.Hosp', titulo_hoja = 'TASA NETA DE MORTALIDAD HOSPITALARIA', orden = 9, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MENOR', decimales = NULL, cero_es_logro = 1, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 9 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 10) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (10, 6, 'Porcentaje de Intervenciones Menores', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'Qx_IMenor', nombre_hoja = 'Qx_I.Menor', titulo_hoja = 'PORCENTAJE DE INTERVENCIONES MENORES', orden = 10, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MENOR', decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 10 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 11) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (11, 6, 'Porcentaje de Intervenciones de Alta Complejidad', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'Qx_IAlta', nombre_hoja = 'Qx_I.Alta', titulo_hoja = 'PORCENTAJE DE INTERVENCIONES DE ALTA COMPLEJIDAD', orden = 11, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MAYOR', decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 11 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 12) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (12, 6, 'Porcentaje de Horas Quirúrgicas Efectivas', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'Qx_GCHProg', nombre_hoja = 'Qx_G.C.H.Prog', titulo_hoja = 'PORCENTAJE DE HORAS QUIRÚRGICAS EFECTIVAS', orden = 12, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MAYOR', decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 12 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 13) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (13, 6, 'Rendimiento de Sala de Operaciones', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'Qx_RendSO', nombre_hoja = 'Qx_Rend.SO', titulo_hoja = 'RENDIMIENTO DE SALA DE OPERACIONES', orden = 13, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MAYOR', decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 13 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 14) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (14, 6, 'Porcentaje de Operaciones Suspendidas', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'Qx_IntSusp', nombre_hoja = 'Qx.Int.Susp', titulo_hoja = 'PORCENTAJE DE OPERACIONES SUSPENDIDAS', orden = 14, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MENOR', decimales = NULL, cero_es_logro = 1, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 14 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 15) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (15, 6, 'Tasa de Cesáreas', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'Qx_HTCesareas', nombre_hoja = 'H_T.Cesareas', titulo_hoja = 'TASA DE CESÁREAS', orden = 15, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MENOR', decimales = NULL, cero_es_logro = 1, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 15 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 16) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (16, 8, '% Prioridad IV y V con respecto al Total de Emergencias', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'Em_PrioIV_V', nombre_hoja = 'Em_Prio.IV_V', titulo_hoja = '% PRIORIDAD IV Y V CON RESPECTO AL TOTAL DE EMERGENCIAS', orden = 16, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MENOR', decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 16 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 17) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (17, 8, '% Prioridad I y II con respecto al Total de Emergencias', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'Em_PrioI_II', nombre_hoja = 'Em_Prio.I_II', titulo_hoja = '% PRIORIDAD I Y II CON RESPECTO AL TOTAL DE EMERGENCIAS', orden = 17, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MAYOR', decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 17 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 18) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (18, 19, 'Concentración de Sesiones Odontológicas', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'O_Concent', nombre_hoja = 'O_Concent.', titulo_hoja = 'CONCENTRACIÓN DE SESIONES ODONTOLÓGICAS', orden = 18, tipo_calculo = 'ACUMULADO', sin_datos_anio = 'NA', base_estandar = 'NIVEL', sentido = 'MENOR', decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 18 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 19) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (19, 19, 'Rendimiento Hora Odontológica', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'O_HrOdont', nombre_hoja = 'O_Hr.Odont', titulo_hoja = 'RENDIMIENTO HORA ODONTOLÓGICA', orden = 19, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'NIVEL_TIPO', sentido = 'MAYOR', decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 19 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 20) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (20, 19, 'Grado de Cumplimiento de Hora Odontólogo', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'O_GCHOdon', nombre_hoja = 'O_G.C.H.Odon', titulo_hoja = 'GRADO DE CUMPLIMIENTO DE HORA ODONTÓLOGO', orden = 20, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MAYOR', decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1, formato = 'PORCENTAJE' WHERE id = 20 AND codigo IS NULL;
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador WHERE id = 21) INSERT INTO dbo.tmi_indicador (id, grupo, indicador, fecha_creacion) VALUES (21, 19, 'Número de trabajos Odontológicos por Sesión', GETDATE());
UPDATE dbo.tmi_indicador SET codigo = 'O_NTOdontS', nombre_hoja = 'O_N.T.Odont.S', titulo_hoja = 'NÚMERO DE TRABAJOS ODONTOLÓGICOS POR SESIÓN', orden = 21, tipo_calculo = 'MENSUAL', sin_datos_anio = 'NA', base_estandar = 'TIPO', sentido = 'MAYOR', decimales = NULL, cero_es_logro = 0, mostrar_no_aplica = 1, activo = 1 WHERE id = 21 AND codigo IS NULL;
SET IDENTITY_INSERT dbo.tmi_indicador OFF;

/* % Acept inicial de cada indicador (tmi_indicador_acept, fila del año actual; los años siguientes copian su fijo).
   Solo para indicadores que aún no tienen ninguna fila. En banda, aceptmenos_fijo = el mismo % hacia abajo. */
INSERT INTO dbo.tmi_indicador_acept (id_indicador, anio, tipo_acept, acept_fijo, aceptmenos_fijo)
SELECT v.id, YEAR(GETDATE()), v.tipo_acept, v.acept, v.aceptmenos
FROM (VALUES
    (1, 'REL', 0.1, NULL),
    (2, 'REL', 0.1, NULL),
    (3, 'REL', 0.05, NULL),
    (4, 'REL', 0.1, NULL),
    (5, 'REL', 0.2, NULL),
    (6, 'ABS', 0.05, 0.05),
    (7, 'REL', 0.2, NULL),
    (8, 'REL', 0.2, NULL),
    (9, 'REL', 0.1, NULL),
    (10, 'REL', 0.2, NULL),
    (11, 'REL', 0.2, NULL),
    (12, 'ABS', 0.1, NULL),
    (13, 'REL', 0.1, NULL),
    (14, 'REL', 0.1, NULL),
    (15, 'REL', 0.1, NULL),
    (16, 'REL', 0.2, NULL),
    (17, 'REL', 0.1, NULL),
    (18, 'REL', 0.1, NULL),
    (19, 'REL', 0.1, NULL),
    (20, 'REL', 0.05, NULL),
    (21, 'REL', 0.1, NULL)) v(id, tipo_acept, acept, aceptmenos)
JOIN dbo.tmi_indicador i ON i.id = v.id
WHERE NOT EXISTS (SELECT 1 FROM dbo.tmi_indicador_acept a WHERE a.id_indicador = v.id);
GO

/* ---------- Fórmula de cada indicador (términos de TOTALIZADO3, como la columna de fórmulas de TMI_SQL) ----------
   Los términos y la expresión SQL no se guardan: el backend los lee de esta columna cada vez que calcula. */
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

/* ---------- Fórmula con letras y la variable de cada letra ----------
   Solo si el indicador todavía no tiene formula_alias. formula_variable es la misma fórmula con el id de la variable de
   cada letra entre llaves: A / B con A = variable 1 y B = variable 2 -> {1} / {2}. Si falta alguna variable, el
   indicador queda sin fórmula con letras. */
CREATE TABLE #letra_ini (codigo VARCHAR(20), letra CHAR(1), variable NVARCHAR(200));
INSERT INTO #letra_ini (codigo, letra, variable) VALUES
    ('CE_Concent', 'A', N'Consulta Externa - Consultas'),
    ('CE_Concent', 'B', N'Consulta Externa - Consultantes al Establecimiento'),
    ('CE_RHrMedico', 'A', N'Consulta Externa - Consultas'),
    ('CE_RHrMedico', 'B', N'Consulta Externa - Horas Médicas Efectivas'),
    ('CE_GCHProg', 'A', N'Consulta Externa - Horas Médicas Efectivas'),
    ('CE_GCHProg', 'B', N'Consulta Externa - Horas Médicas Programadas'),
    ('CE_Recetas', 'A', N'Actividades Intermedias - Recetas Despachadas de C. E'),
    ('CE_Recetas', 'B', N'Consulta Externa - Consultas'),
    ('H_Estancias', 'A', N'Hospitalizacion - Estancias'),
    ('H_Estancias', 'B', N'Hospitalizacion - Egresos'),
    ('H_OCama', 'A', N'Hospitalizacion - Pacientes Días'),
    ('H_OCama', 'B', N'Hospitalizacion - Días Cama Disponible'),
    ('H_ISust', 'A', N'Hospitalizacion - Días Cama Disponible'),
    ('H_ISust', 'B', N'Hospitalizacion - Pacientes Días'),
    ('H_ISust', 'C', N'Hospitalizacion - Egresos'),
    ('H_RCama', 'A', N'Hospitalizacion - Egresos'),
    ('H_RCama', 'B', N'Hospitalizacion -  Camas Hospitalarias'),
    ('H_TBMHosp', 'A', N'Hospitalizacion - Defunciones después de 48 horas'),
    ('H_TBMHosp', 'B', N'Hospitalizacion - Egresos'),
    ('H_TBMHosp', 'C', N'Hospitalizacion - Defunciones antes de 48 horas'),
    ('Qx_IMenor', 'A', N'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento'),
    ('Qx_IMenor', 'B', N'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'),
    ('Qx_IMenor', 'C', N'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad'),
    ('Qx_IMenor', 'D', N'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad'),
    ('Qx_IMenor', 'E', N'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad'),
    ('Qx_IMenor', 'F', N'Centro Quirúrgico - Cirugías sin clasificación de complejidad'),
    ('Qx_IAlta', 'A', N'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad'),
    ('Qx_IAlta', 'B', N'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad'),
    ('Qx_IAlta', 'C', N'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad'),
    ('Qx_IAlta', 'D', N'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento'),
    ('Qx_IAlta', 'E', N'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'),
    ('Qx_IAlta', 'F', N'Centro Quirúrgico - Cirugías sin clasificación de complejidad'),
    ('Qx_GCHProg', 'A', N'Centro Quirúrgico - Horas Uso de Sala'),
    ('Qx_GCHProg', 'B', N'Centro Quirúrgico - Horas Programadas Intervenc.Quirurgicas'),
    ('Qx_RendSO', 'A', N'Centro Quirúrgico - A-Cirugía Mayor de Alta Complejidad'),
    ('Qx_RendSO', 'B', N'Centro Quirúrgico - B-Cirugía Mayor de Mediana Complejidad'),
    ('Qx_RendSO', 'C', N'Centro Quirúrgico - C-Cirugía Mayor de Baja Complejidad'),
    ('Qx_RendSO', 'D', N'Centro Quirúrgico - D-Cirugía Menor de Alto Requerimiento'),
    ('Qx_RendSO', 'E', N'Centro Quirúrgico - E-Cirugía Menor de Bajo Requerimiento'),
    ('Qx_RendSO', 'F', N'Centro Quirúrgico - Cirugías sin clasificación de complejidad'),
    ('Qx_RendSO', 'G', N'Centro Quirúrgico -  Salas Quirúrgicas Funcionales'),
    ('Qx_IntSusp', 'A', N'Centro Quirúrgico - Operaciones Suspendidas'),
    ('Qx_IntSusp', 'B', N'Centro Quirúrgico - Intervenc.Quirurgicas Programadas'),
    ('Qx_HTCesareas', 'A', N'Centro Obstétrico - Cesáreas'),
    ('Qx_HTCesareas', 'B', N'Centro Obstétrico - Total de Partos'),
    ('Em_PrioIV_V', 'A', N'Emergencia - Prioridad IV'),
    ('Em_PrioIV_V', 'B', N'Emergencia - Prioridad V'),
    ('Em_PrioIV_V', 'C', N'Emergencia - Total de Atenciones'),
    ('Em_PrioI_II', 'A', N'Emergencia - Prioridad I'),
    ('Em_PrioI_II', 'B', N'Emergencia - Prioridad II'),
    ('Em_PrioI_II', 'C', N'Emergencia - Total de Atenciones'),
    ('O_Concent', 'A', N'Odontología - Sesiones Odontológicas'),
    ('O_Concent', 'B', N'Odontología - Consultantes de Odontología'),
    ('O_HrOdont', 'A', N'Odontología - Sesiones Odontológicas'),
    ('O_HrOdont', 'B', N'Odontología - Horas Odontológicas Efectivas'),
    ('O_GCHOdon', 'A', N'Odontología - Horas Odontológicas Efectivas'),
    ('O_GCHOdon', 'B', N'Odontología - Horas Odontológicas Programadas'),
    ('O_NTOdontS', 'A', N'Odontología - Trabajos Odontológicos'),
    ('O_NTOdontS', 'B', N'Odontología - Diagnóstico por imágenes'),
    ('O_NTOdontS', 'C', N'Odontología - Procedimientos Especiales'),
    ('O_NTOdontS', 'D', N'Odontología - Sesiones Odontológicas');
CREATE TABLE #alias_ini (codigo VARCHAR(20), alias NVARCHAR(500), formula_variable NVARCHAR(500));
INSERT INTO #alias_ini (codigo, alias) VALUES
    ('CE_Concent', N'A / B'),
    ('CE_RHrMedico', N'A / B'),
    ('CE_GCHProg', N'A / B'),
    ('CE_Recetas', N'A / B'),
    ('H_Estancias', N'A / B'),
    ('H_OCama', N'A / B'),
    ('H_ISust', N'(A - B) / C'),
    ('H_RCama', N'A / B'),
    ('H_TBMHosp', N'A / (B - C)'),
    ('Qx_IMenor', N'(A + B) / (C + D + E + A + B + F)'),
    ('Qx_IAlta', N'A / (A + B + C + D + E + F)'),
    ('Qx_GCHProg', N'A / B'),
    ('Qx_RendSO', N'(A + B + C + D + E + F) / G'),
    ('Qx_IntSusp', N'A / B'),
    ('Qx_HTCesareas', N'A / B'),
    ('Em_PrioIV_V', N'(A + B) / C'),
    ('Em_PrioI_II', N'(A + B) / C'),
    ('O_Concent', N'A / B'),
    ('O_HrOdont', N'A / B'),
    ('O_GCHOdon', N'A / B'),
    ('O_NTOdontS', N'(A + B + C) / D');
UPDATE #alias_ini SET formula_variable = alias;
DECLARE @letra CHAR(1) = 'A';
WHILE @letra <= 'Z'
BEGIN
    UPDATE a SET formula_variable = REPLACE(a.formula_variable COLLATE Latin1_General_BIN, @letra, N'{' + CAST(v.id AS NVARCHAR(10)) + N'}')
    FROM #alias_ini a
    JOIN #letra_ini l ON l.codigo = a.codigo AND l.letra = @letra
    JOIN dbo.tmi_variable v ON v.nombre = l.variable;
    SET @letra = CHAR(ASCII(@letra) + 1);
END
UPDATE i SET formula_alias = a.alias, formula_variable = a.formula_variable
FROM dbo.tmi_indicador i JOIN #alias_ini a ON a.codigo = i.codigo
WHERE i.formula_alias IS NULL AND PATINDEX(N'%[A-Z]%', a.formula_variable COLLATE Latin1_General_BIN) = 0;
DROP TABLE #letra_ini;
DROP TABLE #alias_ini;
GO

/* ---------- Estándares específicos de centro (notas de la hoja Estándares del Excel y cartas o directivas) ---------- */
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar_centro WHERE codcentro = '19' AND id_indicador = 4 AND anio = 2026) INSERT INTO dbo.tmi_estandar_centro (id_centro, codcentro, id_indicador, anio, est_fijo, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, aplica, sustento) SELECT (SELECT MIN(id_centro) FROM dbo.vw_tmi_centro_base WHERE codcentro = 19), '19', 4, 2026, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 1, 'Nota hoja Estándares: Pol. Ancije 2.5';
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar_centro WHERE codcentro = '701' AND id_indicador = 4 AND anio = 2026) INSERT INTO dbo.tmi_estandar_centro (id_centro, codcentro, id_indicador, anio, est_fijo, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, aplica, sustento) SELECT (SELECT MIN(id_centro) FROM dbo.vw_tmi_centro_base WHERE codcentro = 701), '701', 4, 2026, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 'Carta N° 2223-OCPD-EsSalud-2008 (nota hoja Estándares)';
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar_centro WHERE codcentro = '507' AND id_indicador = 5 AND anio = 2026) INSERT INTO dbo.tmi_estandar_centro (id_centro, codcentro, id_indicador, anio, est_fijo, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, aplica, sustento) SELECT (SELECT MIN(id_centro) FROM dbo.vw_tmi_centro_base WHERE codcentro = 507), '507', 5, 2026, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 1, 'Nota hoja Estándares: estancia 16.2';
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar_centro WHERE codcentro = '507' AND id_indicador = 8 AND anio = 2026) INSERT INTO dbo.tmi_estandar_centro (id_centro, codcentro, id_indicador, anio, est_fijo, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, aplica, sustento) SELECT (SELECT MIN(id_centro) FROM dbo.vw_tmi_centro_base WHERE codcentro = 507), '507', 8, 2026, 1.74, 1.74, 1.74, 1.74, 1.74, 1.74, 1.74, 1.74, 1.74, 1.74, 1.74, 1.74, 1.74, 1, 'Carta N° 3002-OCPD-EsSalud-2009';
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar_centro WHERE codcentro = '507' AND id_indicador = 9 AND anio = 2026) INSERT INTO dbo.tmi_estandar_centro (id_centro, codcentro, id_indicador, anio, est_fijo, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, aplica, sustento) SELECT (SELECT MIN(id_centro) FROM dbo.vw_tmi_centro_base WHERE codcentro = 507), '507', 9, 2026, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 1, 'Nota hoja Estándares: mortalidad 20%';
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar_centro WHERE codcentro = '701' AND id_indicador = 2 AND anio = 2026) INSERT INTO dbo.tmi_estandar_centro (id_centro, codcentro, id_indicador, anio, est_fijo, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, aplica, sustento) SELECT (SELECT MIN(id_centro) FROM dbo.vw_tmi_centro_base WHERE codcentro = 701), '701', 2, 2026, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 'CNSR - Directiva N° 06-GCOP-ESSALUD-2016';
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar_centro WHERE codcentro = '700' AND id_indicador = 2 AND anio = 2026) INSERT INTO dbo.tmi_estandar_centro (id_centro, codcentro, id_indicador, anio, est_fijo, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, aplica, sustento) SELECT (SELECT MIN(id_centro) FROM dbo.vw_tmi_centro_base WHERE codcentro = 700), '700', 2, 2026, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 'INCOR - Nota N° 000675-DIR-INCOR-ESSALUD-2025';
IF NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar_centro WHERE codcentro = '702' AND id_indicador = 2 AND anio = 2026) INSERT INTO dbo.tmi_estandar_centro (id_centro, codcentro, id_indicador, anio, est_fijo, est_01, est_02, est_03, est_04, est_05, est_06, est_07, est_08, est_09, est_10, est_11, est_12, aplica, sustento) SELECT (SELECT MIN(id_centro) FROM dbo.vw_tmi_centro_base WHERE codcentro = 702), '702', 2, 2026, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 'IPO - TMI_ESTANDARES_D.csv';
GO


/* ---------- Tablas maestras de estándares: tipos y claves ----------
   Fuente NIVEL = tmi_centro.nivel (I, II, III, catálogo tmi_nivel_centro).
   Fuente TIPO  = tmi_centro.nivel_estandar (H.N. ... P.M., CNSR, IPO, INCOR, catálogo tmi_nivel_estandar_centro).
   tmi_centro.tipo ya no se usa para unir estándares. */
INSERT INTO dbo.tmi_tipo_estandar (codigo, descripcion, orden)
SELECT v.codigo, v.descripcion, v.orden
FROM (VALUES ('NIVEL', 'Nivel', 1), ('NIVEL_TIPO', 'Nivel y Tipo', 2), ('TIPO', 'Tipo', 3), ('CATEGORIA', 'Categoría', 4)) v(codigo, descripcion, orden)
WHERE NOT EXISTS (SELECT 1 FROM dbo.tmi_tipo_estandar t WHERE t.codigo = v.codigo);
GO

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
    -- fuente TIPO = tmi_centro.nivel_estandar (catálogo tmi_nivel_estandar_centro)
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

-- orden de las claves como los catálogos
UPDATE e SET orden = v.orden
FROM dbo.tmi_estandar e
JOIN (VALUES ('H.N.', 1), ('H.IV', 2), ('H.III', 3), ('H.II', 4), ('H.I', 5), ('POL.', 6), ('C.M.', 7), ('P.M.', 8), ('CNSR', 9), ('IPO', 10), ('INCOR', 11)) v(clave, orden)
  ON e.tipo_estandar = 'TIPO' AND e.fuente = 'TIPO' AND e.clave = v.clave AND e.orden <> v.orden;
UPDATE e SET orden = v.orden
FROM dbo.tmi_estandar e
JOIN (VALUES ('NIVEL', 'I', 1), ('NIVEL', 'II', 2), ('NIVEL', 'III', 3), ('TIPO', 'CNSR', 4), ('TIPO', 'IPO', 5), ('TIPO', 'INCOR', 6)) v(fuente, clave, orden)
  ON e.tipo_estandar = 'NIVEL_TIPO' AND e.fuente = v.fuente AND e.clave = v.clave AND e.orden <> v.orden;
GO

/* Claves de los estándares = valores de los centros: Nivel = catálogo tmi_nivel_centro (tmi_centro.nivel) y
   Tipo = catálogo tmi_nivel_estandar_centro (tmi_centro.nivel_estandar). Un código nuevo del catálogo aparece solo en
   la pestaña Estándares (sin valor: los centros con esa clave quedan sin estándar hasta cargarlo). En Nivel y Tipo,
   la parte Tipo son solo los institutos (CNSR, IPO, INCOR), que ganan sobre el nivel. */
INSERT INTO dbo.tmi_estandar (tipo_estandar, orden, fuente, clave, descripcion, prioridad)
SELECT t.tipo_estandar, 100 + n.orden, 'NIVEL', n.codigo, n.codigo, 1
FROM dbo.tmi_nivel_centro n
CROSS JOIN (VALUES ('NIVEL'), ('NIVEL_TIPO')) t(tipo_estandar)
WHERE NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar e
                  WHERE e.tipo_estandar = t.tipo_estandar AND e.fuente = 'NIVEL' AND e.clave = n.codigo);

INSERT INTO dbo.tmi_estandar (tipo_estandar, orden, fuente, clave, descripcion, prioridad)
SELECT 'TIPO', 100 + c.orden, 'TIPO', c.codigo, c.codigo, 1
FROM dbo.tmi_nivel_estandar_centro c
WHERE NOT EXISTS (SELECT 1 FROM dbo.tmi_estandar e
                  WHERE e.tipo_estandar = 'TIPO' AND e.fuente = 'TIPO' AND e.clave = c.codigo);
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


/* ---------- Catálogos de centro (solo agrega lo que falta) ----------
   codigo = valor que se guarda en tmi_centro; orden = orden en filtros y listas.
     tmi_nivel_centro          -> tmi_centro.nivel (I, II, III): une el centro con los estándares de fuente NIVEL
     tmi_nivel_estandar_centro -> tmi_centro.nivel_estandar: une el centro con los estándares de fuente TIPO
     tmi_tipo_centro           -> tmi_centro.tipo: informativo (ya no une estándares)
   El cálculo une por nivel y nivel_estandar; la categoría no tiene catálogo. */
INSERT INTO dbo.tmi_nivel_centro (codigo, descripcion, orden)
SELECT v.codigo, v.descripcion, v.orden
FROM (VALUES ('I', 'Primer nivel', 1), ('II', 'Segundo nivel', 2), ('III', 'Tercer nivel', 3)) v(codigo, descripcion, orden)
WHERE NOT EXISTS (SELECT 1 FROM dbo.tmi_nivel_centro n WHERE n.codigo = v.codigo);

INSERT INTO dbo.tmi_nivel_estandar_centro (codigo, descripcion, orden)
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
WHERE NOT EXISTS (SELECT 1 FROM dbo.tmi_nivel_estandar_centro n WHERE n.codigo = v.codigo);

INSERT INTO dbo.tmi_tipo_centro (codigo, descripcion, orden)
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
    ('P.M.',  'Posta Médica',                      11),
    -- tmi_centro.tipo ahora guarda también las categorías C.A.P. (antes en categoria)
    ('C.A.P.III', 'C.A.P. III',                    12),
    ('C.A.P.II',  'C.A.P. II',                     13),
    ('C.A.P.I',   'C.A.P. I',                      14)) v(codigo, descripcion, orden)
WHERE NOT EXISTS (SELECT 1 FROM dbo.tmi_tipo_centro t WHERE t.codigo = v.codigo);

GO

/* ---------- % Acept hacia abajo en banda: se guarda siempre ----------
   Un indicador que pasa a banda puede tener vacío el % hacia abajo: toma el mismo % que hacia arriba. */
UPDATE a
SET    aceptmenos_fijo = ISNULL(a.aceptmenos_fijo, a.acept_fijo),
       aceptmenos_01 = ISNULL(a.aceptmenos_01, a.acept_01),
       aceptmenos_02 = ISNULL(a.aceptmenos_02, a.acept_02),
       aceptmenos_03 = ISNULL(a.aceptmenos_03, a.acept_03),
       aceptmenos_04 = ISNULL(a.aceptmenos_04, a.acept_04),
       aceptmenos_05 = ISNULL(a.aceptmenos_05, a.acept_05),
       aceptmenos_06 = ISNULL(a.aceptmenos_06, a.acept_06),
       aceptmenos_07 = ISNULL(a.aceptmenos_07, a.acept_07),
       aceptmenos_08 = ISNULL(a.aceptmenos_08, a.acept_08),
       aceptmenos_09 = ISNULL(a.aceptmenos_09, a.acept_09),
       aceptmenos_10 = ISNULL(a.aceptmenos_10, a.acept_10),
       aceptmenos_11 = ISNULL(a.aceptmenos_11, a.acept_11),
       aceptmenos_12 = ISNULL(a.aceptmenos_12, a.acept_12)
FROM   dbo.tmi_indicador_acept a
JOIN   dbo.tmi_indicador i ON i.id = a.id_indicador
WHERE  i.sentido = 'BANDA'
  AND ((a.aceptmenos_fijo IS NULL AND a.acept_fijo IS NOT NULL)
    OR (a.aceptmenos_01 IS NULL AND a.acept_01 IS NOT NULL)
    OR (a.aceptmenos_02 IS NULL AND a.acept_02 IS NOT NULL)
    OR (a.aceptmenos_03 IS NULL AND a.acept_03 IS NOT NULL)
    OR (a.aceptmenos_04 IS NULL AND a.acept_04 IS NOT NULL)
    OR (a.aceptmenos_05 IS NULL AND a.acept_05 IS NOT NULL)
    OR (a.aceptmenos_06 IS NULL AND a.acept_06 IS NOT NULL)
    OR (a.aceptmenos_07 IS NULL AND a.acept_07 IS NOT NULL)
    OR (a.aceptmenos_08 IS NULL AND a.acept_08 IS NOT NULL)
    OR (a.aceptmenos_09 IS NULL AND a.acept_09 IS NOT NULL)
    OR (a.aceptmenos_10 IS NULL AND a.acept_10 IS NOT NULL)
    OR (a.aceptmenos_11 IS NULL AND a.acept_11 IS NOT NULL)
    OR (a.aceptmenos_12 IS NULL AND a.acept_12 IS NOT NULL));
