import asyncio
import contextlib
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.main.controller import apiTmi, apiCierre
from src.main.service.cierreServ import tareaCierre

load_dotenv()

is_production = os.getenv("APP_ENV", "development").strip().lower() == "production"


@asynccontextmanager
async def lifespan(app: FastAPI):
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

cors_origins_env = os.getenv("CORS_ORIGINS")
if cors_origins_env:
    origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https?://.*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(apiTmi.router)
app.include_router(apiCierre.router)

