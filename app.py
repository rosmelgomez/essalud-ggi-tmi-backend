import asyncio
import contextlib
import logging
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()
# un solo formato de log para todo el backend (antes de importar los módulos, que ya escriben al importarse);
# nivel con LOG_LEVEL (DEBUG, INFO, WARNING...; por defecto INFO)
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(),
                    format="%(asctime)s %(levelname)s [%(name)s] %(message)s")

from fastapi import FastAPI, Request
from src.main.controller import apiCentro, apiCierre, apiEstandar, apiIndicador, apiTmiDinamico, apiVariable
from src.main.core.tmiConfig import TMI_EJECUTAR_SQL
from src.main.db.auditoria import USUARIO_ACTUAL
from src.main.db.sqlRunner import ejecutar_scripts
from src.main.security.errores import configurar_errores
from src.main.security.jwtRequestFilter import usuario_de_la_peticion
from src.main.security.webSecurityConfig import configurar_cors
from src.main.model.tablas import crear_tablas
from src.main.service.cierreServ import tareaCierre

is_production = os.getenv("APP_ENV", "development").strip().lower() == "production"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # tablas desde src/main/model (como ddl-auto) y scripts del TMI dinámico (datos iniciales, vistas y procedimientos)
    if TMI_EJECUTAR_SQL:
        await asyncio.to_thread(ejecutar_scripts)
    else:
        await asyncio.to_thread(crear_tablas)
    # inserta la fecha de cierre por defecto y revisa el cierre periódicamente
    tarea = asyncio.create_task(tareaCierre())
    yield
    tarea.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await tarea


app = FastAPI(
    lifespan=lifespan,
    title="microservicio de gestion del tmi",
    description="gestion del tmi",
    docs_url=None if is_production else "/docs",
    redoc_url=None if is_production else "/redoc",
    openapi_url=None if is_production else "/openapi.json",
)


configurar_cors(app)
configurar_errores(app)   # errores de SQL Server: mensaje para el usuario, detalle solo en el log


@app.middleware("http")
async def usuario_para_historial(request: Request, call_next):
    """Usuario del token para el historial de cambios (no valida permisos: eso lo hace get_current_user)."""
    marca = USUARIO_ACTUAL.set(usuario_de_la_peticion(request))
    try:
        return await call_next(request)
    finally:
        USUARIO_ACTUAL.reset(marca)

app.include_router(apiCentro.router)
app.include_router(apiEstandar.router)
app.include_router(apiCierre.router)
app.include_router(apiTmiDinamico.router)
app.include_router(apiVariable.router)
app.include_router(apiIndicador.router)
app.include_router(apiEstandar.routerDinamico)
app.include_router(apiCentro.routerDinamico)

