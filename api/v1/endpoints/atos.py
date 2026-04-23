""" Endpoints para gerenciamento de atos administrativos, incluindo criação, leitura, atualização e exclusão (CRUD).
Ele utiliza as funções de serviço definidas em api.services para interagir com o banco de dados e as funções de segurança para proteger os endpoints que modificam dados. """

import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from api.database.database import get_db
from api.schemas.schemas import AtoCreate, AtoResponse, AtoUpdate
from api.security import get_current_user
from api.services import bulk_insert_atos, create_ato, delete_ato, get_ato, list_atos, update_ato


logger = logging.getLogger(__name__)
router = APIRouter()


# Endpoints get para listar atos e obter detalhes de um ato específico, com suporte a filtros de busca e data de publicação
@router.get("/", response_model=List[AtoResponse])
def read_atos(
    search: str = Query(default=""),
    data_publicacao: str = Query(default=""),
    db: Session = Depends(get_db),
):
    logger.info("Listando atos com filtro: search=%s, data_publicacao=%s", search, data_publicacao)
    return list_atos(db, search=search, data_publicacao=data_publicacao)


# Endpoint get para obter detalhes de um ato específico por ID
@router.get("/{ato_id}", response_model=AtoResponse)
def read_ato(ato_id: int, db: Session = Depends(get_db)):
    logger.info("Buscando ato id=%s", ato_id)
    ato = get_ato(db, ato_id)
    if not ato:
        logger.warning("Ato id=%s não encontrado", ato_id)
        raise HTTPException(status_code=404, detail="Ato não encontrado")
    return ato


# Endpoints post para criar um novo ato, protegidos por autenticação
@router.post("/", response_model=AtoResponse, status_code=201, dependencies=[Depends(get_current_user)])
def create_ato_endpoint(payload: AtoCreate, db: Session = Depends(get_db)):
    logger.info("Criando ato numero_ato=%s", payload.numero_ato)
    try:
        return create_ato(db, payload)
    except ValueError as exc:
        logger.warning("Falha ao criar ato numero_ato=%s: %s", payload.numero_ato, str(exc))
        raise HTTPException(status_code=409, detail=str(exc))


# Endpoint post para criar múltiplos atos em bulk, protegido por autenticação
@router.post("/bulk", response_model=List[AtoResponse], status_code=201, dependencies=[Depends(get_current_user)])
def bulk_create_atos(payload: List[AtoCreate], db: Session = Depends(get_db)):
    logger.info("Criando bulk de atos, quantidade=%s", len(payload))
    return bulk_insert_atos(db, payload)


# Endpoints put para atualizar um ato existente, protegido por autenticação
@router.put("/{ato_id}", response_model=AtoResponse, dependencies=[Depends(get_current_user)])
def update_ato_endpoint(ato_id: int, payload: AtoUpdate, db: Session = Depends(get_db)):
    logger.info("Atualizando ato id=%s", ato_id)
    try:
        ato = update_ato(db, ato_id, payload)
    except ValueError as exc:
        logger.warning("Falha ao atualizar ato id=%s: %s", ato_id, str(exc))
        raise HTTPException(status_code=409, detail=str(exc))

    if not ato:
        logger.warning("Ato id=%s não encontrado para atualização", ato_id)
        raise HTTPException(status_code=404, detail="Ato não encontrado")

    return ato


# Endpoint delete para excluir um ato existente, protegido por autenticação
@router.delete("/{ato_id}", status_code=204, dependencies=[Depends(get_current_user)])
def delete_ato_endpoint(ato_id: int, db: Session = Depends(get_db)):
    logger.info("Excluindo ato id=%s", ato_id)
    deleted = delete_ato(db, ato_id)
    if not deleted:
        logger.warning("Ato id=%s não encontrado para exclusão", ato_id)
        raise HTTPException(status_code=404, detail="Ato não encontrado")

    logger.info("Ato id=%s excluído com sucesso", ato_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)