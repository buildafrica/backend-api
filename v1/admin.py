from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


from .models import Case, Sighting


admin.site.register(Case)
admin.site.register(Sighting)