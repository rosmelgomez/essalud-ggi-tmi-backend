import asyncio
import contextlib
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.main.controller import apiTmi, apiCierre, apiTmiDinamico
from src.main.core.security import agregar_cookie_access_token
from src.main.core.tmiConfig import TMI_EJECUTAR_SQL
from src.main.db.sqlRunner import ejecutar_scripts
from src.main.service.cierreServ import tareaCierre

load_dotenv()

is_production = os.getenv("APP_ENV", "development").strip().lower() == "production"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # scripts del TMI dinámico (tablas, vistas, datos iniciales y procedimientos), como ExecuteQuery del gcpp
    if TMI_EJECUTAR_SQL:
        await asyncio.to_thread(ejecutar_scripts)
    # crea la tabla cierre, inserta la fecha por defecto y revisa el cierre periódicamente
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


# si get_current_user regeneró el access_token con el api_token, se envía en la respuesta como cookie
@app.middleware("http")
async def refrescar_access_token(request: Request, call_next):
    response = await call_next(request)
    agregar_cookie_access_token(request, response)
    return response


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

app.include_router(apiTmi.router)
app.include_router(apiCierre.router)
app.include_router(apiTmiDinamico.router)

