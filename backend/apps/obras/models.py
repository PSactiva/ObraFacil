from django.db import models


class Obra(models.Model):
    class Status(models.TextChoices):
        PLANEJADA = "planejada", "Planejada"
        EM_ANDAMENTO = "em_andamento", "Em andamento"
        CONCLUIDA = "concluida", "Concluída"
        PAUSADA = "pausada", "Pausada"

    nome = models.CharField(max_length=200)
    cliente = models.CharField(max_length=200)
    endereco = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANEJADA)
    data_inicio = models.DateField(null=True, blank=True)
    previsao_conclusao = models.DateField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Obra"
        verbose_name_plural = "Obras"

    def __str__(self):
        return self.nome