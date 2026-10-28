import os

from dotenv import load_dotenv


load_dotenv()


def require_env(name: str, *, min_length: int = 1) -> str:
    value = os.getenv(name, "").strip()
    if len(value) < min_length:
        raise RuntimeError(f"La variable de entorno {name} es obligatoria")
    return value


APP_ENV = os.getenv("APP_ENV", "development").strip().lower()
IS_PRODUCTION = APP_ENV == "production"
AUTO_CREATE_TABLES = os.getenv(
    "AUTO_CREATE_TABLES",
    "false" if IS_PRODUCTION else "true",
).lower() in {"1", "true", "yes"}
BFF_JWT_SECRET = require_env("BFF_JWT_SECRET", min_length=32)
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "true" if IS_PRODUCTION else "false").lower() in {
    "1",
    "true",
    "yes",
}
ALLOWED_ORIGINS = {
    origin.strip().rstrip("/")
    for origin in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
}
if not IS_PRODUCTION:
    ALLOWED_ORIGINS.update({"http://localhost:3000", "http://127.0.0.1:3000"})
elif not ALLOWED_ORIGINS:
    raise RuntimeError("ALLOWED_ORIGINS es obligatoria en producción")

if IS_PRODUCTION and not COOKIE_SECURE:
    raise RuntimeError("COOKIE_SECURE debe estar habilitada en producción")

# TMI dinámico: dónde viven las tablas tmi_* y las fuentes (se usan en los scripts de src/resources/sql/tmi)
TMI_DB = os.getenv("TMI_DB", os.getenv("DB_NAME", "pentahodev_prueba_01")).strip()
TMI_TOTALIZADO3 = os.getenv("TMI_TOTALIZADO3", "pentahodev.dbo.TOTALIZADO3").strip()
TMI_DIM = os.getenv("TMI_DIM", "pentahodevDW.dbo").strip()
# Ejecutar los scripts SQL al iniciar la aplicación (como ExecuteQuery de essalud-gcpp-backend)
TMI_EJECUTAR_SQL = os.getenv("TMI_EJECUTAR_SQL", "true").lower() in {"1", "true", "yes"}
# Solo se calcula el periodo anterior al mes actual (hoy 2026-10 -> 202609): los anteriores ya pasaron su
# fecha de cierre y su Excel se arma con el resultado guardado. false = permite recalcular cualquier periodo.
TMI_CALCULO_SOLO_PERIODO_ANTERIOR = os.getenv("TMI_CALCULO_SOLO_PERIODO_ANTERIOR", "true").lower() in {"1", "true", "yes"}
