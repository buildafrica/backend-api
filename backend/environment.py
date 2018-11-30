import os

ENVIRONMENT = os.environ['DCMPA_ENVIRONMENT']
SETTINGS_MODULE = 'backend.settings.dev'

if ENVIRONMENT == 'staging':
    SETTINGS_MODULE = 'backend.settings.staging'
