"""Configuración de seguridad del TMI (como WebSecurityConfig de essalud-gcpp-backend): rutas públicas y CORS."""

import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
logger = logging.getLogger(__name__)

# Rutas que no exigen sesión (permitAll). Se compara el inicio de la ruta: "/x/" equivale a "/x/**" en Spring.
# Solo lectura: nunca poner aquí rutas que creen, modifiquen o borren datos.
RUTAS_PUBLICAS = [
    ("GET", "/tmi/dinamico/dashboard/"),
]


# Roles que pueden modificar el TMI (crear, editar, borrar, calcular, ejecutar scripts). Separados por coma.
ROLES_ADMIN = {r.strip().upper() for r in os.getenv("TMI_ROLES_ADMIN", "ADMIN").split(",") if r.strip()}
# Autoridad que essalud-gcpp-backend agrega al token cuando usuario.access_tmi = true (JwtUserDetailsServ.ACCESS_TMI)
AUTORIDAD_ACCESO_TMI = "ACCESS_TMI"

# Peticiones que no son GET pero solo leen: no exigen rol de administrador.
RUTAS_POST_LECTURA = [
    ("POST", "/tmi/dinamico/formula/analizar"),   # valida la fórmula sin guardarla
]

_METODOS_LECTURA = {"GET", "HEAD", "OPTIONS"}


def _ruta(request: Request) -> str:
    path = request.url.path
    root_path = request.scope.get("root_path", "")
    if root_path and path.startswith(root_path):
        path = path[len(root_path):]
    return path


def es_ruta_publica(request: Request) -> bool:
    if request.method == "OPTIONS":
        return True
    path = _ruta(request)
    return any(request.method == metodo and path.startswith(ruta) for metodo, ruta in RUTAS_PUBLICAS)


def necesita_admin(request: Request) -> bool:
    """Toda petición que modifica datos (POST, PUT, PATCH, DELETE) exige rol de administrador, salvo RUTAS_POST_LECTURA."""
    if request.method in _METODOS_LECTURA:
        return False
    path = _ruta(request)
    return not any(request.method == metodo and path == ruta for metodo, ruta in RUTAS_POST_LECTURA)


def permitAll() -> bool:
    """Indica si el backend está en modo de desarrollo y no requiere autenticación (JWT)."""
    return os.getenv("APP_SECURITY_PERMIT_ALL", "false").lower() in {"1", "true", "yes"}


def configurar_cors(app: FastAPI) -> None:
    cors_origins_env = os.getenv("CORS_ORIGINS")
    if cors_origins_env:
        origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["Content-Disposition"],  # nombre del Excel descargado
        )
    else:
        # sin lista de orígenes acepta cualquiera con credenciales: solo en desarrollo
        if os.getenv("APP_ENV", "development").strip().lower() == "production":
            raise RuntimeError("CORS_ORIGINS es obligatorio en producción (orígenes del frontend separados por coma).")
        logger.warning("CORS_ORIGINS no está definido: se acepta cualquier origen (solo para desarrollo).")
        app.add_middleware(
            CORSMiddleware,
            allow_origin_regex=r"https?://.*",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["Content-Disposition"],  # nombre del Excel descargado
        )
