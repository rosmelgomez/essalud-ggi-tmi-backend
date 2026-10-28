import base64
import logging
import os
import time
import uuid
from typing import Dict, List, Optional

import warnings
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request, status

warnings.filterwarnings("ignore", category=jwt.InsecureKeyLengthWarning)

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

def _algoritmo_por_clave(clave: bytes) -> str:
    # Igual que jjwt (signWith) en essalud-gcpp-backend: el HMAC depende del tamaño de la clave
    if len(clave) >= 64:
        return "HS512"
    if len(clave) >= 48:
        return "HS384"
    return "HS256"


# Se aceptan los HMAC que puede generar essalud-gcpp-backend; al firmar se usa el que corresponde a la clave
JWT_ALGORITHMS_PERMITIDOS = ["HS256", "HS384", "HS512"]
JWT_ALGORITHM = _algoritmo_por_clave(RAW_SECRET_KEY)
ACCESS_COOKIE_NAME = os.getenv("JWT_ACCESS_COOKIE_NAME", "access_token")

# Refresco transparente del access_token con la cookie api_token (igual que essalud-gcpp-backend)
API_COOKIE_NAME = os.getenv("JWT_API_COOKIE_NAME", "api_token")
JWT_ISSUER = os.getenv("JWT_ISSUER", "essalud-gcpp-backend")
ACCESS_TOKEN_VALIDITY_SECONDS = int(os.getenv("JWT_ACCESS_TOKEN_VALIDITY_SECONDS", "900"))
COOKIE_SECURE = os.getenv("JWT_COOKIE_SECURE", "false").strip().lower() == "true"
COOKIE_SAME_SITE = os.getenv("JWT_COOKIE_SAME_SITE", "lax").strip().lower()


def _decodificar_clave(valor: str) -> bytes:
    valor = valor.strip()
    valor += "=" * (-len(valor) % 4)
    try:
        return base64.b64decode(valor) or valor.encode("utf-8")
    except Exception:
        return valor.encode("utf-8")


_api_secret = os.getenv("APP_SECURITY_JWT_API_SECRET", "").strip()
API_SECRET_KEY: Optional[bytes] = _decodificar_clave(_api_secret) if _api_secret else None
if API_SECRET_KEY is None:
    logger.warning("APP_SECURITY_JWT_API_SECRET no configurado: el access_token no se refrescará automáticamente.")


def get_current_user(request: Request) -> Dict:
    """
    Extrae y valida el JWT desde la Cookie 'access_token' (enviada por Angular con withCredentials)
    o desde la cabecera 'Authorization: Bearer <token>'.
    Si el access_token no existe o expiró, lo regenera con la cookie 'api_token' (como essalud-gcpp-backend);
    el middleware de app.py devuelve el nuevo access_token en una cookie.
    """
    token: Optional[str] = request.cookies.get(ACCESS_COOKIE_NAME)

    if not token and "Authorization" in request.headers:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
        elif auth_header:
            token = auth_header.strip()

    error: Optional[HTTPException] = None
    if token:
        try:
            return _usuario_desde_token(token, RAW_SECRET_KEY, "access")
        except HTTPException as exc:
            error = exc

    usuario = _refrescar_access_token(request)
    if usuario:
        return usuario

    raise error or HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Acceso no autorizado: No se encontró sesión activa.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def _usuario_desde_token(token: str, clave: bytes, tipo_esperado: str) -> Dict:
    try:
        payload = jwt.decode(
            token,
            clave,
            algorithms=JWT_ALGORITHMS_PERMITIDOS,
            options={"verify_exp": True},
        )
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

    token_type = payload.get("token_type")
    # el access_token puede no traer token_type (tokens antiguos); el api_token siempre debe traerlo
    if (token_type or tipo_esperado == "api") and token_type != tipo_esperado:
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


def _refrescar_access_token(request: Request) -> Optional[Dict]:
    """Valida el api_token (cookie de larga duración) y genera un access_token nuevo con los mismos datos."""
    api_token = request.cookies.get(API_COOKIE_NAME)
    if not api_token or API_SECRET_KEY is None:
        return None
    try:
        usuario = _usuario_desde_token(api_token, API_SECRET_KEY, "api")
    except HTTPException as exc:
        logger.info("No se pudo refrescar el access_token: %s", exc.detail)
        return None
    if usuario["claims"].get("iss") != JWT_ISSUER:
        logger.warning("api_token con emisor no permitido: %s", usuario["claims"].get("iss"))
        return None

    ahora = int(time.time())
    claims = {
        "authorities": ",".join(usuario["authorities"]),
        "token_type": "access",
        "jti": str(uuid.uuid4()),
        "sub": usuario["username"],
        "iat": ahora,
        "iss": JWT_ISSUER,
        "exp": ahora + ACCESS_TOKEN_VALIDITY_SECONDS,
    }
    request.state.nuevo_access_token = jwt.encode(claims, RAW_SECRET_KEY, algorithm=JWT_ALGORITHM)
    logger.info("Access token regenerado para '%s' desde el api_token.", usuario["username"])
    return {"username": usuario["username"], "authorities": usuario["authorities"], "claims": claims}


def agregar_cookie_access_token(request: Request, response) -> None:
    """Devuelve al navegador el access_token regenerado en esta petición (si lo hubo)."""
    nuevo = getattr(request.state, "nuevo_access_token", None)
    if nuevo:
        response.set_cookie(
            key=ACCESS_COOKIE_NAME,
            value=nuevo,
            max_age=ACCESS_TOKEN_VALIDITY_SECONDS,
            path="/",
            httponly=True,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAME_SITE,
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
