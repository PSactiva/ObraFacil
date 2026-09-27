from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

from apps.core.views import register_user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.core.urls")),
    path("api/auth/token/", obtain_auth_token, name="api-token"),
    path("api/auth/register/", register_user, name="api-register"),
    path("api/orcamentos/", include("apps.orcamentos.urls")),
    path("api/materiais/", include("apps.materiais.urls")),
    path("api/obras/", include("apps.obras.urls")),
    path("api/rdo/", include("apps.rdo.urls")),
    path("api/calculos/", include("apps.calculos.urls")),
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
