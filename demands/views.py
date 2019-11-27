from rest_framework import viewsets
from demands.models import Demand
from demands.serializers import DemandSerializer
from demands.permissions import IsOwner
from rest_framework import permissions
from rest_framework.response import Response

class DemandViewSet(viewsets.ModelViewSet):
    queryset = Demand.objects.all()
    serializer_class = DemandSerializer
    permission_classes = (permissions.IsAdminUser|IsOwner,)

    def list(self, request):
        serializer = DemandSerializer()
        if request.user.is_superuser:
            serializer = DemandSerializer(Demand.objects.all(), many=True)
        else:
            serializer = DemandSerializer(Demand.objects.filter(owner=request.user), many=True)
        return Response(serializer.data)