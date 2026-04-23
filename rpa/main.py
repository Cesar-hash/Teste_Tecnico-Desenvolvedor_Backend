""" Ponto de entrada para a execução do módulo RPA de forma independente.
Permite rodar o scraper via comando 'python -m rpa'. """

import logging
from rpa.web.scraper import run_scraper


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(message)s"
    )
    logging.info("Executando o módulo RPA diretamente...")
    run_scraper()   