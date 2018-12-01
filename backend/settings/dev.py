from .base import *
import psycopg2.extensions
import dj_database_url

DEBUG = True

ALLOWED_HOSTS.append("https://mpa-dev.herokuapp.com/")

INTERNAL_IPS = [
    '127.0.0.1',
]

DATABASES = {
    'default': {},
    'OPTIONS': {
        'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
    },
}

DATABASES["default"] = dj_database_url.config(conn_max_age=600)

INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware', )

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
