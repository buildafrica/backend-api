from .base import *
import psycopg2.extensions
import dj_database_url
import cloudinary

DEBUG = True

ALLOWED_HOSTS.extend(("localhost", "mpa-dev.herokuapp.com"))

INTERNAL_IPS = [
    '127.0.0.1',
]

DATABASES = {
    'default': {},
    'OPTIONS': {
        'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "Dcmpa",
        'USER': "postgres",
        'PASSWORD': "postgres",
        'HOST': 'localhost'
    },
    'OPTIONS': {
        'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
    },
}

INSTALLED_APPS.append('debug_toolbar')

# Cloudinary Configurations.
cloudinary.config( 
  cloud_name = os.getenv("CLOUD_NAME"), 
  api_key = os.getenv("CLOUDINARY_API_KEY"), 
  api_secret = os.getenv("CLOUDINARY_API_SECRET") 
)

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware', )

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles/')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "static"),
)
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Cloudinary Media Url 
MEDIA_URL = 'https://res.cloudinary.com/thehub/'