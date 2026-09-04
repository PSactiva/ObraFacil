from decimal import Decimal

import pytest

from apps.materiais.models import Material
from apps.orcamentos.models import Orcamento, OrcamentoItem


@pytest.fixture
def material_factory():
    def create_material(nome="Cimento", preco_unitario="50.00"):
        return Material.objects.create(
            nome=nome,
            unidade="kg",
            preco_unitario=Decimal(preco_unitario),
        )

    return create_material


@pytest.mark.django_db
def test_criar_orcamento_com_itens_e_total(authenticated_client, material_factory):
    cimento = material_factory()
    areia = material_factory(nome="Areia", preco_unitario="30.00")

    response = authenticated_client.post(
        "/api/orcamentos/",
        {
            "titulo": "Reforma da cozinha",
            "cliente": "João",
            "itens": [
                {"material": cimento.id, "quantidade": "2.500"},
                {"material": areia.id, "quantidade": "10.000", "preco_unitario": "32.50"},
            ],
        },
        format="json",
    )

    assert response.status_code == 201
    data = response.json()
    assert data["total"] == "450.00"
    assert data["itens"][0]["preco_unitario"] == "50.00"
    assert data["itens"][1]["subtotal"] == "325.00"
    assert OrcamentoItem.objects.count() == 2


@pytest.mark.django_db
def test_atualizar_orcamento_substitui_itens(authenticated_client, material_factory):
    material = material_factory()
    orcamento = Orcamento.objects.create(titulo="Obra")
    OrcamentoItem.objects.create(
        orcamento=orcamento,
        material=material,
        quantidade=Decimal("1.000"),
        preco_unitario=Decimal("50.00"),
    )

    response = authenticated_client.patch(
        f"/api/orcamentos/{orcamento.id}/",
        {"itens": [{"material": material.id, "quantidade": "3.000"}]},
        format="json",
    )

    assert response.status_code == 200
    assert response.json()["total"] == "150.00"
    assert orcamento.itens.count() == 1
    assert orcamento.itens.get().quantidade == Decimal("3.000")


@pytest.mark.django_db
def test_rejeitar_quantidade_invalida(authenticated_client, material_factory):
    material = material_factory()

    response = authenticated_client.post(
        "/api/orcamentos/",
        {
            "titulo": "Obra",
            "itens": [{"material": material.id, "quantidade": "0"}],
        },
        format="json",
    )

    assert response.status_code == 400
    assert "quantidade" in response.json()["itens"]["0"]