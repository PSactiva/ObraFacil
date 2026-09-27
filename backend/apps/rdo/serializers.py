from rest_framework import serializers

from .models import DiarioObra, FotoDiario


class FotoDiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoDiario
        fields = ["id", "imagem", "legenda", "enviada_em"]
        read_only_fields = ["id", "enviada_em"]


class DiarioObraSerializer(serializers.ModelSerializer):
    obra_nome = serializers.CharField(source="obra.nome", read_only=True)
    clima_display = serializers.CharField(source="get_clima_display", read_only=True)
    fotos = FotoDiarioSerializer(many=True, read_only=True)
    imagens = serializers.ListField(child=serializers.ImageField(), write_only=True, required=False, allow_empty=True)

    class Meta:
        model = DiarioObra
        fields = ["id", "obra", "obra_nome", "data", "clima", "clima_display", "temperatura", "ocorrencias", "atividades", "efetivo", "fotos", "imagens", "criado_por", "criado_em"]
        read_only_fields = ["id", "criado_por", "criado_em"]

    def create(self, validated_data):
        imagens = validated_data.pop("imagens", [])
        diario = DiarioObra.objects.create(**validated_data)
        for imagem in imagens:
            FotoDiario.objects.create(diario=diario, imagem=imagem)
        return diario

    def update(self, instance, validated_data):
        imagens = validated_data.pop("imagens", [])
        for campo, valor in validated_data.items():
            setattr(instance, campo, valor)
        instance.save()
        for imagem in imagens:
            FotoDiario.objects.create(diario=instance, imagem=imagem)
        return instance
