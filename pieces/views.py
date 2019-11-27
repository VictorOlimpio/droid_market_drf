from rest_framework import viewsets
from pieces.models import Piece
from pieces.serializers import PieceSerializer

class PieceVewSet(viewsets.ModelViewSet):
    queryset = Piece.objects.all()
    serializer_class = PieceSerializer
