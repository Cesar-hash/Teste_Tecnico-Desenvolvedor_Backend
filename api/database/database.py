"""Conexão com o banco de dados e criação da sessão"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from infra.config import settings


DATABASE_URL = settings.sqlalchemy_database_url
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()