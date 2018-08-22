from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# (TODO):subomi -  Move this to a util folder to be used by all models across apps
class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=False)
    class Meta:
        abstract = True

class User(AbstractUser, BaseModel):
    is_email_verified = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=128, null=True)
    key_expires = models.DateField(null=True)
    reset_password_key = models.CharField(max_length=128, null=True)
    is_reset_password_key_used = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["email", "password"]