from rest_framework import viewsets
from demands.models import Demand
from demands.serializers import DemandSerializer
from demands.permissions import IsOwnerOrAdmin
from users.permissions import IsLoggedInUserOrAdmin
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'limit': self.page_size,
            'results': data
        })

class DemandViewSet(viewsets.ModelViewSet):
    queryset = Demand.objects.all()
    serializer_class = DemandSerializer
    pagination_class = CustomResultsSetPagination

    def list(self, request):
        serializer = DemandSerializer(context={'request': request})
        if request.user.is_superuser:
            serializer = DemandSerializer(Demand.objects.all(), many=True, context={'request': request})
        else:
            serializer = DemandSerializer(Demand.objects.filter(owner=request.user), many=True, context={'request': request})
        return Response(serializer.data)

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsLoggedInUserOrAdmin]
        else:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]