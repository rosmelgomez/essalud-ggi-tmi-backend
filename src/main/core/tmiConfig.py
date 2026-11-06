import os

from dotenv import load_dotenv


load_dotenv()


def require_env(name: str, *, min_length: int = 1) -> str:
    value = os.getenv(name, "").strip()
    if len(value) < min_length:
        raise RuntimeError(f"La variable de entorno {name} es obligatoria")
    return value


# TMI dinámico: todas las tablas del sistema (tmi_*, entre ellas tmi_cierre y tmi_cierre_calendario) se crean en la base de la conexión
# (DB_NAME), nunca en otra; las fuentes (TOTALIZADO3 y DIM_*) solo se leen
TMI_DB = require_env("DB_NAME")
# Fuentes del data warehouse (TOTALIZADO3 y DIM_*): vienen del mismo servidor, una sola variable base.esquema
DIM = os.getenv("TMI_DIM", "pentahodevDW.dbo").strip()
TOTALIZADO3 = os.getenv("TMI_TOTALIZADO3", "pentahodev.dbo").strip()
TMI_TOTALIZADO3 = f"{TOTALIZADO3}.TOTALIZADO3"
TMI_DIM = f"{DIM}"
# Ejecutar los scripts SQL al iniciar la aplicación (como ExecuteQuery de essalud-gcpp-backend)
TMI_EJECUTAR_SQL = os.getenv("TMI_EJECUTAR_SQL", "true").lower() in {"1", "true", "yes"}
# Solo se calcula el periodo anterior al mes actual (hoy 2026-10 -> 202609): los anteriores ya pasaron su
# fecha de cierre y su Excel se arma con el resultado guardado. false = permite recalcular cualquier periodo.
TMI_CALCULO_SOLO_PERIODO_ANTERIOR = os.getenv("TMI_CALCULO_SOLO_PERIODO_ANTERIOR", "false").lower() in {"1", "true", "yes"}
