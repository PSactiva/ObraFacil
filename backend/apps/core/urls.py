from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health_check, name="health-check"),
    path("auth/me/", views.current_user, name="current-user"),
    path("auth/logout/", views.logout_user, name="logout-user"),
    path("auth/password-reset/", views.request_password_reset, name="password-reset"),
    path("auth/password-reset/confirm/", views.confirm_password_reset, name="password-reset-confirm"),
]
