"""Lectura y validación del JWT que emite essalud-gcpp-backend (este backend no genera ni renueva tokens)."""

import base64
import logging
import os
import time
from typing import Dict

import warnings
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status

# InsecureKeyLengthWarning solo existe en versiones recientes de PyJWT
_insecure_key_warning = getattr(jwt, "InsecureKeyLengthWarning", None) or getattr(
    getattr(jwt, "warnings", None), "InsecureKeyLengthWarning", None
)
if _insecure_key_warning is not None:
    warnings.filterwarnings("ignore", category=_insecure_key_warning)

load_dotenv()

logger = logging.getLogger(__name__)

raw_secret_str = (
    os.getenv("JWT_SECRET_BASE64")
    or os.getenv("APP_SECURITY_JWT_ACCESS_SECRET")
    or "cXViZWNhc2g1bTZuN284cDlxdXJzdHV2d3h5emFiY2Qx"
).strip()

missing_padding = len(raw_secret_str) % 4
if missing_padding:
    raw_secret_str += "=" * (4 - missing_padding)

try:
    RAW_SECRET_KEY = base64.b64decode(raw_secret_str)
    if not RAW_SECRET_KEY:
        RAW_SECRET_KEY = raw_secret_str.encode("utf-8")
except Exception as e:
    logger.error("Error al decodificar clave secreta JWT: %s", e)
    RAW_SECRET_KEY = raw_secret_str.encode("utf-8")

# Se aceptan los HMAC que puede generar essalud-gcpp-backend
JWT_ALGORITHMS_PERMITIDOS = ["HS256", "HS384", "HS512"]
ACCESS_COOKIE_NAME = os.getenv("JWT_ACCESS_COOKIE_NAME", "access_token")
# Margen para la diferencia de hora entre el servidor que firma (essalud-gcpp-backend) y este:
# sin él, un reloj adelantado unos segundos da el token por vencido o "todavía no válido" (iat)
JWT_LEEWAY_SECONDS = int(os.getenv("JWT_LEEWAY_SECONDS", "120"))


def usuario_desde_token(token: str, clave: bytes = RAW_SECRET_KEY, tipo_esperado: str = "access") -> Dict:
    try:
        payload = jwt.decode(
            token,
            clave,
            algorithms=JWT_ALGORITHMS_PERMITIDOS,
            options={"verify_exp": True},
            leeway=JWT_LEEWAY_SECONDS,
        )
    except jwt.ExpiredSignatureError:
        logger.info("Token %s vencido.", tipo_esperado)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La sesión ha expirado. Por favor, vuelva a iniciar sesión.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.InvalidTokenError, jwt.PyJWTError) as exc:
        logger.warning("Fallo en verificación de JWT (%s): %s", tipo_esperado, exc)
        if isinstance(exc, jwt.ImmatureSignatureError):
            _avisar_diferencia_reloj(token, tipo_esperado)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o firma no autorizada.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_type = payload.get("token_type")
    # el access_token puede no traer token_type (tokens antiguos)
    if token_type and token_type != tipo_esperado:
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


def _avisar_diferencia_reloj(token: str, tipo: str) -> None:
    """Deja en el log cuánto difiere la hora del token de la de este servidor (causa típica al cambiar de equipo)."""
    try:
        claims = jwt.decode(token, options={"verify_signature": False})
        ahora = int(time.time())
        logger.warning(
            "Token %s emitido en el futuro: emitido hace %s s, vence en %s s (margen %s s). "
            "La hora de este servidor está atrasada respecto a essalud-gcpp-backend: sincronice los relojes.",
            tipo, ahora - int(claims.get("iat", ahora)), int(claims.get("exp", ahora)) - ahora, JWT_LEEWAY_SECONDS,
        )
    except Exception:
        pass
