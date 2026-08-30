from rest_framework import serializers


class AreaInputSerializer(serializers.Serializer):
    comprimento = serializers.FloatField(min_value=0)
    largura = serializers.FloatField(min_value=0)


class ConcretoInputSerializer(AreaInputSerializer):
    espessura = serializers.FloatField(min_value=0)


class PisoInputSerializer(AreaInputSerializer):
    perda_percentual = serializers.FloatField(min_value=0, max_value=50, default=10.0)


class CustoInputSerializer(serializers.Serializer):
    area_m2 = serializers.FloatField(min_value=0)
    preco_unitario = serializers.FloatField(min_value=0)
