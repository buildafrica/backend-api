from rest_framework import serializers
from .models import Sighting

class SightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sighting 
        fields = ('case','sighted_by','location_sighted','date_sighted','additional_info')

