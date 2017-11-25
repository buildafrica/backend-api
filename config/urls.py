from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [

    # Core
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='DCMPA')),
    url(r'^', include('dcmpa.urls')),    

    # Authentication
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
