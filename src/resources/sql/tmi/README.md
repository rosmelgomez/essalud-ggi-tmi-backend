# TMI dinámico: scripts SQL

Se ejecutan **al iniciar la aplicación** (`app.py` → `src/main/db/sqlRunner.py`), igual que `ExecuteQuery` en
essalud-gcpp-backend. También se pueden correr a mano:

```bash
python -m src.main.db.sqlRunner
```

O con `POST /tmi/dinamico/ejecutar-sql`. Todos los scripts son idempotentes: crean lo que falta y no pisan los
datos que el usuario ya cambió.

| Orden | Script | Contenido |
|------:|--------|-----------|
| 1 | `01_tablas.sql` | `tmi_variable`, `tmi_variable_logica`, `tmi_grupo`, `tmi_tipo_calculo`, `tmi_indicador` (+ columnas de cálculo), `tmi_indicador_variable`, `tmi_indicador_ambito`, `tmi_centro_estandar`, `tmi_estandar_acept`, `tmi_exclusion_centro_estandar`, `tmi_variable_pivot`, `tmi_resultado` |
| 2 | `02_vistas_adaptadoras.sql` | Vistas `vw_tmi_*` que leen las tablas existentes con sus columnas reales (`est_01` o `estandar_01`, `flag` o `flag_01..12`, `excl_01`…) |
| 3 | `03_datos.sql` | Datos iniciales: tipos de cálculo, grupos, 37 variables y su lógica, 21 indicadores con fórmula y letras, estándares por centro, ámbito de Emergencia |
| 4 | `04_procedimientos.sql` | `usp_tmi_validar_config`, `usp_tmi_generar_pivot`, `usp_tmi_calcular` |

## Variables de entorno (`.env`)

| Variable | Por defecto | Uso |
|----------|-------------|-----|
| `TMI_DB` | `DB_NAME` | Base donde están las tablas `tmi_*` |
| `TMI_TOTALIZADO3` | `pentahodev.dbo.TOTALIZADO3` | Tabla de hechos |
| `TMI_DIM` | `pentahodevDW.dbo` | Base.esquema de `DIM_GRUPO`, `DIM_ACTIVIDAD`, `DIM_HOJA` |
| `TMI_EJECUTAR_SQL` | `true` | `false` = no ejecutar los scripts al iniciar |
| `TMI_CALCULO_SOLO_PERIODO_ANTERIOR` | `true` | `false` = permite recalcular periodos cerrados |

En la máquina local las fuentes están en `pentahodev_dw`:
`TMI_TOTALIZADO3=pentahodev_dw.dbo.TOTALIZADO3` y `TMI_DIM=pentahodev_dw.dbo`.

### TOTALIZADO3 o las DIM en otro servidor

Las tablas `tmi_*` van en `TMI_DB`. TOTALIZADO3 y las DIM pueden estar en otro servidor SQL Server:

1. El DBA crea, en el servidor de `TMI_DB`, un servidor vinculado al servidor de TOTALIZADO3 (una sola vez),
   con un usuario de solo lectura:
   ```sql
   EXEC sp_addlinkedserver @server = 'SRV_DW', @srvproduct = '', @provider = 'MSOLEDBSQL',
        @datasrc = 'servidor-dw\instancia';          -- nombre o IP del servidor (y la instancia, si tiene)
   EXEC sp_addlinkedsrvlogin @rmtsrvname = 'SRV_DW', @useself = 'FALSE',
        @rmtuser = 'usuario_lectura', @rmtpassword = '****';
   ```
2. En el `.env` se usa nombre de 4 partes (servidor.base.esquema.tabla):
   ```
   TMI_TOTALIZADO3 = [SRV_DW].pentahodev_dw.dbo.TOTALIZADO3
   TMI_DIM = [SRV_DW].pentahodev_dw.dbo
   ```
3. Reiniciar el backend (o "Ejecutar scripts" en la pestaña Calcular) para que los procedimientos tomen el nombre nuevo.

El pivot lee TOTALIZADO3 una sola vez por cálculo: copia a una tabla temporal solo las filas del año y de los grupos
que usan las variables, con un filtro que se resuelve en el servidor remoto; los cruces se hacen después en local.
Las DIM (pequeñas) también se copian a tablas temporales. No hace falta MSDTC: no hay transacciones con el servidor
remoto. Al iniciar, el backend comprueba que puede leer las dos fuentes y, si no, deja un aviso en el log y en
"Ejecutar scripts". Entre corchetes se aceptan nombres con guion, espacio o `\` (`[SRV-DW\INST01]`).

## Flujo

1. `GET  /tmi/dinamico/validar-config`: errores de configuración (debe devolver `[]`).
2. `POST /tmi/dinamico/calcular/{AAAAMM}`: pivot de variables y cálculo → `tmi_resultado`.
3. `GET  /tmi/dinamico/generar-excel/{AAAAMM}?calcular=true`: Excel desde la plantilla vacía `TMI_PLANTILLA_BASE.xlsx`.

La plantilla vacía se regenera desde `TMI_PLANTILLA.xlsx` con:

```bash
python src/resources/plantillas/crear_plantilla_base.py
```

## Cómo administra el usuario
* **Nueva variable**: `tmi_variable` (nombre) + filas en `tmi_variable_logica` (tipgrupo, actividad, servicio, `SUMA` o `MEDIANA`, vigencia).
* **Nuevo indicador**: `tmi_indicador` (nombre de hoja, fórmula `expr_numerador` / `expr_denominador` con letras, `tipo_calculo`, sentido, tolerancia, `base_estandar`) + letras en `tmi_indicador_variable`. Aparece solo como hoja nueva y como columna en Puntajes.
* **Exclusión por periodo**: `tmi_exclusion_centro_estandar` (`excl_MM = 1`; `id_estandar` NULL = todos los indicadores del centro).
* **Centro visible por mes**: `tmi_centro.flag` / `flag_MM`.
* **Estándar propio de un centro**: `tmi_centro_estandar` (`aplica = 0` = NA; `acept` = Rojo propio).
* **Qué centros entran a un indicador**: `tmi_indicador_ambito` (lista blanca o negra por red, tipo o centro).
