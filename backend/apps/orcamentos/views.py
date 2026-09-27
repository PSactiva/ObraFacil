from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.core.audit import AuditedViewSetMixin
from .models import Orcamento
from .serializers import OrcamentoSerializer


class OrcamentoViewSet(AuditedViewSetMixin, viewsets.ModelViewSet):
    queryset = Orcamento.objects.all()
    serializer_class = OrcamentoSerializer
    permission_classes = [IsAuthenticated]
