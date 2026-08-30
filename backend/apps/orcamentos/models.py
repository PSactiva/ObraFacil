from django.db import models


class Orcamento(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    cliente = models.CharField(max_length=200, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Orçamento"
        verbose_name_plural = "Orçamentos"

    def __str__(self):
        return self.titulo
