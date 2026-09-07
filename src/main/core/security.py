import base64
import logging
import os
from typing import Dict, List, Optional

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request, status

load_dotenv()

logger = logging.getLogger(__name__)

JWT_SECRET_BASE64 = os.getenv(
    "APP_SECURITY_JWT_ACCESS_SECRET",
    "",
)
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS512")
ACCESS_COOKIE_NAME = os.getenv("JWT_ACCESS_COOKIE_NAME", "access_token")

try:
    missing_padding = len(JWT_SECRET_BASE64) % 4
    padded_secret = JWT_SECRET_BASE64 + "=" * ((4 - missing_padding) % 4) if missing_padding else JWT_SECRET_BASE64
    RAW_SECRET_KEY = base64.b64decode(padded_secret)
except Exception as e:
    logger.error("Error al decodificar JWT_SECRET_BASE64: %s", e)
    RAW_SECRET_KEY = JWT_SECRET_BASE64.encode("utf-8")


def get_current_user(request: Request) -> Dict:
    """
    Extrae y valida el JWT desde la Cookie 'access_token' (enviada por Angular con withCredentials)
    o desde la cabecera 'Authorization: Bearer <token>'.
    """
    token: Optional[str] = request.cookies.get(ACCESS_COOKIE_NAME)

    if not token and "Authorization" in request.headers:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
        elif auth_header:
            token = auth_header.strip()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso no autorizado: No se encontró sesión activa.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            token,
            RAW_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={"verify_exp": True},
        )

        token_type = payload.get("token_type")
        if token_type and token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tipo de token inválido para este servicio.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token no contiene identidad de usuario válida.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        raw_authorities = payload.get("authorities", "")
        if isinstance(raw_authorities, list):
            authorities = raw_authorities
        elif isinstance(raw_authorities, str):
            authorities = [a.strip() for a in raw_authorities.split(",") if a.strip()]
        else:
            authorities = []

        return {
            "username": username,
            "authorities": authorities,
            "claims": payload,
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La sesión ha expirado. Por favor, vuelva a iniciar sesión.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.InvalidTokenError, jwt.PyJWTError) as exc:
        logger.warning("Fallo en verificación de JWT: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o firma no autorizada.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_role(required_role: str):
    """
    Dependencia para requerir un rol específico (e.g. 'ADMIN', 'ADMIN_RED', 'USER').
    """
    def role_checker(current_user: Dict = Depends(get_current_user)):
        roles = current_user.get("authorities", [])
        if required_role not in roles and "ADMIN" not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso denegado: requiere el rol '{required_role}'.",
            )
        return current_user
    return role_checker
