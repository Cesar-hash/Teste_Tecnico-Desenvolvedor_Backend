""" API de Atos da Receita Federal - Módulo Principal
Este módulo é o ponto de entrada da aplicação FastAPI, responsável por configurar a aplicação, 
incluir os routers dos diferentes módulos e definir as rotas principais. """

import os
import logging
import sys
from fastapi import FastAPI
from api.database.database import Base, engine
from api.v1.api import api_router


logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - [%(levelname)s] - [%(filename)s -> %(funcName)s()] - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Atos da Receita Federal",
    description="API para coletar, armazenar e consultar atos normativos da Receita Federal.",
    version="1.0.0",
)
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
def on_startup():
    if os.getenv("ENV") != "test":
        Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Root"])
def read_root():
    return {"status": "API está online!"}