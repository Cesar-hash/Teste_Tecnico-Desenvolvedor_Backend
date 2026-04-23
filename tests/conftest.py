""" Configurações e fixtures para os testes, utilizando pytest. """

from pathlib import Path
import sys
import os
os.environ["ENV"] = "test"
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from api.database.database import Base, get_db
from api.main import app


# Cria um banco SQLite temporário para os testes. Isso evita dependência do postgreSQL do Docker e garante isolamento.
@pytest.fixture()
def client(tmp_path):
    test_db_path = tmp_path / "test.db"

    engine = create_engine(
        f"sqlite:///{test_db_path}",
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture()
def auth_headers(client):
    client.post(
        "/api/v1/auth/register",
        json={"username": "admin", "password": "1234"},
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "1234"},
    )

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}