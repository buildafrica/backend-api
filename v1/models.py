from django.db import models
from django.utils import timezone


class Case(models.Model):
    """
    Display an individual case.

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
    """
    person_name = models.CharField(max_length=100)
    person_age = models.IntegerField()
    person_address = models.CharField(max_length=500)
    person_phone = models.IntegerField(12)
    person_description = models.CharField(max_length=250)
    missing_date = models.DateField(default=timezone.now)
    last_sighted_date = models.DateField()

    def __str__(self):
        return self.person_name + ' - ' + self.missing_date

   
class Sightings(models.Model):
    '''
    Model for storing sightings for a case 
    Containing basic info such as the associated case ,
    place sighted ,time and date sighted
    '''
    case = models.ForeignKey(Case,on_delete=models.CASCADE)
    location_sighted = models.CharField(max_length=256)
    date_sighted = models.DateTimeField()
    additional_info = models.TextField()
    
    def __str__(self):
        return self.case + ' : ' + self.date_sighted
    
    
