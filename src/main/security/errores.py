"""Respuestas de error sin datos internos.

Los repositorios responden HTTPException(detail=str(e)). Cuando ese texto viene de SQL Server o del driver (nombres de
servidor, tablas, SQL), aquí se reemplaza por un mensaje para el usuario y el detalle queda en el log con un código para
ubicarlo. Los mensajes propios (validaciones, fórmula, RAISERROR de los procedimientos) se muestran igual que antes.
"""

import logging
import re
import uuid

from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)

# texto que solo aparece en errores del driver / SQLAlchemy
_MARCAS_INTERNAS = ("[Microsoft]", "[ODBC", "pyodbc", "(Background on this error", "[SQL:", "sqlalche.me",
                    "SQLExecDirect", "mssql_python")
# mensaje de RAISERROR / THROW de los procedimientos: "[SQL Server]<mensaje> (50000)"
_MENSAJE_USUARIO = re.compile(r"\[SQL Server\](.+?)\s*\(50000\)", re.DOTALL)
_CONOCIDOS = [
    (re.compile(r"duplicate key|UNIQUE KEY|clave duplicada", re.I), "Ya existe un registro con esos datos."),
    (re.compile(r"REFERENCE constraint|conflicted with the (DELETE|REFERENCE)", re.I),
     "No se puede eliminar o cambiar: el registro está en uso en otra parte del TMI."),
    (re.compile(r"FOREIGN KEY constraint", re.I), "El dato relacionado no existe (revise los valores elegidos)."),
    (re.compile(r"cannot insert the value NULL|NULL into column", re.I), "Falta un dato obligatorio."),
    (re.compile(r"String or binary data would be truncated|datos de cadena o binarios", re.I),
     "Un texto es más largo de lo permitido."),
    (re.compile(r"deadlock", re.I), "La base de datos estaba ocupada: vuelva a intentarlo."),
    (re.compile(r"timeout|tiempo de espera", re.I), "La base de datos tardó demasiado en responder: vuelva a intentarlo."),
]


def es_error_interno(texto: str) -> bool:
    return any(m in texto for m in _MARCAS_INTERNAS)


def mensaje_seguro(texto: str, status_code: int) -> str:
    """Mensaje para el usuario a partir del texto del error de base de datos; deja el detalle en el log."""
    if (m := _MENSAJE_USUARIO.search(texto)) and "[TMI-INTERNO]" not in m.group(1):
        return m.group(1).strip()
    codigo = uuid.uuid4().hex[:8]
    logger.error("Error de base de datos [%s] (HTTP %s): %s", codigo, status_code, texto)
    for patron, mensaje in _CONOCIDOS:
        if patron.search(texto):
            return f"{mensaje} (código {codigo})"
    return f"No se pudo completar la operación por un error en la base de datos (código {codigo})."


def configurar_errores(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def _http(request: Request, exc: StarletteHTTPException):
        if isinstance(exc.detail, str) and es_error_interno(exc.detail):
            return JSONResponse({"detail": mensaje_seguro(exc.detail, exc.status_code)},
                                status_code=exc.status_code, headers=getattr(exc, "headers", None))
        return await http_exception_handler(request, exc)

    @app.exception_handler(Exception)
    async def _no_controlado(request: Request, exc: Exception):
        codigo = uuid.uuid4().hex[:8]
        logger.error("Error no controlado [%s] en %s %s", codigo, request.method, request.url.path, exc_info=exc)
        return JSONResponse({"detail": f"Error interno del servidor (código {codigo})."}, status_code=500)
