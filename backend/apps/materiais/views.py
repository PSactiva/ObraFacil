from rest_framework import viewsets

from .models import Material
from .serializers import MaterialSerializer


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.filter(ativo=True)
    serializer_class = MaterialSerializer
