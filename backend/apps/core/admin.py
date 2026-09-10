from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Funcionario


User = get_user_model()


class ObraFacilUserAdmin(UserAdmin):
	list_display = ("username", "email", "is_staff", "is_active", "date_joined")
	list_filter = ("is_staff", "is_superuser", "is_active", "groups")
	search_fields = ("username", "email", "first_name", "last_name")
	actions = ("ativar_usuarios", "desativar_usuarios")

	@admin.action(description="Ativar usuários selecionados")
	def ativar_usuarios(self, request, queryset):
		queryset.update(is_active=True)

	@admin.action(description="Desativar usuários selecionados")
	def desativar_usuarios(self, request, queryset):
		queryset.exclude(pk=request.user.pk).update(is_active=False)


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
		queryset.update(ativo=True)

	@admin.action(description="Desativar funcionários selecionados")
	def desativar_funcionarios(self, request, queryset):
		queryset.update(ativo=False)
