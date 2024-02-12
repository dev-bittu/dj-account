from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
from .managers import UserManager

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

class ConfirmEmail(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    otp = models.IntegerField()
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)

    def is_expired(self):
        return now() > self.created_at+timedelta(days=settings.SITE_SETTINGS['email'].get('otp_expire_in', 10))
