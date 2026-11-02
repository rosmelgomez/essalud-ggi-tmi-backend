import asyncio
import contextlib
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.main.controller import apiCentro, apiCierre, apiEstandar, apiIndicador, apiTmiDinamico, apiVariable
from src.main.core.tmiConfig import TMI_EJECUTAR_SQL
from src.main.db.sqlRunner import ejecutar_scripts
from src.main.model.tablas import crear_tablas
from src.main.service.cierreServ import tareaCierre

load_dotenv()

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


cors_origins_env = os.getenv("CORS_ORIGINS")
if cors_origins_env:
    origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],  # nombre del Excel descargado
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https?://.*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],  # nombre del Excel descargado
    )

app.include_router(apiCentro.router)
app.include_router(apiEstandar.router)
app.include_router(apiCierre.router)
app.include_router(apiTmiDinamico.router)
app.include_router(apiVariable.router)
app.include_router(apiIndicador.router)
app.include_router(apiEstandar.routerDinamico)
app.include_router(apiCentro.routerDinamico)

