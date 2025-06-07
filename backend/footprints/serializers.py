from rest_framework import serializers
from .models import Footprint

class FootprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footprint
        fields = '__all__' 