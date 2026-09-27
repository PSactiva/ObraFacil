from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.core.audit import AuditedViewSetMixin
from .models import Obra
from .serializers import ObraSerializer


class ObraViewSet(AuditedViewSetMixin, viewsets.ModelViewSet):
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer
    permission_classes = [IsAuthenticated]
