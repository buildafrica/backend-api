from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from .views import (GetProfiles, Profiles, ProfilePicture)

urlpatterns = [
    path('user/<int:id>/', GetProfiles.as_view(),name="get-profiles"),
    path('user/', Profiles.as_view(), name="get-my-profile"),
    path('edit/', Profiles.as_view(), name="edit-profile"),
    path('editprofilepicture/', ProfilePicture.as_view(), name="edit-profile-picture")
]

