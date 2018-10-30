import os
from kombu import Exchange, Queue
from celery.schedules import crontab
from datetime import timedelta

#ALL OUR APP SETTINGS (non django setting) goes here

#Custom Email settings
SIGN_UP_FROM_EMAIL = 'noreply@yami.com.ng'
SIGN_UP_MAIL_SUBJECT = 'Yami Registration'
RESET_PASSWORD_FROM_EMAIL = 'noreply@yami.com.ng'
RESET_PASSWORD_MAIL_SUBJECT = 'Yami Password Reset'

#Login settings
# Paths that can be accessed without user logging in. Not a django property. It is being used by custom Auth middleware
LOGIN_EXEMPT_URLS = (r'^/', r'^page/', r'^auth/login', r'^auth/register',r'auth/confirmemail', r'^admin/')

LOGIN_URL = "page/login"