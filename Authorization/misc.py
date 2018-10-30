import secrets
from django.utils import timezone
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

class AuthMisc:
    token_length = 32
    IS_PROFILE_ACTIVATION_KEY = 1
    IS_FORGOT_PASSWORD = 2
    IS_RESET_PASSWORD_KEY = 3
    KEY_EXPIRATION_TIME = 1  # Key expires in 1 day.

    @classmethod
    def generate_and_set_activation_key(cls, user, key_type=None):
        activation_key = secrets.token_urlsafe(cls.token_length)
        user.activation_key = activation_key
        user.activation_key_expires = timezone.now() + timezone.timedelta(days=cls.KEY_EXPIRATION_TIME)
        user.activation_key_type = key_type
        user.save()
        
        return activation_key
        
    @classmethod
    def generate_confirmation_link(cls, request, username, activation_key):
        confirmation_link_url =  "http://localhost:/" # (TODO) reverse("pages-confirm-email")
        domain = get_current_site(request).domain
        full_site_confirmation_link = '%s://%s%s/%s/%s'%(request.scheme, domain, confirmation_link_url, username, activation_key)
        
        return full_site_confirmation_link