""" Endpoints relacionados à interface web da aplicação, incluindo páginas de login, dashboard e listagem de atos administrativos.
Este módulo é responsável por renderizar as páginas HTML utilizando Jinja2 templates e fornecer os dados necessários para exibição, como resumos e listas de atos administrativos.
Ele utiliza as funções de serviço definidas em api.services para obter os dados do banco de dados e os filtros de busca. """

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from api.database.database import get_db
from api.services import dashboard_summary, list_atos


router = APIRouter()
templates = Jinja2Templates(directory="api/templates")


# Redireciona para a página de login por padrão
@router.get("/")
def web_root():
    return RedirectResponse(url="/api/v1/web/login")


# Renderiza a página de login
@router.get("/login")
def login_page(request: Request):
    # Renderiza a página de login
    return templates.TemplateResponse(
        "login.html",
        {"request": request},
    )


# Obtém os resumos para o dashboard e a lista de atos com base nos filtros de busca e data de publicação, 
# e renderiza a página do dashboard com esses dados
@router.get("/dashboard")
def dashboard_page(
    request: Request,
    search: str = Query(default=""),
    data_publicacao: str = Query(default=""),
    db: Session = Depends(get_db),
):
    summary = dashboard_summary(db, search=search, data_publicacao=data_publicacao)
    atos = list_atos(db, search=search, data_publicacao=data_publicacao)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "search": search,
            "data_publicacao": data_publicacao,
            "summary": summary,
            "atos": atos,
        },
    )


# Obtém a lista de atos com base nos filtros de busca e data de publicação 
# e renderiza a página de listagem de atos administrativos
@router.get("/atos")
def atos_page(
    request: Request,
    search: str = Query(default=""),
    data_publicacao: str = Query(default=""),
    db: Session = Depends(get_db),
):
    atos = list_atos(db, search=search, data_publicacao=data_publicacao)

    return templates.TemplateResponse(
        "atos.html",
        {
            "request": request,
            "atos": atos,
            "search": search,
            "data_publicacao": data_publicacao,
        },
    )