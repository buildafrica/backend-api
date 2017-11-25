from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    '''
    This model stores information about site users.
    Fields like email, names and phone number are captured by the 
    user object.
    TODO:
    Add different user types i.e law enforcement, normal users etc.
    '''
    email = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=255,blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def get_full_name(self):
        '''
        Returns user's full name.
        '''
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        '''
        Returns user's first name.
        '''
        return self.first_name

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        '''
        Extends the save method.
        '''
        if not self.email or not self.password:
            raise ValueError("Users must have both an email address and a password")
        
        super(User, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.email


class Case(TimeStampedModel):
    """
    Display an individual case.
    ``owner``
        User that opened the case.
    ``person_name``
        To save name of missing person.
    ``person_age``
            To save age of missing person.
    ``person_address``
            To save address of missing person
    ``person_phone``
            To save phone of missing person
    ``person_description``
            To save description of missing person like height, color complexion etc
    ``missing_date``
            To save missing date of a person
    ``last_sighted_date``
            To save last sighted date of missing person
    ``person_photo``
            Field to upload the pic of a missing person

    TODO:
    Add phone number validator
    """
    owner = models.ForeignKey("User", related_name="cases_opened")    
    person_name = models.CharField(max_length=100)
    person_age = models.IntegerField()
    person_address = models.CharField(max_length=500)
    person_phone = models.CharField(max_length=12)
    person_description = models.CharField(max_length=250)
    missing_date = models.DateField(default=timezone.now)
    last_sighted_date = models.DateField()
    person_photo = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.person_name + ' - ' + self.missing_date

class Sighting(TimeStampedModel):
    '''
    Model for storing sightings for a case 
    Containing basic info such as the associated case ,
    place sighted ,time and date sighted
    '''
    case = models.ForeignKey(Case,on_delete=models.CASCADE)
    owner = models.ForeignKey("User")
    location_sighted = models.CharField(max_length=256)
    date_sighted = models.DateTimeField()
    additional_info = models.TextField()
    
    def __str__(self):
        return self.case + ' : ' + self.date_sighted
