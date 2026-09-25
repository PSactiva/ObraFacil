from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("funcionarios", views.FuncionarioViewSet, basename="funcionario")
router.register("presencas", views.PresencaViewSet, basename="presenca")

urlpatterns = [
    path("health/", views.health_check, name="health-check"),
    path("auth/me/", views.current_user, name="current-user"),
    path("auth/logout/", views.logout_user, name="logout-user"),
    path("auth/password-reset/", views.request_password_reset, name="password-reset"),
    path("auth/password-reset/confirm/", views.confirm_password_reset, name="password-reset-confirm"),
    path("auth/register/", views.register_user, name="register-user"),
    path("", include(router.urls)),
]
