""" Módulo para obter as datas de busca, calculando os últimos dias a partir da data atual. """
from datetime import date, timedelta


def get_search_dates(days_back: int = 3) -> list[str]:
    today = date.today()
    return [
        (today - timedelta(days=offset)).strftime("%d/%m/%Y")
        for offset in range(days_back + 1)
    ]