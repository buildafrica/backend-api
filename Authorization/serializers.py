from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth import get_user_model
from profiles.models import Profiles
from .validators import validate_user_type


#TODO: Had validations. - phone_number & user_type
class RegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=11, required=True, validators=[RegexValidator(regex='^\d{11}$')])
    user_type = serializers.CharField(max_length=10, required=True, validators=[validate_user_type])
    password = serializers.CharField(min_length=8, max_length=128, required=True)
    email = serializers.EmailField(required=True)
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "password", "phone_number", "user_type")
        extra_kwargs = {
            "username": {
                "validators": [UnicodeUsernameValidator()],
            }
        }

class ConfirmEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("username", "activation_key")
        extra_kwargs = {
            "username": {
                "validators": [UnicodeUsernameValidator()],
            }
        }
    

class ResendConfirmEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ("username")
        extra_kwargs = {
            "username": {
                "validators": [UnicodeUsernameValidator()],
            }
        }

class ForgotPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ("username")
        extra_kwargs = {
            "username": {
                "validators": [UnicodeUsernameValidator()],
            }
        }

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=128)
    
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('old_password','password')
        extra_kwargs = {
            "username": {
                "validators": [UnicodeUsernameValidator()],
            }
        }