from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class AuthorizationTests(APITestCase):
    def test_registration_should_be_successful():
        pass
    
    def test_registration_should_return_user_already_logged_in():
        pass
    
    def test_registration_should_return_user_already_exists():
        pass