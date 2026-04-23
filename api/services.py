""" Serviços para manipulação de dados de atos e usuários. """

from collections import Counter
from typing import Iterable, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from api.models.models import Ato, User
from api.schemas.schemas import AtoCreate, AtoUpdate


def create_user(db: Session, username: str, password_hash: str) -> User:
    user = User(username=username, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def create_ato(db: Session, payload: AtoCreate) -> Ato:
    if db.query(Ato).filter(Ato.numero_ato == payload.numero_ato).first():
        raise ValueError("Já existe ato com este número")

    ato = Ato(**payload.model_dump())
    db.add(ato)
    db.commit()
    db.refresh(ato)
    return ato


def bulk_insert_atos(db: Session, atos: Iterable[AtoCreate]) -> list[Ato]:
    atos = list(atos)
    if not atos:
        return []

    numeros = [ato.numero_ato for ato in atos]
    existentes = {
        numero
        for (numero,) in db.query(Ato.numero_ato).filter(Ato.numero_ato.in_(numeros)).all()
    }

    novos = []
    for ato in atos:
        if ato.numero_ato in existentes:
            continue
        novos.append(Ato(**ato.model_dump()))
        existentes.add(ato.numero_ato)

    if not novos:
        return []

    db.add_all(novos)
    db.commit()

    for ato in novos:
        db.refresh(ato)

    return novos


def list_atos(db: Session, search: str = "", data_publicacao: str = "") -> list[Ato]:
    query = db.query(Ato).filter(Ato.is_deleted.is_(False))

    if search:
        like = f"%{search}%"
        query = query.filter(
            or_(
                Ato.tipo_ato.ilike(like),
                Ato.numero_ato.ilike(like),
                Ato.orgao.ilike(like),
                Ato.ementa.ilike(like),
            )
        )

    if data_publicacao:
        query = query.filter(Ato.data_publicacao == data_publicacao)

    return query.order_by(Ato.data_publicacao.desc(), Ato.id.desc()).all()


def get_ato(db: Session, ato_id: int) -> Optional[Ato]:
    return db.query(Ato).filter(Ato.id == ato_id, Ato.is_deleted.is_(False)).first()


def update_ato(db: Session, ato_id: int, payload: AtoUpdate) -> Optional[Ato]:
    ato = get_ato(db, ato_id)
    if not ato:
        return None

    data = payload.model_dump(exclude_unset=True)

    if "numero_ato" in data and data["numero_ato"] != ato.numero_ato:
        duplicated = db.query(Ato).filter(Ato.numero_ato == data["numero_ato"], Ato.id != ato_id).first()
        if duplicated:
            raise ValueError("Já existe ato com este número")

    for key, value in data.items():
        setattr(ato, key, value)

    db.commit()
    db.refresh(ato)
    return ato


def delete_ato(db: Session, ato_id: int) -> bool:
    ato = get_ato(db, ato_id)
    if not ato:
        return False

    ato.is_deleted = True
    db.commit()
    return True


def dashboard_summary(db: Session, search: str = "", data_publicacao: str = "") -> dict:
    atos = list_atos(db, search=search, data_publicacao=data_publicacao)
    tipo_counter = Counter(ato.tipo_ato for ato in atos)
    orgao_counter = Counter(ato.orgao for ato in atos)

    return {
        "total_registros": len(atos),
        "por_tipo_ato": [
            {"label": label, "total": total}
            for label, total in sorted(tipo_counter.items(), key=lambda item: (-item[1], item[0]))
        ],
        "por_orgao": [
            {"label": label, "total": total}
            for label, total in sorted(orgao_counter.items(), key=lambda item: (-item[1], item[0]))
        ],
    }