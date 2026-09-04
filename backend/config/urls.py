from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.core.urls")),
    path("api/auth/token/", obtain_auth_token, name="api-token"),
    path("api/orcamentos/", include("apps.orcamentos.urls")),
    path("api/materiais/", include("apps.materiais.urls")),
    path("api/calculos/", include("apps.calculos.urls")),
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
]
