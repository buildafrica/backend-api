from .models import Profiles
from rest_framework import serializers
from django.core.validators import RegexValidator

class ProfileInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30, required=False)
    phone_number = serializers.CharField(max_length=11, validators=[RegexValidator(regex='^\d{11}$')], required=False)
    
    class Meta:
        model = Profiles
        fields = ('first_name', 'last_name', 'user_type', 'date_of_birth','address',
                    'state', 'gender', 'country', 'phone_number', 'profile_pic')

class ProfilePictureSerializer(serializers.Serializer):
    file = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)

class SaveProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = ('profile_pic',)