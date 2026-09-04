import pytest
from decimal import Decimal
from rest_framework.test import APIClient

from apps.materiais.models import Material


@pytest.fixture
def material_factory():
    """Factory para criar materiais de teste"""
    def create_material(nome="Cimento", unidade="kg", preco_unitario=50.00, categoria="Aglomerantes", ativo=True):
        return Material.objects.create(
            nome=nome,
            unidade=unidade,
            preco_unitario=Decimal(str(preco_unitario)),
            categoria=categoria,
            ativo=ativo
        )
    return create_material


class TestMaterialList:
    """Testes para listagem de materiais"""

    @pytest.mark.django_db
    def test_list_materiais_vazio(self, client):
        """Deve retornar lista vazia quando não há materiais"""
        response = client.get("/api/materiais/")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert data["results"] == []

    @pytest.mark.django_db
    def test_list_materiais_com_items(self, client, material_factory):
        """Deve retornar lista de materiais ativos"""
        material_factory(nome="Cimento", preco_unitario=50.00)
        material_factory(nome="Areia", preco_unitario=30.00)

        response = client.get("/api/materiais/")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2
        results = data["results"]
        assert results[0]["nome"] == "Areia"  # Ordenado por nome (ASC)
        assert results[1]["nome"] == "Cimento"

    @pytest.mark.django_db
    def test_list_materiais_apenas_ativos(self, client, material_factory):
        """Deve retornar apenas materiais ativos (ativo=True)"""
        material_factory(nome="Cimento", ativo=True)
        material_factory(nome="Descontinuado", ativo=False)

        response = client.get("/api/materiais/")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["nome"] == "Cimento"


class TestMaterialCreate:
    """Testes para criação de materiais"""

    @pytest.mark.django_db
    def test_create_material_sucesso(self, authenticated_client):
        """Deve criar um novo material com dados válidos"""
        payload = {
            "nome": "Tijolos",
            "unidade": "unidade",
            "preco_unitario": 2.50,
            "categoria": "Alvenaria",
            "ativo": True
        }
        response = authenticated_client.post("/api/materiais/", payload, format="json")
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "Tijolos"
        assert data["preco_unitario"] == "2.50"
        assert Material.objects.count() == 1

    @pytest.mark.django_db
    def test_create_material_sem_categoria(self, authenticated_client):
        """Deve criar material mesmo sem categoria (campo opcional)"""
        payload = {
            "nome": "Cal",
            "unidade": "kg",
            "preco_unitario": 12.00,
            "ativo": True
        }
        response = authenticated_client.post("/api/materiais/", payload, format="json")
        assert response.status_code == 201
        assert response.json()["categoria"] == ""

    @pytest.mark.django_db
    def test_create_material_sem_nome(self, authenticated_client):
        """Deve rejeitar material sem nome"""
        payload = {
            "unidade": "kg",
            "preco_unitario": 50.00,
            "ativo": True
        }
        response = authenticated_client.post("/api/materiais/", payload, format="json")
        assert response.status_code == 400
        assert "nome" in response.json()


class TestMaterialRetrieve:
    """Testes para obter um material específico"""

    @pytest.mark.django_db
    def test_retrieve_material_existente(self, client, material_factory):
        """Deve retornar um material específico por ID"""
        material = material_factory(nome="Telha")
        response = client.get(f"/api/materiais/{material.id}/")
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Telha"
        assert data["id"] == material.id

    @pytest.mark.django_db
    def test_retrieve_material_nao_existe(self, client):
        """Deve retornar 404 para material inexistente"""
        response = client.get("/api/materiais/999/")
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_retrieve_material_inativo(self, client, material_factory):
        """Deve retornar 404 para material inativo"""
        material = material_factory(nome="Descontinuado", ativo=False)
        response = client.get(f"/api/materiais/{material.id}/")
        assert response.status_code == 404


class TestMaterialUpdate:
    """Testes para atualização de materiais"""

    @pytest.mark.django_db
    def test_update_material_completo(self, authenticated_client, material_factory):
        """Deve atualizar todos os campos do material"""
        material = material_factory(nome="Cimento", preco_unitario=50.00, categoria="Aglomerantes")
        payload = {
            "nome": "Cimento Portland",
            "unidade": "saco",
            "preco_unitario": 65.00,
            "categoria": "Cimentos",
            "ativo": True
        }
        response = authenticated_client.put(f"/api/materiais/{material.id}/", payload, format="json")
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Cimento Portland"
        assert data["preco_unitario"] == "65.00"
        assert data["categoria"] == "Cimentos"

    @pytest.mark.django_db
    def test_update_material_parcial(self, authenticated_client, material_factory):
        """Deve atualizar apenas alguns campos (PATCH)"""
        material = material_factory(nome="Areia", preco_unitario=30.00)
        payload = {"preco_unitario": 35.00}
        response = authenticated_client.patch(f"/api/materiais/{material.id}/", payload, format="json")
        assert response.status_code == 200
        assert response.json()["preco_unitario"] == "35.00"
        assert response.json()["nome"] == "Areia"  # Nome não muda


class TestMaterialDelete:
    """Testes para exclusão de materiais"""

    @pytest.mark.django_db
    def test_delete_material(self, authenticated_client, material_factory):
        """Deve deletar um material"""
        material = material_factory(nome="Temporário")
        assert Material.objects.count() == 1

        response = authenticated_client.delete(f"/api/materiais/{material.id}/")
        assert response.status_code == 204
        assert Material.objects.count() == 0

    @pytest.mark.django_db
    def test_delete_material_nao_existe(self, authenticated_client):
        """Deve retornar 404 ao deletar material inexistente"""
        response = authenticated_client.delete("/api/materiais/999/")
        assert response.status_code == 404
