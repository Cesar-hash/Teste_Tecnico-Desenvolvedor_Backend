""" Modelos para representar as entidades no banco de dados e facilitar a manipulação dos dados."""

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Text, func
from api.database.database import Base


class Ato(Base):
    __tablename__ = "atos"

    id = Column(Integer, primary_key=True, index=True)
    tipo_ato = Column(String(255), nullable=False, index=True)
    numero_ato = Column(String(255), nullable=False, unique=True, index=True)
    orgao = Column(String(255), nullable=False, index=True)
    data_publicacao = Column(Date, nullable=False, index=True)
    ementa = Column(Text, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False, server_default="false")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True, server_default="true")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())