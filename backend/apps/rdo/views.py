from django.db import transaction
from rest_framework import viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from apps.core.audit import AuditedViewSetMixin, contexto_auditoria
from rest_framework.permissions import IsAuthenticated

from .models import DiarioObra
from .serializers import DiarioObraSerializer


class DiarioObraViewSet(AuditedViewSetMixin, viewsets.ModelViewSet):
    queryset = DiarioObra.objects.select_related("obra", "criado_por").prefetch_related("fotos")
    serializer_class = DiarioObraSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        with transaction.atomic(), contexto_auditoria(self.request.user, self.request):
            serializer.save(criado_por=self.request.user)
