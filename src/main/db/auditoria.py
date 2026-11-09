"""Usuario de cada cambio para el historial de la configuración (tmi_config_historial, triggers de 06_historial.sql).

El middleware de app.py guarda el usuario del token en USUARIO_ACTUAL (una variable de contexto: cada petición tiene la
suya, también en los endpoints que corren en un hilo aparte). Cada vez que la API toma una conexión del pool, se copia
a CONTEXT_INFO de esa conexión y los triggers lo leen. Sin usuario (tareas internas) se limpia, para que una conexión
reutilizada no arrastre el usuario de otra petición."""

from contextvars import ContextVar
from typing import Optional

from sqlalchemy import event
from sqlalchemy.engine import Engine

USUARIO_ACTUAL: ContextVar[Optional[str]] = ContextVar("usuario_tmi", default=None)

# lo que cabe en CONTEXT_INFO (VARBINARY(128))
_MAXIMO = 128


def instalar(engine: Engine) -> None:
    @event.listens_for(engine, "checkout")
    def _usuario_en_conexion(dbapi_con, _registro, _proxy):
        usuario = (USUARIO_ACTUAL.get() or "")[:_MAXIMO]
        cursor = dbapi_con.cursor()
        try:
            cursor.execute("DECLARE @c VARBINARY(128); SET @c = CAST(CAST(? AS VARCHAR(128)) AS VARBINARY(128)); "
                           "SET CONTEXT_INFO @c", usuario)
        finally:
            cursor.close()
