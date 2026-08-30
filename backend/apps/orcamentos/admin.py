from django.contrib import admin

from .models import Orcamento


@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "cliente", "criado_em")
    search_fields = ("titulo", "cliente")
    list_filter = ("criado_em",)
