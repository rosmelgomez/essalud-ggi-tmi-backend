/* =====================================================================================================
   TMI DINAMICO - 05 VARIABLES DE Generar_pivot.sql (USP_CIFRAS_CONSOLIDADOVAR)
   Carga, una sola vez, las variables del pivot anterior que no están en tmi_variable:
     - cada conjunto (tipgrupo, actividad, servicio, condición de hoja) es una fila de tmi_variable_logica;
       una variable con varios conjuntos (suma de subconsultas o servicio IN) tiene varias filas y se suman;
     - el Consolidado de Consultas (OR de 6 conjuntos) es una variable compuesta: suma las variables de cada
       conjunto (tmi_variable_componente).
   Solo se agregan filas y componentes a las variables que crea este script: lo que el usuario cambie después no se
   vuelve a pisar. Los conjuntos con grupo o actividad que no existen en las DIM quedan inactivos.
   Generado desde el análisis de Generar_pivot.sql: 111 variables, 119 conjuntos,
   1 compuesta(s).
   ===================================================================================================== */
DECLARE @v TABLE (nombre NVARCHAR(200), tipgrupo INT, actividad INT, servicio INT NULL, condicion_hoja VARCHAR(20) NULL, activo BIT);
INSERT INTO @v (nombre, tipgrupo, actividad, servicio, condicion_hoja, activo) VALUES
    (N'Consulta Apoyo Descentralizado', 27, 3, NULL, NULL, 1),
    (N'Consultas en medicina complementaria', 37, 3, NULL, NULL, 1),
    (N'Salud Ocupacional – Consulta Medico de personal', 49, 677, NULL, NULL, 1),
    (N'Teleconsulta', 58, 3, NULL, NULL, 1),
    (N'Consulta Externa - Consultas de Atención Inmediata - CAI', 50, 335, NULL, NULL, 1),
    (N'Consulta Externa - Consultantes Nuevos', 1, 186, NULL, NULL, 1),
    (N'Consulta Externa - Consultantes Asegurados', 1, 1, NULL, N'ASEGURADO', 1),
    (N'Hospitalizacion - Reingresos', 3, 166, NULL, NULL, 1),
    (N'Centro Quirúrgico - Total Intervenciones Quirúrgicas', 6, 225, NULL, NULL, 1),
    (N'Centro Quirúrgico - Total Intervenciones Quirúrgicas', 6, 226, NULL, NULL, 1),
    (N'Centro Quirúrgico - Total Intervenciones Quirúrgicas', 6, 227, NULL, NULL, 1),
    (N'Centro Quirúrgico - Total Intervenciones Quirúrgicas', 6, 228, NULL, NULL, 1),
    (N'Centro Quirúrgico - Total Intervenciones Quirúrgicas', 6, 229, NULL, NULL, 1),
    (N'Centro Obstétrico - Partos Sin Complicación', 5, 18, NULL, NULL, 1),
    (N'Centro Obstétrico - Partos Con Complicación', 5, 19, NULL, NULL, 1),
    (N'Centro Obstétrico - Nacimientos', 5, 178, NULL, NULL, 1),
    (N'Centro Obstétrico - Nacidos Vivos', 5, 178, 79, NULL, 1),
    (N'Atención No Médica - Control de Enfermería', 43, 603, 247, NULL, 1),
    (N'Atención No Médica - Control de Enfermería', 43, 603, 248, NULL, 1),
    (N'Atención No Médica - Control de Enfermería', 43, 603, 245, NULL, 1),
    (N'Atención No Médica - Control de Enfermería', 43, 603, 262, NULL, 1),
    (N'Atención No Médica - Control de Enfermería', 43, 603, 346, NULL, 1),
    (N'Atención No Médica - Control de Nutrición', 43, 279, 66, NULL, 1),
    (N'Atención No Médica - Control de Trabajo Social', 43, 281, 66, NULL, 1),
    (N'Atención No Médica - Educación Grupal de Trabajo Social', 43, 281, 68, NULL, 1),
    (N'Atención No Médica - Educación Grupal de Enfermería', 43, 277, 68, NULL, 1),
    (N'Atención No Médica - Educación Grupal de Nutrición', 43, 279, 68, NULL, 1),
    (N'Atención No Médica - Educación Grupal de Obstetricia', 43, 278, 68, NULL, 1),
    (N'Atención No Médica - Psicoprofilaxis de Nutrición', 43, 279, 69, NULL, 1),
    (N'Atención No Médica - Psicoprofilaxis de Obstetricia', 43, 278, 69, NULL, 1),
    (N'Atención No Médica - Psicoprofilaxis de Enfermería', 43, 277, 69, NULL, 1),
    (N'Atención No Médica - Visitas Domiciliarias de Enfermeria', 43, 277, 67, NULL, 1),
    (N'Atención No Médica - Visitas Domiciliarias de Nutrición', 43, 279, 67, NULL, 1),
    (N'Atención No Médica - Visitas Domiciliarias de Obstetricia', 43, 278, 67, NULL, 1),
    (N'Atención No Médica - Visitas Domiciliarias de Trabajo Social', 43, 281, 67, NULL, 1),
    (N'Emergencia - Prioridad III', 8, 41, NULL, NULL, 1),
    (N'Actividades Intermedias - Recetas Despachadas', 9, 9, NULL, NULL, 1),
    (N'Actividades Intermedias - Análisis de Laboratorio', 9, 12, NULL, NULL, 1),
    (N'Actividades Intermedias - Exámenes Radiológico', 9, 10, NULL, NULL, 1),
    (N'Actividades Intermedias - Placas Radiológicas', 9, 11, NULL, NULL, 1),
    (N'Actividades Intermedias - Análisis de Laboratorio de C.E', 9, 12, 14, NULL, 1),
    (N'Actividades Intermedias - Exámenes Radiológico de C.E', 9, 10, 14, NULL, 1),
    (N'Actividades Intermedias - Placas Radiológicas de C.E', 9, 11, 14, NULL, 1),
    (N'Atención Primaria - Mamografías Prevent. 50 a 69 años', 53, 165, 155, NULL, 1),
    (N'Atención Primaria - Menores 1 año Tercera Dosis Pentavalente', 53, 444, NULL, NULL, 1),
    (N'Atención Primaria - Muestras Procesadas x PAP Cervico Vaginal', 53, 406, 156, NULL, 1),
    (N'Atención Primaria - Primera Consulta Externa Med. Preventiva', 53, 443, NULL, NULL, 1),
    (N'Atención Primaria - Muestras Procesadas x PAP Cervico Vaginal positivos', 53, 406, 157, NULL, 1),
    (N'Atención Primaria - Menores de 1 año 3Dosis IPV', 53, 662, NULL, NULL, 1),
    (N'Atención Primaria - Niños 6 menor 36m con tamizaje anemia', 53, 637, NULL, NULL, 1),
    (N'Atención Primaria - Niños 6 menor 36m recuperados anemia', 53, 646, NULL, NULL, 1),
    (N'Atención Primaria - Niños 6 menor 36m con tamizaje anemia(acumulado)', 53, 663, NULL, NULL, 1),
    (N'Atención Primaria - Niños 6 menor 36m recuperados anemia(acumulado)', 53, 664, NULL, NULL, 1),
    (N'Acelerador Lineal', 40, 262, 60, NULL, 1),
    (N'Acelerador Lineal Contratado', 41, 438, NULL, NULL, 1),
    (N'Angiografia Cerebral', 12, 89, NULL, NULL, 1),
    (N'Angiografia Retinal', 12, 99, NULL, NULL, 1),
    (N'Braquiterapia a Baja Tasas de Dosis', 40, 545, NULL, NULL, 1),
    (N'Braquiterapia de Alta Tasas de Dosis', 40, 546, NULL, NULL, 1),
    (N'Calorimetria', 12, 441, NULL, NULL, 1),
    (N'Camara Hiperbarica', 40, 305, NULL, NULL, 1),
    (N'Cobalto Terapia', 40, 262, 59, NULL, 1),
    (N'Inmunoterapia Cardiaco', 40, 264, 54, NULL, 1),
    (N'Inmunoterapia Hepático', 40, 264, 56, NULL, 1),
    (N'Inmunoterapia Progenitores Hematopoyeticos', 40, 264, 58, NULL, 1),
    (N'Inmunoterapia Pulmón', 40, 264, 57, NULL, 1),
    (N'Inmunoterapia Renal', 40, 264, 55, NULL, 1),
    (N'Inmunoterapia para VIH (+)', 40, 263, NULL, NULL, 1),
    (N'Laserterapia Ocular', 12, 98, NULL, NULL, 1),
    (N'N° de Dialisis Peritoneal', 11, 33, NULL, NULL, 1),
    (N'Dialisis Peritoneal Automatizado', 11, 522, NULL, NULL, 1),
    (N'Nutrición Entera Total', 40, 272, NULL, NULL, 1),
    (N'Nutrición Parental Periferica (Nutrición Parcial)', 40, 271, NULL, NULL, 1),
    (N'Nutrición Parental Total', 40, 270, NULL, NULL, 1),
    (N'Psicoterapia en Salud Mental', 40, 523, NULL, NULL, 1),
    (N'Quimioterapia', 40, 260, NULL, NULL, 1),
    (N'Radiologia Intervencionista', 12, 108, NULL, NULL, 1),
    (N'Resonancia Magnetica', 12, 104, NULL, NULL, 1),
    (N'Resonancia Magnetica Contratado', 41, 104, NULL, NULL, 1),
    (N'Screening Tasa de Filtración Glomerular (TFG)', 40, 386, NULL, NULL, 1),
    (N'Sesiones de Hemodialisis (Servicio Contratado)', 41, 32, NULL, NULL, 1),
    (N'Sesiones de Hemodialisis (Servicio Propio)', 11, 32, NULL, NULL, 1),
    (N'Tomografia Axial Computarizada', 12, 93, NULL, NULL, 1),
    (N'Tomografia Multicorte', 12, 434, NULL, NULL, 1),
    (N'Tratamiento Especializado con Yodo 131', 40, 291, 75, NULL, 1),
    (N'Tratamiento Hospital de Dia', 40, 268, NULL, NULL, 1),
    (N'Tratamiento Paciente Insuficiencia Renal Cronica Terminal', 40, 267, NULL, NULL, 1),
    (N'Tratamiento Nefroprotector', 40, 388, NULL, NULL, 1),
    (N'Tratamiento para el Paciente Hemofilico', 40, 266, NULL, NULL, 1),
    (N'Tratamiento para el Paciente Drogo - Resistente (TBC)', 40, 265, NULL, NULL, 1),
    (N'Valoración del Daño Renal', 40, 387, NULL, NULL, 1),
    (N'Cobaltoterapia', 40, 262, 59, NULL, 1),
    (N'Trasplante Corazón', 7, 151, NULL, NULL, 1),
    (N'Trasplante Corneas', 7, 149, NULL, NULL, 1),
    (N'Trasplante Higado', 7, 153, NULL, NULL, 1),
    (N'Trasplante Renal', 7, 150, NULL, NULL, 1),
    (N'Trasplante Progenitores Hematopoyeticos', 7, 152, NULL, NULL, 1),
    (N'Trasplante Pulmón', 7, 310, NULL, NULL, 1),
    (N'Trasplante Pancreas', 7, 528, NULL, NULL, 1),
    (N'Psicología - Atencion Psicología', 20, 58, NULL, NULL, 1),
    (N'Psicología - Psicoprofilaxis de Psicologia', 20, 574, 115, NULL, 1),
    (N'Psicología - Visitas Domiciliarias de Psicologia', 20, 574, 67, NULL, 1),
    (N'Psicología - Educación Grupal en Psicología', 20, 574, 68, NULL, 1),
    (N'Teleconsultas médicas', 58, 3, NULL, NULL, 1),
    (N'Telemonitoreo médicas', 59, 3, NULL, NULL, 1),
    (N'Telemonitoreo de enfermería', 59, 277, NULL, NULL, 1),
    (N'Telemonitoreo de Obstetricia', 59, 278, NULL, NULL, 1),
    (N'Teleorientación de enfermería', 60, 277, NULL, NULL, 1),
    (N'Teleorientación de Obstetricia', 60, 278, NULL, NULL, 1),
    (N'Teleorientación de Nutrición', 60, 279, NULL, NULL, 1),
    (N'Teleorientación de Psicología', 60, 280, NULL, NULL, 1),
    (N'Ecografías', 12, 85, NULL, NULL, 1),
    (N'Electrocardiogramas', 12, 80, NULL, NULL, 1),
    (N'Cardio-tocografías materno fetal', 12, 452, NULL, NULL, 1),
    (N'Tomografías Multicorte', 12, 434, NULL, NULL, 1),
    (N'Tomografías Ac', 12, 93, NULL, NULL, 1),
    (N'Tomografías PET/CT', 12, 560, NULL, NULL, 1),
    (N'Medicina Complementaria - Consultas', 37, 3, NULL, NULL, 1),
    (N'Cons. Apoyo Desc (Itinerante) - Consultas', 27, 3, NULL, NULL, 1);

DECLARE @c TABLE (nombre NVARCHAR(200), componente NVARCHAR(200));
INSERT INTO @c (nombre, componente) VALUES
    (N'Consolidado de Consultas', N'Consulta Apoyo Descentralizado'),
    (N'Consolidado de Consultas', N'Consultas en medicina complementaria'),
    (N'Consolidado de Consultas', N'Salud Ocupacional – Consulta Medico de personal'),
    (N'Consolidado de Consultas', N'Teleconsulta'),
    (N'Consolidado de Consultas', N'Consulta Externa - Consultas'),
    (N'Consolidado de Consultas', N'Consulta Externa - Consultas de Atención Inmediata - CAI');

DECLARE @nuevas TABLE (id INT, nombre NVARCHAR(200));
INSERT INTO dbo.tmi_variable (nombre, descripcion, total_anual, activo, usuario_creacion)
OUTPUT INSERTED.id, INSERTED.nombre INTO @nuevas
SELECT n.nombre, N'Generar_pivot.sql', 'SUMA_MESES', 1, 'carga_inicial'
FROM (SELECT nombre FROM @v UNION SELECT nombre FROM @c) n
WHERE NOT EXISTS (SELECT 1 FROM dbo.tmi_variable t WHERE t.nombre = n.nombre);

INSERT INTO dbo.tmi_variable_logica (id_variable, tipgrupo, actividad, servicio, condicion_hoja, activo)
SELECT n.id, x.tipgrupo, x.actividad, x.servicio, x.condicion_hoja, x.activo
FROM @v x JOIN @nuevas n ON n.nombre = x.nombre;

INSERT INTO dbo.tmi_variable_componente (id_variable, id_variable_componente)
SELECT n.id, t.id
FROM @c x JOIN @nuevas n ON n.nombre = x.nombre JOIN dbo.tmi_variable t ON t.nombre = x.componente;
GO
