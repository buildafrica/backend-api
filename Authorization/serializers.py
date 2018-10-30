from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from profiles.models import Profiles


#TODO: Had validations. - phone_number & user_type
class RegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=11, validators=[RegexValidator(regex='^\d{11}$')])
    user_type = serializers.CharField(max_length=10, required=True)
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "password", "phone_number", "user_type")

class ConfirmEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ("username", "activation_key")
    

class ResendConfirmEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ("username")

class ForgotPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ("username")

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=128)
    
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('old_password','password')