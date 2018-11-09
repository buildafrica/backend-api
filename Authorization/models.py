from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from Util.models import BaseModel
from .managers import CustomUserManager
from .validators import validate_activation_key_type

class User(AbstractUser, BaseModel):

    is_email_verified = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=128, null=True)
    activation_key_expires = models.DateTimeField(null=True)
    activation_key_used = models.BooleanField(default=False)
    activation_key_type = models.IntegerField(null=True, validators=[validate_activation_key_type])

    REQUIRED_FIELDS = ["email", "password"]

    