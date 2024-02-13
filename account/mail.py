from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from random import randint
from .models import ConfirmEmail, PasswordReset

def email_verification_mail(user):
    """Send email verification otp to complete registration
    Parameters:
        user: request.user
    Returns:
        delivered: int - 1 if delivered else 0
    """

    # Generate a random OTP (One Time Password) for email verification
    otp = randint(100000, 999999)

    # Prepare email subject and content
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

    # Check if there is an existing ConfirmEmail object for the user, delete it if it exists
    if cnfm := ConfirmEmail.objects.filter(user=user).first():
        cnfm.delete()

    # Create a new ConfirmEmail object for the current user with the generated OTP
    cnfm = ConfirmEmail(user=user, otp=otp)
    cnfm.save()

    # Send the verification email using Django's send_mail function
    return send_mail(subject, content, settings.EMAIL_HOST_USER, [user.email], fail_silently = not settings.DEBUG)

def reset_password_mail(user):
    if pswdrst := PasswordReset.objects.filter(user=user).first():
        pswdrst.delete()
    pswdrst = PasswordReset(user=user)
    pswdrst.save()

    subject = "Reset Your Password - Action Required"
    content = f"Dear {user.username},\n" \
                "We have received a request to reset your password. To proceed with resetting your password, please click on the link below:\n\n" \
                f"Reset Password Link: {settings.SITE_SETTINGS['site']['SITE_LINK']}{reverse('account:reset_password', args=[user.id, pswdrst.token])}\n\n" \
                "If you did not request this password reset, please ignore this email. Your current password will remain unchanged.\n\n" \
                "Thank you,\n" \
                f"{settings.SITE_SETTINGS['site']['SITE_NAME'].title()} Team"
    
    return send_mail(subject, content, settings.EMAIL_HOST_USER, [user.email], fail_silently = not settings.DEBUG)
