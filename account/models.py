from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from .managers import UserManager

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

class ConfirmEmail(models.Model):
    expire_in = models.DateTimeField(auto_now=True)
    otp = models.CharField(max_length=settings.SITE_SETTINGS['email'].get('otp_length', 6))
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
