"""Configuración de seguridad del TMI (como WebSecurityConfig de essalud-gcpp-backend): rutas públicas y CORS."""

import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Rutas que no exigen sesión (permitAll). Se compara el inicio de la ruta: "/x/" equivale a "/x/**" en Spring.
# Solo lectura: nunca poner aquí rutas que creen, modifiquen o borren datos.
RUTAS_PUBLICAS = [
    ("GET", "/tmi/dinamico/dashboard/"),
]


def es_ruta_publica(request: Request) -> bool:
    if request.method == "OPTIONS":
        return True
    path = request.url.path
    root_path = request.scope.get("root_path", "")
    if root_path and path.startswith(root_path):
        path = path[len(root_path):]
    return any(request.method == metodo and path.startswith(ruta) for metodo, ruta in RUTAS_PUBLICAS)


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
        app.add_middleware(
            CORSMiddleware,
            allow_origin_regex=r"https?://.*",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["Content-Disposition"],  # nombre del Excel descargado
        )
