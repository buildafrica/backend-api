from django.conf import settings
from django.contrib.auth import get_user_model

User = settings.AUTH_USER_MODEL

class UserObjectsMixin(object):

    @staticmethod
    def get_user_by_username(username):
        try:
            user = User.objects.get(username=username, isActive=1)
            return user
        except (User.DoesNotExist, Exception) as e:
            return e
