from django.conf import settings
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


class LogAlteracao(models.Model):
	class Acao(models.TextChoices):
		CRIACAO = "create", "Criação"
		EDICAO = "update", "Edição"
		EXCLUSAO = "delete", "Exclusão"

	usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="logs_alteracao")
	usuario_nome = models.CharField(max_length=150)
	acao = models.CharField(max_length=10, choices=Acao.choices)
	app_label = models.CharField(max_length=100)
	modelo = models.CharField(max_length=100)
	objeto_id = models.CharField(max_length=100)
	objeto_repr = models.CharField(max_length=255)
	detalhes = models.JSONField(default=dict)
	ip_address = models.GenericIPAddressField(null=True, blank=True)
	criado_em = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-criado_em"]
		verbose_name = "Log de alteração"
		verbose_name_plural = "Logs de alterações"

	def __str__(self):
		return f"{self.usuario_nome} — {self.get_acao_display()} {self.modelo} #{self.objeto_id}"
