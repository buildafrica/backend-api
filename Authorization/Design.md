Authentication is jwt based tokens. Included in the payload is an expiry time. To allow the jwt expire. 

- A middleware is designed to auth users before passing request to the view. 
- A view is designed to set users token. 


* Auth Backend
* Auth Model
* Auth Middleware

Users Model
- Username
- Email
- Password
- Auth Misc
    - is_staff
    - is_superuser

Profile Model
- UserType (E.g Legal, Police, Regular)
- Phone Number
- Country
- State
- Date of Birth


AbstractBaseUser
- password
- last_login
- get_username()
- save()
- is_anonymous()
- is_authenticated()
- set_password(): void
- check_password(): Boolean
- get_session_auth_hash(): String


AbstractUser
- username_validator
- username
- first_name
- last_name
- email 
- is_staff
- is_active
- date_joined
- EMAIL_FIELD
- USERNAME_FIELD = "username"
- REQUIRED_FIELDS = ["email"]
- get_full_name()
- get_short_name()
- email_user()