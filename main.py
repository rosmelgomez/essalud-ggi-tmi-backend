from fastapi import FastAPI
from src.controller import apiTmi

app = FastAPI(
title="microservicio de gestion del tmi",
description="gestion del tmi",
)

app.include_router(apiTmi.router)
