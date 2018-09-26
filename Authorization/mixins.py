from django.contrib.auth import get_user_model

User = get_user_model()

class UserObjectsMixin(object):

    @staticmethod
    def get_user_by_username(username):
        try:
            user = User.objects.get(username=username, isActive=1)
        except (User.DoesNotExist, Exception) as e:
            return e
