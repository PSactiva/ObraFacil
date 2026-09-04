from decimal import Decimal

from django.db import models

from apps.materiais.models import Material


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

    @property
    def total(self):
        return sum((item.subtotal for item in self.itens.all()), Decimal("0"))


class OrcamentoItem(models.Model):
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name="itens")
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name="itens_orcamento")
    quantidade = models.DecimalField(max_digits=12, decimal_places=3)
    preco_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Item do orçamento"
        verbose_name_plural = "Itens do orçamento"

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.material.nome} - {self.quantidade} {self.material.unidade}"
