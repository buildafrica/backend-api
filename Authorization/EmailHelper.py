from django.core.mail import send_mail
from django.conf import settings
import os
class AuthEmailTypes:
    """Different Email Types"""
    Signup = 1
    Reset_Password = 2

EmailFileNames = {
    AuthEmailTypes.Signup:"signup.html",
    AuthEmailTypes.Reset_Password:"resetPassword.html",
    }


class AuthEmailHelper:
    """Helper class for sending different Auth email messages"""
    __templateFolder = 'mailTemplates/'
    __path = os.path.dirname(os.path.abspath(__file__)) + '/' +  __templateFolder 
    
    def __init__(self):
        self.files = {}
        for emailtype in range(1, 3):
            filename = EmailFileNames[emailtype]
            file = open(AuthEmailHelper.__path + filename,'r')
            self.files[emailtype] = file.read()
            file.close()

    def send_signup_mail(self, email, firstname, activation_link): 
        try:
            message = self.files[AuthEmailTypes.Signup].replace("[[firstname]]",firstname).replace("[[activationLink]]", activation_link)
            from_email = settings.SIGN_UP_FROM_EMAIL
            subject = settings.SIGN_UP_MAIL_SUBJECT
            send_mail(subject=subject, message=message, from_email=from_email,recipient_list=[email], html_message=message)
        except Exception as e:
            print("Error occured sending Signup Email>>>> ", e)

    def send_reset_password_mail(self, email, firstname, reset_link): 
        try:
            message = self.files[AuthEmailTypes.Reset_Password].replace("[[firstname]]", firstname).replace("[[activationLink]]", reset_link)
            from_email = settings.RESET_PASSWORD_FROM_EMAIL
            subject = settings.RESET_PASSWORD_MAIL_SUBJECT
            send_mail(subject=subject, message=message, from_email=from_email,recipient_list=[email], html_message=message)
        except Exception as e:
            print("Error occured sending Reset Password Email>>>> ", e)
        

EmailHelper = AuthEmailHelper()


