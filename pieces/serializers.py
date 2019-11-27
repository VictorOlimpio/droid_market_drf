from rest_framework import serializers
from pieces.models import Piece
from demands.serializers import DemandSerializer

class PieceSerializer(serializers.ModelSerializer):
    demands = DemandSerializer(many=True, read_only=True)
    class Meta:
        model = Piece
        fields = ['id', 'type', 'description', 'value', 'demands']