""" Testes para as rotas de RPA, utilizando pytest e o cliente de teste do FastAPI. """

def test_trigger_extraction(client, auth_headers, monkeypatch):
    from api.v1.endpoints import rpa

    fake_data = [
        {
            "tipo_ato": "Solução de Consulta",
            "numero_ato": "999",
            "orgao": "COSIT",
            "data_publicacao": "2026-04-21",
            "ementa": "Teste de scraping",
        }
    ]

    monkeypatch.setattr(rpa, "scrape_recent_acts", lambda: fake_data)

    response = client.post("/api/v1/rpa/trigger-extraction", headers=auth_headers)
    assert response.status_code == 200

    body = response.json()
    assert body["found"] == 1
    assert body["inserted"] == 1
    assert body["items"][0]["numero_ato"] == "999"