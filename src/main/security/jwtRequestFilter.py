"""Dependencia que protege los routers (como JwtRequestFilter de essalud-gcpp-backend)."""

import logging
from typing import Dict, Optional

from fastapi import HTTPException, Request, status

from src.main.security.jwtTokenUtil import ACCESS_COOKIE_NAME, usuario_desde_token
from src.main.security.webSecurityConfig import AUTORIDAD_ACCESO_TMI, ROLES_ADMIN, es_ruta_publica, necesita_admin

logger = logging.getLogger(__name__)


def get_current_user(request: Request) -> Optional[Dict]:
    """
    Valida el access_token que emite essalud-gcpp-backend: cookie 'access_token' (Angular con withCredentials)
    o cabecera 'Authorization: Bearer <token>'. Este backend no genera ni renueva tokens: si venció, responde 401
    y el frontend lo renueva en essalud-gcpp-backend y repite la petición.
    En las rutas públicas (RUTAS_PUBLICAS) no exige token: devuelve el usuario si el token es válido, si no None.
    Las peticiones que modifican datos (POST, PUT, PATCH, DELETE) exigen además un rol de TMI_ROLES_ADMIN (403 si no).
    """
    publica = es_ruta_publica(request)
    token = _resolver_token(request)

    if not token:
        if publica:
            return None
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso no autorizado: No se encontró sesión activa.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        usuario = usuario_desde_token(token)
    except HTTPException:
        if publica:
            return None
        raise
    if necesita_admin(request) and not es_admin(usuario):
        logger.warning("Acceso denegado: %s sin rol %s o sin %s en %s %s", usuario.get("username"),
                       "/".join(sorted(ROLES_ADMIN)), AUTORIDAD_ACCESO_TMI, request.method, request.url.path)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No tiene permiso para modificar el TMI: se requiere el rol de administrador "
                                   "con acceso al TMI.")
    return usuario


def es_admin(usuario: Optional[Dict]) -> bool:
    """Administrador del TMI: alguno de los roles de TMI_ROLES_ADMIN (como hasAuthority('ADMIN') de essalud-gcpp-backend)
    y la autoridad ACCESS_TMI, que essalud-gcpp-backend agrega al token cuando usuario.access_tmi = true."""
    roles = {str(a).strip().upper() for a in (usuario or {}).get("authorities") or []}
    roles |= {r[5:] for r in roles if r.startswith("ROLE_")}   # acepta también ROLE_ADMIN
    return bool(roles & ROLES_ADMIN) and AUTORIDAD_ACCESO_TMI in roles


def _resolver_token(request: Request) -> Optional[str]:
    token: Optional[str] = request.cookies.get(ACCESS_COOKIE_NAME)

    if not token and "Authorization" in request.headers:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
        elif auth_header:
            token = auth_header.strip()
    return token


def nombre_usuario(current_user: dict) -> str:
    return (current_user or {}).get("username")


def usuario_de_la_peticion(request: Request) -> Optional[str]:
    """Nombre del usuario del token de la petición, o None si no hay token válido (sin validar permisos)."""
    token = _resolver_token(request)
    if not token:
        return None
    try:
        return nombre_usuario(usuario_desde_token(token))
    except Exception:
        return None
