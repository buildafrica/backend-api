from django.contrib import admin

from .models import UserProfile,Case,Sighting

admin.site.register(UserProfile)
admin.site.register(Case)
admin.site.register(Sighting)