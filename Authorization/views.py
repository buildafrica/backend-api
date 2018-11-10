from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.views import APIView

from .serializers import ( RegistrationSerializer, ConfirmEmailSerializer, ResendConfirmEmailSerializer,
                        ForgotPasswordSerializer, ChangePasswordSerializer )
from .responseHelper import ResponseHelper, StatusCodes
from .EmailHelper import EmailHelper
from .mixins import UserObjectsMixin
from .misc import AuthMisc

from profiles.models import Profiles

get_api_response = ResponseHelper.get_api_response
get_api_server_error = ResponseHelper.api_server_error
get_api_success = ResponseHelper.api_success
get_400_error = ResponseHelper.api_400_error
User = get_user_model()

# Create your views here.
class AuthRegistration(APIView):
    """ Get or Create a user """
    authentication_classes = ()
    permission_classes = ()

    def get_user_by_email(self, email):
        try:
            return User.objects.get(email=email, isActive=1)
        except (User.DoesNotExist, Exception) as e:
            return e
    
    def get_user_by_username(self, username):
        try: 
            return User.objects.get(username=username, isActive=1)
        except (User.DoesNotExist, Exception) as e:
            return e        

    """ Create new user """
    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return  get_400_error(serializer.errors)

        if request.user.is_authenticated:
            return get_api_response(StatusCodes.Already_Logged_In, httpStatusCode=status.HTTP_400_BAD_REQUEST)

        user = self.get_user_by_email(serializer.initial_data.get("email"))
        if not isinstance(user, Exception):
            return get_api_response(StatusCodes.User_with_Email_Exists, httpStatusCode=status.HTTP_400_BAD_REQUEST)

        user = self.get_user_by_username(serializer.validated_data["username"])
        if not isinstance(user, Exception):
            return get_api_response(StatusCodes.User_with_Username_Exists, httpStatusCode=status.HTTP_400_BAD_REQUEST)


        username = serializer.validated_data["username"]
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data["last_name"]
        user_type = serializer.validated_data["user_type"]
        phone_number = serializer.validated_data["phone_number"]

        user = User.objects.create_user(username, email=email, password=password)
        profile = Profiles.customprofileManager.create_profile(user, phone_number=phone_number, user_type=user_type)
        
        try:
            activation_key = AuthMisc.generate_and_set_activation_key(user, key_type=AuthMisc.IS_PROFILE_ACTIVATION_KEY)
        except (ValidationError, Exception) as e:
            return get_api_server_error()

        confirmation_link = AuthMisc.generate_confirmation_link(request, username, activation_key)
        
        try:
            EmailHelper.send_signup_mail(user.email, user.first_name, confirmation_link) 
        except (Exception) as e:
            return get_api_server_error()

        return get_api_success()

    """ Delete a User """
    def delete(self, request, format=None):
        
        if not request.user.is_authenticated:
            return get_api_response(StatusCodes.Does_Not_Exist, httpStatusCode=status.HTTP_400_BAD_REQUEST)
        
        request.user.isActive = 0
        profile = Profiles.objects.select_related("user").get(user=request.user)
        profile.isActive = 0
        profile.save()
        request.user.save()

        return get_api_success()

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
    authentication_classes = ()
    permission_classes = ()

    def put(self, request, format=None):
        serializer = ConfirmEmailSerializer(data=request.data)

        if not serializer.is_valid():
            return get_api_response(StatusCodes.Invalid_Field, errors=serializer.errors, httpStatusCode=status.HTTP_400_BAD_REQUEST)

        user_model = self.get_user_by_username(serializer.validated_data["username"])
        if isinstance(user_model, Exception):
            return get_api_response(StatusCodes.Does_Not_Exist, httpStatusCode=status.HTTP_400_BAD_REQUEST)

        if user_model.is_email_verified:
            return get_api_response(StatusCodes.User_Already_Verified, httpStatusCode=status.HTTP_400_BAD_REQUEST)

        if not user_model.activation_key_type == AuthMisc.IS_PROFILE_ACTIVATION_KEY:
            return get_api_response(StatusCodes.Invalid_Field, httpStatusCode=status.HTTP_400_BAD_REQUEST)
        
        if not user_model.activation_key == serializer.validated_data["activation_key"]:
            return get_api_response(StatusCodes.Invalid_Activation_Key, httpStatusCode=status.HTTP_400_BAD_REQUEST)
        
        if timezone.now() > user_model.activation_key_expires:
            return get_api_response(StatusCodes.Activation_Key_Expired, httpStatusCode=status.HTTP_400_BAD_REQUEST)

        user_model.is_email_verified = True
        user_model.activation_key_used = True
        user_model.save()

        return get_api_success()

class AuthResendConfirmationEmail(UserObjectsMixin, APIView):

    def put(self, request, format=None):
        serializer = ResendConfirmEmailSerializer(data=request.data)

        if not serializer.is_valid():
            return  get_400_error(serializer.errors)

        user = self.get_user_by_username(serializer.validated_data["username"])
        if isinstance(user, Exception):
            return get_api_response(StatusCodes.Does_Not_Exist, httpStatusCode=status.HTTP_400_BAD_REQUEST)
        
        if user.is_email_verified:
            return get_api_response(StatusCodes.User_Already_Verified, httpStatusCode=status.HTTP_400_BAD_REQUEST)
        
        try:
            activation_key = AuthMisc.generate_and_set_activation_key(user, key_type=AuthMisc.IS_PROFILE_ACTIVATION_KEY)
        except (ValidationError, Exception) as e:
            return get_api_server_error()

        confirmation_link = AuthMisc.generate_confirmation_link(request, serializer.validated_data["username"], activation_key)

        try:
            EmailHelper.send_signup_mail(user.email, user.firstname, confirmation_link) 
        except (Exception) as e:
            return get_api_server_error()

        return get_api_success()
        

class AuthForgotPassword(APIView):
    
    def put(self, request, format=None):
        serializer = ForgotPasswordSerializer(data=request.data)
        
        if not serializer.is_valid():
            return get_400_error(serializer.errors)
    
        user = self.get_user_by_username(serializer.validated_data["username"])
        if isinstance(user, Exception):
            return get_api_response(StatusCodes.Does_Not_Exist, httpStatusCode=status.HTTP_400_BAD_REQUEST)

        try:
            activation_key = AuthMisc.generate_and_set_activation_key(user, AuthMisc.IS_FORGOT_PASSWORD)
        except (ValidationError, Exception) as e:
            return get_api_server_error()
        
        reset_link = AuthMisc.generate_confirmation_link(serializer.validated_data["username"], activation_key)

        try:
            EmailHelper.send_reset_password_mail(user.email, user.firstname, reset_link) 
        except (Exception) as e:
            return get_api_server_error()

        return get_api_success()
        

class AuthChangePassword(APIView):

    def put(self, request, format=None):
        serializer = ChangePasswordSerializer(data=request.data)

        if not serializer.is_valid():
            if not request.user.check_password(serializer.validated_data["old_password"]):
                return get_api_response(AuthStatusCodes.Invalid_Credentials, httpStatusCode=status.HTTP_400_BAD_REQUEST)
            
            return get_400_error(serializer.errors)
        
        request.user.set_password(serializer.validated_data["password"])
        request.user.save()
        
        return get_api_success()