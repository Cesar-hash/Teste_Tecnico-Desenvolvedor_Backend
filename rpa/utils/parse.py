""" Módulo responsável por realizar o parsing do conteúdo HTML retornado pela função fetch_page e extrair os dados dos atos publicados na data de busca. 
Retorna uma lista de dicionários, onde cada dicionário representa um ato publicado, contendo as chaves: tipo_ato, numero_ato, orgao, data_publicacao e ementa. """

import logging
from typing import Any, Dict, List
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def parse_data(html_content: str) -> List[Dict[str, Any]]:
    if not html_content:
        logger.warning("Conteúdo HTML vazio recebido para parsing.")
        return []

    soup = BeautifulSoup(html_content, "html.parser")
    result_table = soup.find("table", id="tabelaAtos")
    if not result_table:
        logger.warning("Tabela de atos não encontrada.")
        return []

    tbody = result_table.find("tbody")
    if not tbody:
        logger.warning("Corpo da tabela de atos não encontrado.")
        return []

    acts = []

    for row in tbody.find_all("tr", class_="linhaResultados"):
        cells = row.find_all("td")
        if len(cells) != 5:
            continue

        data_publicacao_br = cells[3].get_text(strip=True)
        data_publicacao = f"{data_publicacao_br[6:10]}-{data_publicacao_br[3:5]}-{data_publicacao_br[0:2]}"

        acts.append(
            {
                "tipo_ato": cells[0].get_text(strip=True),
                "numero_ato": cells[1].get_text(strip=True),
                "orgao": cells[2].get_text(strip=True),
                "data_publicacao": data_publicacao,
                "ementa": cells[4].get_text(strip=True),
            }
        )

    logger.info("Parsing concluído. Total de atos extraídos: %d", len(acts))
    return acts