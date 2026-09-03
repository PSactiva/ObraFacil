from django.db import transaction
from rest_framework import serializers

from .models import Orcamento, OrcamentoItem


class OrcamentoItemSerializer(serializers.ModelSerializer):
    material_nome = serializers.CharField(source="material.nome", read_only=True)
    preco_unitario = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    subtotal = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    class Meta:
        model = OrcamentoItem
        fields = [
            "id",
            "material",
            "material_nome",
            "quantidade",
            "preco_unitario",
            "subtotal",
        ]
        read_only_fields = ["id", "material_nome", "subtotal"]

    def validate_quantidade(self, value):
        if value <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        return value

    def validate_preco_unitario(self, value):
        if value < 0:
            raise serializers.ValidationError("O preço unitário não pode ser negativo.")
        return value

    def validate_material(self, value):
        if not value.ativo:
            raise serializers.ValidationError("Não é possível adicionar material inativo.")
        return value


class OrcamentoSerializer(serializers.ModelSerializer):
    itens = OrcamentoItemSerializer(many=True, required=False)
    total = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    class Meta:
        model = Orcamento
        fields = [
            "id",
            "titulo",
            "descricao",
            "cliente",
            "criado_em",
            "atualizado_em",
            "itens",
            "total",
        ]
        read_only_fields = ["id", "criado_em", "atualizado_em", "total"]

    @transaction.atomic
    def create(self, validated_data):
        itens_data = validated_data.pop("itens", [])
        orcamento = Orcamento.objects.create(**validated_data)
        self._create_itens(orcamento, itens_data)
        return orcamento

    @transaction.atomic
    def update(self, instance, validated_data):
        itens_data = validated_data.pop("itens", None)
        instance = super().update(instance, validated_data)
        if itens_data is not None:
            instance.itens.all().delete()
            self._create_itens(instance, itens_data)
        return instance

    def _create_itens(self, orcamento, itens_data):
        for item_data in itens_data:
            material = item_data["material"]
            item_data.setdefault("preco_unitario", material.preco_unitario)
            OrcamentoItem.objects.create(orcamento=orcamento, **item_data)
