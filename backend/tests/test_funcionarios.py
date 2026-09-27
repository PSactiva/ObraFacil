import pytest

from apps.core.models import Funcionario


@pytest.mark.django_db
def test_listar_funcionarios_autenticado(authenticated_client):
    Funcionario.objects.create(nome="João Silva", cargo="Pedreiro", email="joao@example.com", telefone="11999999999")
    Funcionario.objects.create(nome="Maria Santos", cargo="Encarregada", email="maria@example.com")

    response = authenticated_client.get("/api/funcionarios/")

    assert response.status_code == 200
    assert len(response.json()["results"]) == 2
    assert response.json()["results"][0]["nome"] == "João Silva"


@pytest.mark.django_db
def test_listar_funcionarios_sem_autenticacao(client):
    Funcionario.objects.create(nome="João Silva", cargo="Pedreiro")

    response = client.get("/api/funcionarios/")

    assert response.status_code == 401


@pytest.mark.django_db
def test_criar_funcionario_autenticado(authenticated_client):
    response = authenticated_client.post(
        "/api/funcionarios/",
        {
            "nome": "Pedro Costa",
            "cargo": "Encanador",
            "email": "pedro@example.com",
            "telefone": "11988888888",
            "ativo": True,
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.json()["nome"] == "Pedro Costa"
    assert Funcionario.objects.get(nome="Pedro Costa").cargo == "Encanador"


@pytest.mark.django_db
def test_editar_funcionario_autenticado(authenticated_client):
    funcionario = Funcionario.objects.create(nome="Ana Silva", cargo="Auxiliar")

    response = authenticated_client.patch(
        f"/api/funcionarios/{funcionario.id}/",
        {"cargo": "Mestre de obra"},
        format="json",
    )

    assert response.status_code == 200
    assert response.json()["cargo"] == "Mestre de obra"
    assert Funcionario.objects.get(id=funcionario.id).cargo == "Mestre de obra"


@pytest.mark.django_db
def test_desativar_funcionario_autenticado(authenticated_client):
    funcionario = Funcionario.objects.create(nome="Carlos", cargo="Pedreiro", ativo=True)

    response = authenticated_client.patch(
        f"/api/funcionarios/{funcionario.id}/",
        {"ativo": False},
        format="json",
    )

    assert response.status_code == 200
    assert response.json()["ativo"] is False


@pytest.mark.django_db
def test_excluir_funcionario_autenticado(authenticated_client):
    funcionario = Funcionario.objects.create(nome="Bruno", cargo="Carpinteiro")

    response = authenticated_client.delete(f"/api/funcionarios/{funcionario.id}/")

    assert response.status_code == 204
    assert not Funcionario.objects.filter(id=funcionario.id).exists()


@pytest.mark.django_db
def test_rejeitar_funcionario_nome_vazio(authenticated_client):
    response = authenticated_client.post(
        "/api/funcionarios/",
        {
            "nome": "   ",
            "cargo": "Pedreiro",
        },
        format="json",
    )

    assert response.status_code == 400
    assert "nome" in response.json()


@pytest.mark.django_db
def test_rejeitar_funcionario_cargo_vazio(authenticated_client):
    response = authenticated_client.post(
        "/api/funcionarios/",
        {
            "nome": "João",
            "cargo": "   ",
        },
        format="json",
    )

    assert response.status_code == 400
    assert "cargo" in response.json()
