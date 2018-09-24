from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .views import AuthMisc

def validate_activation_key_type(value):
    """
    Validate activation key type
    """
    
    if value not in [AuthMisc.IS_FORGOT_PASSWORD, AuthMisc.IS_PROFILE_ACTIVATION_KEY, AuthMisc.IS_RESET_PASSWORD_KEY]:
        raise ValidationError("Invalid activation key type")