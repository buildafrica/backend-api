from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

from Util.models import BaseModel
from .managers import ProfilesManager

# Create your models here.
class Profiles(BaseModel):
    '''Stores the user profile related information'''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, validators=[RegexValidator(regex='^\d{11}$')])
    user_type = models.CharField(max_length=10, null=False)
    address = models.TextField(max_length=100, null=True)
    country = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=6, null=True)
    date_of_birth = models.DateField(null=True)
    is_email_verified = models.BooleanField(default=False)
    profile_pic = models.URLField(null=True)

    customprofileManager = ProfilesManager()

    