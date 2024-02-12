from django.core.mail import send_mail
from django.conf import settings
from random import randint
from .models import ConfirmEmail

def email_verification_mail(user):
    otp = randint(100000, 999999)

    subject = "Account Verification OTP for Registration"
    content = f"Dear {user.username},\n" \
                "Thank you for registering on our website." \
                "To complete the registration process and verify your email address, please use the following One Time Password (OTP):\n\n" \
                f"OTP: {otp}\n\n" \
                "Please enter this OTP on the registration page to finalize your account setup." \
                "If you have not attempted to register on our site, please disregard this email.\n" \
                "If you encounter any issues or need assistance, feel free to contact our support team at Support Email Address.\n" \
                "Thank you for choosing our platform.\n\n" \
                "Best regards,\n" \
                f"{settings.SITE_SETTINGS['site']['SITE_NAME'].title()} Team"

    if cnfm := ConfirmEmail.objects.filter(user=user).first():
        cnfm.delete()
    cnfm = ConfirmEmail(user=user, otp=otp)
    cnfm.save()

    return send_mail(subject, content, settings.EMAIL_HOST_USER, [user.email], fail_silently = not settings.DEBUG)
