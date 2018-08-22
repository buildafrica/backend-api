from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

from .serializers import RegistrationSerializerMixin

# Create your views here.
class Register(APIView):
    """ Create Users """

    """ Register a new User """
    def post(self, request, format=None):
        serializer = RegistrationSerializerMixin(data=request.data)
        if not serializer.is_valid():
            return "Bad Boy!"
        
        User = get_user_model()
        # Check for Duplicates.
        User.objects.
        
        return "Good Boy!"
    
class AuthDetail(APIView):
    """ Retrieve, update and delete a user """

    """ Delete a User """
    def delete(self, request, format=None):
        pass