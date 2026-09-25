import pytest
from django.contrib.auth.models import User
from django.test import override_settings
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
def test_obter_usuario_atual_com_token(client, user):
    token_response = client.post(
        "/api/auth/token/",
        {"username": "testuser", "password": "testpass123"},
        format="json",
    )
    client.credentials(HTTP_AUTHORIZATION=f"Token {token_response.json()['token']}")

    response = client.get("/api/auth/me/")

    assert response.status_code == 200
    assert response.json() == {"id": user.id, "username": "testuser"}


@pytest.mark.django_db
def test_logout_invalida_token(client, user):
    token_response = client.post(
        "/api/auth/token/",
        {"username": "testuser", "password": "testpass123"},
        format="json",
    )
    client.credentials(HTTP_AUTHORIZATION=f"Token {token_response.json()['token']}")

    logout_response = client.post("/api/auth/logout/", {}, format="json")

    assert logout_response.status_code == 204
    assert client.get("/api/auth/me/").status_code == 401


@pytest.mark.django_db
def test_cadastrar_usuario(client):
    response = client.post(
        "/api/auth/register/",
        {
            "username": "novo-usuario",
            "email": "novo-usuario@example.com",
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
            "email": "novo-usuario@example.com",
            "password": "senha-forte-123",
            "password_confirmation": "outra-senha-123",
        },
        format="json",
    )

    assert response.status_code == 400
    assert "password_confirmation" in response.json()


@pytest.mark.django_db
@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
def test_solicitar_recuperacao_envia_usuario_e_link(client, user, mailoutbox):
    user.email = "testuser@example.com"
    user.save(update_fields=["email"])

    response = client.post(
        "/api/auth/password-reset/",
        {"email": "testuser@example.com"},
        format="json",
    )

    assert response.status_code == 200
    assert len(mailoutbox) == 1
    assert "testuser" in mailoutbox[0].body
    assert "uid=" in mailoutbox[0].body
    assert "token=" in mailoutbox[0].body


@pytest.mark.django_db
def test_redefinir_senha_com_link_valido(client, user):
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    response = client.post(
        "/api/auth/password-reset/confirm/",
        {
            "uid": uid,
            "token": token,
            "password": "nova-senha-forte-123",
            "password_confirmation": "nova-senha-forte-123",
        },
        format="json",
    )

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.check_password("nova-senha-forte-123")


@pytest.mark.django_db
def test_redefinir_senha_rejeita_token_reutilizado(client, user):
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    dados = {
        "uid": uid,
        "token": token,
        "password": "nova-senha-forte-123",
        "password_confirmation": "nova-senha-forte-123",
    }
    assert client.post("/api/auth/password-reset/confirm/", dados, format="json").status_code == 200
    assert client.post("/api/auth/password-reset/confirm/", dados, format="json").status_code == 400
