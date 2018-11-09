from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from profiles.models import Profiles
from .responseHelper import StatusCodes

import pdb

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
        
        cls.user = get_user_model().objects.create_user(cls.username, email=cls.email, password=cls.password, first_name=cls.first_name, last_name=cls.last_name)
        cls.profile = Profiles.customprofileManager.create_profile(cls.user, phone_number=cls.phone_number, user_type=cls.user_type)

        cls.second_email = "john.seyi@gmail.com"
        cls.second_username = "john77" 


    def setup(self):
        ''' Stuffs to do before every test '''        
        pass
    
    def tearDown(self):
        ''' Stuffs to do after every test '''
        pass

    def test_a_registration_should_be_successful(self):
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
        self.assertEqual(response.json()["status"], StatusCodes.Success, "User registeration failed")

    def test_registration_should_return_user_already_logged_in(self):
        user = get_user_model().objects.get(username=self.username)
        self.client.force_authenticate(user = user)

        response = self.client.post(reverse("auth-register"), data = {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "phone_number": self.phone_number,
            "user_type": self.user_type
        }, format='json')

        self.assertEqual(response.status_code, 400, "Logged in user, re-registering")
        self.assertEqual(response.json()["status"], StatusCodes.Already_Logged_In, "User already logged in")
        
        self.client.force_authenticate(user = None)
    
    def test_registration_should_return_user_already_exists(self):
        response = self.client.post(reverse("auth-register"), data = {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "phone_number": self.phone_number,
            "user_type": self.user_type
        }, format='json')

        self.assertEqual(response.status_code, 400, "User re-registering failure")
        self.assertEqual(response.json()["status"], StatusCodes.User_with_Email_Exists, "User with Email already exists")

    def test_registration_should_return_invalid_fields_wrong_values(self):
        response = self.client.post(reverse("auth-register"), data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": "yyy",
            "phone_number": "070m",
            "user_type": "xxx"
        }, format='json')

        res = response.json()
        errors = res["errors"]
        self.assertEqual(response.status_code, 400, "Logged in user, re-registering")
        self.assertEqual(res["status"], StatusCodes.Invalid_Field, "Invalid fields")
        for field in ["phone_number", "user_type", "password", "username", "email"]:
            self.assertTrue(field in errors)
    
    def test_auth_confirm_email(self):
        """
        - Register second user.
        - Lookup Database manually and retriev auth token
        - Confirm Email with request. 
        - Verify confirmation
        """
        
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

        u = get_user_model().objects.get(email=self.second_email)

        response = self.client.put(reverse("auth-confirm-email"), data={
            "username": u.username,
            "activation_key": u.activation_key
        }, format="json")

        u.refresh_from_db()
        self.assertEqual(response.status_code, 200, "User email not confirmed")
        self.assertEqual(response.json()["status"], StatusCodes.Success, "User email not confirmed.")
        self.assertTrue(u.is_email_verified, "User email is not verified in DB")
    
    def test_delete_account_unaunthenticated_should_fail(self):
        pass
    
    def test_delete_account_aunthenticated_should_pass(self):
        pass
    
    def test_delete_deleted_account_should_fail(self):
        pass