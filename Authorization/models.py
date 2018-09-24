from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from .managers import CustomUserManager
from .validators import validate_activation_key_type

# (TODO):subomi -  Move this to a util folder to be used by all models across apps
class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=False)
    class Meta:
        abstract = True

class User(AbstractUser, BaseModel):
    is_email_verified = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=128, null=True)
    activation_key_expires = models.DateField(null=True)
    activation_key_used = models.BooleanField(default=False)
    activation_key_type = models.IntegerField(null=True, validators=[validate_activation_key_type])

    REQUIRED_FIELDS = ["email", "password"]

    