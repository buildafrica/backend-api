from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from cloudinary import uploader

from .models import Profiles
from .serializers import ProfileInfoSerializer, ProfilePictureSerializer, SaveProfilePictureSerializer
from .responseHelper import (ResponseHelper, StatusCodes, get_api_response,
                            get_api_server_error, get_api_success, get_400_error)
class ProfilesMixin(object):

    def get_user_by_id(self, id):
        pass


# Create your views here.
class GetProfiles(ProfilesMixin, APIView):
    pass

class Profiles(ProfilesMixin, APIView):

    def get(self, request, *args, **kwargs):
        """
        Get a logged in users profile
        """
        profile = Profiles.objects.get(user = request.user)
        serializer = ProfileInfoSerializer(profile)
        return get_api_response(StatusCodes.Success, data = serializer.data, httpStatusCode= status.HTTP_200_OK )


    def put(self, request, *args, **kwargs):
        """
        PUT Request:
            To edit a user's profile, excluding profile picture uploads which have
            a different API.
        """
        profile = Profiles.objects.get(user = request.user)
        serializer = ProfileInfoSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return get_api_response(StatusCodes.Success, data = serializer.data, httpStatusCode= status.HTTP_200_OK)

        return get_400_error(serializer.errors)

class ProfilePicture(ProfilesMixin, APIView):
    parser_classes = (MultiPartParser,)

    def put(self, request, *args, **kwargs):
        """
        To save a new profile picture.
        """
        serializer = ProfilePictureSerializer(data = request.data)
        if serializer.is_valid():
            image = serializer.validated_data['file']
            profile = request.user.profile
            
            upload_response = uploader.upload(image, tags=["profile picture"], folder="profilepics")
            if("public_id" not in upload_response):
                #TODO: log error
                return  get_api_server_error()

            profile.profile_pic = upload_response["secure_url"]
            profile.save()
            response = SaveProfilePictureSerializer(profile)
            return get_api_response(StatusCodes.Success, data = response.data, httpStatusCode= status.HTTP_200_OK)
            
        return get_400_error(serializer.errors)
