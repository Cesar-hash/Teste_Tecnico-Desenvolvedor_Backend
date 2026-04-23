""" Testes para as rotas do dashboard, utilizando pytest e o cliente de teste do FastAPI. """

def test_dashboard_summary(client, auth_headers):
    atos = [
        {
            "tipo_ato": "Instrução Normativa",
            "numero_ato": "1",
            "orgao": "RFB",
            "data_publicacao": "2026-04-20",
            "ementa": "Ato 1",
        },
        {
            "tipo_ato": "Portaria",
            "numero_ato": "2",
            "orgao": "RFB",
            "data_publicacao": "2026-04-20",
            "ementa": "Ato 2",
        },
    ]

    response = client.post("/api/v1/atos/bulk", json=atos, headers=auth_headers)
    assert response.status_code == 201

    dashboard = client.get("/api/v1/dashboard/")
    assert dashboard.status_code == 200

    body = dashboard.json()
    assert body["total_registros"] == 2
    assert len(body["por_tipo_ato"]) == 2
    assert body["por_orgao"][0]["label"] == "RFB"
    assert body["por_orgao"][0]["total"] == 2