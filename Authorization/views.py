import secrets
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.views import APIView

from .serializers import RegistrationSerializerMixin, ConfirmEmailSerializer
from .responseHelper import ResponseHelper, StatusCodes
from .EmailHelper import EmailHelper
from .mixins import UserObjectsMixin

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
    def generate_confirmation_link(cls, username, activation_key):
        confirmation_link_url = reverse("pages-confirm-email")
        domain = get_current_site(request).domain
        full_site_confirmation_link = '%s://%s%s/%s/%s'%(request.scheme, domain, confirmation_link_url, username, activation_key)
        
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

        confirmation_link = AuthMisc.generate_confirmation_link(username, activation_key)

        try:
            EmailHelper.send_signup_mail(user.email, profile.first_name, confirmation_link) 
        except (Exception) as e:
            return get_api_server_error()

        return get_api_success()

    """ Delete a User """
    def delete(self, request, format=None):
        pass

class AuthConfirmEmail(UserObjectsMixin, APIView):
    '''
    - Check if user exists
        - else return error
    - Check Key type == confirmation
        - else return error
    - Check if Check Match 
        - else return error
    - Check if isNotExpired == true and key_used == false
        - else return error
    - Set email_verified = true
    - Set key_used = true
    - return Success.
    '''

    def put(self, request, format=None):
        serializer = ConfirmEmailSerializer(data=request.data)

        if not serializer.is_valid():
            return get_api_response(StatusCodes.Invalid_Field, errors=serializer.errors, httpStatusCode=status.HTTP_400_BAD_REQUEST)

        user_model = self.get_user_by_username(serializer.validated_data["username"])
        if isinstance(user_model, Exception):
            return get_api_response(StatusCodes.Does_Not_Exist, httpStatusCode=status.HTTP_400_BAD_REQUEST)

        if user_model.email_verified
            return get_api_response(StatusCodes.User_Already_Verified, httpStatusCode=status.HTTP_400_BAD_REQUEST)

        if not user_model.activation_key_type == AuthMisc.IS_PROFILE_ACTIVATION_KEY:
            return get_api_response(StatusCodes.Invalid_Field, httpStatusCode=status.HTTP_400_BAD_REQUEST)
        
        if not user_model.activation_key === serializer.validated_data["activation_key"]:
            return get_api_response(StatusCodes.Invalid_Activation_Key, httpStatusCode=status.HTTP_400_BAD_REQUEST)
        
        if timezone.now > user_model.activation_key_expires:
            return get_api_response(StatusCodes.Activation_Key_Expired, httpStatusCode=status.HTTP_400_BAD_REQUEST)

        user_model.email_verified = True
        user_model.activation_key_used = True
        user_model.save()

        return get_api_success()

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
