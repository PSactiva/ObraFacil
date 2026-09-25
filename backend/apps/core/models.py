from django.db import models
from django.utils import timezone



class Funcionario(models.Model):
	nome = models.CharField(max_length=200)
	cargo = models.CharField(max_length=120)
	email = models.EmailField(blank=True)
	telefone = models.CharField(max_length=30, blank=True)
	ativo = models.BooleanField(default=True)
	criado_em = models.DateTimeField(auto_now_add=True)
	atualizado_em = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["nome"]
		verbose_name = "Funcionário"
		verbose_name_plural = "Funcionários"

	def __str__(self):
		return f"{self.nome} - {self.cargo}"


class Presenca(models.Model):
	funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, related_name="presencas")
	obra = models.ForeignKey("obras.Obra", on_delete=models.SET_NULL, null=True, blank=True, related_name="presencas")
	data = models.DateField(default=timezone.localdate)
	registrado_em = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-registrado_em"]
		verbose_name = "Presença"
		verbose_name_plural = "Presenças"
		constraints = [
			models.UniqueConstraint(fields=["funcionario", "data"], name="presenca_funcionario_data_unica"),
		]

	def __str__(self):
		return f"{self.funcionario.nome} - {self.data}"
