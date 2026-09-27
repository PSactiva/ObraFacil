from django.conf import settings
from django.db import models


class DiarioObra(models.Model):
    class CondicaoClimatica(models.TextChoices):
        ENSOLARADO = "ensolarado", "Ensolarado"
        NUBLADO = "nublado", "Nublado"
        CHUVOSO = "chuvoso", "Chuvoso"
        PARCIAL = "parcial", "Parcialmente nublado"

    obra = models.ForeignKey("obras.Obra", on_delete=models.CASCADE, related_name="diarios")
    data = models.DateField()
    clima = models.CharField(max_length=20, choices=CondicaoClimatica.choices)
    temperatura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ocorrencias = models.TextField(blank=True)
    atividades = models.TextField(blank=True)
    efetivo = models.PositiveIntegerField(default=0)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="diarios_obra")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data", "-criado_em"]
        constraints = [models.UniqueConstraint(fields=["obra", "data"], name="unique_diario_por_obra_data")]
        verbose_name = "Diário de Obra"
        verbose_name_plural = "Diários de Obra"

    def __str__(self):
        return f"{self.obra} — {self.data}"


class FotoDiario(models.Model):
    diario = models.ForeignKey(DiarioObra, on_delete=models.CASCADE, related_name="fotos")
    imagem = models.ImageField(upload_to="rdo/%Y/%m/")
    legenda = models.CharField(max_length=200, blank=True)
    enviada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["enviada_em"]

    def __str__(self):
        return self.legenda or self.imagem.name
