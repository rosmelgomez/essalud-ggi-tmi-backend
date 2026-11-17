# TMI dinámico: scripts SQL

Se ejecutan **al iniciar la aplicación** (`app.py` → `src/main/db/sqlRunner.py`), igual que `ExecuteQuery` en
essalud-gcpp-backend. También se pueden correr a mano:

```bash
python -m src.main.db.sqlRunner
```

O con `POST /tmi/configuracion/ejecutar-sql`. Antes de los scripts se crean las tablas que falten desde los modelos de `src/main/model` (como `ddl-auto` de
Spring Boot). Todos los scripts son idempotentes: crean lo que falta y no pisan los datos que el usuario ya cambió.

| Orden | Script | Contenido |
|------:|--------|-----------|
| 1 | `src/main/model/*.py` | Tablas `tmi_*` y `cierre`: `Base.metadata.create_all` crea las que faltan (no agrega columnas a las que ya existen) |
| 2 | `02_vistas_adaptadoras.sql` | Vistas `vw_tmi_*` que leen las tablas en un solo formato: estándar por tipo, nivel y categoría (`vw_tmi_std`), centros con código numérico y su `flag` (`vw_tmi_centro_base`), exclusiones por mes (`vw_tmi_exclusion`) y estándar propio de centro (`vw_tmi_estandar_centro`) |
| 3 | `03_datos.sql` | Datos iniciales: tipos de cálculo, grupos, 37 variables y su lógica, 21 indicadores con su fórmula (`[grupo;actividad#servicio]`), estándares por centro |
| 3b | `src/resources/centro`, `src/resources/estandares` | Centros, exclusiones y estándares iniciales: se cargan solo si la tabla está vacía |
| 3c | `05_variables_pivot.sql` | Variables del pivot anterior (`Generar_pivot.sql`) que faltan en `tmi_variable`; no pisa lo que el usuario cambió |
| 4 | `04_procedimientos.sql` | `usp_tmi_validar_config`, `fn_tmi_exclusion` (cada mes excluido queda 0 o NA: `res_MM` del mes o, si es NULL, `resultado` de la fila), `fn_tmi_estandar` (regla única de exclusiones, estándar y % Acept: la usan `usp_tmi_calcular` y el SQL descargable del indicador), `usp_tmi_calcular` |
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

1. `GET  /tmi/configuracion/validar-config`: errores de configuración (debe devolver `[]`).
2. `POST /tmi/calculo/calcular/{AAAAMM}`: fórmula de cada indicador sobre TOTALIZADO3 (enero..AAAAMM), en tiempo
   real: no se guarda.
3. `GET  /tmi/excel/{AAAAMM}`: Excel desde la plantilla vacía `TMI_PLANTILLA_BASE.xlsx`.

### Versiones de TOTALIZADO3 y justificación del cálculo

TOTALIZADO3 es la foto de hoy: los estadísticos pueden corregir meses anteriores. TOTALIZADO3 **nunca se modifica**;
solo se lee.

- `TOTALIZADO3_BACKUP` (en la base del TMI): la misma estructura de TOTALIZADO3 más `periodo_backup`, `fecha_backup`
  y `usuario_backup`. La copia del periodo P tiene TOTALIZADO3 de enero a P tal como estaba. La guarda el cierre de P
  (`usp_tmi_backup_totalizado3`); una copia guardada no se pisa salvo `POST /tmi/backup/{AAAAMM}?reemplazar=true`.
- `usp_tmi_calcular @PERIODO, @ORIGEN, @USUARIO`: `ACTUAL` lee TOTALIZADO3 de hoy (enero..periodo); `BACKUP` lee la
  copia del cierre del periodo (`periodo_backup = periodo`, "como fue"). Siempre en tiempo real: no escribe nada.
  Calcula cada mes de enero al periodo con la regla de ese mes y devuelve 4 resultados: final por centro, resultado
  del mes (con la fórmula y su desarrollo), términos y cada mes. Todos los meses van en una sola pasada (tablas
  temporales con la columna `mes`, tabla `#meses`), no un ciclo que repite el cálculo mes por mes; solo
  `fn_tmi_estandar` se llama una vez por mes.
- El resultado no se guarda en ninguna tabla. El cierre solo guarda la copia de los datos (`TOTALIZADO3_BACKUP`).
- El backend guarda en memoria el cálculo en tiempo real de cada periodo y origen, y lo vuelve a calcular si cambia
  TOTALIZADO3 (o la copia), la configuración (`tmi_config_historial`) o pasan `TMI_VIVO_CACHE_SEG` segundos (600).
- `?origen=ACTUAL|BACKUP` en `/resultado` y `/generar-excel`: ACTUAL = datos de hoy; BACKUP = la copia del cierre.
  Sin origen se usa ACTUAL. Los dashboards usan siempre ACTUAL.
- `GET /tmi/justificacion/{AAAAMM}/{id_indicador}` (y `/{codcentro}/terminos`, `/{codcentro}/filas`):
  resultado como fue y con datos actuales, términos y filas de TOTALIZADO3 que cambiaron (antes, ahora, `usuariomod`,
  `fechamod`).

La plantilla vacía se regenera desde `TMI_PLANTILLA.xlsx` con:

```bash
python src/resources/plantillas/crear_plantilla_base.py
```

## Cómo administra el usuario
* **Nueva variable**: `tmi_variable` (nombre y cálculo `SUMA` o `MEDIANA` de la variable) + conjuntos en `tmi_variable_logica` (tipgrupo, actividad, servicio, condición de hoja). La condición de hoja (`ASEGURADO`, `NO ASEGURADO`) cuenta solo las filas de TOTALIZADO3 cuya `tipohoja` tiene esa condición en `DIM_HOJA` para el año, como `Generar_pivot.sql`; en la fórmula va como `[1;1@ASEGURADO]` (espacios como `_`). Los conjuntos de una variable se combinan con OR (un registro cuenta una vez); una variable compuesta suma otras variables del mismo cálculo (`tmi_variable_componente`).
* **Nuevo indicador**: `tmi_indicador` en dos partes. Aparece solo como hoja nueva y como columna en Puntajes.
  1. *Cálculo*: el usuario escribe la fórmula con letras: `formula_alias` = `(A - B) / C`, cada letra una
     variable, con + - * /, paréntesis y números. La variable de cada letra se guarda en `formula_variable`: la misma
     fórmula con el id de la variable entre llaves (`(A - B) / C` con A = 1, B = 2, C = 5 -> `({1} - {2}) / {5}`). El backend la
     expande con los conjuntos de cada variable (y de sus componentes) a `formula`; si una variable cambia, se regeneran
     las fórmulas de los indicadores que la usan (y al iniciar). `formula` tiene términos de TOTALIZADO3, como la
     columna de fórmulas de TMI_SQL:
     `([3;50#0] - [3;49#0]) / [3;47#0]` (`[grupo;actividad#servicio]`, `#0` = todos, `#77,78` = varios servicios;
     `MEDIANA([3;51#0])` para recursos; `+ - * /`, paréntesis y números). `PUT /indicadores/{id}/formula` la valida
     (`src/main/core/tmiFormula.py`). Los términos (T1, T2...) y la expresión SQL no se guardan: cada vez que se
     calcula o se valida, Python lee `formula` de los indicadores activos y deja en la conexión `#termino` y `#formula`
     (`tmiBaseRep.crear_tablas_formula`), que usan `usp_tmi_calcular` y `usp_tmi_validar_config`. Por eso esos dos
     procedimientos se llaman desde el backend, no desde SSMS.
     *Regla de nulos* (la elige el usuario por indicador, `PUT /indicadores/{id}`; se aplica al leer la fórmula):
     | Campo | `CERO` | `NA` |
     |-------|--------|------|
     | `si_variable_nula` (letra sin dato en el mes) | vale 0: `ISNULL(A,0)` (por defecto) | el mes queda NA |
     | `si_division_cero` (divisor 0 o sin dato) | resultado 0: `ISNULL(A / NULLIF(B,0), 0)` | el mes queda NA (por defecto) |

     `CERO` + `CERO` es la lógica de `00_TMI_CREACION_VISTAS_2025.sql` (`ISNULL(ISNULL(A,0) / NULLIF(ISNULL(B,0),0), 0)`).
     El centro sin ningún dato del indicador en todo el año lo decide `sin_datos_anio`: `MOSTRAR` = 0, `NA`, `OCULTAR`. `tipo_calculo`: MENSUAL o ACUMULADO (enero..mes).
     Las variables (`tmi_variable`) ya no intervienen en el cálculo y ya no hay pivot de variables.
  2. *Estándares*: `base_estandar` (FK a `tmi_tipo_estandar.codigo`), sentido, tolerancia y formato; los valores por
     clave y mes en `tmi_estandar_nivel` / `_tipo` / `_categoria`.
* **Tipos de estándar** (tablas maestras):
  * `tmi_tipo_estandar`: `NIVEL`, `NIVEL_TIPO`, `TIPO`, `CATEGORIA`…
  * `tmi_estandar`: claves de cada tipo. `fuente` = tabla de valores (`NIVEL` / `TIPO` / `CATEGORIA`), `clave` = valor del
    centro en `tmi_centro`, `prioridad` = cuál gana si el centro cumple dos claves del mismo tipo (en `NIVEL_TIPO`,
    CNSR / IPO / INCOR tienen prioridad 2 y toman su estándar por tipo; el resto, por nivel).
  * Orden del estándar en el cálculo: estándar propio del centro → clave del tipo de estándar con mayor prioridad que
    tenga valor (`tmi_estandar_nivel` / `_tipo` / `_categoria`). No hay otra fuente: `tmi_indicador_estandar` se quitó
    (el backend la borra al iniciar).
* **% Acept**: estándar ± el porcentaje del indicador en `tmi_indicador_acept` (`tipo_acept`: `REL` = % del
  estándar, `ABS` = se suma o resta directo; `acept` = hacia arriba y, en banda, `aceptmenos` = hacia abajo, siempre
  guardado). Menor es mejor: estándar + %; mayor es mejor: estándar − %. `tmi_indicador` ya no guarda el % Acept: al
  crear un indicador se crea su fila del año actual y cada año nuevo copia el fijo del año anterior. También con estándar
  propio del centro el % Acept sale del indicador (el centro no guarda uno propio). Se edita en la pestaña "% Acept" (`PUT /indicadores/{id}/acept`). Se guarda en `tmi_indicador_acept`, una fila por indicador y año como los estándares: `acept_fijo` / `aceptmenos_fijo` (el del año) y `acept_01..12` / `aceptmenos_01..12` (cada mes toma el fijo en su fecha de cierre; vacío = usa el fijo); `tipo_acept` = REL / ABS del año.
  En el resultado del cálculo las columnas son `acept` y `aceptmenos`.
* **Exclusión por periodo**: `tmi_exclusion_centro_indicador` (`excl_MM = 1`; `id_indicador` NULL = todos los indicadores del centro).
* **Centro visible por mes**: `tmi_centro.flag` / `flag_MM`.
* **Estándar propio de un centro**: `tmi_estandar_centro` (`aplica = 0` = NA; el % Acept es siempre el del indicador).
  Funciona como `tmi_estandar_nivel`: `est_fijo` del año y `est_MM`; en la fecha de cierre el mes toma el fijo
  (un año nuevo copia los registros del año anterior) y desde entonces se puede cambiar solo ese mes.
* **Qué centros entran a un indicador**: los que tienen estándar (mayor que 0) en la tabla de su tipo de estándar
  (unión por `nivel_centro` / `tipo_centro` / `categoria_centro`). Sin estándar el centro queda NA "Sin estándar".
  Todos los centros entran al cálculo; las exclusiones (`tmi_exclusion_centro_indicador`) dicen si un centro queda en 0 o NA. `tmi_indicador_ambito` se quitó (el backend la borra al iniciar).
