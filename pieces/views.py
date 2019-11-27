from rest_framework import viewsets
from pieces.models import Piece
from pieces.serializers import PieceSerializer
from pieces.permissions import IsLoggedInUserOrAdmin
from users.permissions import IsAdminUser

class PieceVewSet(viewsets.ModelViewSet):
    queryset = Piece.objects.all()
    serializer_class = PieceSerializer

    def get_permissions(self):
        permission_classes = [IsLoggedInUserOrAdmin]
        if self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]