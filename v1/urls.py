from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from . import views


urlpatterns = [    
    url(r'^cases/$', views.CaseView.as_view(), name='cases'),
    url(r'^sightings/$', views.SightingView.as_view(), name='sightings')
] 