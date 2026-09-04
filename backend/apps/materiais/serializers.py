from rest_framework import serializers

from .models import Material


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ["id", "nome", "unidade", "preco_unitario", "categoria", "ativo"]
        read_only_fields = ["id"]
