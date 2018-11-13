import os

ENVIRONMENT = os.environ['DCMPA_ENVIRONMENT']
SETTINGS_MODULE = 'config.settings.local'

if ENVIRONMENT == 'local':
    SETTINGS_MODULE = 'config.settings.local'

