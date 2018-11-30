import os

ENVIRONMENT = os.environ['DCMPA_ENVIRONMENT']
SETTINGS_MODULE = 'backend.settings.dev'

if ENVIRONMENT == 'testing':
    SETTINGS_MODULE = 'backend.settings.testing'
