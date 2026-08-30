from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OrcamentoViewSet

router = DefaultRouter()
router.register("", OrcamentoViewSet, basename="orcamento")

urlpatterns = [
    path("", include(router.urls)),
]
