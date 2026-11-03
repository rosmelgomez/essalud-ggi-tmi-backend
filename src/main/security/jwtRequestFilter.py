"""Dependencia que protege los routers (como JwtRequestFilter de essalud-gcpp-backend)."""

from typing import Dict, Optional

from fastapi import HTTPException, Request, status

from src.main.security.jwtTokenUtil import ACCESS_COOKIE_NAME, usuario_desde_token
from src.main.security.webSecurityConfig import es_ruta_publica


def get_current_user(request: Request) -> Optional[Dict]:
    """
    Valida el access_token que emite essalud-gcpp-backend: cookie 'access_token' (Angular con withCredentials)
    o cabecera 'Authorization: Bearer <token>'. Este backend no genera ni renueva tokens: si venció, responde 401
    y el frontend lo renueva en essalud-gcpp-backend y repite la petición.
    En las rutas públicas (RUTAS_PUBLICAS) no exige token: devuelve el usuario si el token es válido, si no None.
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
        return usuario_desde_token(token)
    except HTTPException:
        if publica:
            return None
        raise


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
