from django.contrib import admin

from .models import Obra


@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    list_display = ("nome", "cliente", "status", "data_inicio", "previsao_conclusao")
    list_filter = ("status",)
    search_fields = ("nome", "cliente", "endereco")