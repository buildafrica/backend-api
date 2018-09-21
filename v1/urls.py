from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from . import views


urlpatterns = [    
    url(r'^cases/$', views.CaseView.as_view(), name='cases'),
    url(r'^cases/(?P<pk>[0-9]+)/$', views.CaseDetailView.as_view(), name="case_detail"),
    url(r'^sightings/$', views.SightingView.as_view(), name='sightings'),
    url(r'^sightings/(?P<pk>[0-9]+)/$', views.SightingDetailView.as_view(), name="sighting_detail"),
] 