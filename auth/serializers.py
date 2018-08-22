from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from profiles.models import Profiles

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "password")

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles # Stub
        fields = ("phone_number", "user_type")

class RegistrationSerializerMixin(object):

    def __init__(self, data):
        self.user = UserSerializer(data)
        self.profile = ProfileSerializer(data)
    
    def is_valid(self):
        return True if (self.user.is_valid() and self.profile.is_valid()) else False
    