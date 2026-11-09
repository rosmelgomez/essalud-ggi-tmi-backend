"""Pruebas del backend del TMI: python -m pytest  (desde la carpeta del proyecto; usan el .env para la configuración,
pero no consultan la base de datos)."""

import logging
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from dotenv import load_dotenv  # noqa: E402

load_dotenv(os.path.join(RAIZ, ".env"))
logging.disable(logging.CRITICAL)
