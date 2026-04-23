""" Testes para as rotas de autenticação, utilizando pytest e o cliente de teste do FastAPI. """

def test_register_and_login(client):
    register = client.post("/api/v1/auth/register", json={"username": "maria", "password": "1234"})
    assert register.status_code == 201

    login = client.post("/api/v1/auth/login", json={"username": "maria", "password": "1234"})
    assert login.status_code == 200

    body = login.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"