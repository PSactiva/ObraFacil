import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_health_check(client):
    r = client.get("/api/health/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@pytest.mark.django_db
def test_calcular_area_permite_acesso_publico(client):
    response = client.post(
        "/api/calculos/area/",
        {"comprimento": 4, "largura": 3},
        format="json",
    )

    assert response.status_code == 200
    assert response.json() == {"area_m2": 12.0}


@pytest.mark.django_db
def test_obter_token_com_credenciais_validas(client, user):
    response = client.post(
        "/api/auth/token/",
        {"username": "testuser", "password": "testpass123"},
        format="json",
    )

    assert response.status_code == 200
    assert response.json().get("token")


@pytest.mark.django_db
def test_rejeitar_credenciais_invalidas_para_token(client, user):
    response = client.post(
        "/api/auth/token/",
        {"username": "testuser", "password": "senha-incorreta"},
        format="json",
    )

    assert response.status_code == 400
