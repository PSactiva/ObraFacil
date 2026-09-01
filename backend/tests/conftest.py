import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def user():
    """Cria um usuário de teste"""
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def authenticated_client(user):
    """Cria um cliente autenticado"""
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def client():
    """Cria um cliente não autenticado"""
    return APIClient()
