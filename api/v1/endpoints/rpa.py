""" Endpoint para acionar o processo de scraping e inserção dos atos recentes.
Este endpoint é protegido por autenticação, garantindo que apenas usuários autorizados possam acioná-lo."""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.database.database import get_db
from api.schemas.schemas import AtoCreate, AtoResponse
from api.security import get_current_user
from api.services import bulk_insert_atos
from rpa.web.scraper import scrape_recent_acts


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/trigger-extraction", dependencies=[Depends(get_current_user)])
def trigger_rpa_extraction(db: Session = Depends(get_db)):
    logger.info("iniciando processo de scraping de atos recentes")
    items = scrape_recent_acts()
    logger.info("Scraping finalizado. Total encontrado=%s", len(items))
    
    created = bulk_insert_atos(db, [AtoCreate.model_validate(item) for item in items])
    logger.info("Processo de inserção finalizado. Total inserido=%s", len(created))

    return {
        "found": len(items),
        "inserted": len(created),
        "items": [AtoResponse.model_validate(item).model_dump(mode="json") for item in created],
    }