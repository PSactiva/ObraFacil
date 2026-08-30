from django.contrib import admin

from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("nome", "unidade", "preco_unitario", "categoria", "ativo")
    list_filter = ("categoria", "ativo")
    search_fields = ("nome",)
