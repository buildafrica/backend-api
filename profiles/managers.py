from django.db import models

class ProfilesManager(models.Manager):
    '''
    Profiles model manager for the profile model
    '''

    def create_profile(self, user, phone_number, user_type, **extra_fields):
        
        if not user or not phone_number or not user_type:
            raise ValueError("Profile must have an user, phone number and user type")
        
        profile = self.model(
            user=user,
            phone_number=phone_number,
            user_type=user_type,
            **extra_fields,
        )
        profile.save()
        return profile