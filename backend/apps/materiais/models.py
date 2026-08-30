from django.db import models


class Material(models.Model):
    nome = models.CharField(max_length=200)
    unidade = models.CharField(max_length=20, help_text="Ex: m², m³, kg, un")
    preco_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    categoria = models.CharField(max_length=100, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Material"
        verbose_name_plural = "Materiais"

    def __str__(self):
        return f"{self.nome} ({self.unidade})"
