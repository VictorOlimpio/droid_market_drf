from rest_framework import serializers
from pieces.models import Piece

class PieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piece
        fields = ['id', 'type', 'description', 'value']