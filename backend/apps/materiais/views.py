from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.core.audit import AuditedViewSetMixin
from .models import Material
from .serializers import MaterialSerializer


class MaterialViewSet(AuditedViewSetMixin, viewsets.ModelViewSet):
    queryset = Material.objects.filter(ativo=True)
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]
