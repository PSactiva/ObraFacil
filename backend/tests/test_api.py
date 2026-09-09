import pytest
from django.contrib.auth.models import User
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


@pytest.mark.django_db
def test_cadastrar_usuario(client):
    response = client.post(
        "/api/auth/register/",
        {
            "username": "novo-usuario",
            "password": "senha-forte-123",
            "password_confirmation": "senha-forte-123",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.json()["username"] == "novo-usuario"
    assert User.objects.filter(username="novo-usuario").exists()


@pytest.mark.django_db
def test_rejeitar_cadastro_com_senhas_diferentes(client):
    response = client.post(
        "/api/auth/register/",
        {
            "username": "novo-usuario",
            "password": "senha-forte-123",
            "password_confirmation": "outra-senha-123",
        },
        format="json",
    )

    assert response.status_code == 400
    assert "password_confirmation" in response.json()
