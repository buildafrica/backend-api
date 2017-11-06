from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

urlpatterns = [    
    # API (v1)
    url(r'^api/v1/', include('v1.urls')),
] 