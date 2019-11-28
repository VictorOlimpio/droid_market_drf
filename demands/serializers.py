from rest_framework import serializers
from demands.models import Demand

class DemandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Demand
        fields = "__all__"