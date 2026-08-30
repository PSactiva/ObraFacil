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
