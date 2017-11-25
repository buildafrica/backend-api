from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager, models.Manager):
    '''
    Custom model manager for the custom User model.
    '''
    def create_user(self, email, password, date_of_birth=None,
                    phone_number=None, first_name=None, last_name=None):
        '''
        Creates and saves a User with the given details.
        '''
        if not email or not password:
            raise ValueError("Users must have both an email address and a password")

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, email, password, date_of_birth=None,
                        phone_number=None, first_name=None, last_name=None):
        '''
        Creates and saves a staff with the given details.
        '''
        user = self.create_user(
            email,
            password,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, date_of_birth=None,
                        phone_number=None, first_name=None, last_name=None):
        '''
        Creates and saves a superuser with the given details.
        '''
        user = self.create_user(
            email,
            password,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
