from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.db import models


username_validator = RegexValidator(
    regex=r'^[A-Za-z][A-Za-z0-9]{2,19}$',
    message="Username must be 3–20 characters, start with a letter, and contain only letters and numbers."
)
class CustomUser(AbstractUser):
    username = models.CharField(
        unique=True,
        validators=[username_validator],
        max_length=20,
        )
    email = models.EmailField(
            unique=True,
            validators=[EmailValidator()], # Use Django's built-in EmailValidator
            max_length=254,
        )
    groups = models.ManyToManyField('auth.Group', 
                                    related_name='customuser_set', 
                                    blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', 
                                              related_name='customuser_permissions', 
                                              blank=True)
    
    name = models.CharField(max_length=50, blank=True, help_text="First name of the user")
    surname = models.CharField(max_length=50, blank=True, help_text="Last name of the user")
    country = models.CharField(max_length=50, blank=True, help_text="Country of the user")
    
    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username.lower()

        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    def clean(self):
        if self.email:
            existing = CustomUser.objects.filter(email__iexact=self.email)
            if self.pk:
                existing = existing.exclude(pk=self.pk)
            if existing.exists():
                raise ValidationError({'email': 'Email address is already in use'})
            
        if self.username:
            existing = CustomUser.objects.filter(username__iexact=self.username)
            if self.pk:
                existing = existing.exclude(pk=self.pk)
            if existing.exists():
                raise ValidationError({'username': 'Username is already taken'})

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 1. RegexValidator
#       1.
#       ^ --- ------ --- --> Start of the string
#       [A-Za-z] --- --- --> First character must be a letter
#       [A-Za-z0-9]{2,19} -> Followed by 2 to 19 letters or numbers
#       $ --- ------ --- --> End of string
#       2.
#       message = is shown when user tries something invalid


# 2. AbstractUser
#       1.
#       AbstractUser inherits all the built-in fields (username, email, password, etc.)
#       AbstractUser permits to override things like the username field or add custom fields.
#       2.
#       User is a concrete model (already linked to the database)
#       More difficult to modify