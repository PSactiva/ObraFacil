from django.contrib import admin

from .models import DiarioObra, FotoDiario


class FotoDiarioInline(admin.TabularInline):
    model = FotoDiario
    extra = 0


@admin.register(DiarioObra)
class DiarioObraAdmin(admin.ModelAdmin):
    list_display = ("obra", "data", "clima", "efetivo", "criado_por")
    list_filter = ("clima", "data")
    inlines = [FotoDiarioInline]
