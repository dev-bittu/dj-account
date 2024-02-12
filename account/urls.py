from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("register/", views.Register.as_view(), name="register"),

    path("verify/", views.VerifyEmail.as_view(), name="verify_email"),
    path("verify/send-otp/", views.SendVerificationOtp.as_view(), name="send_verification_otp"),
]
