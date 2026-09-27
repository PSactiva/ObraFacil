import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.core.models import Funcionario


@pytest.mark.django_db
def test_usuario_comum_nao_acessa_admin(client, user):
    assert client.login(username="testuser", password="testpass123")

    response = client.get(reverse("admin:index"))

    assert response.status_code == 302
    assert "/admin/login/" in response.url


@pytest.mark.django_db
def test_staff_acessa_admin_e_pode_excluir_usuario(client, staff_user, user):
    assert client.login(username="adminuser", password="adminpass123")

    response = client.post(
        reverse("admin:auth_user_delete", args=[user.pk]),
        {"post": "Sim, tenho certeza"},
    )

    assert response.status_code == 302
    assert not get_user_model().objects.filter(pk=user.pk).exists()


@pytest.mark.django_db
def test_staff_pode_excluir_funcionario(client, staff_user):
    funcionario = Funcionario.objects.create(nome="Ana", cargo="Pedreira")
    assert client.login(username="adminuser", password="adminpass123")

    response = client.post(
        reverse("admin:core_funcionario_delete", args=[funcionario.pk]),
        {"post": "Sim, tenho certeza"},
    )

    assert response.status_code == 302
    assert not Funcionario.objects.filter(pk=funcionario.pk).exists()