from django.conf import settings
from django.contrib.auth import get_user_model

class UserObjectsMixin(object):

    @staticmethod
    def get_user_by_username(username):
        try:
            user = get_user_model().objects.get(username=username, isActive=1)
            return user
        except (get_user_model().DoesNotExist, Exception) as e:
            return e
