from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from profiles.models import Profiles
from .responseHelper import StatusCodes
from .misc import AuthMisc

import pdb

class AuthorizationTests(APITestCase):
    userTearDownRequired = False

    @classmethod
    def setUpTestData(cls):
        cls.username = "seyi77"
        cls.first_name = "Seyi"
        cls.last_name = "John"
        cls.email = "seyi.john@gmail.com"
        cls.password = "john12345"
        cls.phone_number = "08090924356"
        cls.user_type = "regular"

    def setup(self):
        ''' Stuffs to do before every test '''        
        pass
    
    def tearDown(self):
        ''' Stuffs to do after every test '''
        if self.userTearDownRequired:
            get_user_model().objects.all().delete()
            self.userTearDownRequired = False

    def create_user(self):
        user = get_user_model().objects.create_user(self.username, email=self.email, password=self.password, first_name=self.first_name, last_name=self.last_name)
        profile = Profiles.customprofileManager.create_profile(user, phone_number=self.phone_number, user_type=self.user_type)
        
        try:
            AuthMisc.generate_and_set_activation_key(user, key_type=AuthMisc.IS_PROFILE_ACTIVATION_KEY)
        except (ValidationError, Exception) as e:
            raise e
        
        self.tearDownRequired = True
        return user

    # Test Registration API
    def test_a_registration_should_be_successful(self):
        response = self.client.post(reverse("auth-register"), data = {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "phone_number": self.phone_number,
            "user_type": self.user_type
        }, format='json')

        self.assertEqual(response.status_code, 200, "User registeration failed")
        self.assertEqual(response.json()["status"], StatusCodes.Success, "User registeration failed")
        self.tearDownRequired = True


    def test_registration_should_return_user_already_logged_in(self):
        user = self.create_user()
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
        user = self.create_user()
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
    
    # Confirm Email API
    def test_auth_confirm_email(self):
        """
        - Register second user.
        - Lookup Database manually and retriev auth token
        - Confirm Email with request. 
        - Verify confirmation
        """
        user = self.create_user()

        response = self.client.put(reverse("auth-confirm-email"), data={
            "username": user.username,
            "activation_key": user.activation_key
        }, format="json")

        user.refresh_from_db()
        self.assertEqual(response.status_code, 200, "User email not confirmed")
        self.assertEqual(response.json()["status"], StatusCodes.Success, "User email not confirmed.")
        self.assertTrue(user.is_email_verified, "User email is not verified in DB")

    # Delete Account API
    def test_delete_account_unaunthenticated_should_fail(self):
        response = self.client.delete(reverse("auth-delete-account"))

        self.assertEqual(response.status_code, 400, "Delete account without logging - Improper status code")
        self.assertEqual(response.json()["status"], StatusCodes.User_Unaunthenticated, "Delete account without logging - Improper status message")
    
    def test_delete_deleted_account_should_fail(self):
        # TODO
        pass
    
    def test_delete_account_authenticated_should_pass(self):
        user = self.create_user()
        self.client.force_authenticate(user = user)

        user.isActive = 0
        user.profile.isActive = 0
        user.save()
        user.profile.save()

        response = self.client.delete(reverse("auth-delete-account"))
        self.assertEqual(response.status_code, 200, "Delete account not successful - Improper status code")
        self.assertEqual(response.json()["status"], StatusCodes.Success, "Delete account not successful - Improper status message")

        self.client.force_authenticate(user = None)

    # TODO: Resend Confirm Email API
    
    def test_forgot_password_unaunthenticated_should_pass(self):
        pass

    def test_change_password_unaunthenticated_should_fail(self):
        user = self.create_user()
        new_password = "newpassword1"

        response = self.client.put(reverse("auth-change-password"), data={
            "old_password": self.password,
            "password": new_password
        }, format= "json")

        user.refresh_from_db()
        self.assertEqual(response.status_code, 401, "Change password failed - Improper status code")
        self.assertFalse(user.password == new_password, "Password changed wrongly.")

    def test_change_password_aunthenticated_should_pass(self):
        user = self.create_user()
        self.client.force_authenticate(user = user)
        new_password = "newpassword1"

        response = self.client.put(reverse("auth-change-password"), data={
            "old_password": self.password,
            "password": new_password
        }, format="json")

        user.refresh_from_db()
        self.assertEqual(response.status_code, 200, "Change password failed - Improper status code")
        self.assertEqual(response.json()["status"], StatusCodes.Success, "Change password failed - Improper status message")
        self.assertFalse(user.password == new_password, "Password changed wrongly.")

        self.client.force_authenticate(user = None)