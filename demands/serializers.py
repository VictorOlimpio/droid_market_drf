from rest_framework import serializers
from demands.models import Demand

class DemandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Demand
        fields = ['owner', 'piece', 'street',
                  'neighborhood', 'city', 'state',
                  'number', 'postal_code', 'status',
                  'created_at', 'updated_at', 'contact',
                  'piece_description', 'address']