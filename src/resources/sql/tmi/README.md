# TMI dinámico: scripts SQL

Se ejecutan **al iniciar la aplicación** (`app.py` → `src/main/db/sqlRunner.py`), igual que `ExecuteQuery` en
essalud-gcpp-backend. También se pueden correr a mano:

```bash
python -m src.main.db.sqlRunner
```

O con `POST /tmi/dinamico/ejecutar-sql`. Antes de los scripts se crean las tablas que falten desde los modelos de `src/main/model` (como `ddl-auto` de
Spring Boot). Todos los scripts son idempotentes: crean lo que falta y no pisan los datos que el usuario ya cambió.

| Orden | Script | Contenido |
|------:|--------|-----------|
| 1 | `src/main/model/*.py` | Tablas `tmi_*` y `cierre`: `Base.metadata.create_all` crea las que faltan (no agrega columnas a las que ya existen) |
| 2 | `02_vistas_adaptadoras.sql` | Vistas `vw_tmi_*` que leen las tablas existentes con sus columnas reales (`est_01` o `estandar_01`, `flag` o `flag_01..12`, `excl_01`…) |
| 3 | `03_datos.sql` | Datos iniciales: tipos de cálculo, grupos, 37 variables y su lógica, 21 indicadores con su fórmula (`[grupo;actividad#servicio]`), estándares por centro, ámbito de Emergencia |
| 4 | `04_procedimientos.sql` | `usp_tmi_validar_config`, `fn_tmi_exclusion` (cada mes excluido queda 0 o NA: `res_MM` del mes o, si es NULL, `resultado` de la fila), `fn_tmi_estandar` (regla única de exclusiones, estándar y % Acept: la usan `usp_tmi_calcular` y el SQL descargable del indicador), `usp_tmi_calcular`, `usp_tmi_avisos_config` (avisos que no bloquean: centros sin estándar o sin % Acept en el periodo) |
| 5 | `06_historial.sql` | Triggers `tr_hist_*` de las tablas de configuración: guardan en `tmi_config_historial` quién cambió qué y cuándo (usuario del token vía `CONTEXT_INFO`) |

## Variables de entorno (`.env`)

| Variable | Por defecto | Uso |
|----------|-------------|-----|
| (DB_NAME) | — | Base de la conexión: ahí se crean todas las tablas del sistema (`tmi_*`, entre ellas `tmi_cierre` y `tmi_cierre_calendario`); no se configura aparte |
| `pentahodevDW` | `pentahodev_dw.dbo` | Base.esquema del data warehouse: de ahí se leen `TOTALIZADO3` y las `DIM_*` (vienen del mismo servidor) |
| `TMI_EJECUTAR_SQL` | `true` | `false` = no ejecutar los scripts al iniciar |
| `TMI_CALCULO_SOLO_PERIODO_ANTERIOR` | `true` | `false` = permite recalcular periodos cerrados |

En la máquina local las fuentes están en `pentahodev_dw`:
`pentahodevDW=pentahodev_dw.dbo`.

### TOTALIZADO3 o las DIM en otro servidor

Todas las tablas del sistema van en la base de la conexión (`DB_NAME`). TOTALIZADO3 y las DIM pueden estar en otro servidor SQL Server:

1. El DBA crea, en el servidor de `DB_NAME`, un servidor vinculado al servidor de TOTALIZADO3 (una sola vez),
   con un usuario de solo lectura:
   ```sql
   EXEC sp_addlinkedserver @server = 'SRV_DW', @srvproduct = '', @provider = 'MSOLEDBSQL',
        @datasrc = 'servidor-dw\instancia';          -- nombre o IP del servidor (y la instancia, si tiene)
   EXEC sp_addlinkedsrvlogin @rmtsrvname = 'SRV_DW', @useself = 'FALSE',
        @rmtuser = 'usuario_lectura', @rmtpassword = '****';
   ```
2. En el `.env` se usa el nombre con el servidor (servidor.base.esquema):
   ```
   pentahodevDW = [SRV_DW].pentahodev_dw.dbo
   ```
3. Reiniciar el backend (o "Ejecutar scripts" en la pestaña Calcular) para que los procedimientos tomen el nombre nuevo.

El cálculo lee TOTALIZADO3 una sola vez por periodo: copia a una tabla temporal solo las filas de enero al corte y de
los grupos que usan las fórmulas, con un filtro que se resuelve en el servidor remoto; los cruces se hacen después en local.
Las DIM (pequeñas) también se copian a tablas temporales. No hace falta MSDTC: no hay transacciones con el servidor
remoto. Al iniciar, el backend comprueba que puede leer las dos fuentes y, si no, deja un aviso en el log y en
"Ejecutar scripts". Entre corchetes se aceptan nombres con guion, espacio o `\` (`[SRV-DW\INST01]`).

## Flujo

1. `GET  /tmi/dinamico/validar-config`: errores de configuración (debe devolver `[]`).
2. `POST /tmi/dinamico/calcular/{AAAAMM}`: fórmula de cada indicador sobre TOTALIZADO3 → `tmi_resultado`.
3. `GET  /tmi/dinamico/generar-excel/{AAAAMM}?calcular=true`: Excel desde la plantilla vacía `TMI_PLANTILLA_BASE.xlsx`.

### Versiones de TOTALIZADO3 y justificación del cálculo

TOTALIZADO3 es la foto de hoy: los estadísticos pueden corregir meses anteriores. TOTALIZADO3 **nunca se modifica**;
solo se lee.

- `TOTALIZADO3_BACKUP` (en la base del TMI): la misma estructura de TOTALIZADO3 más `periodo_backup`, `fecha_backup`
  y `usuario_backup`. La copia del periodo P tiene TOTALIZADO3 de enero a P tal como estaba. La guarda el cierre de P
  (`usp_tmi_backup_totalizado3`); una copia guardada no se pisa salvo `POST /tmi/dinamico/backup/{AAAAMM}?reemplazar=true`.
- `usp_tmi_calcular @PERIODO, @ORIGEN, @USUARIO`: `ACTUAL` lee TOTALIZADO3 de hoy; `BACKUP` lee la copia del cierre
  del periodo ("como fue"). `tmi_resultado` guarda los dos (clave con `origen_datos`), con la fórmula, su desarrollo
  con los valores (`formula_desarrollo`), quién calculó y la copia usada. `tmi_resultado_termino` guarda el valor de
  cada término (grupo, actividad, servicio) y las filas sumadas.
- Calcular (pantalla) usa siempre TOTALIZADO3 (ACTUAL); el cierre calcula con la copia (BACKUP). `tmi_resultado` y
  `tmi_resultado_indicador` guardan los dos (clave con `origen_datos`) y la pantalla elige cuál ver y descargar
  (`?origen=ACTUAL|BACKUP` en `/resultado` y `/generar-excel`). Sin origen se usa el oficial: BACKUP si existe, si no
  ACTUAL (`vw_tmi_resultado`, `vw_tmi_resultado_indicador`, `fn_tmi_resultado`); el dashboard usa el oficial.
- `GET /tmi/dinamico/justificacion/{AAAAMM}/{id_indicador}` (y `/{codcentro}/terminos`, `/{codcentro}/filas`):
  resultado como fue y con datos actuales, términos y filas de TOTALIZADO3 que cambiaron (antes, ahora, `usuariomod`,
  `fechamod`).

La plantilla vacía se regenera desde `TMI_PLANTILLA.xlsx` con:

```bash
python src/resources/plantillas/crear_plantilla_base.py
```

## Cómo administra el usuario
* **Nueva variable**: `tmi_variable` (nombre y cálculo `SUMA` o `MEDIANA` de la variable) + conjuntos en `tmi_variable_logica` (tipgrupo, actividad, servicio, vigencia). Los conjuntos de una variable se combinan con OR (un registro cuenta una vez); una variable compuesta suma otras variables del mismo cálculo (`tmi_variable_componente`).
* **Nuevo indicador**: `tmi_indicador` en dos partes. Aparece solo como hoja nueva y como columna en Puntajes.
  1. *Cálculo*: el usuario escribe la fórmula con letras: `formula_alias` = `(A - B) / C`, cada letra una
     variable (`tmi_indicador_variable`, una variable por letra), con + - * /, paréntesis y números. El backend la
     expande con los conjuntos de cada variable (y de sus componentes) a `formula`; si una variable cambia, se regeneran
     las fórmulas de los indicadores que la usan (y al iniciar). `formula` tiene términos de TOTALIZADO3, como la
     columna de fórmulas de TMI_SQL:
     `([3;50#0] - [3;49#0]) / [3;47#0]` (`[grupo;actividad#servicio]`, `#0` = todos, `#77,78` = varios servicios;
     `MEDIANA([3;51#0])` para recursos; `+ - * /`, paréntesis y números). `PUT /indicadores/{id}/formula` la valida
     (`src/main/core/tmiFormula.py`) y guarda sus términos (`tmi_indicador_termino`, T1, T2...) y la expresión SQL
     (`formula_sql`); al iniciar se regeneran desde `formula`.
     *Regla de nulos* (la elige el usuario por indicador, `PUT /indicadores/{id}`; al cambiarla se regenera `formula_sql`):
     | Campo | `CERO` | `NA` |
     |-------|--------|------|
     | `si_variable_nula` (letra sin dato en el mes) | vale 0: `ISNULL(A,0)` (por defecto) | el mes queda NA |
     | `si_division_cero` (divisor 0 o sin dato) | resultado 0: `ISNULL(A / NULLIF(B,0), 0)` | el mes queda NA (por defecto) |

     `CERO` + `CERO` es la lógica de `00_TMI_CREACION_VISTAS_2025.sql` (`ISNULL(ISNULL(A,0) / NULLIF(ISNULL(B,0),0), 0)`).
     El centro sin ningún dato del indicador en todo el año lo decide `sin_datos_anio`: `MOSTRAR` = 0, `NA`, `OCULTAR`. `tipo_calculo`: MENSUAL o ACUMULADO (enero..mes). `GET /indicadores/{id}/resultado-directo/{AAAAMM}`
     ejecuta el query automático del indicador sobre TOTALIZADO3 (sin estándares ni exclusiones) y devuelve el SQL.
     Las variables (`tmi_variable`) ya no intervienen en el cálculo y ya no hay pivot de variables.
  2. *Estándares*: `base_estandar` (FK a `tmi_tipo_estandar.codigo`), sentido, tolerancia y formato; los valores por
     clave y mes en `tmi_estandar_nivel` / `_tipo` / `_categoria`.
* **Tipos de estándar** (tablas maestras):
  * `tmi_tipo_estandar`: `NIVEL`, `NIVEL_TIPO`, `TIPO`, `CATEGORIA`…
  * `tmi_estandar`: claves de cada tipo. `fuente` = tabla de valores (`NIVEL` / `TIPO` / `CATEGORIA`), `clave` = valor del
    centro en `tmi_centro`, `prioridad` = cuál gana si el centro cumple dos claves del mismo tipo (en `NIVEL_TIPO`,
    CNSR / IPO / INCOR tienen prioridad 2 y toman su estándar por tipo; el resto, por nivel).
  * Orden del estándar en el cálculo: estándar propio del centro → clave del tipo de estándar con mayor prioridad que
    tenga valor → reglas especiales del panel (`tmi_indicador_estandar`).
* **% Acept**: se calcula, no se guarda por mes: estándar ± el porcentaje del indicador (`tmi_indicador.tipo_tolerancia`:
  `REL` = % del estándar, `ABS` = puntos; `tolerancia`; en banda `tolerancia` = hacia arriba y `tolerancia_menos` =
  hacia abajo, NULL = el mismo). Menor es mejor: estándar + %; mayor es mejor: estándar − %. El % Acept propio del
  centro (`tmi_centro_estandar.acept`) gana. Se edita en la pestaña "% Acept" (`PUT /indicadores/{id}/tolerancia`).
  En los resultados (`tmi_resultado`, `tmi_resultado_indicador`) las columnas son `acept` y `aceptmenos`.
* **Exclusión por periodo**: `tmi_exclusion_centro_indicador` (`excl_MM = 1`; `id_indicador` NULL = todos los indicadores del centro).
* **Centro visible por mes**: `tmi_centro.flag` / `flag_MM`.
* **Estándar propio de un centro**: `tmi_centro_estandar` (`aplica = 0` = NA; `acept` = % Acept propio).
* **Qué centros entran a un indicador**: los que tienen estándar (mayor que 0) en la tabla de su tipo de estándar
  (unión por `nivel_centro` / `tipo_centro` / `categoria_centro`). Sin estándar el centro queda NA "Sin estándar".
  `tmi_indicador_ambito` ya no se usa en el cálculo.
