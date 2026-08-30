from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import services
from .serializers import (
    AreaInputSerializer,
    ConcretoInputSerializer,
    CustoInputSerializer,
    PisoInputSerializer,
)


@api_view(["POST"])
def calcular_area_view(request):
    s = AreaInputSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    d = s.validated_data
    r = services.calcular_area(d["comprimento"], d["largura"])
    return Response({"area_m2": float(r)})


@api_view(["POST"])
def calcular_concreto_view(request):
    s = ConcretoInputSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    d = s.validated_data
    r = services.calcular_volume_concreto(d["comprimento"], d["largura"], d["espessura"])
    return Response({"volume_m3": float(r)})


@api_view(["POST"])
def calcular_piso_view(request):
    s = PisoInputSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    d = s.validated_data
    return Response(services.calcular_piso(d["comprimento"], d["largura"], d.get("perda_percentual", 10.0)))


@api_view(["POST"])
def estimar_custo_view(request):
    s = CustoInputSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    d = s.validated_data
    r = services.estimar_custo_por_m2(d["area_m2"], d["preco_unitario"])
    return Response({"custo_total": float(r)})
