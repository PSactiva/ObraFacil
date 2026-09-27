from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Funcionario, LogAlteracao, Presenca


User = get_user_model()


class ObraFacilUserAdmin(UserAdmin):
	list_display = ("username", "email", "is_staff", "is_active", "date_joined")
	list_filter = ("is_staff", "is_superuser", "is_active", "groups")
	search_fields = ("username", "email", "first_name", "last_name")
	actions = ("ativar_usuarios", "desativar_usuarios")

	@admin.action(description="Ativar usuários selecionados")
	def ativar_usuarios(self, request, queryset):
		for usuario in queryset:
			if not usuario.is_active:
				usuario.is_active = True
				usuario.save(update_fields=["is_active"])

	@admin.action(description="Desativar usuários selecionados")
	def desativar_usuarios(self, request, queryset):
		for usuario in queryset.exclude(pk=request.user.pk):
			if usuario.is_active:
				usuario.is_active = False
				usuario.save(update_fields=["is_active"])


admin.site.unregister(User)
admin.site.register(User, ObraFacilUserAdmin)


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
	list_display = ("nome", "cargo", "email", "telefone", "ativo", "atualizado_em")
	list_filter = ("ativo", "cargo")
	search_fields = ("nome", "cargo", "email", "telefone")
	actions = ("ativar_funcionarios", "desativar_funcionarios")

	@admin.action(description="Ativar funcionários selecionados")
	def ativar_funcionarios(self, request, queryset):
		for funcionario in queryset:
			if not funcionario.ativo:
				funcionario.ativo = True
				funcionario.save(update_fields=["ativo"])

	@admin.action(description="Desativar funcionários selecionados")
	def desativar_funcionarios(self, request, queryset):
		for funcionario in queryset:
			if funcionario.ativo:
				funcionario.ativo = False
				funcionario.save(update_fields=["ativo"])


@admin.register(Presenca)
class PresencaAdmin(admin.ModelAdmin):
	list_display = ("funcionario", "obra", "data", "registrado_em")
	list_filter = ("data", "obra")
	search_fields = ("funcionario__nome", "obra__nome")
	readonly_fields = ("data", "registrado_em")


@admin.register(LogAlteracao)
class LogAlteracaoAdmin(admin.ModelAdmin):
	list_display = ("criado_em", "usuario_nome", "acao", "modelo", "objeto_id", "ip_address")
	list_filter = ("acao", "app_label", "modelo", "criado_em")
	search_fields = ("usuario_nome", "objeto_repr", "objeto_id")
	readonly_fields = tuple(campo.name for campo in LogAlteracao._meta.fields)
	date_hierarchy = "criado_em"
	ordering = ("-criado_em",)

	def has_view_permission(self, request, obj=None):
		return request.user.is_superuser

	def has_add_permission(self, request):
		return False

	def has_change_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False
