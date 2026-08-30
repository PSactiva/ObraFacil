from rest_framework import viewsets

from .models import Orcamento
from .serializers import OrcamentoSerializer


class OrcamentoViewSet(viewsets.ModelViewSet):
    queryset = Orcamento.objects.all()
    serializer_class = OrcamentoSerializer
