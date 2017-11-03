from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    '''
    This model stores information about site users.
    Fields like email, names and phone number are captured by the 
    user object
    '''
    user = models.OneToOneField(User)
    