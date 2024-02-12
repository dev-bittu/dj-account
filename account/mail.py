from django.core.mail import send_mail
from django.conf import settings
from random import randint
from .models import ConfirmEmail

def email_verification_mail(user):
    otp = randint(100000, 999999)

    subject = f"Email confirmation: {settings.SITE_SETTINGS['site'].get('SITE_NAME', 'mysite')}"
    content = f"Your otp is {otp}"

    if cnfm := ConfirmEmail.objects.filter(user=user).first():
        cnfm.delete()
    cnfm = ConfirmEmail(user=user, otp=otp)
    cnfm.save()

    return send_mail(subject, content, settings.EMAIL_HOST_USER, [user.email], fail_silently = not settings.DEBUG)
