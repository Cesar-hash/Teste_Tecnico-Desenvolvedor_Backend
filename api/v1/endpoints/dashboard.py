""" Endpoint para fornecer um resumo geral dos atos administrativos, incluindo contagem total, contagem por tipo e contagem por data de publicação.
Este endpoint é útil para exibir um dashboard com estatísticas sobre os atos administrativos cadastrados no sistema. 
Ele aceita filtros de busca e data de publicação para refinar os resultados exibidos no dashboard. 
O endpoint utiliza as funções de serviço definidas em api.services para calcular os resumos a partir dos dados armazenados no banco de dados. """

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from api.database.database import get_db
from api.schemas.schemas import DashboardResponse
from api.services import dashboard_summary


router = APIRouter()


@router.get("/", response_model=DashboardResponse)
def get_dashboard(
    search: str = Query(default=""),
    data_publicacao: str = Query(default=""),
    db: Session = Depends(get_db),
):
    return dashboard_summary(db, search=search, data_publicacao=data_publicacao)