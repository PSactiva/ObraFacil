from django.db import models


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
