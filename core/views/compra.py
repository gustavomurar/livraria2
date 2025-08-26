from rest_framework.viewsets import ModelViewSet
from core.models import Compra
from core.serializers.compra import (
    CompraCreateUpdateSerializer,
    CompraListSerializer,
    CompraSerializer,
)

class CompraViewSet(ModelViewSet):
    # queryset = Compra.objects.order_by('-id')
    # serializer_class = CompraSerializer

    def get_serializer_class(self):
        if self.action in {'list'}:
            return CompraListSerializer
        if self.action in {'create', 'update', 'partial_update'}:
            return CompraCreateUpdateSerializer
        return CompraSerializer
    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_superuser:
            return Compra.objects.all()
        if usuario.groups.filter(name='administradores'):
            return Compra.objects.all()
        return Compra.objects.filter(usuario=usuario)
