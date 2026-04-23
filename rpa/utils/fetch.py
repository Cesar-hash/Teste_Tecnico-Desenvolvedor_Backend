""" Módulo responsável por realizar a requisição HTTP para a página de consulta da Receita, filtrando os atos pela data. """

import logging
from requests_html import HTMLSession
from infra.config import settings


logger = logging.getLogger(__name__)


def fetch_page(search_date: str) -> str:
    """ Realiza a requisição HTTP para a página de consulta da Receita
    filtrando os atos pela data"""
    
    payload = {
        "dt_inicio": search_date,
        "dt_fim": search_date,
        "consulta.tipoAto": "0",
        "consulta.ordenacao": "2",
    }

    logger.info("Buscando atos para a data %s", search_date)

    session = HTMLSession()
    response = session.post(settings.rpa_target_url, data=payload, timeout=30)
    response.raise_for_status()

    logger.info("Resposta recebida com status_code=%s para data=%s", response.status_code, search_date)
    return response.text