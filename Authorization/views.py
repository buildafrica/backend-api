import secrets
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.views import APIView

from .serializers import RegistrationSerializerMixin
from .responseHelper import ResponseHelper, StatusCodes
from .EmailHelper import EmailHelper

from profiles.models import Profiles

get_api_response = ResponseHelper.get_api_response
get_api_server_error = ResponseHelper.api_server_error
get_api_success = ResponseHelper.api_success
User = get_user_model()

class AuthMisc:
    token_length = 32
    IS_PROFILE_ACTIVATION_KEY = 1
    IS_FORGOT_PASSWORD = 2
    IS_RESET_PASSWORD_KEY = 3
    KEY_EXPIRATION_TIME = 1  # Key expires in 1 day.

    @classmethod
    def generate_and_set_activation_key(cls, user, key_type=None):
        activation_key = secrets.token_urlsafe(cls.token_length)
        user.activation_key = activation_key
        user.activation_key_expires = timezone.now() + timezone.timedelta(days=cls.KEY_EXPIRATION_TIME)
        user.activation_key_type = key_type
        user.save()
        
        return activation_key


    @classmethod
    def generate_confirmation_link(cls, activation_key):
        confirmation_link_url = reverse("pages-confirm-email")
        domain = get_current_site(request).domain
        full_site_confirmation_link = '%s://%s%s?key=%s'%(request.scheme, domain, confirmation_link_url, activation_key)
        
        return full_site_confirmation_link



# Create your views here.
class AuthRegistration(APIView):
    """ Get or Create a user """

    def get_user_by_email(email):
        try:
            return User.objects.get(email=email, isActive=1)
        except (User.DoesNotExist, Exception) as e:
                return e

    """ Create new user """
    def post(self, request, format=None):
        serializer = RegistrationSerializerMixin(data=request.data)
        if not serializer.is_valid():
            return  get_api_response(StatusCodes.Invalid_Field, errors=serializer.errors, httpStatusCode=status.HTTP_400_BAD_REQUEST)

        if request.user.is_authenticated:
            return get_api_response(StatusCodes.Already_Logged_In, httpStatusCode=status.HTTP_400_BAD_REQUEST)

        userExists = self.get_user_by_email(serializer.initial_data.get("email"))
        if isinstance(userExists, Exception):
            return get_api_response(StatusCodes.User_with_Email_Exists, httpStatusCode=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data["username"]
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data["last_name"]
        user_type = serializer.validated_data["user_type"]
        phone_number = serializer.validated_data["phone_number"]

        user = User.objects.create_user(username, email=email, password=password)
        profile = Profiles.customprofileManager.create_profile(user, phone_number, user_type)
        
        try:
            activation_key = AuthMisc.generate_and_set_activation_key(user, AuthMisc.IS_PROFILE_ACTIVATION_KEY)
        except (ValidationError, Exception) as e:
            return get_api_server_error()

        confirmation_link = AuthMisc.generate_confirmation_link(activation_key)

        try:
            EmailHelper.send_signup_mail(user.email, profile.first_name, confirmation_link) 
        except (Exception) as e:
            return get_api_server_error()

        return get_api_success()

        
class AuthDetail(APIView):
    """ Retrieve, update and delete a user """

    """ Delete a User """
    def delete(self, request, format=None):
        pass

class AuthConfirmEmail(APIView):

    def put(self, request, format=None):
        return get_api_server_error()

class AuthResendConfirmationEmail(APIView):

    def put(self, request, format=None):
        pass

class AuthForgotPassword(APIView):
    
    def put(self, request, format=None):
        pass
    
    

class AuthChangePassword(APIView):

    def put(self, request, format=None):
        pass
    

class AuthResetPassword(APIView):

    def put(self, request, format=None):
        pass
