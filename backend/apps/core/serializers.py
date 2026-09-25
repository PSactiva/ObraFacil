from rest_framework import serializers

from django.utils import timezone

from .models import Funcionario, Presenca


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = [
            "id",
            "nome",
            "cargo",
            "email",
            "telefone",
            "ativo",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = ["id", "criado_em", "atualizado_em"]

    def validate_nome(self, value):
        if not value.strip():
            raise serializers.ValidationError("O nome não pode estar vazio.")
        return value

    def validate_cargo(self, value):
        if not value.strip():
            raise serializers.ValidationError("O cargo não pode estar vazio.")
        return value


class PresencaSerializer(serializers.ModelSerializer):
    funcionario_nome = serializers.CharField(source="funcionario.nome", read_only=True)
    funcionario_cargo = serializers.CharField(source="funcionario.cargo", read_only=True)
    obra_nome = serializers.CharField(source="obra.nome", read_only=True, allow_null=True)

    class Meta:
        model = Presenca
        fields = [
            "id",
            "funcionario",
            "funcionario_nome",
            "funcionario_cargo",
            "obra",
            "obra_nome",
            "data",
            "registrado_em",
        ]
        read_only_fields = ["id", "funcionario_nome", "funcionario_cargo", "obra_nome", "data", "registrado_em"]

    def validate_funcionario(self, funcionario):
        if not funcionario.ativo:
            raise serializers.ValidationError("Não é possível registrar ponto para funcionário inativo.")
        if Presenca.objects.filter(funcionario=funcionario, data=timezone.localdate()).exists():
            raise serializers.ValidationError("Este funcionário já teve a presença registrada hoje.")
        return funcionario
