from rest_framework import viewsets
from demands.models import Demand
from demands.serializers import DemandSerializer
from demands.permissions import IsOwnerOrAdmin
from users.permissions import IsLoggedInUserOrAdmin
from rest_framework.response import Response

class DemandViewSet(viewsets.ModelViewSet):
    queryset = Demand.objects.all()
    serializer_class = DemandSerializer

    def list(self, request):
        serializer = DemandSerializer()
        if request.user.is_superuser:
            serializer = DemandSerializer(Demand.objects.all(), many=True)
        else:
            serializer = DemandSerializer(Demand.objects.filter(owner=request.user), many=True)
        return Response(serializer.data)

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsLoggedInUserOrAdmin]
        else:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]