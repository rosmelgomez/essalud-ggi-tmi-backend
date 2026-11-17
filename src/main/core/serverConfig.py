"""Configuración del servidor (como server.servlet.context-path=/ggi de essalud-gcpp-backend)."""

import os

from dotenv import load_dotenv

load_dotenv()

# Prefijo común de todas las APIs: cada controlador solo declara el suyo (/variable, /indicador...) y app.py los
# monta todos debajo de este. Se cambia con TMI_CONTEXT_PATH en el .env.
CONTEXT_PATH = "/" + os.getenv("TMI_CONTEXT_PATH", "/tmi").strip().strip("/")
