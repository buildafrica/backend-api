from .base import *
import psycopg2.extensions
import cloudinary

DEBUG = True

INTERNAL_IPS = [
    '127.0.0.1',
]

DATABASES["default"] = dj_database_url.config(conn_max_age=600)

INSTALLED_APPS.append('debug_toolbar')

# Cloudinary Configurations.
cloudinary.config( 
  cloud_name = os.getenv("CLOUD_NAME"), 
  api_key = os.getenv("CLOUDINARY_API_KEY"), 
  api_secret = os.getenv("CLOUDINARY_API_SECRET") 
)

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware', )

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


# Cloudinary Media Url 
MEDIA_URL = 'https://res.cloudinary.com/thehub/'