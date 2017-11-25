from rest_framework import serializers
from .models import Case, Sighting

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'        

class SightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sighting 
        fields = ('case','sighted_by','location_sighted','date_sighted','additional_info')

