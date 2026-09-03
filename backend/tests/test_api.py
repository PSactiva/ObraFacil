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
