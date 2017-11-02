from django.db import models
from django.utils import timezone


# Table to store a missing person case
class Case(models.Model):
    person_name = models.CharField(max_length=100)
    person_age = models.IntegerField()
    person_address = models.CharField(max_length=500)
    person_phone = models.IntegerField(12)
    person_description = models.CharField(max_length=250)
    missing_date = models.DateField(default=timezone.now)
    last_sighted_date = models.DateField()

    def __str__(self):
        return self.person_name + ' - ' + self.missing_date
