from django.urls import path

from . import views

urlpatterns = [
    path("area/", views.calcular_area_view, name="calcular-area"),
    path("concreto/", views.calcular_concreto_view, name="calcular-concreto"),
    path("piso/", views.calcular_piso_view, name="calcular-piso"),
    path("custo/", views.estimar_custo_view, name="estimar-custo"),
]
