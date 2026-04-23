""" Testes para as rotas de Atos, utilizando pytest e o cliente de teste do FastAPI. """

def test_create_list_update_delete_ato(client, auth_headers):
    payload = {
        "tipo_ato": "Instrução Normativa",
        "numero_ato": "123",
        "orgao": "RFB",
        "data_publicacao": "2026-04-20",
        "ementa": "Dispõe sobre teste.",
    }

    created = client.post("/api/v1/atos/", json=payload, headers=auth_headers)
    assert created.status_code == 201
    ato_id = created.json()["id"]

    listed = client.get("/api/v1/atos/")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    updated = client.put(
        f"/api/v1/atos/{ato_id}",
        json={"ementa": "Ementa alterada."},
        headers=auth_headers,
    )
    assert updated.status_code == 200
    assert updated.json()["ementa"] == "Ementa alterada."

    deleted = client.delete(f"/api/v1/atos/{ato_id}", headers=auth_headers)
    assert deleted.status_code == 204

    listed_after_delete = client.get("/api/v1/atos/")
    assert listed_after_delete.status_code == 200
    assert listed_after_delete.json() == []