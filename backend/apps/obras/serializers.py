from rest_framework import serializers

from .models import Obra


class ObraSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Obra
        fields = [
            "id",
            "nome",
            "cliente",
            "endereco",
            "status",
            "status_display",
            "data_inicio",
            "previsao_conclusao",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = ["id", "status_display", "criado_em", "atualizado_em"]

    def validate(self, attrs):
        data_inicio = attrs.get("data_inicio", getattr(self.instance, "data_inicio", None))
        previsao = attrs.get("previsao_conclusao", getattr(self.instance, "previsao_conclusao", None))
        if data_inicio and previsao and previsao < data_inicio:
            raise serializers.ValidationError({"previsao_conclusao": "A previsão não pode ser anterior ao início."})
        return attrs