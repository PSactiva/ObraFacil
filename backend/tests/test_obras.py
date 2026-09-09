from datetime import date

import pytest

from apps.obras.models import Obra


@pytest.mark.django_db
def test_listar_obras_publicamente(client):
    Obra.objects.create(nome="Residência Jardins", cliente="Ana Costa")

    response = client.get("/api/obras/")

    assert response.status_code == 200
    assert response.json()["results"][0]["nome"] == "Residência Jardins"
    assert response.json()["results"][0]["status_display"] == "Planejada"


@pytest.mark.django_db
def test_criar_obra_autenticado(authenticated_client):
    response = authenticated_client.post(
        "/api/obras/",
        {
            "nome": "Edifício Aurora",
            "cliente": "João Silva",
            "endereco": "Rua Central, 100",
            "status": "em_andamento",
            "data_inicio": "2026-09-01",
            "previsao_conclusao": "2027-03-01",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.json()["status_display"] == "Em andamento"
    assert Obra.objects.get(nome="Edifício Aurora").cliente == "João Silva"


@pytest.mark.django_db
def test_rejeitar_previsao_anterior_ao_inicio(authenticated_client):
    response = authenticated_client.post(
        "/api/obras/",
        {
            "nome": "Obra inválida",
            "cliente": "Cliente",
            "data_inicio": date(2026, 9, 10),
            "previsao_conclusao": date(2026, 9, 1),
        },
        format="json",
    )

    assert response.status_code == 400
    assert "previsao_conclusao" in response.json()
