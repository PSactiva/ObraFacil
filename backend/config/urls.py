from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.core.urls")),
    path("api/orcamentos/", include("apps.orcamentos.urls")),
    path("api/materiais/", include("apps.materiais.urls")),
    path("api/calculos/", include("apps.calculos.urls")),
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
]
