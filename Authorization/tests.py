from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from profiles.models import Profiles

class AuthorizationTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "seyi77"
        cls.first_name = "Seyi"
        cls.last_name = "John"
        cls.email = "seyi.john@gmail.com"
        cls.password = "john12345"
        cls.phone_number = "08090924356"
        cls.user_type = "regular"
        
        cls.user = User.objects.create_user(cls.username, email=cls.email, password=cls.password, first_name=cls.first_name, last_name=cls.last_name)
        cls.profile = Profiles.customprofileManager.create_profile(cls.user, phone_number=cls.phone_number, user_type=cls.user_type)

        cls.second_email = "john.seyi@gmail.com"
        cls.second_username = "john77" 


    def setup(self):
        ''' Stuffs to do before every test '''
        self.client.login(username=self.username, password=self.password)
        pass
    
    def tearDown(self):
        ''' Stuffs to do after every test '''
        pass

    def test_registration_should_be_successful(self):
        response = self.client.post(reverse("auth-register"), data = {
            "username": self.second_username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.second_email,
            "password": self.password,
            "phone_number": self.phone_number,
            "user_type": self.user_type
        }, format='json')

        self.assertEqual(response.status_code, 200, "User registeration failed")

    def test_registration_should_return_user_already_logged_in(self):
        pass
    
    def test_registration_should_return_user_already_exists(self):
        pass